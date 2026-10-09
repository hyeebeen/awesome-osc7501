#!/bin/sh
# tmux-passthrough.sh — experiment: does OSC 7501 survive tmux?
#
# tmux does not understand OSC 7501 and drops it. The DCS passthrough
# escape (ESC P tmux; ... ESC \, inner ESCs doubled) can carry arbitrary
# sequences to the outer terminal, but only with
#     set -g allow-passthrough on      (tmux >= 3.3)
#
# For each of the 4 combinations (allow-passthrough off/on × bare/wrapped)
# this script:
#   1. starts an isolated tmux server  (tmux -L osc7501test -f /dev/null)
#   2. attaches a tmux client under `script -q -c` so everything the client
#      writes to its terminal lands in a typescript file; the client's stdin
#      is a FIFO held open (otherwise an immediate EOF kills the client)
#   3. types a command into the pane that uses examples/osc7501.sh to emit
#      state=working (bare, or DCS-wrapped via OSC7501_TMUX_PASSTHROUGH=1)
#   4. kills the server (which makes the client — and therefore `script`,
#      whose typescript is stdio-buffered — exit), then greps the typescript
#      for the raw OSC 7501 bytes
#
# Expected (verified against tmux 3.5a):
#   allow-passthrough off + bare      -> absent (tmux drops unknown OSC)
#   allow-passthrough off + wrapped   -> absent (passthrough disabled)
#   allow-passthrough on  + bare      -> absent (still an unknown OSC)
#   allow-passthrough on  + wrapped   -> present (passed through)
#
# Usage: sh examples/tmux-passthrough.sh
set -u

libdir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
sock=osc7501test
sess=oscx
dir="/tmp/osc7501-tmux-$$"

mkdir -p "$dir" || exit 1

cleanup() {
    (unset TMUX TMUX_PANE; tmux -L "$sock" kill-server 2>/dev/null)
    [ -n "${holder:-}" ] && kill "$holder" 2>/dev/null
    rm -rf "$dir"
}
trap cleanup 0
trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM

# tmc — talk to the isolated server without nesting confusion
tmc() {
    (unset TMUX TMUX_PANE; exec tmux -L "$sock" "$@")
}

# Clear any stale server left over from an earlier (e.g. interrupted) run.
tmc kill-server 2>/dev/null

holder=''

# run_case ALLOW WRAPPED -> prints the result line; returns 0 if it matches
# the expectation.
run_case() {
    allow=$1
    wrapped=$2
    ts="$dir/ts-allow-$allow-wrapped-$wrapped.log"
    hold="$dir/hold-$allow-$wrapped"

    tmc new-session -d -s "$sess" -x 100 -y 30
    tmc set-option -g allow-passthrough "$allow"

    # Keep the client's stdin open: an instant EOF would make the tmux
    # client exit (and take the session with it) before we can drive it.
    mkfifo "$hold"
    (sleep 30) >"$hold" &
    holder=$!

    script -q -c "env TERM=xterm-256color tmux -L $sock attach" "$ts" \
        <"$hold" >/dev/null 2>&1 &
    spid=$!
    sleep 1

    # Type a command into the pane that emits the report through the library.
    if [ "$wrapped" = 1 ]; then pt=1; else pt=0; fi
    pane_cmd="sh -c '. $libdir/osc7501.sh; export OSC7501_TMUX_PASSTHROUGH=$pt; export OSC7501_OUT=-; osc7501_status working tmux-payload'"
    tmc send-keys -t "$sess:0" -l "$pane_cmd"
    tmc send-keys -t "$sess:0" Enter
    sleep 2

    # Killing the server takes the attached client down with it, which
    # makes `script` exit and flush its (stdio-buffered) typescript.
    tmc kill-server 2>/dev/null
    wait "$spid" 2>/dev/null
    kill "$holder" 2>/dev/null
    holder=''

    # What the outer terminal should have received (tmux unwraps the DCS
    # passthrough and un-doubles the ESCs, so both cases search for the
    # same raw bytes).
    pat=$(printf '\033]7501;state=working:msg=%s\033\\' \
        "$(printf '%s' tmux-payload | base64 | tr -d '\n')")
    if [ -f "$ts" ] && grep -aqF -- "$pat" "$ts"; then
        found=present
    else
        found=absent
    fi

    if [ "$allow" = on ] && [ "$wrapped" = 1 ]; then want=present; else want=absent; fi
    label=$(printf 'allow-passthrough=%-3s  %-11s -> %s' "$allow" \
        "$( [ "$wrapped" = 1 ] && echo DCS-wrapped || echo bare )" "$found")
    if [ "$found" = "$want" ]; then
        echo "$label  (as expected)"
        return 0
    fi
    echo "$label  (UNEXPECTED, wanted $want)" >&2
    return 1
}

fails=0
run_case off 0 || fails=$((fails + 1))
run_case off 1 || fails=$((fails + 1))
run_case on  0 || fails=$((fails + 1))
run_case on  1 || fails=$((fails + 1))

echo
if [ "$fails" -eq 0 ]; then
    echo "all 4 cases behaved as expected."
    exit 0
fi
echo "$fails case(s) behaved unexpectedly." >&2
exit 1
