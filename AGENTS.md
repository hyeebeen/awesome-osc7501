# AGENTS.md

Working agreement for coding agents and maintainers contributing to this repo.
Everything below exists to keep the data trustworthy: first-hand sources,
explicit status and evidence enums, deterministic generation, and AI
contributions that a human actually verified.

## Purpose & scope

This repo helps people understand the OSC 7501 "Program Status Protocol" and
gives agents reliable, checkable context about it: a byte-level deep-dive of
the spec, runnable examples, and a support matrix in which every claim traces
back to a first-hand source with a verification date.

It is deliberately **not** a promotion list: no ranking, no hype, no
unverifiable claims. Anything that cannot be traced to a first-hand source is
recorded as `unconfirmed` or not recorded at all. Facts about the protocol
come from the spec and this repo's docs; facts about integrations come from
`data/*.yml` and the generated matrix — never from memory or search results.

## Data flow

`data/*.yml` is the single source of truth; everything listed below it is
generated (rerun after every data edit):

```text
data/integrations.yml + data/resources.yml + data/featured.yml
        │
        ▼
scripts/validate.py      schema + hygiene checks (id uniqueness, urls resolve,
                        featured picks consistent with featured: true)
        │
        ▼
scripts/build.py        deterministic regeneration (no wall-clock timestamps)
        ├─ docs/support-matrix.md     4 category tables inside ONE generated region
        ├─ README.md / README.en.md   top3 + featured + status counts + verified date
        ├─ data/integrations.json     machine-readable export
        ├─ data/resources.json        machine-readable export
        └─ llms.txt                   whole file (no markers; build.py owns it)
```

- Generated regions are delimited by `<!-- BEGIN GENERATED: ... -->` /
  `<!-- END GENERATED: ... -->` markers; everything between them is replaced
  wholesale on every build. **Never hand-edit them** — edit `data/*.yml` and
  rerun `python3 scripts/build.py`.
- `llms.txt` has no markers: the build script owns the entire file, so counts,
  verification dates and research links can never drift.
- One command runs the full gate (validate → build `--check` → unit tests →
  markdownlint with 0 errors):

```sh
sh scripts/check.sh   # or: make check
```

## Data model

`data/integrations.yml` and `data/resources.yml` both hold an `entries:` list
validated against `data/schema.json` (`data/featured.schema.json` covers the
README picks). Every field:

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `id` | string | yes | Stable kebab-case slug, unique across both files; never change once published — it is rendered as the permanent anchor `docs/support-matrix.md#<id>`. |
| `name` | string | yes | Display name (vendor/qualifier allowed). |
| `url` | string | yes | Primary link: http(s) URL or an existing repo-root-relative path; must equal the first `source` url. |
| `category` | enum | yes | `receiver` / `agent` / `cli` / `library` / `spec` / `reference` / `article` / `discussion`. |
| `role` | string | yes | One-line role of the project (terminal, multiplexer, AI coding agent, library…). |
| `status` | enum | yes | Support status; exact definitions below. |
| `status_note` | string \| null | no | Caveat rendered next to the status (e.g. 「推断」). |
| `version` | string | yes | Version/tag/date cell, copied verbatim; `—` when none. Version strings live only here and in the matrix/timeline. |
| `evidence_type` | enum | yes | Kind of evidence; exact definitions below. |
| `evidence_note` | string \| null | no | Free text for the evidence column; for `not-found` this note *is* the cell. |
| `source` | array | yes | At least one first-hand source, each `{url, label}`; `url` required, `label` optional display text. |
| `verified_at` | date | yes | `YYYY-MM-DD` date a human last verified the entry from the sources (Asia/Shanghai, CST). |
| `why` | string \| null | no | Chinese one-liner: why the entry is worth reading (used by featured picks). |
| `why_en` | string | if featured | English one-liner; the build renders the English picks from it. |
| `featured` | boolean | yes | `true` = eligible for the curated README picks; must be listed in `data/featured.yml`. |
| `track` | object | no | Optional `{repo: owner/name, pr: number}` tracking hint reserved for recheck runs; currently unused by the data. |
| `aliases` | string[] | no | Historical ids of merged/deleted entries; must never collide with a live id. |

Status enum — pick the status you can *evidence*, not the one that sounds best:

