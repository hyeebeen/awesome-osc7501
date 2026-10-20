#!/usr/bin/env python3
"""Validate data/*.yml against their schemas (data/schema.json, data/featured.schema.json).

Checks:
  1. JSON Schema (draft 2020-12) validation of integrations.yml, resources.yml
     and featured.yml
  2. id uniqueness across both entry files
  3. every url / source[].url is http(s) or an existing repo-relative path
  4. entry url == first source url
  5. no duplicate urls across different resources.yml entries
  6. every featured.yml id (top3 + groups, no repeats) exists in
     integrations.yml or resources.yml
  7. featured.yml ids cover exactly the entries with featured: true
  8. aliases never collide with a live id
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
FEATURED = DATA / "featured.yml"


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

    featured_schema = json.loads((DATA / "featured.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(featured_schema)
    featured_validator = Draft202012Validator(featured_schema, format_checker=FormatChecker())

    seen_ids: dict[str, str] = {}
    all_docs: dict[str, dict] = {}

    if not FEATURED.exists():
        print(f"error: missing {FEATURED.relative_to(REPO)}", file=sys.stderr)
        return 1
    featured = yaml.safe_load(FEATURED.read_text(encoding="utf-8"))
    for err in sorted(featured_validator.iter_errors(featured), key=lambda e: list(e.absolute_path)):
        loc = f"{FEATURED.name}#{'/'.join(str(p) for p in err.absolute_path)}"
        errors.append(f"schema: {loc}: {err.message}")

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

    # resources.yml: no url may appear under two different entries (the url is
    # the identity of a curated resource; duplicates get merged with `aliases`)
    resource_urls: dict[str, str] = {}
    for i, entry in enumerate(all_docs["resources"].get("entries", [])):
        where = f"resources.yml entries[{i}] ({entry.get('id', '<missing>')})"
        for url in [entry.get("url")] + [s.get("url") for s in entry.get("source", [])]:
            if not isinstance(url, str):
                continue
            if url in resource_urls and resource_urls[url] != entry.get("id"):
                errors.append(
                    f"{where}: duplicate url {url!r} (also in entry {resource_urls[url]!r}); "
                    "keep one entry and record the other id under `aliases`"
                )
            else:
                resource_urls[url] = entry.get("id")

    # aliases are historical slugs of merged/deleted entries; they must not
    # collide with any live id (in either file)
    for label, path in FILES:
        for i, entry in enumerate(all_docs[label].get("entries", [])):
            for alias in entry.get("aliases", []):
                if alias in seen_ids:
                    errors.append(
                        f"{path.name} entries[{i}] ({entry.get('id')!r}): alias {alias!r} collides with a live id"
                    )

    # featured.yml: ids exist, are used once, and match featured:true exactly
    top3 = featured.get("top3") or []
    group_ids = [i for g in (featured.get("groups") or []) for i in (g.get("ids") or [])]
    picked: list[str] = top3 + group_ids
    seen_pick: set[str] = set()
    for i, fid in enumerate(picked):
        if fid in seen_pick:
            errors.append(f"featured.yml: id {fid!r} listed more than once")
        seen_pick.add(fid)
        if fid not in seen_ids:
            errors.append(f"featured.yml: unknown id {fid!r} (not in integrations.yml or resources.yml)")
    featured_true = {
        e.get("id")
        for label, _ in FILES
        for e in all_docs[label].get("entries", [])
        if e.get("featured") is True
    }
    for fid in sorted(set(picked) - featured_true):
        errors.append(f"featured.yml: id {fid!r} is listed but not featured:true in data")
    for fid in sorted(featured_true - set(picked)):
        errors.append(f"featured.yml: id {fid!r} is featured:true in data but never listed")

    # counts per file / category / status
    for label, path in FILES:
        entries = all_docs[label].get("entries", [])
        print(f"{label}: {len(entries)}")
        for field in ("category", "status"):
            counts = Counter(e.get(field, "?") for e in entries)
            print(f"  by {field}: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print(f"featured: {len(top3)} top3 + {len(group_ids)} grouped = {len(picked)} picks")

    if errors:
        print(f"\n{len(errors)} error(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("OK: schema valid, ids unique, all urls resolve, featured picks consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
