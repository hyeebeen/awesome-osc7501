#!/bin/sh
# wrap.sh — run a command wrapped in OSC 7501 status reports.
#
#   wrap.sh [--app NAME] -- cmd args...
#
# * before the command starts:  state=working  msg="Running: cmd"
# * on success (exit 0):        state=done     msg carries the elapsed seconds
# * on failure:                 state=error    msg carries the exit code
# * on Ctrl-C (SIGINT):         state=idle, exit 130
# The child's exit code is preserved.
#
# Reports go where examples/osc7501.sh sends them (/dev/tty by default;
# OSC7501_OUT / OSC7501_TMUX_PASSTHROUGH are honored).
set -u

. "$(dirname "$0")/osc7501.sh"

usage() {
    echo "usage: $0 [--app NAME] -- cmd args..." >&2
}

app=''
while [ $# -gt 0 ]; do
    case "$1" in
        --app)
            [ $# -ge 2 ] || { usage; exit 2; }
            app=$2
            shift 2
            ;;
        --app=*)
            app=${1#--app=}
            shift
            ;;
        --)
            shift
            break
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "$0: unrecognized argument '$1'" >&2
            usage
            exit 2
            ;;
    esac
done
[ $# -gt 0 ] || { usage; exit 2; }

cmd_str=''
for _arg in "$@"; do
    cmd_str="${cmd_str:+$cmd_str }$_arg"
done

# _now_ms — milliseconds since epoch; falls back to whole seconds if
# `date +%s%3N` is unsupported (e.g. BSD date), which only coarsens
# the reported duration.
_now_ms() {
    _t=$(date +%s%3N 2>/dev/null)
    case $_t in
        ''|*[!0-9]*) date +%s ;;
        *) echo "$_t" ;;
    esac
}

# _report STATE MSG — include app= when one was given
_report() {
    if [ -n "$app" ]; then
        osc7501_report "$1" "app=$app" "msg=$2"
    else
        osc7501_status "$1" "$2"
    fi
}

start=$(_now_ms)

trap '_report idle "Interrupted: '"$cmd_str"'"; exit 130' INT
trap '_report idle "Terminated: '"$cmd_str"'"; exit 143' TERM

_report working "Running: $cmd_str"

"$@"
rc=$?

secs=$(awk "BEGIN{printf \"%.1f\", ($(_now_ms) - $start)/1000}")
if [ "$rc" -eq 0 ]; then
    _report done "Done: $cmd_str (${secs}s)"
else
    _report error "Failed: $cmd_str (exit $rc)"
fi
exit "$rc"
