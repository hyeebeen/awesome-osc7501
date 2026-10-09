#!/usr/bin/env python3
"""Unit tests for examples/osc7501_parser.py (OSC 7501 parsing + records).

Run: python3 -m unittest discover -s examples -v
"""

import base64
import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from osc7501_parser import (  # noqa: E402
    Osc7501Parser,
    Query,
    RecordStore,
    Report,
)

ESC = b"\x1b"
BEL = b"\x07"
ST = ESC + b"\\"

TERRAFORM_MSG = "Apply 3 to add, 1 to change, 0 to destroy?"
TERRAFORM_B64 = "QXBwbHkgMyB0byBhZGQsIDEgdG8gY2hhbmdlLCAwIHRvIGRlc3Ryb3k/"


def b64(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def parse(data: bytes):
    return Osc7501Parser().feed(data)


def report(state, **kw):
    return Report(state=state, **kw)


class TestOsc7501Parser(unittest.TestCase):
    # --- happy paths -----------------------------------------------------

    def test_terraform_spec_example(self):
        seq = (
            ESC + b"]7501;state=blocked:kind=permission:app=terraform:msg="
            + TERRAFORM_B64.encode() + ST
        )
        events = parse(seq)
        self.assertEqual(len(events), 1)
        ev = events[0]
        self.assertIsInstance(ev, Report)
        self.assertEqual(ev.state, "blocked")
        self.assertEqual(ev.kind, "permission")
        self.assertEqual(ev.app, "terraform")
        self.assertEqual(ev.msg, TERRAFORM_MSG)
        self.assertIsNone(ev.id)
        self.assertIsNone(ev.progress)
        self.assertIsNone(ev.title)

    def test_bel_terminator(self):
        seq = ESC + b"]7501;state=done:msg=" + b64("ok").encode() + BEL
        events = parse(seq)
        self.assertEqual([e.state for e in events], ["done"])
        self.assertEqual(events[0].msg, "ok")

    def test_esc_backslash_terminator(self):
        seq = ESC + b"]7501;state=done:msg=" + b64("ok").encode() + ST
        events = parse(seq)
        self.assertEqual([e.state for e in events], ["done"])

    def test_byte_by_byte_feed(self):
        seq = (
            b"noise" + ESC + b"]7501;state=working:progress=42:msg="
            + b64("busy").encode() + ST + b"trailing"
        )
        parser = Osc7501Parser()
        events = []
        for i in range(len(seq)):
            events.extend(parser.feed(seq[i : i + 1]))
        self.assertEqual(len(events), 1)
        ev = events[0]
        self.assertEqual(ev.state, "working")
        self.assertEqual(ev.progress, 42)
        self.assertEqual(ev.msg, "busy")

    def test_mixed_with_plain_output_and_other_sequences(self):
        seq = (
            b"ls -l\r\ntotal 0\n"
            + ESC + b"]0;window title" + BEL
            + ESC + b"[0mplain\x1b[?1;2c"
            + ESC + b"]7501;state=done" + ST
            + b"\x1b[2Kdone\n"
        )
        events = parse(seq)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].state, "done")

    def test_multiple_sequences_one_feed(self):
        seq = (
            ESC + b"]7501;state=working" + ST
            + ESC + b"]7501;state=done" + BEL
        )
        self.assertEqual([e.state for e in parse(seq)], ["working", "done"])

    def test_non_7501_osc_skipped(self):
        seq = ESC + b"]75001;state=working" + ST  # wrong number
        self.assertEqual(parse(seq), [])
        seq = ESC + b"]0;title" + BEL + ESC + b"]7501;?" + ST
        events = parse(seq)
        self.assertEqual(len(events), 1)
        self.assertIsInstance(events[0], Query)

    def test_bare_esc_aborts_osc_then_new_sequence_parses(self):
        # ESC ] 7501 ; state=working, then a bare ESC (aborts), then a
        # fresh OSC 7501 query.
        seq = ESC + b"]7501;state=working" + ESC + b"X" + ESC + b"]7501;?" + ST
        events = parse(seq)
        self.assertEqual(len(events), 1)
        self.assertIsInstance(events[0], Query)

    # --- queries -----------------------------------------------------------

    def test_query_st(self):
        events = parse(ESC + b"]7501;?" + ST)
        self.assertEqual([type(e) for e in events], [Query])

    def test_query_bel(self):
        events = parse(ESC + b"]7501;?" + BEL)
        self.assertEqual([type(e) for e in events], [Query])

    def test_query_with_future_pairs_ignored(self):
        # Replies may append pairs after '?' in future revisions; the spec
        # says programs must ignore what they don't recognize.
        events = parse(ESC + b"]7501;?:state=idle:future=1" + ST)
        self.assertEqual([type(e) for e in events], [Query])

    # --- pair-level rules ----------------------------------------------------

    def test_malformed_pair_no_equals_skipped(self):
        ev = parse(ESC + b"]7501;state=working:junk:progress=7" + ST)[0]
        self.assertEqual(ev.state, "working")
        self.assertEqual(ev.progress, 7)

    def test_malformed_pair_empty_key_skipped(self):
        ev = parse(ESC + b"]7501;=zz:state=done" + ST)[0]
        self.assertEqual(ev.state, "done")
        self.assertNotIn("", ev.raw_pairs)

    def test_malformed_pair_bad_key_charset_skipped(self):
        ev = parse(ESC + b"]7501;State=done:x9=y:state=done" + ST)[0]
        self.assertEqual(ev.state, "done")

    def test_malformed_pair_value_charset_skipped(self):
        # '!' is outside the value charset → the pair is skipped (not fatal)
        ev = parse(ESC + b"]7501;state=working:msg=x!y:progress=3" + ST)[0]
        self.assertIsNone(ev.msg)
        self.assertEqual(ev.progress, 3)

    def test_unknown_key_ignored_but_report_kept(self):
        ev = parse(ESC + b"]7501;state=done:frobnicate=1.2_3" + ST)[0]
        self.assertEqual(ev.state, "done")
        self.assertEqual(ev.raw_pairs.get("frobnicate"), "1.2_3")

    def test_duplicate_key_later_wins(self):
        ev = parse(
            ESC + b"]7501;app=first:state=working:app=second" + ST
        )[0]
        self.assertEqual(ev.app, "second")
        ev = parse(ESC + b"]7501;state=done:state=error" + ST)[0]
        self.assertEqual(ev.state, "error")

    def test_whitespace_stripped_around_key_and_value(self):
        ev = parse(ESC + b"]7501; state = done : app = my.app " + ST)[0]
        self.assertEqual(ev.state, "done")
        self.assertEqual(ev.app, "my.app")

    # --- whole-report drops ---------------------------------------------------

    def test_missing_or_unknown_state_ignored(self):
        self.assertEqual(parse(ESC + b"]7501;progress=50" + ST), [])
        self.assertEqual(parse(ESC + b"]7501;state=happynet" + ST), [])
        self.assertEqual(parse(ESC + b"]7501;state=" + ST), [])
        self.assertEqual(parse(ESC + b"]7501;" + ST), [])

    def test_bad_id_whole_report_ignored(self):
        bad_ids = [
            "a,b",            # ',' is legal in values, illegal in ids
            "a//b",           # empty segment
            "a/" + "b" * 33,  # over-long segment
            "/".join(["s"] * 9),  # 9 levels deep
            "/".join(["x" * 32] * 4),  # total 131 bytes > 128
        ]
        for bid in bad_ids:
            self.assertEqual(
                parse(ESC + b"]7501;state=done:id=" + bid.encode() + ST),
                [],
                msg=f"id={bid!r} should invalidate the report",
            )

    def test_good_id_max_shape_accepted(self):
        rid = "/".join(["seg"] * 8)  # 8 levels, 31 bytes total
        ev = parse(ESC + b"]7501;state=done:id=" + rid.encode() + ST)[0]
        self.assertEqual(ev.id, rid)

    def test_bad_base64_msg_whole_report_dropped(self):
        self.assertEqual(parse(ESC + b"]7501;state=working:msg=a_b" + ST), [])
        self.assertEqual(parse(ESC + b"]7501;state=working:msg=abc" + ST), [])

    def test_msg_control_chars_whole_report_dropped(self):
        for text in ("a\x01b", "a\x7fb", "a\x85b", "a\x9fb"):
            seq = ESC + b"]7501;state=done:msg=" + b64(text).encode() + ST
            self.assertEqual(parse(seq), [], msg=repr(text))

    def test_msg_length_limits(self):
        # encoded 2732 / decoded 2047: accepted
        ok = "a" * 2047
        seq = ESC + b"]7501;state=done:msg=" + b64(ok).encode() + ST
        self.assertEqual(len(b64(ok)), 2732)
        self.assertEqual(parse(seq)[0].msg, ok)
        # decoded 2049 (encoded exactly 2732): over decoded limit → dropped
        seq = ESC + b"]7501;state=done:msg=" + b64("a" * 2049).encode() + ST
        self.assertEqual(parse(seq), [])
        # encoded 2736 (> 2732): over encoded limit → dropped
        seq = ESC + b"]7501;state=done:msg=" + b64("a" * 2050).encode() + ST
        self.assertEqual(parse(seq), [])

    def test_title_length_limits(self):
        seq = ESC + b"]7501;state=done:title=" + b64("t" * 192).encode() + ST
        self.assertEqual(len(b64("t" * 192)), 256)
        self.assertEqual(parse(seq)[0].title, "t" * 192)
        seq = ESC + b"]7501;state=done:title=" + b64("t" * 193).encode() + ST
        self.assertEqual(parse(seq), [])

    def test_key_over_16_bytes_drops_report(self):
        self.assertEqual(parse(ESC + b"]7501;state=done" + ST)[0].state, "done")
        self.assertEqual(
            parse(ESC + b"]7501;" + b"a" * 17 + b"=1:state=done" + ST), []
        )
        ev = parse(ESC + b"]7501;" + b"a" * 16 + b"=1:state=done" + ST)[0]
        self.assertEqual(ev.state, "done")

    def test_sequence_over_4096_bytes_dropped(self):
        # exactly 4096: ESC ] (2) + "7501;" (5) + body + ST (2) → body 4087
        body = b"state=working:pad=" + b"a" * 4069   # 18 + 4069 = 4087
        self.assertEqual(2 + 5 + len(body) + 2, 4096)
        ev = parse(ESC + b"]7501;" + body + ST)[0]
        self.assertEqual(ev.state, "working")
        # 4097: dropped
        body = b"state=working:pad=" + b"a" * 4070
        self.assertEqual(2 + 5 + len(body) + 2, 4097)
        self.assertEqual(parse(ESC + b"]7501;" + body + ST), [])
        # BEL is one byte shorter than ST, so push the body one byte further
        # to exceed the limit with a BEL terminator too (total 4097).
        body = b"state=working:pad=" + b"a" * 4071
        self.assertEqual(2 + 5 + len(body) + 1, 4097)
        self.assertEqual(parse(ESC + b"]7501;" + body + BEL), [])

    # --- per-key defaults -------------------------------------------------------

    def test_kind_rules(self):
        ev = parse(ESC + b"]7501;state=blocked:kind=auth" + ST)[0]
        self.assertEqual(ev.kind, "auth")
        # invalid kind value → treated as absent
        ev = parse(ESC + b"]7501;state=blocked:kind=bogus" + ST)[0]
        self.assertIsNone(ev.kind)
        # kind only meaningful on blocked
        for state in ("working", "done", "error", "idle", "clear"):
            ev = parse(
                ESC + b"]7501;state=" + state.encode() + b":kind=permission" + ST
            )[0]
            self.assertIsNone(ev.kind, msg=state)

    def test_progress_rules(self):
        for state, val, want in [
            ("working", "50", 50),
            ("working", "0", 0),
            ("working", "100", 100),
            ("blocked", "7", 7),
            ("working", "101", None),   # out of range
            ("working", "-1", None),    # not a plain integer
            ("working", "5.5", None),
            ("working", "abc", None),
            ("working", "", None),
            ("done", "50", None),       # only working/blocked carry progress
            ("error", "50", None),
        ]:
            ev = parse(
                ESC + b"]7501;state=" + state.encode()
                + b":progress=" + val.encode() + ST
            )[0]
            self.assertEqual(ev.progress, want, msg=f"{state} progress={val!r}")

    def test_app_rules(self):
        ev = parse(ESC + b"]7501;state=done:app=my.app-2" + ST)[0]
        self.assertEqual(ev.app, "my.app-2")
        ev = parse(ESC + b"]7501;state=done:app=" + b"a" * 33 + ST)[0]
        self.assertIsNone(ev.app)  # over 32 bytes → absent
        ev = parse(ESC + b"]7501;state=done:app=a,b" + ST)[0]
        self.assertIsNone(ev.app)  # ',' passes the value charset but not app's

    def test_optional_padding_base64(self):
        padded = base64.b64encode(b"hi there").decode("ascii")
        unpadded = padded.rstrip("=")
        for enc in (padded, unpadded):
            ev = parse(
                ESC + b"]7501;state=done:msg=" + enc.encode() + ST
            )[0]
            self.assertEqual(ev.msg, "hi there")

    def test_msg_invalid_utf8_dropped(self):
        enc = base64.b64encode(b"\xff\xfe\xfd").decode("ascii")
        self.assertEqual(parse(ESC + b"]7501;state=done:msg=" + enc.encode() + ST), [])

    # --- RecordStore ------------------------------------------------------------

    def store(self):
        return RecordStore()

    def test_recordstore_full_replacement(self):
        s = self.store()
        s.apply(report("working", app="terraform", msg="applying"))
        rec = s.get()
        self.assertEqual(rec["state"], "working")
        self.assertEqual(rec["app"], "terraform")
        s.apply(report("done"))  # replaces wholesale; absent keys disappear
        rec = s.get()
        self.assertEqual(rec["state"], "done")
        self.assertIsNone(rec["app"])
        self.assertIsNone(rec["msg"])

    def test_recordstore_clear_subtree_only(self):
        s = self.store()
        s.apply(report("done", app="root"))
        s.apply(report("working", id="build"))
        s.apply(report("blocked", id="build/test"))
        s.apply(report("done", id="build/test/unit"))
        s.apply(report("error", id="deploy"))
        s.apply(report("clear", id="build"))
        self.assertEqual(s.ids(), ["", "deploy"])
        # clear without id clears everything
        s.apply(report("clear"))
        self.assertEqual(s.ids(), [])

    def test_recordstore_effective_app_inheritance(self):
        s = self.store()
        s.apply(report("done", app="terraform"))
        s.apply(report("working", id="plan"))
        s.apply(report("blocked", id="plan/apply", app="custom"))
        s.apply(report("working", id="plan/apply/step"))
        self.assertEqual(s.effective_app(None), "terraform")
        self.assertEqual(s.effective_app("plan"), "terraform")
        self.assertEqual(s.effective_app("plan/apply"), "custom")
        self.assertEqual(s.effective_app("plan/apply/step"), "custom")

    def test_recordstore_prompt_and_exit_drop_transient(self):
        s = self.store()
        for state in ("working", "blocked", "done", "error", "idle"):
            s.apply(report(state, id="job-" + state))
        s.on_prompt()
        self.assertEqual(s.ids(), ["job-done", "job-error", "job-idle"])
        s.apply(report("working", id="w2"))
        s.apply(report("blocked", id="b2"))
        s.on_process_exit()
        self.assertEqual(s.ids(), ["job-done", "job-error", "job-idle"])

    def test_recordstore_ris_clears_all(self):
        s = self.store()
        s.apply(report("done", id="a"))
        s.apply(report("error"))
        s.on_ris()
        self.assertEqual(s.ids(), [])

    def test_recordstore_eviction_lru(self):
        s = self.store()
        for i in range(300):
            s.apply(report("done", id="r%d" % i))
        self.assertEqual(len(s), 256)
        self.assertIsNone(s.get("r0"))
        self.assertIsNone(s.get("r43"))
        self.assertIsNotNone(s.get("r44"))
        self.assertIsNotNone(s.get("r299"))
        # updating a record makes it most-recent again
        s.apply(report("done", id="r44"))
        s.apply(report("done", id="r300"))
        self.assertIsNotNone(s.get("r44"))
        self.assertIsNone(s.get("r45"))

    # --- CLI -----------------------------------------------------------------------

    def test_cli_file_and_stdin(self):
        payload = (
            ESC + b"]7501;state=blocked:kind=permission:app=terraform:msg="
            + TERRAFORM_B64.encode() + ST
            + ESC + b"]7501;?" + BEL
        )
        script = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "osc7501_parser.py")
        with tempfile.NamedTemporaryFile(delete=False) as fh:
            fh.write(payload)
            path = fh.name
        try:
            out = subprocess.run(
                [sys.executable, script, path],
                capture_output=True, check=True, text=True,
            ).stdout
        finally:
            os.unlink(path)
        lines = [json.loads(line) for line in out.splitlines()]
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0]["type"], "report")
        self.assertEqual(lines[0]["msg"], TERRAFORM_MSG)
        self.assertEqual(lines[1]["type"], "query")
        # stdin mode agrees
        out2 = subprocess.run(
            [sys.executable, script],
            input=payload, capture_output=True, check=True,
        ).stdout.decode()
        self.assertEqual(
            [json.loads(line) for line in out2.splitlines()], lines
        )


if __name__ == "__main__":
    unittest.main()
