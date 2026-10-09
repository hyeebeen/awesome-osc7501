#!/bin/sh
# detect.sh — OSC 7501 feature detection.
#
#   detect.sh [-t SECONDS]      (default timeout: 1 second)
#
# Sends `OSC 7501 ; ? ST` immediately followed by a primary device attributes
# query (DA1, CSI c) to /dev/tty, then looks at which reply arrives first:
#   * `ESC ] 7501 ; ?` first  -> supported
#   * DA1 reply (ESC [ ? ... c) first -> unsupported (DA1 first)
#   * nothing before the timeout -> unsupported (no reply)
# If there is no usable tty, prints "no tty" and exits 2.
#
# Also reports whether the current terminfo entry has the extended `Pst`
# capability. NOTE: this is NOT authoritative — a missing Pst does not imply
# the terminal lacks OSC 7501 support (ssh, multiplexers or stale terminfo
# can all hide it); the query reply above is always authoritative.
#
# Exit codes: 0 supported, 1 unsupported, 2 no tty.

timeout=1
while getopts 't:h' _opt; do
    case "$_opt" in
        t) timeout=$OPTARG ;;
        h) sed -n '2,5p' "$0"; exit 0 ;;
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

reply=''
_i=0
while [ "$_i" -lt 2 ]; do
    _i=$((_i + 1))
    _chunk=$(dd bs=512 count=1 </dev/tty 2>/dev/null)
    reply="$reply$_chunk"
    # Stop as soon as we have something decidable.
    case "$reply" in
        *"${ESC}]7501;?"*|*"${ESC}[?"*) break ;;
    esac
done

osc_pat="${ESC}]7501;?"
da1_pat="${ESC}[?"
pos_osc=$(printf '%s' "$reply" | awk -v p="$osc_pat" 'NR == 1 { print index($0, p) + 0 }')
pos_da1=$(printf '%s' "$reply" | awk -v p="$da1_pat" 'NR == 1 { print index($0, p) + 0 }')
: "${pos_osc:=0}" "${pos_da1:=0}"   # empty reply -> awk prints nothing

result=1
if [ "$pos_osc" -gt 0 ] && { [ "$pos_da1" -eq 0 ] || [ "$pos_osc" -lt "$pos_da1" ]; }; then
    echo "supported"
    result=0
elif [ "$pos_da1" -gt 0 ]; then
    echo "unsupported (DA1 first)"
else
    echo "unsupported (no reply)"
fi

# terminfo check — informational only, not authoritative (see header).
if infocmp -x 2>/dev/null | grep -q Pst; then
    echo "terminfo: Pst present (reports OSC 7501 support)"
else
    echo "terminfo: Pst absent (NOT authoritative — see comment in detect.sh)"
fi

exit "$result"
