# examples — OSC 7501 (Program Status Protocol) 示例

针对 [OSC 7501 规范](https://www.superlogical.com/rex/docs/build/program-status)
（rev 0.4）的一组发送端与接收端示例：shell 函数库、字节级演示、特性检测、
假终端挂具、带完整校验的 Python 增量解析器及单测、tmux 透传实验。

运行记录见 examples/RUNLOG.md。

## osc7501.sh — POSIX sh 函数库（source 使用）

不是可执行脚本，供其它脚本 `. /path/to/osc7501.sh` 引入：

```sh
. ./osc7501.sh
osc7501_report blocked 'kind=permission' 'app=myapp' 'msg=Allow this?'   # 完整报告
osc7501_status working "compiling…"                                      # 博文同款简化版
osc7501_clear          # 清空所有记录
osc7501_clear build/x  # 只清该 id 子树
```

- `msg=` / `title=` 传明文，库自动做标准 base64（`tr -d '\n'`），ST 用 `ESC \`。
- 输出目标：默认 `/dev/tty`（可写时），否则 stdout；`OSC7501_OUT=文件` 追加写入，
  `OSC7501_OUT=-` 写 stdout。
- tmux 内（`$TMUX` 非空）且 `OSC7501_TMUX_PASSTHROUGH=1` 时，序列用 DCS
  passthrough 包裹（`ESC P tmux; … ESC \`，内部 ESC 加倍）；需要 tmux ≥ 3.3
  且在 tmux 里 `set -g allow-passthrough on`。

预期输出：无（函数库），报告以原始字节写到上述目标。

## bytes-demo.sh — 规范示例的逐字节演示

```sh
sh examples/bytes-demo.sh
```

打印三段序列的 `od -An -tx1 -c` 十六进制/字符对照：
(a) 规范 Terraform 示例
`ESC ] 7501 ; state=blocked:kind=permission:app=terraform:msg=<base64> ESC \`
（断言 base64 == `QXBwbHkgMyB0byBhZGQsIDEgdG8gY2hhbmdlLCAwIHRvIGRlc3Ryb3k/`，
即 "Apply 3 to add, 1 to change, 0 to destroy?"）；(b) ST 结尾的检测查询
`ESC ] 7501 ; ? ESC \`；(c) BEL 结尾的同款查询。末尾附「字节→含义」速查表。
任何断言失败时非零退出；成功时以 `all assertions passed.` 结束、退出码 0。

## wrap.sh — 命令包装器

```sh
sh examples/wrap.sh -- sleep 1
sh examples/wrap.sh --app make -- make -j4
```

开始时发 `state=working`（msg=`Running: <cmd>`）；成功发 `done`（msg 带耗时秒数）；
失败发 `error`（msg 带退出码）并保留原退出码；Ctrl-C（SIGINT）时发 `idle`
后以 130 退出。报告走 osc7501.sh 的输出逻辑（默认 /dev/tty）。
预期输出：被包装命令的正常输出；状态报告本身对终端不可见。

## detect.sh — 特性检测

```sh
sh examples/detect.sh            # 默认 1 秒超时
sh examples/detect.sh -t 2
```

在 /dev/tty 上 `stty -echo -icanon min 0 time N` 后发送
`ESC ] 7501 ; ? ESC \` + DA1（`ESC [ c`），按先到的回复判定。会一直读到
OSC 回复终止（`ESC \` 或 BEL——规范不要求回复复用请求的终止符）或 DA1
回复以 `c` 结束为止，因此 rev 0.4 里带 `states=`/`kinds=` 列表的回复不会被
截断；超时前两者都没有则判不支持。预期输出（退出码）：

- `supported`（0），随后两行 `states: …` 与 `kinds: …`——回复带列表时原样
  打印；不带列表时打印固定缺省值并附 `(default)`
  （idle,working,done,blocked,error / permission,question,auth，规范规定
  这两组缺省值永远不变）。回复里不认识的 pair 一律忽略（规范要求）
- `unsupported (DA1 first)`（1）
- `unsupported (no reply)`（1）
- `no tty`（2，无可用终端）

退出前用 trap 恢复 stty。

## fake_terminal.py — 假终端挂具

Python 3 标准库。在 pty 里运行一条命令并扮演终端：盯着子进程输出，看到
`ESC ] 7501 ; ?` 查询或 DA1 请求（`ESC [ c`）时按所选模式作答；子进程输出
转义后（`^[` = ESC，`^G` = BEL）原样转发到 stdout，退出码与子进程一致：

```sh
python3 examples/fake_terminal.py --mode v04    -- sh examples/detect.sh
python3 examples/fake_terminal.py --mode bare   -- sh examples/detect.sh
python3 examples/fake_terminal.py --mode da1    -- sh examples/detect.sh
python3 examples/fake_terminal.py --mode silent -- sh examples/detect.sh
```

- `--mode v04`：按 libghostty-vt（rev 0.4）回复完整查询应答
  `ESC ] 7501 ; ?:states=idle,working,done,blocked,error:kinds=permission,question,auth ESC \`
  随后 DA1 `ESC [ ?62;22c`
- `--mode bare`：只回裸 `?`（`ESC ] 7501 ; ? ESC \`），随后 DA1
- `--mode da1`：只回 DA1——复现「DA1 先到 → 不支持」路径
- `--mode silent`：什么都不回——复现「无回复」路径

box 上没有实现 OSC 7501 的真实终端，RUNLOG 里 supported / DA1-first
两条路径无法覆盖；用这个挂具可以本地驱动 detect.sh 的全部四条路径。

## osc7501_parser.py — 增量解析器 + 记录存储

Python 3.11+，仅标准库。作为库：

```python
from osc7501_parser import Osc7501Parser, RecordStore
events = Osc7501Parser().feed(chunk_bytes)   # 可跨 chunk 边界，任意切分
# Query(states, kinds) / Report(state, id, kind, progress, app, title, msg, raw_pairs)
store = RecordStore()
for ev in events:
    if isinstance(ev, Report):
        store.apply(ev)
```

按规范做全部校验：state 必填且合法；畸形 pair 跳过；未知 key 忽略；重复 key
后者生效；kind 仅 blocked 有效；progress 仅 working/blocked 且 0–100；app/id
字符集与长度；msg/title base64（padding 可选）解码失败或含控制字符整条丢弃；
整条 4096 字节上限等。`RecordStore` 实现整条替换、clear 子树、app 最近祖先继承、
`on_process_exit()`/`on_prompt()` 清理 working/blocked、超 256 条 LRU 淘汰、
`on_ris()` 全清。

rev 0.4 的检测回复三件套：`parse_query_reply()` 解析 `?` 后可选的
`states=`/`kinds=` 列表（缺列表即固定缺省值，未知 pair 忽略）；
`make_query_reply()` 构造终端侧回复（`clear` 不计入 states 列表；终止符可选，
规范不要求复用请求的）；`choose_state()` 是程序侧用法：想用新 state 时先查
回复里的 states 列表，没有就回退到已有的。

作为 CLI：

```sh
python3 examples/osc7501_parser.py typescript.log   # 缺省读 stdin
```

预期输出：每个解析出的事件一行 JSON，例如

```json
{"type": "report", "state": "blocked", "id": null, "kind": "permission", "progress": null, "app": "terraform", "title": null, "msg": "Apply 3 to add, 1 to change, 0 to destroy?", "raw_pairs": {...}}
{"type": "query"}
```

## test_osc7501_parser.py — 单元测试

```sh
python3 -m unittest discover -s examples -v
```

预期输出：全部用例 `ok`，结尾 `OK`（当前 49 个用例，覆盖上述每条规则及
RecordStore 语义）。任何回归都会非零退出。

## tmux-passthrough.sh — tmux 透传实验

```sh
sh examples/tmux-passthrough.sh
```

用 `script -q -c` 在隔离 tmux 服务器（`tmux -L osc7501test -f /dev/null`）上
分别以 allow-passthrough off/on × 裸 OSC 7501 / DCS 包裹四种组合发送
`state=working` 报告，然后检查外层 typescript 里是否出现对应字节，打印 4 个
结果。预期（已在 tmux 3.5a 上验证）：

```text
allow-passthrough=off  bare        -> absent  (as expected)
allow-passthrough=off  DCS-wrapped -> absent  (as expected)
allow-passthrough=on   bare        -> absent  (as expected)
allow-passthrough=on   DCS-wrapped -> present  (as expected)

all 4 cases behaved as expected.
```

即：tmux 不识别 7501，裸序列一律被丢弃；只有 allow-passthrough on 且 DCS 包裹
时才能透传（需要 tmux ≥ 3.3）。全部符合预期时退出码 0。结束自动 kill-server。
