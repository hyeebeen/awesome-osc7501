# RUNLOG — examples 运行记录

- 运行日期：2026-10-09（Asia/Shanghai，CST）
- 环境：Linux 6.12.94+、POSIX sh（`/bin/sh`）、tmux 3.5a、Python 3.13.5、`base64`/`tr`/`sed`/`od`/`script` 来自 coreutils/util-linux
- 说明：以下输出均为真实运行结果的原样摘录（长输出有截断标注），未做美化。
  本机没有实现 OSC 7501 的终端模拟器，因此发送端示例的输出以字节形式
  （`od`）或通过解析器 CLI 验证；检测脚本在无应答环境下按预期返回 unsupported。

## bytes-demo.sh

```sh
$ sh examples/bytes-demo.sh; echo "exit=$?"
osc7501.sh byte demo — canonical OSC 7501 sequences

=== (a) spec's Terraform example (ST = ESC \) ===
msg base64 OK: QXBwbHkgMyB0byBhZGQsIDEgdG8gY2hhbmdlLCAwIHRvIGRlc3Ryb3k/
sequence matches the spec's Terraform example.
  1b  5d  37  35  30  31  3b  73  74  61  74  65  3d  62  6c  6f
 033   ]   7   5   0   1   ;   s   t   a   t   e   =   b   l   o
  63  6b  65  64  3a  6b  69  6e  64  3d  70  65  72  6d  69  73
   c   k   e   d   :   k   i   n   d   =   p   e   r   m   i   s
 ...（中间 6 行省略，见脚本完整输出）...
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
```

## wrap.sh（OSC7501_OUT=- 写 stdout，用 od 查看）

```sh
$ OSC7501_OUT=- sh examples/wrap.sh --app make -- sleep 0.2 | od -An -c
 033   ]   7   5   0   1   ;   s   t   a   t   e   =   w   o   r
   k   i   n   g   :   a   p   p   =   m   a   k   e   :   m   s
   g   =   U   n   V   u   b   m   l   u   Z   z   o   g   c   2
   x   l   Z   X   A     M   C   4   y 033   \ 033   ]   7   5
   0   1   ;   s   t   a   t   e   =   d   o   n   e   :   a   p
   p   =   m   a   k   e   :   m   s   g   =   R   G   9   u   Z
   T   o   g   c   2   x   l   Z   X   A     M   C   4   y   I
   C   g   w   L   j   J   z   K   Q   =   = 033   \
```

两条序列（working → done）各以 `ESC \` 结尾，`msg` 为 base64。失败路径
（`sh examples/wrap.sh -- false`）退出码 1，并发送 `state=error` 报告
（msg 含 `exit 1`，字节形态同上）。

## detect.sh（包在 script 里给它一个 pty）

```sh
$ script -q -c "sh examples/detect.sh -t 1" /dev/null; echo "exit=$?"
]7501;?\[cunsupported (no reply)
terminfo: Pst absent (NOT authoritative — see comment in detect.sh)
exit=0
```

本环境没有会应答 `OSC 7501 ; ?` 或 DA1 的终端在 pty 另一端（`script` 只录
制不回答），因此落在 `unsupported (no reply)` 分支——这正是超时降级路径。

## test_osc7501_parser.py

```sh
$ python3 -m unittest discover -s examples 2>&1 | tail -3
----------------------------------------------------------------------
Ran 39 tests in 0.087s

OK
```

## tmux-passthrough.sh（tmux 3.5a）

```sh
$ sh examples/tmux-passthrough.sh; echo "exit=$?"
allow-passthrough=off  bare        -> absent  (as expected)
allow-passthrough=off  DCS-wrapped -> absent  (as expected)
allow-passthrough=on   bare        -> absent  (as expected)
allow-passthrough=on   DCS-wrapped -> present  (as expected)

all 4 cases behaved as expected.
exit=0
```

结论（tmux 3.5a 实测）：tmux 不识别 OSC 7501，裸序列一律被丢弃；仅当
`set -g allow-passthrough on` 且序列用 DCS passthrough（`ESC P tmux; … ESC \`，
内部 ESC 加倍）包裹时才能透传到外层终端。与 pi 文档「tmux 与 screen 不转发」
的说法一致（tmux 部分，本机实测）。

## osc7501_parser.py（解析 script 录制的 typescript）

```sh
$ script -q -c "sh examples/wrap.sh --app demo -- sleep 0.2; \
    OSC7501_OUT=- sh examples/wrap.sh -- false" /tmp/ts7501.log >/dev/null 2>&1
$ python3 examples/osc7501_parser.py /tmp/ts7501.log
{"type": "report", "state": "working", "id": null, "kind": null, "progress": null, "app": "demo", "title": null, "msg": "Running: sleep 0.2", "raw_pairs": {"state": "working", "app": "demo", "msg": "UnVubmluZzogc2xlZXAgMC4y"}}
{"type": "report", "state": "done", "id": null, "kind": null, "progress": null, "app": "demo", "title": null, "msg": "Done: sleep 0.2 (0.2s)", "raw_pairs": {"state": "done", "app": "demo", "msg": "RG9uZTogc2xlZXAgMC4yICgwLjJzKQ=="}}
{"type": "report", "state": "working", "id": null, "kind": null, "progress": null, "app": null, "title": null, "msg": "Running: false", "raw_pairs": {"state": "working", "msg": "UnVubmluZzogZmFsc2U="}}
{"type": "report", "state": "error", "id": null, "kind": null, "progress": null, "app": null, "title": null, "msg": "Failed: false (exit 1)", "raw_pairs": {"state": "error", "msg": "RmFpbGVkOiBmYWxzZSAoZXhpdCAxKQ=="}}
exit=0
```

解析器从录制的 typescript 中还原出 4 个事件（working → done → working →
error），base64 的 msg 均被正确解码；注意第二条 wrap.sh 未传 `--app`，因此
报告里没有 `app`，接收端记录的 app 字段为空——完整替换语义的直观体现。
