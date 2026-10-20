# Makefile — task runner for this repo (validate / build / test / lint / check).
#
# NOTE: this box has no `make` binary. Every target below is therefore also
# runnable without make:
#
#   make validate == python3 scripts/validate.py
#   make build    == python3 scripts/build.py
#   make check    == sh scripts/check.sh
#                    (runs, in order: validate -> build --check -> unit tests
#                     -> markdownlint-cli2 "**/*.md" "#node_modules")
#   make test     == python3 -m unittest discover -s examples
#   make lint     == markdownlint-cli2 "**/*.md" "#node_modules"
#   make recheck  == python3 scripts/recheck.py
#                    (report-only: queries the GitHub API via `gh` or
#                     GITHUB_TOKEN, never edits data/ or docs/)
#
# scripts/check.sh is the canonical CI sequence; `make check` just calls it so
# the two can never drift.

.PHONY: validate build check test lint recheck

validate:
	python3 scripts/validate.py

build:
	python3 scripts/build.py

check:
	sh scripts/check.sh

test:
	python3 -m unittest discover -s examples

lint:
	markdownlint-cli2 "**/*.md" "#node_modules"

recheck:
	python3 scripts/recheck.py