| Status | Definition |
| --- | --- |
| `released` | A published release/tag contains the change, verified by compare (see [How to verify a status](#how-to-verify-a-status)). |
| `implemented-self-reported` | Official docs state it is implemented, but no version/release can be found. |
| `merged-unreleased` | Merged on the default branch, but no release contains it. |
| `in-progress` | Open PR / branch. |
| `announced` | Public statement only. |
| `closed` | PR closed unmerged / effort abandoned. |
| `unsupported` | No implementation found, or the maintainer declined. |
| `unconfirmed` | Could not be checked. |

Evidence enum:

| Evidence | Definition |
| --- | --- |
| `verified` | Traceable to a first-hand source (spec, source code, PR, release, the author's own post). |
| `self-reported` | The party itself claims it. |
| `self-reported-third-party` | Relayed by a third party, not the integrator. |
| `inferred` | Concluded from multiple first-hand sources; always labelled as an inference. |
| `not-found` | Nothing found; `evidence_note` carries the full cell text. |

Field notes:

- `verified_at` is the date a human opened the sources and confirmed the entry
  — `YYYY-MM-DD` in Asia/Shanghai time (label CST, UTC+8). It is never copied
  from the upstream event date.
- `why` / `why_en` carry one sentence each on why the entry matters; `why` may
  be `null` for non-featured entries, `why_en` must exist for anything picked
  in `data/featured.yml`.
- `featured` marks eligibility; `data/featured.yml` (top3 + groups) must list
  exactly the ids with `featured: true` — `scripts/validate.py` enforces both
  directions.
- `aliases` — when two entries merge, keep one `id` and record the other under
  the surviving entry's `aliases`; ids are permanent anchors (each integration
  renders as an `<a id>` in `docs/support-matrix.md`, so links of the form
  `docs/support-matrix.md#<id>` must keep working forever).

## How to verify a status

The compare rule (also in [docs/support-matrix.md](docs/support-matrix.md)):

```sh
# does a release contain the merge commit? ahead|identical = contained
gh api repos/OWNER/REPO/compare/MERGE_SHA...TAG --jq .status
```

- Merged PR contained in a stable release (or a version-looking tag when the
  repo has no releases) → `released`; merged but contained in nothing →
  `merged-unreleased`; PR open → `in-progress`; closed unmerged → `closed`.
- `python3 scripts/recheck.py` re-queries the GitHub API for the recheckable
  statuses and prints **suggestions only** — it never edits data; a human
  confirms and then edits `data/integrations.yml` (`--fail-on-change` exits 2
  on drift; CI runs it weekly, report-only).
- Timezone rule: all times are Asia/Shanghai, labelled CST (UTC+8); convert
  GitHub timestamps the same way before writing them down.

## Rules

- **First-hand sources only**: spec text, implementation source and PRs,
  official releases/changelogs, the author's own posts. Second-hand coverage
  may be filed as an `article`/`discussion` resource but never decides a
  status.
- **Never invent numbers, dates, quotes, star counts or PR numbers.** Copy
  them verbatim from the source; when quoting, quote verbatim (keep original
  typos, note them if it matters).
- Mark uncertainty in `status_note` / `evidence_note` (e.g. 「推断」), not in
  prose; if it cannot be verified, `unconfirmed` is a valid answer.
- Version strings and release dates live only in `data/*.yml`,
  `docs/support-matrix.md` and `docs/timeline.md`; README, deep-dive, why\* and
  practice link to the matrix instead.
- Write about projects, not companies or people: no company names or personal
  background of maintainers beyond what the project itself publishes.
- Don't chase hype: an entry needs verifiable adoption facts, not momentum.

## Policy on AI-generated contributions

- AI-generated contributions are allowed, but must be disclosed in the PR.
- Every changed fact must carry a first-hand link checked by a human; that
  human sets `verified_at` and is accountable for the claim.
- Automated workflows (bots, scheduled agents) only open issues/reports — they
  never edit content, data files or generated files.
- PRs that only reformat generated files (marker regions, `data/*.json`,
  `llms.txt`) are rejected; rerun `python3 scripts/build.py` instead.

## Checklist before committing

- [ ] `python3 scripts/validate.py` passes after your data edits.
- [ ] `python3 scripts/build.py` ran; `git diff` shows no hand edits inside
      `BEGIN GENERATED` regions or in `llms.txt`.
- [ ] `sh scripts/check.sh` (or `make check`) passes end to end — validate,
      build `--check`, unit tests, markdownlint 0 errors.
- [ ] Every new/changed fact has a first-hand source link and a fresh
      `verified_at` (CST); `status` and `evidence_type` follow the enums above.
- [ ] Version strings appear only in `data/*.yml`, `docs/support-matrix.md`,
      `docs/timeline.md`.
- [ ] Status re-verifications recorded under `research/`; `CHANGELOG.md` has
      an entry for the change.
