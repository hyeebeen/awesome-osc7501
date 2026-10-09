#!/bin/sh
# bytes-demo.sh — print the exact bytes of the canonical OSC 7501 sequences
# so you can eyeball (or diff) what actually goes down the wire.
#
# Usage: sh examples/bytes-demo.sh
# Exits non-zero if any assertion fails.
set -u

. "$(dirname "$0")/osc7501.sh"

ESC=$(printf '\033')

fail() {
    echo "FAIL: $*" >&2
    exit 1
}

section() {
    echo
    echo "=== $1 ==="
}

# ---------------------------------------------------------------------------
echo "osc7501.sh byte demo — canonical OSC 7501 sequences"

# ---------------------------------------------------------------------------
section "(a) spec's Terraform example (ST = ESC \\)"

msg='Apply 3 to add, 1 to change, 0 to destroy?'
expected_b64='QXBwbHkgMyB0byBhZGQsIDEgdG8gY2hhbmdlLCAwIHRvIGRlc3Ryb3k/'

actual_b64=$(_osc7501_b64 "$msg")
[ "$actual_b64" = "$expected_b64" ] ||
    fail "base64 mismatch: got '$actual_b64', want '$expected_b64'"

# Build the sequence through the library (stdout target) …
OSC7501_OUT=-
seq_a=$(osc7501_report blocked 'kind=permission' 'app=terraform' "msg=$msg")
unset OSC7501_OUT
[ -n "$seq_a" ] || fail "library produced an empty sequence"

# … and compare with the sequence written out in the spec.
expected_a="${ESC}]7501;state=blocked:kind=permission:app=terraform:msg=${expected_b64}${ESC}\\"
[ "$seq_a" = "$expected_a" ] || fail "sequence mismatch vs spec example"

echo "msg base64 OK: $actual_b64"
echo "sequence matches the spec's Terraform example."
printf '%s' "$seq_a" | od -An -tx1 -c

# ---------------------------------------------------------------------------
section "(b) feature detection query, ST-terminated"

seq_b="${ESC}]7501;?${ESC}\\"
printf '%s' "$seq_b" | od -An -tx1 -c

# ---------------------------------------------------------------------------
section "(c) feature detection query, BEL-terminated"

seq_c="${ESC}]7501;?$(printf '\a')"
printf '%s' "$seq_c" | od -An -tx1 -c

# ---------------------------------------------------------------------------
section "byte -> meaning cheat sheet"

cat <<'EOF'
1b          ESC    starts every escape sequence
1b 5d       ESC ]  OSC (Operating System Command) introducer
37 35 30 31 '7501' the OSC number (ASCII "7501")
3b          ';'    separates the OSC number from the key=value pairs
3f          '?'    feature-detection query (instead of pairs)
1b 5c       ESC \  ST — string terminator (ends the OSC)
07          BEL    alternate string terminator
EOF

echo
echo "all assertions passed."
