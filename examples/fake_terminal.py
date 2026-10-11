#!/usr/bin/env python3
"""Run a command inside a pty and pretend to be a terminal (test harness).

Watches the command's output for the OSC 7501 feature-detection query
(``ESC ] 7501 ; ?`` + ST or BEL) and the DA1 request (``CSI c``) and answers
them according to ``--mode``. Everything the command writes is forwarded to
stdout with control bytes escaped (ESC -> ``^[``, BEL -> ``^G``, other
non-printables -> ``^XY``). Exits with the command's exit code.

Modes:
  v04     reply to the 7501 query with Ghostty/libghostty-vt's full rev 0.4
          answer ``?:states=idle,working,done,blocked,error:
          kinds=permission,question,auth``, then DA1 ``ESC [ ?62;22c``
  bare    reply with a bare ``?`` (a reply without lists), then DA1
  da1     answer only DA1 — reproduces the "DA1 first -> unsupported" path
  silent  answer nothing — reproduces the "no reply" path

Usage:
  python3 fake_terminal.py --mode v04 -- sh detect.sh
  python3 fake_terminal.py --mode=da1 -- python3 -c 'print("hi")'

Standard library only (Python 3.9+). No real terminal required: this exists
so detect.sh's supported / DA1-first paths can be driven locally.
"""

from __future__ import annotations

import os
import pty
import select
import sys

ESC = b"\x1b"
QUERY_ST = b"\x1b]7501;?\x1b\\"    # OSC 7501 ; ? ST
QUERY_BEL = b"\x1b]7501;?\x07"     # OSC 7501 ; ? BEL
DA1_REQUEST = b"\x1b[c"            # CSI c
# libghostty-vt rev 0.4: computed from its State/Kind enums, ST-terminated.
V04_REPLY = (
    b"\x1b]7501;?:states=idle,working,done,blocked,error"
    b":kinds=permission,question,auth\x1b\\"
)
BARE_REPLY = b"\x1b]7501;?\x1b\\"
DA1_REPLY = b"\x1b[?62;22c"

MODES = ("v04", "bare", "da1", "silent")

USAGE = "usage: fake_terminal.py [--mode MODE] -- COMMAND [ARGS...]"


def escape(data: bytes) -> str:
    out = []
    for b in data:
        if b == 0x1B:
            out.append("^[")
        elif b == 0x07:
            out.append("^G")
        elif b in (0x09, 0x0A, 0x0D):
            out.append(chr(b))
        elif 0x20 <= b < 0x7F:
            out.append(chr(b))
        else:
            out.append("^%02x" % b)
    return "".join(out)


def answer(buf: bytes, mode: str, write) -> bytes:
    """Consume recognized requests in buf, replying per mode.

    Returns the unconsumed tail (capped so sequences split across reads
    are still matched). Answering every occurrence, not just the first,
    is what a terminal does.
    """
    while True:
        best = None  # (index, kind, length)
        for seq, kind in ((QUERY_ST, "osc"), (QUERY_BEL, "osc"),
                          (DA1_REQUEST, "da1")):
            i = buf.find(seq)
            if i != -1 and (best is None or i < best[0]):
                best = (i, kind, len(seq))
        if best is None:
            break
        i, kind, length = best
        buf = buf[i + length:]
        if kind == "osc" and mode in ("v04", "bare"):
            write(V04_REPLY if mode == "v04" else BARE_REPLY)
        elif kind == "da1" and mode != "silent":
            write(DA1_REPLY)
    return buf[-16:]


def parse_args(argv):
    mode = "v04"
    cmd = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--":
            cmd = argv[i + 1:]
            break
        if arg == "--mode":
            i += 1
            if i >= len(argv):
                print("fake_terminal.py: --mode needs a value", file=sys.stderr)
                sys.exit(2)
            mode = argv[i]
        elif arg.startswith("--mode="):
            mode = arg.split("=", 1)[1]
        elif arg in ("-h", "--help"):
            print(__doc__.strip())
            return None, None
        else:
            cmd = argv[i:]
            break
        i += 1
    if mode not in MODES:
        print("fake_terminal.py: unknown mode %r (choose from: %s)"
              % (mode, " ".join(MODES)), file=sys.stderr)
        sys.exit(2)
    if not cmd:
        print(USAGE, file=sys.stderr)
        sys.exit(2)
    return mode, cmd


def main(argv) -> int:
    mode, cmd = parse_args(argv)
    if cmd is None:
        return 0

    pid, master = pty.fork()
    if pid == 0:  # child: the command runs with the pty as its tty
        try:
            os.execvp(cmd[0], cmd)
        except OSError as exc:
            print("fake_terminal.py: %s" % exc, file=sys.stderr)
            os._exit(127)

    def write_master(data: bytes) -> None:
        try:
            os.write(master, data)
        except OSError:
            pass

    buf = b""
    last = "\n"
    while True:
        try:
            ready, _, _ = select.select([master], [], [], 0.2)
        except InterruptedError:
            continue
        if master not in ready:
            continue
        try:
            data = os.read(master, 4096)
        except OSError:  # EIO once the child side is gone
            break
        if not data:
            break
        text = escape(data)
        sys.stdout.write(text)
        sys.stdout.flush()
        if text:
            last = text[-1]
        buf = answer(buf + data, mode, write_master)

    if last != "\n":
        sys.stdout.write("\n")
    sys.stdout.flush()

    _, status = os.waitpid(pid, 0)
    code = os.waitstatus_to_exitcode(status)
    return code if code >= 0 else 128 - code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
