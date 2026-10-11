#!/usr/bin/env python3
"""Incremental parser for OSC 7501 (Program Status Protocol).

Spec: https://www.superlogical.com/rex/docs/build/program-status (rev 0.4)

Feed raw bytes (from a pty, a log file, a socket, ...) to ``Osc7501Parser``
and get back ``Query`` / ``Report`` events. Parsing is fully incremental:
sequences may be split across ``feed()`` calls at arbitrary byte boundaries.
Non-7501 OSC sequences and plain data are skipped.

``RecordStore`` implements the terminal-side record semantics on top of the
parser: whole-record replacement, subtree clears, ``app`` inheritance from
the nearest ancestor, working/blocked cleanup on process exit / new prompt,
LRU eviction past 256 records, and RIS reset.

Rev 0.4 feature-detection replies: ``parse_query_reply`` and
``choose_state`` are the program side, ``make_query_reply`` the terminal
side.

CLI: ``python3 osc7501_parser.py [file]`` reads the file (stdin by default)
and prints one JSON object per parsed event per line.

Python 3.11+, standard library only.
"""

from __future__ import annotations

import base64
import binascii
import json
import re
import sys
from dataclasses import dataclass, field
from typing import Optional

# --- limits from the spec ------------------------------------------------
MAX_SEQUENCE_BYTES = 4096   # whole sequence, incl. ESC ] and terminator
MAX_KEY_BYTES = 16
MAX_MSG_ENCODED = 2732
MAX_MSG_DECODED = 2048
MAX_TITLE_ENCODED = 256
MAX_TITLE_DECODED = 192
MAX_APP_BYTES = 32
# Spec rev 0.4 still caps id at 128 bytes total. kitty's author points out
# that 8 full segments plus separators need 8*32 + 7 = 263 bytes, so a
# maximal id does not fit; unresolved as of 2026-10-11.
# https://github.com/kovidgoyal/kitty/issues/10638
MAX_ID_TOTAL = 128
MAX_ID_SEGMENT = 32
MAX_ID_DEPTH = 8
MAX_RECORDS = 256

STATES = ("idle", "working", "done", "blocked", "error", "clear")
KINDS = ("permission", "question", "auth")
TRANSIENT_STATES = ("working", "blocked")

# Query-reply defaults (rev 0.4): a reply without states means exactly these
# five (not counting clear); without kinds, exactly these three. The lists
# are fixed and do not change in later revisions.
DEFAULT_STATES = ("idle", "working", "done", "blocked", "error")
DEFAULT_KINDS = ("permission", "question", "auth")

KEY_RE = re.compile(r"[a-z]+")
VALUE_RE = re.compile(r"[A-Za-z0-9_.,+/=-]*")
APP_RE = re.compile(r"[A-Za-z0-9_.+-]{1,%d}" % MAX_APP_BYTES)
ID_SEGMENT_RE = re.compile(r"[A-Za-z0-9_.+-]{1,%d}" % MAX_ID_SEGMENT)
DIGITS_RE = re.compile(r"[0-9]+")

OSC_PREFIX = b"7501;"       # what follows "ESC ]" for this protocol
ESC = 0x1B
BEL = 0x07

# Hard cap on the body we accumulate, purely to bound memory; sequences that
# would exceed it are over-limit anyway.
_BODY_STORE_CAP = MAX_SEQUENCE_BYTES + 16


# --- events ---------------------------------------------------------------

@dataclass
class Event:
    """Base class for parser events."""


@dataclass
class Query(Event):
    """`OSC 7501 ; ? ST` — feature-detection query (or a terminal's reply).

    Rev 0.4: a reply starts with `?` and MAY append `states=...` and
    `kinds=...` pairs. Programs MUST ignore pairs they do not understand;
    a missing list means the fixed defaults, so `states`/`kinds` are always
    populated (a bare `?` → DEFAULT_STATES / DEFAULT_KINDS).
    """

    states: tuple[str, ...] = DEFAULT_STATES
    kinds: tuple[str, ...] = DEFAULT_KINDS


@dataclass
class Report(Event):
    """A valid `OSC 7501 ; pairs ST` report.

    Fields set to ``None`` mean "key absent or invalid → treated as
    default/absent" per the spec. ``raw_pairs`` holds the final (after
    duplicate resolution) well-formed key=value strings, including keys this
    parser does not know.
    """

    state: str
    id: Optional[str] = None
    kind: Optional[str] = None
    progress: Optional[int] = None
    app: Optional[str] = None
    title: Optional[str] = None
    msg: Optional[str] = None
    raw_pairs: dict = field(default_factory=dict)


