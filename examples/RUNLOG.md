# 示例运行记录（RUNLOG）

以下输出均为在 box 上真实运行所得，原样保留（不可见控制字节已转义：`^[` = ESC，`^G` = BEL）。

- 运行时间：2026-10-09 23:53–23:55 CST
- 运行环境：Linux 6.12.94+ x86_64 / Debian GNU/Linux 13 (trixie) / Python 3.13.5 / tmux 3.5a / GNU coreutils od 9.7 / `/bin/sh` = dash
- 未覆盖：box 上没有实现 OSC 7501 的真实终端，`detect.sh` 只验证了「无 tty」和「无回复」两条路径；`supported` 与 `DA1 first` 路径需要在真实终端（如 cmux、Rex 或接了 libghostty-vt 的宿主）里复核。

## 1. 单元测试、字节演示、tmux 透传实验

```text
### env
Linux 6.12.94+ x86_64
Debian GNU/Linux 13 (trixie)
Python 3.13.5
tmux 3.5a
od (GNU coreutils) 9.7
2026-10-09 23:53 CST
### unittest
----------------------------------------------------------------------
Ran 39 tests in 0.101s

OK
### bytes-demo
osc7501.sh byte demo — canonical OSC 7501 sequences

=== (a) spec's Terraform example (ST = ESC \) ===
msg base64 OK: QXBwbHkgMyB0byBhZGQsIDEgdG8gY2hhbmdlLCAwIHRvIGRlc3Ryb3k/
sequence matches the spec's Terraform example.
  1b  5d  37  35  30  31  3b  73  74  61  74  65  3d  62  6c  6f
 033   ]   7   5   0   1   ;   s   t   a   t   e   =   b   l   o
  63  6b  65  64  3a  6b  69  6e  64  3d  70  65  72  6d  69  73
   c   k   e   d   :   k   i   n   d   =   p   e   r   m   i   s
  73  69  6f  6e  3a  61  70  70  3d  74  65  72  72  61  66  6f
   s   i   o   n   :   a   p   p   =   t   e   r   r   a   f   o
  72  6d  3a  6d  73  67  3d  51  58  42  77  62  48  6b  67  4d
   r   m   :   m   s   g   =   Q   X   B   w   b   H   k   g   M
  79  42  30  62  79  42  68  5a  47  51  73  49  44  45  67  64
   y   B   0   b   y   B   h   Z   G   Q   s   I   D   E   g   d
  47  38  67  59  32  68  68  62  6d  64  6c  4c  43  41  77  49
   G   8   g   Y   2   h   h   b   m   d   l   L   C   A   w   I
  48  52  76  49  47  52  6c  63  33  52  79  62  33  6b  2f  1b
   H   R   v   I   G   R   l   c   3   R   y   b   3   k   / 033
  5c
   \

=== (b) feature detection query, ST-terminated ===
  1b  5d  37  35  30  31  3b  3f  1b  5c
 033   ]   7   5   0   1   ;   ? 033   \

=== (c) feature detection query, BEL-terminated ===
  1b  5d  37  35  30  31  3b  3f  07
 033   ]   7   5   0   1   ;   ?  \a

=== byte -> meaning cheat sheet ===
1b          ESC    starts every escape sequence
1b 5d       ESC ]  OSC (Operating System Command) introducer
37 35 30 31 '7501' the OSC number (ASCII "7501")
3b          ';'    separates the OSC number from the key=value pairs
3f          '?'    feature-detection query (instead of pairs)
1b 5c       ESC \  ST — string terminator (ends the OSC)
07          BEL    alternate string terminator

all assertions passed.
exit=0
### tmux-passthrough
allow-passthrough=off  bare        -> absent  (as expected)
allow-passthrough=off  DCS-wrapped -> absent  (as expected)
allow-passthrough=on   bare        -> absent  (as expected)
allow-passthrough=on   DCS-wrapped -> present  (as expected)

all 4 cases behaved as expected.
exit=0
```

## 2. wrap.sh、解析器 CLI、detect.sh

```text
### wrap.sh (success) -> parser
wrap exit=0
{"type": "report", "state": "working", "id": null, "kind": null, "progress": null, "app": "demo", "title": null, "msg": "Running: sh -c sleep 1", "raw_pairs": {"state": "working", "app": "demo", "msg": "UnVubmluZzogc2ggLWMgc2xlZXAgMQ=="}}
{"type": "report", "state": "done", "id": null, "kind": null, "progress": null, "app": "demo", "title": null, "msg": "Done: sh -c sleep 1 (1.0s)", "raw_pairs": {"state": "done", "app": "demo", "msg": "RG9uZTogc2ggLWMgc2xlZXAgMSAoMS4wcyk="}}
### wrap.sh (failure, exit 3) -> parser
wrap exit=3
{"type": "report", "state": "working", "id": null, "kind": null, "progress": null, "app": "demo", "title": null, "msg": "Running: sh -c exit 3", "raw_pairs": {"state": "working", "app": "demo", "msg": "UnVubmluZzogc2ggLWMgZXhpdCAz"}}
{"type": "report", "state": "error", "id": null, "kind": null, "progress": null, "app": "demo", "title": null, "msg": "Failed: sh -c exit 3 (exit 3)", "raw_pairs": {"state": "error", "app": "demo", "msg": "RmFpbGVkOiBzaCAtYyBleGl0IDMgKGV4aXQgMyk="}}
### parser on mixed stream (BEL + ST + noise + other OSC + query + hierarchical ids)
{"type": "report", "state": "working", "id": null, "kind": null, "progress": null, "app": "deploy", "title": null, "msg": "Deploying v2.4.1", "raw_pairs": {"state": "working", "app": "deploy", "msg": "RGVwbG95aW5nIHYyLjQuMQ=="}}
{"type": "report", "state": "blocked", "id": "eu-west", "kind": "permission", "progress": null, "app": null, "title": "EU West", "msg": "Approve?", "raw_pairs": {"state": "blocked", "kind": "permission", "id": "eu-west", "title": "RVUgV2VzdA==", "msg": "QXBwcm92ZT8="}}
{"type": "query"}
### detect.sh without tty
no tty
exit=2
### detect.sh inside script(1) pty (no terminal emulator answers)
^[]7501;?^[\^[[cunsupported (no reply)
terminfo: Pst absent (NOT authoritative — see comment in detect.sh)
```
