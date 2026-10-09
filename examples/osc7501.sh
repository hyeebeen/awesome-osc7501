#!/bin/sh
# osc7501.sh — POSIX sh helpers for the OSC 7501 "Program Status Protocol"
# (spec: https://www.superlogical.com/rex/docs/build/program-status)
#
# Source this file, then use:
#   osc7501_report STATE [key=value ...]   full report, e.g.
#       osc7501_report blocked 'kind=permission' 'app=myapp' 'msg=Allow this?'
#   osc7501_status STATE "message"         blog-style shorthand (state + msg only)
#   osc7501_clear [id]                     clear one record subtree / all records
#
# STATE is one of: idle working done blocked error clear
#
# msg= and title= values are plain text here; they are automatically encoded
# as standard base64 (newlines stripped) as the protocol requires. All other
# key=value pairs are passed through verbatim (id=, kind=, progress=, app=...).
#
# Output target:
#   * default: /dev/tty if writable, otherwise stdout
#   * OSC7501_OUT=path  append the raw escape sequences to that file instead
#   * OSC7501_OUT=-     write to stdout
#
# tmux: tmux does not forward OSC 7501 (it drops unknown OSC). When running
# inside tmux ($TMUX non-empty) AND OSC7501_TMUX_PASSTHROUGH=1, every sequence
# is wrapped in a DCS passthrough:
#       ESC P tmux ; <payload with every ESC doubled> ESC \
#   which tmux unwraps and forwards to the outer terminal. This requires
#   tmux >= 3.3 and the server option `set -g allow-passthrough on`
#   (put it in ~/.tmux.conf or run `tmux set -g allow-passthrough on`).
#
# No external dependencies beyond POSIX sh + base64(1) + tr(1) + sed(1).

# _osc7501_b64 TEXT — base64 of TEXT without trailing newline
_osc7501_b64() {
    printf '%s' "$1" | base64 | tr -d '\n'
}

# _osc7501_double_esc — double every ESC byte on stdin (for DCS passthrough)
_osc7501_double_esc() {
    sed "s/$(printf '\033')/$(printf '\033\033')/g"
}

# _osc7501_emit SEQ — write raw sequence SEQ to the configured target
_osc7501_emit() {
    _seq=$1
    # tmux DCS passthrough wrapping (see header comment)
    if [ -n "${TMUX:-}" ] && [ "${OSC7501_TMUX_PASSTHROUGH:-0}" = "1" ]; then
        _seq=$(printf '\033Ptmux;%s\033\\' "$(printf '%s' "$_seq" | _osc7501_double_esc)")
    fi
    if [ -n "${OSC7501_OUT:-}" ]; then
        if [ "$OSC7501_OUT" = "-" ]; then
            printf '%s' "$_seq"
        else
            printf '%s' "$_seq" >>"$OSC7501_OUT"
        fi
    elif ! printf '%s' "$_seq" 2>/dev/null >/dev/tty; then
        # /dev/tty unwritable or unopenable (no controlling terminal):
        # fall back to stdout. (A permission test like [ -w /dev/tty ] is
        # not enough — the device can be mode 666 yet lack a controlling tty.
        # stderr is redirected before the /dev/tty open so the shell's
        # “cannot create /dev/tty” diagnostic stays out of the way.)
        printf '%s' "$_seq"
    fi
    unset _seq
}

# osc7501_report STATE [key=value ...]
#   msg=TITLE and title=TEXT values are base64-encoded automatically;
#   every other pair is emitted verbatim. ST is ESC \ (the spec's terminator).
osc7501_report() {
    if [ $# -lt 1 ]; then
        echo "usage: osc7501_report STATE [key=value ...]" >&2
        return 2
    fi
    _osc7501_state=$1
    shift
    case "$_osc7501_state" in
        idle|working|done|blocked|error|clear) ;;
        *)
            echo "osc7501_report: invalid state '$_osc7501_state'" \
                "(want idle|working|done|blocked|error|clear)" >&2
            unset _osc7501_state
            return 2
            ;;
    esac
    _osc7501_pairs="state=$_osc7501_state"
    for _osc7501_kv in "$@"; do
        case "$_osc7501_kv" in
            msg=*|title=*)
                _osc7501_k=${_osc7501_kv%%=*}
                _osc7501_v=${_osc7501_kv#*=}
                _osc7501_pairs="$_osc7501_pairs:$_osc7501_k=$(_osc7501_b64 "$_osc7501_v")"
                ;;
            *)
                _osc7501_pairs="$_osc7501_pairs:$_osc7501_kv"
                ;;
        esac
    done
    _osc7501_emit "$(printf '\033]7501;%s\033\\' "$_osc7501_pairs")"
    _rc=$?
    unset _osc7501_state _osc7501_pairs _osc7501_kv _osc7501_k _osc7501_v
    return $_rc
}

# osc7501_status STATE "message" — the simple helper from the announcement
# blog post: state + base64 msg, nothing else.
osc7501_status() {
    if [ $# -ne 2 ]; then
        echo "usage: osc7501_status STATE \"message\"" >&2
        return 2
    fi
    osc7501_report "$1" "msg=$2"
}

# osc7501_clear [id] — delete the record for id and all of its children;
# without an id, clear every record on this terminal.
osc7501_clear() {
    if [ $# -gt 1 ]; then
        echo "usage: osc7501_clear [id]" >&2
        return 2
    fi
    if [ $# -eq 1 ]; then
        osc7501_report clear "id=$1"
    else
        osc7501_report clear
    fi
}