# --- helpers ----------------------------------------------------------------

def _has_control(text: str) -> bool:
    """True if text contains U+0000-U+001F, U+007F-U+009F."""
    for ch in text:
        cp = ord(ch)
        if cp <= 0x1F or 0x7F <= cp <= 0x9F:
            return True
    return False


def _decode_b64(s: str) -> Optional[bytes]:
    """Standard base64, padding optional; strict (no foreign characters)."""
    if len(s) % 4 == 1:
        return None
    pad = (-len(s)) % 4
    try:
        return base64.b64decode(s + "=" * pad, validate=True)
    except (binascii.Error, ValueError):
        return None


def _decode_text(s: str, max_encoded: int, max_decoded: int) -> Optional[str]:
    """base64 -> UTF-8 text with the spec's limits/control-character rules.

    Returns None if the report must be discarded (over limit, bad base64,
    bad UTF-8, or decoded text contains control characters).
    """
    if len(s) > max_encoded:
        return None
    raw = _decode_b64(s)
    if raw is None or len(raw) > max_decoded:
        return None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None
    if _has_control(text):
        return None
    return text


def _valid_id(v: str) -> bool:
    if not 1 <= len(v) <= MAX_ID_TOTAL:  # charset is ASCII, so len == bytes
        return False
    segments = v.split("/")
    if len(segments) > MAX_ID_DEPTH:
        return False
    return all(ID_SEGMENT_RE.fullmatch(s) for s in segments)


# --- query reply (rev 0.4) ----------------------------------------------------

def parse_query_reply(body: bytes | str) -> Optional[dict]:
    """Parse the body of a query reply: `?` + optional `:key=value` pairs.

    The body must start with `?`, else None. `states` / `kinds` become
    tuples of comma-separated names (empty items ignored); unknown pairs
    are ignored, as the spec requires. A missing list means the fixed
    defaults (DEFAULT_STATES without clear / DEFAULT_KINDS), so a bare `?`
    and a reply without the pairs parse the same.
    """
    if isinstance(body, bytes):
        body = body.decode("ascii", "replace")
    if not body.startswith("?"):
        return None
    info: dict = {}
    for segment in body[1:].split(":"):
        if "=" not in segment:
            continue  # malformed pair: no '=' → ignore
        key, val = segment.split("=", 1)
        key = key.strip(" \t")
        val = val.strip(" \t")
        if key in ("states", "kinds"):  # unknown pairs: ignored
            info[key] = tuple(
                item for item in (i.strip(" \t") for i in val.split(",")) if item
            )
    if "states" not in info:
        info["states"] = DEFAULT_STATES
    if "kinds" not in info:
        info["kinds"] = DEFAULT_KINDS
    return info


def make_query_reply(
    states: Optional[tuple] = None,
    kinds: Optional[tuple] = None,
    terminator: bytes | str = b"\x1b\\",
) -> bytes:
    """Build a terminal's reply to `OSC 7501 ; ?` (receiver side).

    Lists are omitted when None (a bare `?` reply means the fixed
    defaults). `clear` is never listed: the states pair counts it out.
    The spec does not require reusing the request's terminator — Ghostty
    does; pass ``terminator=b"\x07"`` for a BEL reply.
    """
    body = "?"
    if states:
        listed = [s for s in states if s != "clear"]
        if listed:
            body += ":states=" + ",".join(listed)
    if kinds:
        body += ":kinds=" + ",".join(kinds)
    if isinstance(terminator, str):
        terminator = terminator.encode("ascii")
    return b"\x1b]7501;" + body.encode("ascii") + terminator


def choose_state(wanted: str, fallback: str, reply_info: Optional[dict]) -> str:
    """Pick the state to report, given a parsed query reply (program side).

    Rev 0.4: a program that wants a state from a later revision checks the
    reply's states list and falls back to one that is present. Without
    reply info there is nothing to check: the wanted state is returned.
    """
    if not reply_info:
        return wanted
    if wanted in (reply_info.get("states") or ()):
        return wanted
    return fallback


# --- parser ------------------------------------------------------------------

