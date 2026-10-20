#!/usr/bin/env python3
"""Deterministic generator: data/*.yml is the single source of truth.

Inputs: data/integrations.yml, data/resources.yml, data/featured.yml
(README「只看 3 条」/ 精选 picks) and examples/test_osc7501_parser.py (test count).

Outputs (regenerated in place; no wall-clock timestamps, so runs are idempotent):

  docs/support-matrix.md   the 4 category tables inside ONE generated marker
                           region; each row's name cell starts with a stable
                           anchor <a id="ID"></a>, so docs/support-matrix.md#ID
                           is a permanent link
  data/integrations.json   machine-readable export for agents
  data/resources.json      same export shape for the curated resource list
  README.md                只看 3 条 (top3) + 精选 (featured) blocks,
                           支持概览 count table, verification date and inline
                           unit-test count
  README.en.md             same blocks, English variants

Markers (everything between BEGIN/END is replaced wholesale on every run; all
bytes outside the markers are left untouched). A missing marker is an error:
nothing is inserted and the build aborts non-zero.

  <!-- BEGIN GENERATED: matrix (scripts/build.py; edit data/integrations.yml instead) --> ... <!-- END GENERATED: matrix -->
  <!-- BEGIN GENERATED: top3 (scripts/build.py; edit data/featured.yml instead) --> ... <!-- END GENERATED: top3 -->
  <!-- BEGIN GENERATED: featured (scripts/build.py; edit data/featured.yml instead) --> ... <!-- END GENERATED: featured -->
  <!-- BEGIN GENERATED: status-counts --> ... <!-- END GENERATED: status-counts -->
  <!-- BEGIN GENERATED: verified-at -->DATE<!-- END GENERATED: verified-at -->
  <!-- BEGIN GENERATED: test-count -->N<!-- END GENERATED: test-count -->

Data files are validated first (delegates to scripts/validate.py, which checks
the schemas + id/url hygiene + featured consistency); the build aborts non-zero
on any error.

Usage:
  python3 scripts/build.py           regenerate outputs in place
  python3 scripts/build.py --check   build in memory; exit 1 and list any file
                                     that would change (CI / idempotency)
"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- markers ---
MATRIX_BEGIN = "<!-- BEGIN GENERATED: matrix (scripts/build.py; edit data/integrations.yml instead) -->"
MATRIX_END = "<!-- END GENERATED: matrix -->"
COUNTS_BEGIN = "<!-- BEGIN GENERATED: status-counts -->"
COUNTS_END = "<!-- END GENERATED: status-counts -->"
TOP3_BEGIN = "<!-- BEGIN GENERATED: top3 (scripts/build.py; edit data/featured.yml instead) -->"
TOP3_END = "<!-- END GENERATED: top3 -->"
FEATURED_BEGIN = "<!-- BEGIN GENERATED: featured (scripts/build.py; edit data/featured.yml instead) -->"
FEATURED_END = "<!-- END GENERATED: featured -->"
VERIFIED_BEGIN = "<!-- BEGIN GENERATED: verified-at -->"
VERIFIED_END = "<!-- END GENERATED: verified-at -->"
TESTCOUNT_BEGIN = "<!-- BEGIN GENERATED: test-count -->"
TESTCOUNT_END = "<!-- END GENERATED: test-count -->"

# the fixed third「只看 3 条」item is a repo path, not a data entry
TOP3_LOCAL = {
    "zh": "- [docs/practice.md](docs/practice.md) - 本仓库可运行的发送端/接收端示例与实测记录（含 tmux 透传），读完能直接动手。",
    "en": "- [docs/practice.md](docs/practice.md) - Runnable sender/receiver examples from this repo, with real run logs (including tmux passthrough).",
}

# spec block for the JSON exports (facts from README.md: rev 0.4, 2026-10-10)
SPEC = {
    "name": "OSC 7501 Program Status Protocol",
    "revision": "0.4",
    "url": "https://www.superlogical.com/rex/docs/build/program-status",
}

# canonical enum orders (schema order; also the display order)
STATUS_ORDER = [
    "released",
    "implemented-self-reported",
    "merged-unreleased",
    "in-progress",
    "announced",
    "closed",
    "unsupported",
    "unconfirmed",
]
EVIDENCE_ORDER = [
    "verified",
    "self-reported",
    "self-reported-third-party",
    "inferred",
    "not-found",
]
CATEGORY_ORDER = ["receiver", "agent", "cli", "library", "spec", "reference", "article", "discussion"]

# status -> Chinese table-cell label (exact inverse of scripts/migrate_matrix.py)
STATUS_ZH_CELL = {
    "released": "已发布",
    "implemented-self-reported": "已实现",
    "merged-unreleased": "已合并未发版",
    "in-progress": "开发中",
    "announced": "仅宣布",
    "closed": "已关闭",
    "unsupported": "未支持",
    "unconfirmed": "未确认",
}
# status -> Chinese label as used by the 状态定义 table / README count table
STATUS_ZH_LABEL = {**STATUS_ZH_CELL, "implemented-self-reported": "已实现（自述）"}
STATUS_EN = {
    "released": "Released",
    "implemented-self-reported": "Implemented (self-reported)",
    "merged-unreleased": "Merged, unreleased",
    "in-progress": "In development",
    "announced": "Announced",
    "closed": "Closed",
    "unsupported": "Unsupported",
    "unconfirmed": "Unconfirmed",
}
# evidence_type -> Chinese label; not-found has no fixed label (the note is the
# cell text, verbatim), so it maps to None
EVIDENCE_ZH_LABEL = {
    "verified": "已验证",
    "self-reported": "自述",
    "self-reported-third-party": "自述（第三方）",
    "inferred": "推断",
    "not-found": None,
}

# category -> H3 heading inside the generated matrix region (order/headings as
# the four hand-written tables that used to live in docs/support-matrix.md)
MATRIX_SECTIONS = [
    ("receiver", "表 1 · 终端 / 多路复用器 / agent 工作台 / 嵌入库（接收端）"),
    ("agent", "表 2 · AI agent 与 coding CLI（发送端）"),
    ("cli", "表 3 · 非 AI CLI（发送端）"),
    ("library", "表 4 · TUI 库 / SDK"),
]

TESTS_FILE = REPO / "examples" / "test_osc7501_parser.py"


class BuildError(Exception):
    pass


# ------------------------------------------------------------------ input ---
def validate_data() -> None:
    """Delegate schema + hygiene checks to scripts/validate.py (aborts on error)."""
    proc = subprocess.run([sys.executable, str(REPO / "scripts" / "validate.py")], cwd=REPO)
    if proc.returncode != 0:
        raise BuildError("data validation failed (scripts/validate.py returned non-zero); aborting")


def load_entries(name: str) -> list[dict]:
    path = REPO / "data" / f"{name}.yml"
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    entries = doc.get("entries") or []
    if not entries:
        raise BuildError(f"{path.relative_to(REPO)} has no entries")
    return entries


def load_featured() -> dict:
    path = REPO / "data" / "featured.yml"
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not (doc and doc.get("top3") and doc.get("groups")):
        raise BuildError(f"{path.relative_to(REPO)} needs top3 and groups")
    return doc


def count_unit_tests() -> int:
    """Number of `def test_...` functions in the example test file (ast, no execution)."""
    tree = ast.parse(TESTS_FILE.read_text(encoding="utf-8"))
    return sum(
        1
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_")
    )


# -------------------------------------------------------------- rendering ---
def status_cell(entry: dict) -> str:
    """Inverse of migrate_matrix.parse_status: label +（note）appended."""
    cell = STATUS_ZH_CELL[entry["status"]]
    note = entry.get("status_note")
    return f"{cell}（{note}）" if note else cell


def evidence_cell(entry: dict) -> str:
    """Inverse of migrate_matrix.parse_evidence (exact inverse mapping)."""
    etype, note = entry["evidence_type"], entry.get("evidence_note")
    if etype == "not-found":
        return note  # rendered verbatim, no fixed label
    if etype == "self-reported-third-party":
        return f"自述（{note or '第三方'}）"
    label = EVIDENCE_ZH_LABEL[etype]
    return f"{label}（{note}）" if note else label


def source_link(src: dict) -> str:
    """One source item: <url> autolink, or [label](url); relative urls are
    repo-root-relative in the yml and must render relative to docs/."""
    url = src["url"]
    label = src.get("label")
    if not url.startswith(("http://", "https://")):
        url = "../" + url
    return f"[{label}]({url})" if label else f"<{url}>"


def matrix_row(entry: dict) -> str:
    cells = [
        f'<a id="{entry["id"]}"></a>{entry["name"]}',
        entry["role"],
        status_cell(entry),
        entry["version"],
        evidence_cell(entry),
        " · ".join(source_link(s) for s in entry["source"]),
        entry["verified_at"],
    ]
    for cell in cells:
        if "|" in cell:
            raise BuildError(f"{entry['id']}: cell contains a table-breaking pipe: {cell!r}")
    return "| " + " | ".join(cells) + " |"


def matrix_block(entries: list[dict]) -> str:
    covered = {cat for cat, _ in MATRIX_SECTIONS}
    orphans = sorted({e["category"] for e in entries} - covered)
    if orphans:
        raise BuildError(f"categories not shown in the matrix: {orphans}")
    header = "| 名称 | 角色 | 状态 | 版本 | 证据类型 | 来源链接 | 核实日期 |"
    sep = "| --- | --- | --- | --- | --- | --- | --- |"
    sections = []
    for cat, heading in MATRIX_SECTIONS:
        rows = [matrix_row(e) for e in entries if e["category"] == cat]
        if not rows:
            raise BuildError(f"no entries for matrix category {cat!r}")
        sections.append("\n".join([f"### {heading}", "", header, sep, *rows]))
    return "\n\n".join(sections)


def counts_block(lang: str, entries: list[dict]) -> str:
    """README 支持概览 / Overview table (zh labels in README.md, en in README.en.md)."""
    counts = Counter(e["status"] for e in entries)
    total = len(entries)
    latest = max(e["verified_at"] for e in entries)
    rows = [(s, counts[s]) for s in STATUS_ORDER if counts.get(s)]
    if lang == "zh":
        head = f"状态类别统计（{total} 个条目，统计口径见 [docs/support-matrix.md](docs/support-matrix.md)；最近核实 {latest}）："
        label = lambda s: STATUS_ZH_LABEL[s]  # noqa: E731
        c0, c1, total_row = "状态", "数量", "合计"
    else:
        head = f"Status counts ({total} tracked entries; methodology in the [support matrix](docs/support-matrix.md); latest verified {latest}):"
        label = lambda s: STATUS_EN[s]  # noqa: E731
        c0, c1, total_row = "Status", "Count", "Total"
    lines = [head, "", f"| {c0} | {c1} |", "| --- | --- |"]
    lines += [f"| {label(s)} | {n} |" for s, n in rows]
    lines.append(f"| {total_row} | {total} |")
    return "\n".join(lines)


# ------------------------------------------------------ featured / top3 ---
def featured_item(entry: dict, lang: str, integration_ids: set[str]) -> str:
    """- [name](url) - why（状态，见 [矩阵](docs/support-matrix.md#id)）
    status label comes from data; resources have no matrix row/anchor, so no
    matrix link is rendered for them."""
    eid = entry["id"]
    if lang == "zh":
        label = STATUS_ZH_LABEL[entry["status"]]
        tail = f"（{label}，见 [矩阵](docs/support-matrix.md#{eid})）" if eid in integration_ids else f"（{label}）"
        return f"- [{entry['name']}]({entry['url']}) - {entry['why']}{tail}"
    label = STATUS_EN[entry["status"]]
    tail = f" ({label}, see [matrix](docs/support-matrix.md#{eid}))" if eid in integration_ids else f" ({label})"
    return f"- [{entry['name']}]({entry['url']}) - {entry['why_en']}{tail}"


def top3_block(lang: str, featured: dict, by_id: dict[str, dict], integration_ids: set[str]) -> str:
    items = [featured_item(by_id[i], lang, integration_ids) for i in featured["top3"]]
    items.append(TOP3_LOCAL[lang])
    return "\n".join(items)


def featured_block(lang: str, featured: dict, by_id: dict[str, dict], integration_ids: set[str]) -> str:
    sections = []
    for group in featured["groups"]:
        title = group["title_zh"] if lang == "zh" else group["title_en"]
        items = [featured_item(by_id[i], lang, integration_ids) for i in group["ids"]]
        sections.append(f"#### {title}\n\n" + "\n".join(items))
    return "\n\n".join(sections)


# ------------------------------------------------------------------- json ---
def entry_json(entry: dict, anchored: bool) -> dict:
    out = {"id": entry["id"]}
    # resources are not rendered in docs/support-matrix.md, so their anchor
    # target does not exist; the field is kept for shape parity, value null
    out["anchor"] = f"docs/support-matrix.md#{entry['id']}" if anchored else None
    for key, value in entry.items():  # yml key order, minus id
        if key != "id":
            out[key] = value
    return out


def export_doc(entries: list[dict], source: str, anchored: bool) -> dict:
    by_status = {s: n for s in STATUS_ORDER if (n := Counter(e["status"] for e in entries).get(s))}
    by_category = {c: n for c in CATEGORY_ORDER if (n := Counter(e["category"] for e in entries).get(c))}
    return {
        "schema": "data/schema.json",
        "generated_by": "scripts/build.py",
        "source": source,
        "spec": SPEC,
        "counts": {"by_status": by_status, "by_category": by_category, "total": len(entries)},
        "latest_verified_at": max(e["verified_at"] for e in entries),
        "status_labels_zh": STATUS_ZH_LABEL,
        "evidence_labels_zh": EVIDENCE_ZH_LABEL,
        "entries": [entry_json(e, anchored) for e in entries],
    }


def dumps_json(doc: dict) -> str:
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


# -------------------------------------------------------------- rewriting ---
def replace_region(text: str, path: Path, begin: str, end: str, mid: str) -> str:
    """Replace the exact span between the two markers with `mid`; abort on a
    missing marker (nothing is inserted)."""
    i = text.find(begin)
    if i < 0:
        raise BuildError(f"{path.relative_to(REPO)}: marker not found: {begin}")
    j = text.find(end, i + len(begin))
    if j < 0:
        raise BuildError(f"{path.relative_to(REPO)}: marker not found: {end}")
    return text[: i + len(begin)] + mid + text[j:]


def generate() -> dict[Path, str]:
    integrations = load_entries("integrations")
    resources = load_entries("resources")
    featured = load_featured()
    n_tests = count_unit_tests()

    by_id: dict[str, dict] = {}
    for e in (*integrations, *resources):
        if e["id"] in by_id:
            raise BuildError(f"duplicate id across data files: {e['id']}")
        by_id[e["id"]] = e
    picked = [*featured["top3"], *(i for g in featured["groups"] for i in g["ids"])]
    missing = [i for i in picked if i not in by_id]
    if missing:
        raise BuildError(f"data/featured.yml references unknown ids: {missing}")
    integration_ids = {e["id"] for e in integrations}
    latest_verified = max(e["verified_at"] for e in by_id.values())

    outputs: dict[Path, str] = {}

    # docs/support-matrix.md: one generated region with the 4 category tables
    matrix_md = REPO / "docs" / "support-matrix.md"
    text = matrix_md.read_text(encoding="utf-8")
    text = replace_region(text, matrix_md, MATRIX_BEGIN, MATRIX_END, "\n\n" + matrix_block(integrations) + "\n\n")
    outputs[matrix_md] = text

    # JSON exports
    outputs[REPO / "data" / "integrations.json"] = dumps_json(export_doc(integrations, "data/integrations.yml", anchored=True))
    outputs[REPO / "data" / "resources.json"] = dumps_json(export_doc(resources, "data/resources.yml", anchored=False))

    # README.md (zh) / README.en.md (en): top3 + featured + count table +
    # verification date + inline test count
    for name, lang in (("README.md", "zh"), ("README.en.md", "en")):
        readme = REPO / name
        text = readme.read_text(encoding="utf-8")
        text = replace_region(text, readme, TOP3_BEGIN, TOP3_END, "\n\n" + top3_block(lang, featured, by_id, integration_ids) + "\n\n")
        text = replace_region(text, readme, FEATURED_BEGIN, FEATURED_END, "\n\n" + featured_block(lang, featured, by_id, integration_ids) + "\n\n")
        text = replace_region(text, readme, COUNTS_BEGIN, COUNTS_END, "\n\n" + counts_block(lang, integrations) + "\n\n")
        text = replace_region(text, readme, VERIFIED_BEGIN, VERIFIED_END, latest_verified)
        text = replace_region(text, readme, TESTCOUNT_BEGIN, TESTCOUNT_END, str(n_tests))
        outputs[readme] = text

    return outputs


def same_as_disk(path: Path, content: str) -> bool:
    return path.exists() and path.read_text(encoding="utf-8") == content


def main(argv: list[str]) -> int:
    check = "--check" in argv
    if argv and not check:
        print(f"error: unknown arguments: {argv}", file=sys.stderr)
        return 2

    try:
        validate_data()
        outputs = generate()
    except BuildError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if check:
        drifted = [p for p, content in outputs.items() if not same_as_disk(p, content)]
        if drifted:
            print("build --check: generated files out of date; run: python3 scripts/build.py", file=sys.stderr)
            for p in drifted:
                print(f"  would change: {p.relative_to(REPO)}", file=sys.stderr)
            return 1
        print("build --check: OK ({} generated files up to date)".format(len(outputs)))
        return 0

    for path, content in outputs.items():
        if same_as_disk(path, content):
            print(f"unchanged: {path.relative_to(REPO)}")
        else:
            path.write_text(content, encoding="utf-8")
            print(f"wrote:     {path.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
