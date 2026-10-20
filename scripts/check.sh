#!/bin/sh
# CI check sequence — exactly what `make check` runs (this box has no make).
# validate -> build --check (idempotency) -> unit tests -> markdownlint
set -eu

echo "== validate: data/*.yml against data/schema.json =="
python3 scripts/validate.py

echo "== build --check: generated files up to date =="
python3 scripts/build.py --check

echo "== unit tests: examples/test_osc7501_parser.py =="
python3 -m unittest discover -s examples

echo "== markdownlint: **/*.md =="
markdownlint-cli2 "**/*.md" "#node_modules"

echo "ALL CHECKS PASSED"