class Osc7501Parser:
    """Incremental OSC 7501 parser.

    States:
      scan     looking for ESC
      esc      saw ESC, deciding what follows
      osc      inside an OSC string (after ESC ]), collecting body
      osc_esc  saw ESC inside an OSC; next byte decides ST vs abort
    """

    def __init__(self) -> None:
        self._state = "scan"
        self._prefix_pos = 0        # bytes matched against b"7501;" so far
        self._mismatched = False    # OSC number is not 7501
        self._is_7501 = False       # full "7501;" prefix matched
        self._body = bytearray()
        self._body_len = 0          # actual body byte count (never truncated)

    # -- public API

    def feed(self, data: bytes) -> list[Event]:
        events: list[Event] = []
        for b in data:
            ev = self._feed_byte(b)
            if ev is not None:
                events.append(ev)
        return events

    # -- state machine

    def _feed_byte(self, b: int) -> Optional[Event]:
        if self._state == "scan":
            if b == ESC:
                self._state = "esc"
            return None

        if self._state == "esc":
            if b == 0x5D:  # ']'
                self._state = "osc"
                self._prefix_pos = 0
                self._mismatched = False
                self._is_7501 = False
                self._body = bytearray()
                self._body_len = 0
            elif b == ESC:
                pass  # stay: this ESC may open another sequence
            else:
                self._state = "scan"
            return None

        if self._state == "osc_esc":
            if b == 0x5C:  # '\' — ST terminates the OSC
                self._state = "scan"
                return self._finish(2)
            # ESC <other> aborts the string; the ESC starts a new sequence
            # and the current byte belongs to it.
            self._reset_osc()
            if b == 0x5D:  # ']'
                self._state = "osc"
                self._prefix_pos = 0
                self._mismatched = False
                self._is_7501 = False
                self._body = bytearray()
                self._body_len = 0
            elif b == ESC:
                self._state = "esc"
            else:
                self._state = "scan"
            return None

        # state == "osc"
        if b == BEL:
            self._state = "scan"
            return self._finish(1)
        if b == ESC:
            self._state = "osc_esc"
            return None
        if self._is_7501:
            self._body_len += 1
            if len(self._body) < _BODY_STORE_CAP:
                self._body.append(b)
        elif not self._mismatched:
            if b == OSC_PREFIX[self._prefix_pos]:
                self._prefix_pos += 1
                if self._prefix_pos == len(OSC_PREFIX):
                    self._is_7501 = True
            else:
                self._mismatched = True
        return None

    def _reset_osc(self) -> None:
        self._prefix_pos = 0
        self._mismatched = False
        self._is_7501 = False
        self._body = bytearray()
        self._body_len = 0

    def _finish(self, term_len: int) -> Optional[Event]:
        """OSC terminated; decide whether it yields an event."""
        was_7501, body, body_len = self._is_7501, bytes(self._body), self._body_len
        self._reset_osc()
        if not was_7501:
            return None
        # Whole-sequence limit: ESC ] + "7501;" + body + terminator.
        if 2 + len(OSC_PREFIX) + body_len + term_len > MAX_SEQUENCE_BYTES:
            return None
        stripped = body.strip(b" \t")
        if stripped.startswith(b"?"):
            info = parse_query_reply(stripped)
            return Query(states=info["states"], kinds=info["kinds"])
        return self._parse_report(body)

    # -- report parsing

    @staticmethod
    def _parse_report(body: bytes) -> Optional[Report]:
        pairs: dict[str, str] = {}
        for segment in body.split(b":"):
            if b"=" not in segment:
                continue  # malformed pair: no '=' → skip
            key_b, val_b = segment.split(b"=", 1)
            key = key_b.strip(b" \t").decode("ascii", "replace")
            val = val_b.strip(b" \t").decode("ascii", "replace")
            if not KEY_RE.fullmatch(key):
                continue  # empty key / not [a-z]+ → skip pair
            if len(key) > MAX_KEY_BYTES:
                return None  # key over the 16-byte limit → whole report dropped
            if not VALUE_RE.fullmatch(val):
                continue  # value has bytes outside the value charset → skip pair
            pairs[key] = val  # duplicate key: later value wins

        state = pairs.get("state")
        if state not in STATES:
            return None  # state missing or unknown → whole report ignored

        rid = pairs.get("id")
        if rid is not None and not _valid_id(rid):
            return None  # id not syntactically valid → whole report ignored

        kind = pairs.get("kind")
        if state != "blocked" or kind not in KINDS:
            kind = None  # only meaningful (and validated) on blocked

        progress = None
        p = pairs.get("progress")
        if (
            state in ("working", "blocked")
            and p is not None
            and DIGITS_RE.fullmatch(p)
        ):
            iv = int(p)
            if 0 <= iv <= 100:
                progress = iv

        app = pairs.get("app")
        if app is not None and not APP_RE.fullmatch(app):
            app = None  # charset/length violation → treated as absent
        # rev 0.4: app is an identifier for grouping/filtering/icons, not a
        # label to show the user — title is the label.

        msg = None
        enc = pairs.get("msg")
        if enc is not None:
            msg = _decode_text(enc, MAX_MSG_ENCODED, MAX_MSG_DECODED)
            if msg is None:
                return None  # bad/oversized/controlled msg → whole report dropped

        title = None
        enc = pairs.get("title")
        if enc is not None:
            title = _decode_text(enc, MAX_TITLE_ENCODED, MAX_TITLE_DECODED)
            if title is None:
                return None

        return Report(
            state=state,
            id=rid,
            kind=kind,
            progress=progress,
            app=app,
            title=title,
            msg=msg,
            raw_pairs=pairs,
        )


