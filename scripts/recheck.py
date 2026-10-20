#!/usr/bin/env python3
"""Report-only recheck of integration statuses against live GitHub data.

READ-ONLY BY DESIGN: this script never writes to data/, docs/, README* or any
other repo file. Its only output is the report on stdout or the --out file.
It never edits data/integrations.yml — a human must do that.

What it does
------------
For every entry in data/integrations.yml whose status is one of
merged-unreleased, in-progress, announced, unsupported, unconfirmed:

  1. collect GitHub PR/issue URLs from source[].url
     (regex github.com/OWNER/REPO/(pull|issues)/N);
  2. query the GitHub REST API for each PR (state, merged_at, merge_commit_sha)
     or issue (state, state_reason, closed_at) — via `gh api` when `gh` is on
     PATH, otherwise via urllib with $GITHUB_TOKEN (Authorization: Bearer);
     a repo that returns 404 is recorded as "repo-unavailable";
  3. for a merged PR, look at the repo's latest 20 releases (falling back to
     its latest 20 tags when it has no releases) and use
     compare/{merge_commit_sha}...{tag}: status ahead|identical means the tag
     contains the merge commit. The earliest containing release is reported;
     prereleases are skipped unless only prereleases contain the commit;
  4. derive a *suggested* status from the observed facts (see suggest()) and
     report the entry only when the suggestion differs from the current one.

Usage
-----
  python3 scripts/recheck.py                       # markdown to stdout
  python3 scripts/recheck.py --format json
  python3 scripts/recheck.py --out recheck.md
  python3 scripts/recheck.py --only kitty,tuist --sleep 0.2
  python3 scripts/recheck.py --limit 5             # smoke-test prefix

Exit codes: 0 normal (also when there are findings or API errors);
            2 with --fail-on-change when any suggestion differs;
            1 on fatal problems (bad arguments, unreadable data, no credentials).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DATA_FILE = REPO / "data" / "integrations.yml"

TARGET_STATUSES = [
    "merged-unreleased",
    "in-progress",
    "announced",
    "unsupported",
    "unconfirmed",
]
DISCLAIMER = "Suggestions only. A human must verify and edit data/integrations.yml."
GH_URL_RE = re.compile(
    r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/(pull|issues)/(\d+)"
)
CST = timezone(timedelta(hours=8), name="CST")


class NotFound(Exception):
    """HTTP 404 from the GitHub API (repo/PR/issue/compare gone)."""


class ApiError(Exception):
    """Any other GitHub API failure."""


def parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def cst(value: str | None) -> str:
    """Render a GitHub ISO timestamp as 'YYYY-MM-DD HH:MM CST' (UTC+8)."""
    dt = parse_iso(value)
    if dt is None:
        return "unknown"
    return dt.astimezone(CST).strftime("%Y-%m-%d %H:%M CST")


def now_cst() -> str:
    return datetime.now(CST).strftime("%Y-%m-%d %H:%M CST")


class GitHub:
    """Minimal read-only GitHub REST client: `gh api` if available, else urllib."""

    def __init__(self, sleep: float):
        self.sleep = sleep
        self.use_gh = shutil.which("gh") is not None
        self.token = "" if self.use_gh else os.environ.get("GITHUB_TOKEN", "")
        if not self.use_gh and not self.token:
            raise SystemExit(
                "error: `gh` is not on PATH and GITHUB_TOKEN is not set — "
                "cannot query the GitHub API"
            )
        self._last_call = 0.0
        self.calls = 0

    def describe(self) -> str:
        return "`gh api`" if self.use_gh else "urllib + GITHUB_TOKEN (Authorization: Bearer)"

    def _throttle(self) -> None:
        if self.calls:
            wait = self.sleep - (time.monotonic() - self._last_call)
            if wait > 0:
                time.sleep(wait)
        self._last_call = time.monotonic()
        self.calls += 1

    def get(self, path: str) -> object:
        """GET an API path; transient failures are retried once."""
        last_error: ApiError | None = None
        for attempt in (1, 2):
            self._throttle()
            try:
                return self._get_once(path)
            except NotFound:
                raise
            except ApiError as exc:
                last_error = exc
                if attempt == 1:
                    time.sleep(2.0)
        assert last_error is not None
        raise last_error

    def _get_once(self, path: str) -> object:
        if self.use_gh:
            try:
                proc = subprocess.run(
                    ["gh", "api", path], capture_output=True, text=True, timeout=45
                )
            except subprocess.TimeoutExpired as exc:
                raise ApiError(f"gh api {path}: timed out after 45s") from exc
            if proc.returncode == 0:
                try:
                    return json.loads(proc.stdout)
                except json.JSONDecodeError as exc:  # pragma: no cover
                    raise ApiError(f"gh api {path}: non-JSON output: {exc}") from exc
            m = re.search(r"HTTP (\d{3})", proc.stderr)
            if m and int(m.group(1)) == 404:
                raise NotFound(path)
            detail = proc.stderr.strip() or f"exit code {proc.returncode}"
            raise ApiError(f"gh api {path}: {detail}")
        url = f"https://api.github.com/{path}"
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "awesome-osc7501-recheck",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                raise NotFound(path) from exc
            raise ApiError(f"GET {path}: HTTP {exc.code}") from exc
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise ApiError(f"GET {path}: {exc}") from exc


class Checker:
    """Fetches PRs/issues/releases/compares with per-run caching."""

    def __init__(self, gh: GitHub):
        self.gh = gh
        self._releases: dict[str, list[dict]] = {}
        self._tags: dict[str, list[dict]] = {}
        self._compare: dict[tuple[str, str, str], bool] = {}

    # -- cached REST helpers ------------------------------------------------
    def releases(self, repo: str) -> list[dict]:
        if repo not in self._releases:
            data = self.gh.get(f"repos/{repo}/releases?per_page=20")
            self._releases[repo] = data if isinstance(data, list) else []
        return self._releases[repo]

    def tags(self, repo: str) -> list[dict]:
        if repo not in self._tags:
            data = self.gh.get(f"repos/{repo}/tags?per_page=20")
            self._tags[repo] = data if isinstance(data, list) else []
        return self._tags[repo]

    def compare_contains(self, repo: str, sha: str, tag: str) -> bool:
        key = (repo, sha, tag)
        if key not in self._compare:
            try:
                data = self.gh.get(f"repos/{repo}/compare/{sha}...{tag}")
                status = data.get("status") if isinstance(data, dict) else None
                self._compare[key] = status in ("ahead", "identical")
            except NotFound:
                # no common ancestor / tag moved — treat as "does not contain"
                self._compare[key] = False
        return self._compare[key]

    # -- observations --------------------------------------------------------
    @staticmethod
    def _safe(fn, repo: str) -> list[dict]:
        """Call releases()/tags(); a repo that disappears mid-run yields []."""
        try:
            return fn(repo)
        except NotFound:
            return []
    def observe_pr(self, repo: str, number: str, url: str) -> dict:
        obs = {"kind": "pr", "repo": repo, "number": int(number), "url": url,
               "unavailable": False, "state": None, "merged_at": None,
               "merge_commit_sha": None, "containment": None}
        try:
            data = self.gh.get(f"repos/{repo}/pulls/{number}")
        except NotFound:
            obs["unavailable"] = True
            return obs
        obs["state"] = data.get("state")
        obs["merged_at"] = data.get("merged_at")
        obs["merge_commit_sha"] = data.get("merge_commit_sha")
        if obs["merged_at"] and obs["merge_commit_sha"]:
            obs["containment"] = self.containment(
                repo, obs["merged_at"], obs["merge_commit_sha"]
            )
        return obs

    def observe_issue(self, repo: str, number: str, url: str) -> dict:
        obs = {"kind": "issue", "repo": repo, "number": int(number), "url": url,
               "unavailable": False, "state": None, "state_reason": None,
               "closed_at": None, "is_pr": False}
        try:
            data = self.gh.get(f"repos/{repo}/issues/{number}")
        except NotFound:
            obs["unavailable"] = True
            return obs
        obs["state"] = data.get("state")
        obs["state_reason"] = data.get("state_reason")
        obs["closed_at"] = data.get("closed_at")
        if data.get("pull_request"):  # a PR masquerading as an issue URL
            obs["is_pr"] = True
            pr = self.observe_pr(repo, number, url)
            pr["kind"] = "pr (via issues URL)"
            return pr
        return obs

    def containment(self, repo: str, merged_at: str, sha: str) -> dict | None:
        """Earliest release/tag containing the merge commit, or None.

        Prereleases are skipped unless only prereleases contain the commit;
        the tag fallback is used only when the repo has no (non-draft) releases.
        """
        releases = [
            r for r in self._safe(self.releases, repo)
            if not r.get("draft") and r.get("tag_name") and r.get("published_at")
        ]
        stable = sorted(
            (r for r in releases
             if not r.get("prerelease") and r["published_at"] >= merged_at),
            key=lambda r: r["published_at"],
        )
        for r in stable:
            if self.compare_contains(repo, sha, r["tag_name"]):
                return {"tag": r["tag_name"], "published_at": r["published_at"],
                        "prerelease": False, "tag_only": False, "version_tag": True}
        prerelease = sorted(
            (r for r in releases
             if r.get("prerelease") and r["published_at"] >= merged_at),
            key=lambda r: r["published_at"],
        )
        for r in prerelease:
            if self.compare_contains(repo, sha, r["tag_name"]):
                return {"tag": r["tag_name"], "published_at": r["published_at"],
                        "prerelease": True, "tag_only": False, "version_tag": True,
                        "only_prerelease": True}
        if not releases:  # fall back to tags when the repo has no releases
            for t in self._safe(self.tags, repo):
                name = t.get("name") or ""
                if self.compare_contains(repo, sha, name):
                    version_tag = re.search(r"\d+\.\d+", name) is not None
                    return {"tag": name, "published_at": None, "prerelease": False,
                            "tag_only": True, "version_tag": version_tag}
        return None


# -- facts / suggestions ------------------------------------------------------
def fact_lines(entry_obs: list[dict]) -> list[str]:
    lines: list[str] = []
    for o in entry_obs:
        where = f"{o['repo']}#{o['number']}"
        if o.get("unavailable"):
            lines.append(f"{o['repo']} unavailable (HTTP 404) — cannot recheck {where}")
        elif o["kind"].startswith("pr"):
            if o.get("merged_at"):
                line = (f"PR {where} merged {cst(o['merged_at'])}"
                        f" (merge commit {str(o.get('merge_commit_sha'))[:10]})")
                c = o.get("containment")
                if c is None:
                    line += "; no release among the latest 20 contains the merge commit"
                elif c.get("tag_only"):
                    line += f"; no GitHub releases — tag “{c['tag']}” contains the merge commit"
                elif c.get("only_prerelease"):
                    line += (f"; only a prerelease contains it: {c['tag']}"
                             f" ({cst(c['published_at'])})")
                else:
                    line += (f"; earliest containing release: {c['tag']}"
                             f" ({cst(c['published_at'])})")
            elif o.get("state") == "open":
                line = f"PR {where} open"
            else:
                line = f"PR {where} closed without merge"
            lines.append(line)
        else:
            state = o.get("state")
            reason = o.get("state_reason")
            if state == "open":
                lines.append(f"issue {where} open")
            elif state == "closed":
                lines.append(
                    f"issue {where} closed ({reason or 'no reason recorded'})"
                    + (f" {cst(o.get('closed_at'))}" if o.get("closed_at") else "")
                )
            else:
                lines.append(f"issue {where} state {state}")
    return lines


def suggest(current: str, entry_obs: list[dict]) -> tuple[str, str] | None:
    """Derive (suggested_status, short_reason) from observations, or None.

    Rules (first match wins):
      * every GitHub link 404s            -> unconfirmed (repo unavailable)
      * a merged PR is in a stable release (or version-looking tag) -> released
      * a merged PR is only in prereleases / non-version tags       -> merged-unreleased
      * a merged PR is in no release/tag  -> merged-unreleased
      * PRs exist, none merged, one open  -> in-progress
      * PRs exist, all closed unmerged    -> closed
      * only issues (no PR links)         -> no suggestion (facts only)
    """
    prs = [o for o in entry_obs if o["kind"].startswith("pr")]
    if not entry_obs:
        return None
    if all(o.get("unavailable") for o in entry_obs):
        return "unconfirmed", "every GitHub link 404s (repo unavailable)"
    merged = [p for p in prs if p.get("merged_at")]
    if merged:
        with_c = [(p, p["containment"]) for p in merged if p.get("containment")]
        with_c.sort(key=lambda pc: pc[1].get("published_at") or "9999")
        stable = [pc for pc in with_c
                  if not pc[1]["prerelease"]
                  and (not pc[1]["tag_only"] or pc[1]["version_tag"])]
        if stable:
            p, c = stable[0]
            where = f"{p['repo']}#{p['number']}"
            if c["tag_only"]:
                return ("released",
                        f"PR {where} merged {cst(p['merged_at'])} is contained in tag "
                        f"{c['tag']} (no GitHub releases; tag-only evidence)")
            return ("released",
                    f"PR {where} merged {cst(p['merged_at'])} shipped in release "
                    f"{c['tag']} ({cst(c['published_at'])})")
        pre = [pc for pc in with_c if pc[1]["prerelease"]]
        if pre:
            p, c = pre[0]
            return ("merged-unreleased",
                    f"PR {p['repo']}#{p['number']} merged {cst(p['merged_at'])} is only "
                    f"in prerelease {c['tag']} ({cst(c['published_at'])})")
        tagonly = [pc for pc in with_c if pc[1]["tag_only"]]
        if tagonly:
            p, c = tagonly[0]
            return ("merged-unreleased",
                    f"PR {p['repo']}#{p['number']} merged {cst(p['merged_at'])} is "
                    f"contained only in non-version tag {c['tag']} "
                    f"(no GitHub releases; not evidence of a shipped release)")
        p = merged[0]
        return ("merged-unreleased",
                f"PR {p['repo']}#{p['number']} merged {cst(p['merged_at'])} but no "
                f"release among the latest 20 contains the merge commit")
    if prs:
        open_prs = [p for p in prs if p.get("state") == "open" and not p.get("unavailable")]
        if open_prs:
            names = ", ".join(f"{p['repo']}#{p['number']}" for p in open_prs)
            return "in-progress", f"PR(s) still open: {names}"
        names = ", ".join(f"{p['repo']}#{p['number']}" for p in prs)
        return "closed", f"all PRs closed without merge: {names}"
    # issues only: report facts, no status inference
    return None


# -- report rendering ---------------------------------------------------------
def render_markdown(report: dict) -> str:
    s = report["summary"]
    out = [
        "# OSC 7501 status recheck report",
        "",
        f"> {DISCLAIMER}",
        "",
        f"- generated: {report['generated_at']}",
        f"- source of truth: `data/integrations.yml` ({report['total_entries']} entries, "
        f"{s['checked_entries']} checked with target statuses "
        f"{', '.join(TARGET_STATUSES)})",
        f"- GitHub API: {report['api']}, {report['api_calls']} calls",
        f"- **suggestions: {len(report['findings'])}** "
        f"(entries whose suggested status differs from the current one)",
        "",
    ]
    if report["findings"]:
        out.append("## Suggested changes")
        out.append("")
        for i, f in enumerate(report["findings"], 1):
            out.append(f"### {i}. {f['id']} — {f['name']}")
            out.append("")
            out.append(f"- current status: `{f['current_status']}`")
            out.append(f"- **suggested status: `{f['suggested_status']}`** ({f['reason']})")
            out.append("- observed facts:")
            out.extend(f"  - {line}" for line in f["facts"])
            out.append("- links:")
            for label, url in f["links"]:
                out.append(f"  - [{label}]({url})")
            out.append("")
    else:
        out.append("No status changes suggested — every rechecked entry still "
                   "matches the observed GitHub state (or could not be rechecked "
                   "via PR/issue links).")
        out.append("")
    out.append("## Errors")
    out.append("")
    if report["errors"]:
        for e in report["errors"]:
            out.append(f"- {e['id']}: {e['url']}: {e['error']}")
    else:
        out.append("- none")
    out.append("")
    out.append(
        f"## Summary — checked {s['checked_entries']} entries "
        f"({s['checked_links']} GitHub links, {s['checked_repos']} repos) · "
        f"suggestions {len(report['findings'])} · errors {len(report['errors'])}"
    )
    out.append("")
    return "\n".join(out)


def render_json(report: dict) -> str:
    return json.dumps(report, ensure_ascii=False, indent=2) + "\n"


# -- main ----------------------------------------------------------------------
def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Report-only status recheck against the GitHub API "
                    "(never modifies data/ or docs/)."
    )
    ap.add_argument("--format", choices=["md", "json"], default="md",
                    help="report format (default: md)")
    ap.add_argument("--out", default=None, metavar="FILE",
                    help="write the report to FILE instead of stdout")
    ap.add_argument("--only", default=None, metavar="ID[,ID...]",
                    help="recheck only these entry ids (comma-separated)")
    ap.add_argument("--limit", type=int, default=None, metavar="N",
                    help="recheck at most N entries (smoke tests)")
    ap.add_argument("--sleep", type=float, default=0.5, metavar="SECONDS",
                    help="sleep between GitHub API calls (default: 0.5)")
    ap.add_argument("--fail-on-change", action="store_true",
                    help="exit 2 when any suggested status differs from the data file")
    args = ap.parse_args(argv)

    if not DATA_FILE.exists():
        print(f"error: {DATA_FILE} not found", file=sys.stderr)
        return 1

    doc = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8"))
    entries = doc["entries"]

    only = None
    if args.only:
        wanted = {x.strip() for x in args.only.split(",") if x.strip()}
        known = {e["id"] for e in entries}
        unknown = wanted - known
        if unknown:
            print(f"error: unknown id(s): {', '.join(sorted(unknown))}", file=sys.stderr)
            return 1
        only = wanted

    targets = [
        e for e in entries
        if e["status"] in TARGET_STATUSES and (only is None or e["id"] in only)
    ]
    if args.limit is not None:
        targets = targets[: args.limit]

    gh = GitHub(sleep=args.sleep)
    checker = Checker(gh)
    findings: list[dict] = []
    errors: list[dict] = []
    n_links = 0
    repos: set[str] = set()

    for i, entry in enumerate(targets, 1):
        eid = entry["id"]
        print(f"[{i}/{len(targets)}] {eid} ({entry['status']})",
              file=sys.stderr, flush=True)
        entry_obs: list[dict] = []
        entry_urls: list[tuple[str, str]] = []
        for src in entry.get("source", []):
            m = GH_URL_RE.search(src["url"])
            if not m:
                continue
            repo, kind, number = m.groups()
            repos.add(repo)
            n_links += 1
            entry_urls.append((f"{repo} {kind} #{number}", src["url"]))
            try:
                if kind == "pull":
                    obs = checker.observe_pr(repo, number, src["url"])
                else:
                    obs = checker.observe_issue(repo, number, src["url"])
            except ApiError as exc:
                errors.append({"id": eid, "url": src["url"], "error": str(exc)})
                continue
            entry_obs.append(obs)

        suggestion = suggest(entry["status"], entry_obs)
        if suggestion is None:
            continue
        suggested, reason = suggestion
        if suggested == entry["status"]:
            continue
        links = list(entry_urls)
        for o in entry_obs:
            c = o.get("containment")
            if c and not c.get("tag_only"):
                links.append((f"release {c['tag']}",
                              f"https://github.com/{o['repo']}/releases/tag/{c['tag']}"))
        findings.append({
            "id": eid,
            "name": entry["name"],
            "current_status": entry["status"],
            "suggested_status": suggested,
            "reason": reason,
            "facts": fact_lines(entry_obs),
            "links": links,
        })

    report = {
        "tool": "scripts/recheck.py",
        "generated_at": now_cst(),
        "disclaimer": DISCLAIMER,
        "target_statuses": TARGET_STATUSES,
        "total_entries": len(entries),
        "api": gh.describe(),
        "api_calls": gh.calls,
        "findings": findings,
        "errors": errors,
        "summary": {
            "checked_entries": len(targets),
            "checked_links": n_links,
            "checked_repos": len(repos),
            "findings": len(findings),
            "errors": len(errors),
        },
    }

    text = (render_json if args.format == "json" else render_markdown)(report)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)

    dest = args.out or "stdout"
    print(
        f"recheck: {len(targets)} entries checked, {len(findings)} suggestions, "
        f"{len(errors)} errors, {gh.calls} API calls; report written to {dest}",
        file=sys.stderr,
    )
    if args.fail_on_change and findings:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
