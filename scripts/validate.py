#!/usr/bin/env python3
"""Validate data/integrations.yml + data/resources.yml against data/schema.json.

Checks:
  1. JSON Schema (draft 2020-12) validation of both files
  2. id uniqueness across both files
  3. every url / source[].url is http(s) or an existing repo-relative path
  4. entry url == first source url
Prints counts per file / category / status. Exits 1 on any error.

Usage: python3 scripts/validate.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
FILES = [  # (label, path) — integrations count is asserted by the schema users, printed here
    ("integrations", DATA / "integrations.yml"),
    ("resources", DATA / "resources.yml"),
]


def check_url(url: str, where: str, errors: list[str]) -> None:
    if url.startswith(("http://", "https://")):
        return
    if url.startswith(("/", "~")) or ".." in url.split("/"):
        errors.append(f"{where}: {url!r} is not http(s) and not a safe repo-relative path")
        return
    if not (REPO / url).exists():
        errors.append(f"{where}: {url!r} is neither http(s) nor an existing repo-relative path")


def main() -> int:
    errors: list[str] = []

    schema = json.loads((DATA / "schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    seen_ids: dict[str, str] = {}
    all_docs: dict[str, dict] = {}

    for label, path in FILES:
        if not path.exists():
            print(f"error: missing {path.relative_to(REPO)}", file=sys.stderr)
            return 1
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        all_docs[label] = doc
        for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path)):
            loc = f"{path.name}#{'/'.join(str(p) for p in err.absolute_path)}"
            errors.append(f"schema: {loc}: {err.message}")

        for i, entry in enumerate(doc.get("entries", [])):
            where = f"{path.name} entries[{i}]"
            eid = entry.get("id", "<missing>")
            if eid in seen_ids:
                errors.append(f"{where}: duplicate id {eid!r} (also in {seen_ids[eid]})")
            else:
                seen_ids[eid] = where
            for url in [entry.get("url")] + [s.get("url") for s in entry.get("source", [])]:
                if not isinstance(url, str) or not url:
                    errors.append(f"{where}: empty or missing url")
                    continue
                check_url(url, where, errors)
            source = entry.get("source") or []
            if source and entry.get("url") != source[0].get("url"):
                errors.append(f"{where}: url {entry.get('url')!r} != first source url {source[0].get('url')!r}")

    # counts per file / category / status
    for label, path in FILES:
        entries = all_docs[label].get("entries", [])
        print(f"{label}: {len(entries)}")
        for field in ("category", "status"):
            counts = Counter(e.get(field, "?") for e in entries)
            print(f"  by {field}: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))

    if errors:
        print(f"\n{len(errors)} error(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("OK: schema valid, ids unique, all urls resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
