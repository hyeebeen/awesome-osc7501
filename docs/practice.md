# OSC 7501 实践指南（重点）

可复制运行的用法集。所有示例都在 Linux + tmux 3.5a 上实际运行过，真实输出
记录在 [examples/RUNLOG.md](../examples/RUNLOG.md)。核实日期 2026-10-09
（Asia/Shanghai，CST）。

## 1 最小发送端：一个 shell 函数

```sh
status() {
  printf '\e]7501;state=%s:msg=%s\e\\' "$1" "$(printf '%s' "$2" | base64 | tr -d '\n')"
}
status working "compiling…"   # 开工
status blocked "Allow this?"  # 等输入
status done "finished"        # 完成
```

这是作者博文里的原版。要点：`msg` 必须是标准 base64；终止符用 `ESC \`（也
可用 BEL）。

## 2 用本仓库的函数库

[examples/osc7501.sh](../examples/osc7501.sh) 在上式基础上补齐了校验与输出
目标选择：

```sh
. ./examples/osc7501.sh
osc7501_report blocked 'kind=permission' 'app=myapp' 'msg=Allow this?'
osc7501_status working "compiling…"
osc7501_clear          # 清空所有记录
osc7501_clear build/x  # 只清 id=build/x 子树
```

- 输出默认走 `/dev/tty`（写不进则退回 stdout）；`OSC7501_OUT=文件` 可把原始
  字节录下来调试，`OSC7501_OUT=-` 写 stdout。
- 在 tmux 里且 `OSC7501_TMUX_PASSTHROUGH=1` 时自动做 DCS 透传包裹。

## 3 包装任意命令：wrap.sh

```sh
sh examples/wrap.sh -- sleep 1
sh examples/wrap.sh --app make -- make -j4
sh examples/wrap.sh -- rsync -a src/ host:dst/
```

行为：开始发 `state=working`（msg=`Running: <cmd>`）；成功发 `done`（msg 带
耗时）；失败发 `error`（msg 带退出码）并保留原退出码；Ctrl-C 发 `idle` 后以
130 退出。实测字节（`OSC7501_OUT=-` + `od`）：

```text
033 ] 7 5 0 1 ; s t a t e = w o r k i n g : a p p = m a k e : m s g = U n V u b m l u Z z o g…
033 \ 033 ] 7 5 0 1 ; s t a t e = d o n e : a p p = m a k e : m s g = R G 9 u Z T o g…
033 \
```

（完整输出见 [RUNLOG · wrap.sh 一节](../examples/RUNLOG.md)。）

## 4 检测终端是否支持：detect.sh

```sh
sh examples/detect.sh            # 默认 1 秒超时
sh examples/detect.sh -t 2
```

发送 `OSC 7501 ; ? ST` + DA1（`CSI c`），按先到的回复判定：`supported` /
`unsupported (DA1 first)` / `unsupported (no reply)` / `no tty`。末尾附带
terminfo `Pst` 检查——仅供参考，**缺 `Pst` 不能推断不支持**，查询回复才权威。
在无应答环境（`script` 包一层 pty）里的真实输出：

```text
unsupported (no reply)
terminfo: Pst absent (NOT authoritative — see comment in detect.sh)
```

## 5 解析器 CLI：验证你发出的字节

[examples/osc7501_parser.py](../examples/osc7501_parser.py) 实现了带完整校验的
增量解析（可作接收端参考），也能当调试器用：

```sh
script -q -c "sh examples/wrap.sh --app demo -- sleep 0.2" /tmp/ts.log
python3 examples/osc7501_parser.py /tmp/ts.log
```

真实输出（节选，完整见 [RUNLOG · 解析器一节](../examples/RUNLOG.md)）：

```json
{"type": "report", "state": "working", "app": "demo", "msg": "Running: sleep 0.2", "raw_pairs": {"state": "working", "app": "demo", "msg": "UnVubmluZzogc2xlZXAgMC4y"}}
{"type": "report", "state": "done", "app": "demo", "msg": "Done: sleep 0.2 (0.2s)", "raw_pairs": {"state": "done", "app": "demo", "msg": "RG9uZTogc2xlZXAgMC4yICgwLjJzKQ=="}}
```

## 6 tmux 透传：配置与实测

tmux 不识别 7501，裸序列被丢弃。两种出路：

1. 让被包裹的程序用 DCS passthrough（`OSC7501_TMUX_PASSTHROUGH=1` 时本仓库
   函数库自动做）：tmux ≥ 3.3 且开启

   ```sh
   tmux set -g allow-passthrough on   # 或写进 ~/.tmux.conf
   ```

2. 等/推动 tmux 原生支持（见 [tmux #5713](https://github.com/tmux/tmux/issues/5713)，
   维护者目前观望）。

tmux 3.5a 上的四象限实测（[examples/tmux-passthrough.sh](../examples/tmux-passthrough.sh)）：

```text
allow-passthrough=off  bare        -> absent  (as expected)
allow-passthrough=off  DCS-wrapped -> absent  (as expected)
allow-passthrough=on   bare        -> absent  (as expected)
allow-passthrough=on   DCS-wrapped -> present  (as expected)
```

## 7 调试技巧：script 录制 + od 查看

状态报告对终端「不可见」，调试时把字节落盘：

```sh
# 录制：script 会原样捕获转义序列
script -q -c "你的命令" /tmp/session.log

