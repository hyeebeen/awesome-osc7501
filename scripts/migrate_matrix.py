#!/usr/bin/env python3
"""One-off migration: parse the 4 hand-written tables in docs/support-matrix.md
into data/integrations.yml (the new single source of truth).

Kept in the repo for provenance. docs/support-matrix.md stays frozen; re-running
this script regenerates data/integrations.yml deterministically from it.

Usage: python3 scripts/migrate_matrix.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "docs" / "support-matrix.md"
DST = REPO / "data" / "integrations.yml"

# generated once from docs/support-matrix.md on 2026-10-21; now the single source of truth
HEADER = (
    "# generated once from docs/support-matrix.md on 2026-10-21; now the single source of truth\n"
    "# regenerate with: python3 scripts/migrate_matrix.py (markdown tables are frozen)\n"
)

# table number (## 表 N · ...) -> category
CATEGORY_BY_TABLE = {1: "receiver", 2: "agent", 3: "cli", 4: "library"}

# 状态 cell starts with -> status enum (longest prefixes first)
STATUS_MAP = [
    ("已合并未发版", "merged-unreleased"),
    ("已实现", "implemented-self-reported"),
    ("已发布", "released"),
    ("开发中", "in-progress"),
    ("仅宣布", "announced"),
    ("已关闭", "closed"),
    ("未支持", "unsupported"),
    ("未确认", "unconfirmed"),
]

# 证据类型 cell -> evidence enum (longest / most specific first)
EVIDENCE_MAP = [
    ("自述（第三方）", "self-reported-third-party"),
    ("已验证", "verified"),
    ("自述", "self-reported"),
    ("推断", "inferred"),
    # anything else -> not-found with the full original text in evidence_note
]

# names whose slug would be generic / ambiguous / non-ASCII -> fixed stable id
ID_OVERRIDES = {
    "Ghostty 应用": "ghostty-app",
    "ServerBox（flutter_server_box）": "serverbox",
    "agent（lydakis/agent）": "lydakis-agent",
    "Terraform / Homebrew": "terraform-homebrew-poc",
}

ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
LINK_RE = re.compile(r"<([^<>]+)>|\[([^\]]+)\]\(([^)]+)\)")


def derive_id(name: str) -> str:
    """Stable kebab-case ASCII slug from the 名称 cell."""
    if name in ID_OVERRIDES:
        return ID_OVERRIDES[name]
    base = re.sub(r"（.*?）", "", name).strip()  # drop fullwidth parenthetical
    slug = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")
    if not slug or not ID_RE.fullmatch(slug):
        raise ValueError(f"cannot derive ASCII id from name: {name!r}")
    return slug


def unwrap_paren(text: str) -> str | None:
    """'（foo）' -> 'foo'; '' -> None; anything else verbatim."""
    text = text.strip()
    if not text:
        return None
    if text.startswith("（") and text.endswith("）"):
        return text[1:-1].strip()
    return text


def parse_status(cell: str) -> tuple[str, str | None]:
    for prefix, enum in STATUS_MAP:
        if cell.startswith(prefix):
            return enum, unwrap_paren(cell[len(prefix) :])
    raise ValueError(f"unmapped 状态 cell: {cell!r}")


def parse_evidence(cell: str) -> tuple[str, str | None]:
    for prefix, enum in EVIDENCE_MAP:
        if cell.startswith(prefix):
            note = cell[len(prefix) :]
            if enum == "self-reported-third-party":
                return enum, unwrap_paren(note) or "第三方"
            return enum, unwrap_paren(note)
    return "not-found", cell  # full original text, verbatim


def normalize_url(url: str) -> str:
    """Repo-relative for relative links: ../research/x.md -> research/x.md."""
    while url.startswith("../"):
        url = url[len("../") :]
    return url


def parse_links(cell: str) -> list[dict]:
    """来源链接 cell -> ordered [{url, label}]; label only for [text](url) links."""
    links = []
    for m in LINK_RE.finditer(cell):
        if m.group(1) is not None:  # <https://...> autolink
            links.append({"url": normalize_url(m.group(1).strip()), "label": None})
        else:  # [text](url)
            links.append({"url": normalize_url(m.group(3).strip()), "label": m.group(2).strip()})
    return links


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_tables(text: str) -> list[tuple[str, list[list[str]]]]:
    """Return [(category, [row cells...]), ...] for the 4 「表 N」 tables.

    Row cells: [名称, 角色, 状态, 版本, 证据类型, 来源链接, 核实日期]
    """
    lines = text.splitlines()
    tables: list[tuple[str, list[list[str]]]] = []
    i = 0
    while i < len(lines):
        m = re.match(r"^## 表 (\d+) ·", lines[i])
        if not m:
            i += 1
            continue
        category = CATEGORY_BY_TABLE[int(m.group(1))]
        rows: list[list[str]] = []
        i += 1
        while i < len(lines) and not lines[i].startswith("## "):
            line = lines[i]
            if line.startswith("|"):
                cells = split_row(line)
                header = cells[0] == "名称"
                separator = bool(re.fullmatch(r":?-{3,}:?", cells[0]))
                if not header and not separator:
                    if len(cells) != 7:
                        raise ValueError(f"expected 7 cells, got {len(cells)}: {line!r}")
                    rows.append(cells)
            i += 1
        tables.append((category, rows))
    if len(tables) != 4:
        raise ValueError(f"expected 4 tables, found {len(tables)}")
    return tables


def build_entry(category: str, cells: list[str]) -> dict:
    name, role, status_cell, version, evidence_cell, links_cell, verified_at = cells
    links = parse_links(links_cell)
    if not links:
        raise ValueError(f"no links in 来源链接 cell of {name!r}")
    status, status_note = parse_status(status_cell)
    evidence_type, evidence_note = parse_evidence(evidence_cell)
    return {
        "id": derive_id(name),
        "name": name,
        "url": links[0]["url"],
        "category": category,
        "role": role,
        "status": status,
        "status_note": status_note,
        "version": version,
        "evidence_type": evidence_type,
        "evidence_note": evidence_note,
        "source": links,
        "verified_at": verified_at,
        "why": None,  # one-line "why it matters"; filled later for featured items
        "featured": False,
    }


class Dumper(yaml.SafeDumper):
    pass


def _repr_str(dumper: yaml.Dumper, data: str):
    # force quotes on date-like strings so they round-trip as str, not date
    style = "'" if re.fullmatch(r"\d{4}-\d{2}-\d{2}", data) else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


Dumper.add_representer(str, _repr_str)


def main() -> int:
    tables = parse_tables(SRC.read_text(encoding="utf-8"))
    entries = []
    for category, rows in tables:
        for cells in rows:
            entries.append(build_entry(category, cells))

    ids = [e["id"] for e in entries]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"duplicate ids: {sorted(dupes)}")

    DST.parent.mkdir(parents=True, exist_ok=True)
    body = yaml.dump(
        {"entries": entries},
        Dumper=Dumper,
        allow_unicode=True,
        sort_keys=False,
        width=4096,
        default_flow_style=False,
    )
    DST.write_text(HEADER + body, encoding="utf-8")

    per_table = {c: len(rows) for c, rows in tables}
    print(f"wrote {DST.relative_to(REPO)}: {len(entries)} entries ({per_table})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
