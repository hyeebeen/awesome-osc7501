#!/bin/sh
# detect.sh — OSC 7501 feature detection (spec rev 0.4).
#
#   detect.sh [-t SECONDS]      (default timeout: 1 second)
#
# Sends `OSC 7501 ; ? ST` immediately followed by a primary device attributes
# query (DA1, CSI c) to /dev/tty, then looks at which reply arrives first:
#   * an OSC 7501 reply (starts with `ESC ] 7501 ; ?`) first -> supported
#   * a DA1 reply (ESC [ ? ... c) first -> unsupported (DA1 first)
#   * nothing before the timeout -> unsupported (no reply)
# If there is no usable tty, prints "no tty" and exits 2.
#
# Rev 0.4: the reply is `?` optionally followed by
# `:states=<comma list>:kinds=<comma list>`; unknown pairs are ignored.
# Reads until the OSC reply is terminated (ESC \ or BEL — the spec does not
# require the reply to reuse the query's terminator) or the DA1 reply ends
# with `c`, so a states=/kinds= listing is not truncated. A reply without
# the lists means the fixed defaults: idle,working,done,blocked,error and
# permission,question,auth — printed with "(default)". If supported, the
# accepted states and kinds are printed after the verdict.
#
# Exit codes: 0 supported, 1 unsupported, 2 no tty.

timeout=1
while getopts 't:h' _opt; do
    case "$_opt" in
        t) timeout=$OPTARG ;;
        h) sed -n '2,4p' "$0"; exit 0 ;;
        *) echo "usage: $0 [-t SECONDS]" >&2; exit 2 ;;
    esac
done
shift $((OPTIND - 1))

# A usable tty must be openable both ways.
if ! (: </dev/tty) >/dev/null 2>&1 || ! (: >/dev/tty) 2>/dev/null; then
    echo "no tty"
    exit 2
fi

saved=$(stty -g </dev/tty 2>/dev/null) || {
    echo "no tty"
    exit 2
}
restore() {
    stty "$saved" </dev/tty 2>/dev/null
}
trap 'restore' 0
trap 'restore; exit 130' INT
trap 'restore; exit 143' TERM

# `time N` is in deciseconds; clamp to 1..255.
deciseconds=$(awk -v t="$timeout" 'BEGIN{
    d = int(t * 10 + 0.5); if (d < 1) d = 1; if (d > 255) d = 255; print d
}')
stty -echo -icanon min 0 time "$deciseconds" </dev/tty

ESC=$(printf '\033')
# OSC 7501 ; ? ST, then DA1 (CSI c)
printf '%s]7501;?%s\\' "$ESC" "$ESC" >/dev/tty
printf '%s[c' "$ESC" >/dev/tty

# Decide from $reply: prints the result lines and exits 0 (supported),
# 1 (unsupported) or 42 (nothing decidable yet — keep reading; pass the
# argument "final" to force a decision at timeout).
# $reply is passed through the environment because command substitution
# strips trailing newlines and awk -v would eat backslashes in ESC \.
decide() {
    DT_REPLY="$reply" DT_FINAL="${1:-}" awk 'BEGIN {
        r = ENVIRON["DT_REPLY"]
        esc = "\033"
        pre = esc "]7501;?"
        pos_osc = index(r, pre)
        pos_da1 = index(r, esc "[?")

        # OSC reply body: after the prefix, up to ESC \ or BEL. The value
        # charset has no ESC, so the first terminator ends the reply.
        body = ""
        osc_done = 0
        if (pos_osc > 0) {
            rest = substr(r, pos_osc + length(pre))
            i = index(rest, esc "\\")   # ST
            j = index(rest, "\007")     # BEL
            if (i > 0 && (j == 0 || i < j)) {
                body = substr(rest, 1, i - 1); osc_done = 1
            } else if (j > 0) {
                body = substr(rest, 1, j - 1); osc_done = 1
            } else {
                body = rest   # truncated: parse what arrived so far
            }
        }
        # A DA1 reply always ends with `c`.
        da1_done = (pos_da1 > 0 && substr(r, length(r)) == "c")

        if (ENVIRON["DT_FINAL"] == "" && !osc_done && !da1_done) exit 42

        if (pos_osc > 0 && (pos_da1 == 0 || pos_osc < pos_da1)) {
            print "supported"
            states = ""
            kinds = ""
            n = split(body, seg, ":")   # body: ":states=..:kinds=.." or ""
            for (k = 1; k <= n; k++) {
                eq = index(seg[k], "=")
                if (eq == 0) continue
                key = substr(seg[k], 1, eq - 1)
                val = substr(seg[k], eq + 1)
                if (key == "states") states = val
                else if (key == "kinds") kinds = val
                # unknown pairs: ignored, as the spec requires
            }
            if (states == "")
                print "states: idle,working,done,blocked,error (default)"
            else
                print "states: " states
            if (kinds == "")
                print "kinds: permission,question,auth (default)"
            else
                print "kinds: " kinds
            exit 0
        }
        if (pos_da1 > 0) {
            print "unsupported (DA1 first)"
            exit 1
        }
        print "unsupported (no reply)"
        exit 1
    }'
}

# Read until the OSC reply is complete, the DA1 reply has ended, or the
# read times out with no data (min 0 time N makes each dd return then).
reply=''
result=''
rc=42
_iter=0
while [ "$_iter" -lt 100 ]; do
    _iter=$((_iter + 1))
    _chunk=$(dd bs=512 count=1 </dev/tty 2>/dev/null)
    [ -n "$_chunk" ] || break
    reply="$reply$_chunk"
    result=$(decide)
    rc=$?
    [ "$rc" -ne 42 ] && break
done
if [ "$rc" -eq 42 ]; then
    result=$(decide final)
    rc=$?
fi

printf '%s\n' "$result"
exit "$rc"