# 查看原始字节
od -An -tx1 -c /tmp/session.log | less

# 只找 7501 序列（printf 把 ESC 写进 grep 模式）
od -An -c /tmp/session.log | grep '7501'

# 用解析器还原语义（见第 5 节）
python3 examples/osc7501_parser.py /tmp/session.log
```

发送侧也可以不经过终端：`OSC7501_OUT=/tmp/reports.bin 你的命令`，然后对文件
跑解析器。

## 8 在自己的 CLI / agent 里接入：步骤清单

1. **规划 state 机**：何时发哪个 state——
   - 任务开始 → `working`（可带 `progress=0..100`，不确定就省略）；
   - 需要用户批准/回答/登录 → `blocked` + `kind=permission|question|auth`；
   - 成功结束 → `done`；
   - 失败结束 → `error`；
   - 用户取消 → `idle`。
2. **规划 id**：单任务用根记录（省略 id）即可；有子任务（并行 agent、构建
   步骤）用层级路径如 `build/x`、`subagents/<run>`（pi-subagents 的做法），
   结束时对子树 `clear`。
3. **每条报告完整替换记录**：想保留 `app` 就每条都写；子记录可从祖先继承 app。
4. **退出路径务必收尾**：正常退出前发 `done`/`error`；被信号打断发 `idle`；
   依赖接收端「进程退出/新提示符丢弃 working/blocked」只作兜底，别当主路径
   （SSH 远端没有 OSC 133 A 时兜底会失效）。
5. **发送前自检**：msg/title 先 base64；控制字符先替换掉；msg ≤ 2048 解码字节；
   整条 ≤ 4096。
6. **检测（可选但推荐）**：用 `OSC 7501 ; ?` + DA1 探测（照抄
   [detect.sh](../examples/detect.sh) 的时序）；不支持就静默跳过或降级到
   OSC 9;4。检测到支持时，建议顺手隐藏你自己画的 spinner。
7. **多路复用器**：tmux 里要么放弃（静默降级），要么透传（第 6 节）；不要
   重试或告警——丢弃是正常降级。

一个最小骨架（POSIX sh）：

```sh
. ./examples/osc7501.sh
trap 'osc7501_status idle "cancelled"; exit 130' INT
osc7501_report working 'app=mytool' 'msg=step 1/2'
# …干活…
osc7501_report blocked 'kind=permission' 'app=mytool' 'msg=Deploy to prod?'
# …等确认…
osc7501_report done 'app=mytool' 'msg=shipped'
```
