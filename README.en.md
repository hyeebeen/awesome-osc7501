# Awesome OSC 7501

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of resources for [OSC 7501, the "Program Status Protocol"](https://www.superlogical.com/rex/docs/build/program-status): protocol deep dive, reference implementation, ecosystem adoption, practice guides, and a timeline.

[简体中文](README.md) · English (this file)

**Verification date: 2026-10-09 (Asia/Shanghai, CST).** Every entry traces back to a
primary source (spec, source code, PR, release, or a first-party post). Version
numbers and release dates live only in [docs/support-matrix.md](docs/support-matrix.md)
and [docs/timeline.md](docs/timeline.md); everywhere else we state a status category only. Anything
unverified is marked "unconfirmed".

## Part 1 · Core: the protocol

Details in [docs/deep-dive.md](docs/deep-dive.md) (Chinese).

- **The problem.** Terminals cannot tell what a long-running program (especially an
  AI coding agent) is doing. The author's [launch post](https://x.com/mitchellh/status/2107577887159386152)
  cites 250+ orchestrators each guessing Claude Code's state via
  heuristics, and Herdr making ~10 compatibility changes in 3 months. Proprietary
  out-of-band APIs have an O(N) integration problem and need extra bridging across
  SSH and containers ([blog post](https://mitchellh.com/writing/program-status-osc7501)).
- **What it is.** An OSC escape sequence programs write into the PTY stream to
  report structured status; the terminal decides how to present it.
- **Design principles.** Terminal-native (works over SSH/containers for free),
  presentation-agnostic, no heartbeat, unknown keys ignored (= extension
  mechanism), implementable in one line of POSIX sh, detection optional.
- **30-second version.**

  ```sh
  printf '\033]7501;state=working:app=demo\033\\'
  ```

  `ESC ]` starts an OSC; `7501` is the number; `state=working:app=demo` are
  `key=value` pairs joined by `:`; terminated by ST (`ESC \`) or BEL.
- **State model.** `idle`, `working`, `blocked`, `done`, `error`, plus `clear`
  (deletes a record subtree). Working/blocked records must be dropped on process
  exit or a new shell prompt (OSC 133 A); done/error persist; no keep-alive.
- **Record model.** Each report fully replaces the record for its hierarchical
  `id`; children inherit `app` from the nearest ancestor; RIS clears everything;
  DECSTR does not; alternate-screen switches are unaffected.
- **Detection & fallback.** Send `OSC 7501 ; ?` followed by DA1 (`CSI c`): a DA1
  reply arriving first means unsupported. The terminfo capability `Pst` is a
  SHOULD and is never authoritative. Terminals that never heard of 7501 simply
  ignore the unknown OSC, so blind sending degrades safely. tmux drops unknown
  OSC; a DCS passthrough with `allow-passthrough on` works (verified on tmux 3.5a,
  see [examples/RUNLOG.md](examples/RUNLOG.md)).
- **Security.** Control characters in decoded `msg`/`title` must be rejected; the
  only bytes a terminal may ever write back is the fixed query reply; show which
  session a status came from; rate-limit notifications. Reports are capped at
  4096 bytes.
- **Open questions** in the spec (per-pane multiplexer behavior, records after SSH
  disconnect, Ctrl+Z semantics, id collisions on a shared pty, DA1 race
  requirements for middle layers): see deep-dive §5.

## Part 2 · Focus: ecosystem and practice

Curated highlights (full lists with statuses in the
[support matrix](docs/support-matrix.md)):

- **Spec & origin** — [the spec](https://www.superlogical.com/rex/docs/build/program-status),
  the [original gist](https://gist.github.com/mitchellh/7acae3abd8355c1c00287d67e96c913a),
  the author's [blog post](https://mitchellh.com/writing/program-status-osc7501)
  and [announcement](https://x.com/mitchellh/status/2107577887159386152).
- **Reference implementation** — [libghostty-vt PR #14560](https://github.com/ghostty-org/ghostty/pull/14560)
  by the author (merged, unreleased); parser, query-reply logic and a C API.
- **Receivers (terminals / multiplexers / agent workbenches)** —
  [Rex](https://www.superlogical.com/rex/docs/build/program-status) (implemented
  per its official docs; version unconfirmed),
  [cmux](https://github.com/manaflow-ai/cmux/pull/18742) (merged, unreleased),
  [termio](https://github.com/termio-sh/termio/pull/713) (released),
  [SwiftTerm](https://github.com/migueldeicaza/SwiftTerm/pull/746) (released),
  TUIOS, Termy, con-terminal, phux, thurm, wietty (released); Tern — Stencil's
  closed-source Rust-native neoterminal, announced only by its developer; tmux and
  the major terminals (Kitty, WezTerm, Alacritty, Windows Terminal, zellij, iTerm2)
  do not support it yet; foot unconfirmed.
- **Senders (AI agents / coding CLIs)** —
  [Claude Code](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
  (released), [pi](https://github.com/earendil-works/pi) (released),
  [Docker Agent](https://github.com/docker/docker-agent/pull/4544) (released),
  [Crush](https://github.com/charmbracelet/crush/pull/4041) (released),
  [Factory Droid](https://docs.factory.com/changelog/release-notes) (released
  (inferred)), plus many more merged or in progress; Amp, Codex CLI and opencode
  announced only (per the author); Tern — a terminal, see receivers — announced
  only by its developer.
- **Non-AI CLIs** — tuist (merged, unreleased), git-stack (released), Hugo,
  Composer, Expo, bunny.net (in development), firebase-tools (closed, redo planned).
- **TUI libraries / SDKs** — [Bubble Tea](https://github.com/charmbracelet/bubbletea)
  (released), charmbracelet/x, ultraviolet, libvaxis, tuika (released),
  libghostty-rs, xterm.dart.
- **Why integrate** — stop screen-scraping for state; surface "this agent needs
  you" when the user has switched away; manage many sessions from a sidebar or a
  unified inbox, even from a phone; cross-SSH/containers with zero out-of-band
  plumbing; library-level network effects. Full analysis with sources in
  [docs/why-integrate.md](docs/why-integrate.md) (Chinese).
- **Opposition & wait-and-see** — tmux's maintainer calls it
  ["premature"](https://github.com/tmux/tmux/issues/5713); firebase-tools closed
  two implementations pending a redo; pre-existing sequences (iTerm2 OSC 21337,
  Orca OSC 9999) compete in the same space.

### Overview

79 tracked entries: 18 released (incl. Factory Droid, inferred), 1 implemented per
official docs (Rex), 24 merged-but-unreleased, 12 in development, 5 announced,
1 closed, 16 unsupported, 2 unconfirmed — breakdown and sources in the
[support matrix](docs/support-matrix.md).

### Examples

Runnable sender and receiver examples (POSIX sh helpers, byte-level demo, command
wrapper, feature detection, a fully validating Python incremental parser with 39
tests, and a tmux passthrough experiment) live in [examples/](examples/); real
recorded output in [examples/RUNLOG.md](examples/RUNLOG.md). The how-to guide is
[docs/practice.md](docs/practice.md) (Chinese).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Primary sources only; every status claim
needs a link and a verification date; versions go into the matrix/timeline only.

## License

[CC0-1.0](LICENSE).