# --- terminal-side record semantics ------------------------------------------

class RecordStore:
    """Record bookkeeping for one terminal, per the spec's lifecycle rules."""

    MAX_RECORDS = MAX_RECORDS

    def __init__(self) -> None:
        self._records: dict[str, dict] = {}  # "" is the root record
        self._clock = 0

    # -- mutations

    def apply(self, report: Report) -> None:
        self._clock += 1
        if report.state == "clear":
            if report.id is None:
                self._records.clear()  # no id: clear every record
            else:
                self._remove_subtree(report.id)
            return
        rid = report.id if report.id is not None else ""
        # Each report fully replaces the record for its id.
        self._records[rid] = {
            "state": report.state,
            "kind": report.kind,
            "progress": report.progress,
            "app": report.app,
            "title": report.title,
            "msg": report.msg,
            "updated": self._clock,
        }
        self._evict()

    def on_process_exit(self) -> None:
        """working/blocked records must be discarded when a process exits."""
        self._drop_transient()

    def on_prompt(self) -> None:
        """Same cleanup at a new shell prompt (OSC 133 A)."""
        self._drop_transient()

    def on_ris(self) -> None:
        """RIS (full reset) clears everything; DECSTR does not."""
        self._records.clear()

    # -- queries

    def get(self, id: Optional[str] = None) -> Optional[dict]:
        return self._records.get(id if id else "")

    def ids(self) -> list[str]:
        return sorted(self._records)

    def __len__(self) -> int:
        return len(self._records)

    def effective_app(self, id: Optional[str]) -> Optional[str]:
        """app of the record, else of its nearest ancestor that sets one."""
        rid = id if id else ""
        parts = rid.split("/") if rid else []
        for i in range(len(parts), -1, -1):
            rec = self._records.get("/".join(parts[:i]))
            if rec is not None and rec.get("app"):
                return rec["app"]
        return None

    # -- internals

    def _remove_subtree(self, rid: str) -> None:
        prefix = rid + "/"
        for key in [k for k in self._records if k == rid or k.startswith(prefix)]:
            del self._records[key]

    def _drop_transient(self) -> None:
        for key in [
            k for k, v in self._records.items() if v["state"] in TRANSIENT_STATES
        ]:
            del self._records[key]

    def _evict(self) -> None:
        # Over MAX_RECORDS: evict least-recently-updated first.
        while len(self._records) > self.MAX_RECORDS:
            oldest = min(self._records, key=lambda k: self._records[k]["updated"])
            del self._records[oldest]


# --- CLI ----------------------------------------------------------------------

def event_to_json(ev: Event) -> dict:
    if isinstance(ev, Query):
        return {
            "type": "query",
            "states": list(ev.states),
            "kinds": list(ev.kinds),
        }
    return {
        "type": "report",
        "state": ev.state,
        "id": ev.id,
        "kind": ev.kind,
        "progress": ev.progress,
        "app": ev.app,
        "title": ev.title,
        "msg": ev.msg,
        "raw_pairs": ev.raw_pairs,
    }


def main(argv: list[str]) -> int:
    if len(argv) > 2:
        print(f"usage: {argv[0]} [file]", file=sys.stderr)
        return 2
    parser = Osc7501Parser()
    if len(argv) == 2:
        with open(argv[1], "rb") as fh:
            while True:
                chunk = fh.read(4096)
                if not chunk:
                    break
                for ev in parser.feed(chunk):
                    print(json.dumps(event_to_json(ev), ensure_ascii=False))
    else:
        while True:
            chunk = sys.stdin.buffer.read(4096)
            if not chunk:
                break
            for ev in parser.feed(chunk):
                print(json.dumps(event_to_json(ev), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
