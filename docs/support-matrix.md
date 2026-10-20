# 支持矩阵（全部版本动态集中于此）

本页是仓库中**唯一**列出版本号与发布日期的清单之一（另一处是
[timeline.md](timeline.md)）。所有时间均为 Asia/Shanghai（CST）；核实日期见各行末列
（2026-10-11 已发版且本轮未复核的行保持 2026-10-11，其余为 2026-10-21；来源与方法见
[research/2026-10-21.md](../research/2026-10-21.md)，上两轮见
[research/2026-10-11.md](../research/2026-10-11.md) 与
[research/2026-10-09.md](../research/2026-10-09.md)）。

## 分类明细

<!-- BEGIN GENERATED: matrix (scripts/build.py; edit data/integrations.yml instead) -->

### 表 1 · 终端 / 多路复用器 / agent 工作台 / 嵌入库（接收端）

| 名称 | 角色 | 状态 | 版本 | 证据类型 | 来源链接 | 核实日期 |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="libghostty-vt"></a>libghostty-vt | 嵌入式 VT 库（作者本人的参考实现） | 已合并未发版 | main，已跟到 rev 0.4（PR #14630 合并 2026-10-11 03:44；不在最新 tag v1.3.1 中） | 已验证 | <https://github.com/ghostty-org/ghostty/pull/14560> · <https://github.com/ghostty-org/ghostty/pull/14630> | 2026-10-21 |
| <a id="ghostty-app"></a>Ghostty 应用 | 终端 | 未支持 | —（应用侧忽略报告，库已支持） | 已验证 | <https://github.com/ghostty-org/ghostty/blob/main/src/termio/stream_handler.zig> | 2026-10-11 |
| <a id="rex"></a>Rex（Superlogical） | agent 工作台（规范发源地） | 已实现（官方文档自述） | 版本未确认（beta 邀请制为推断） | 自述 | <https://www.superlogical.com/rex/docs/build/program-status> | 2026-10-11 |
| <a id="tern"></a>Tern（Stencil） | 终端（Stencil 的 Rust 原生 neoterminal，闭源） | 仅宣布 | 0.6.4（自述，未确认；无公开 release） | 自述 | <https://x.com/_can1357/status/2108468517217665065> | 2026-10-11 |
| <a id="cmux"></a>cmux | agent 多路复用器（基于 Ghostty） | 已发布 | v0.65.1（2026-10-13 07:11） | 已验证 | <https://github.com/manaflow-ai/cmux/pull/18742> · [文档](https://github.com/manaflow-ai/cmux/blob/main/docs/program-status.md) · <https://github.com/manaflow-ai/cmux/pull/19091> · <https://github.com/manaflow-ai/cmux/releases/tag/v0.65.1> | 2026-10-21 |
| <a id="termio"></a>termio | agentic 开发环境 | 已发布 | v0.56.0（2026-10-09 21:31） | 已验证 | <https://github.com/termio-sh/termio/pull/713> · <https://github.com/termio-sh/termio/releases/tag/v0.56.0> | 2026-10-11 |
| <a id="swiftterm"></a>SwiftTerm | 终端组件库（macOS/Linux） | 已发布 | v1.99.0（2026-10-09 04:21；后续 PR #748 已合并） | 已验证 | <https://github.com/migueldeicaza/SwiftTerm/releases/tag/v1.99.0> | 2026-10-11 |
| <a id="tuios"></a>TUIOS | 终端 | 已发布 | v0.9.0（2026-10-08 14:39） | 已验证 | <https://github.com/Gaurav-Gosain/tuios/releases/tag/v0.9.0> | 2026-10-11 |
| <a id="termy"></a>Termy | 终端 | 已发布 | v1.0.0-rc.2（2026-10-08 17:01） | 已验证 | <https://github.com/lassejlv/termy/pull/408> · <https://github.com/lassejlv/termy/releases/tag/v1.0.0-rc.2> | 2026-10-11 |
| <a id="con-terminal"></a>con-terminal | 终端 | 已发布 | v0.1.0-beta.122（2026-10-09 20:49） | 已验证 | <https://github.com/nowledge-co/con-terminal/pull/451> · <https://github.com/nowledge-co/con-terminal/releases/tag/v0.1.0-beta.122> | 2026-10-11 |
| <a id="phux"></a>phux | 多路复用器 | 已发布 | v0.52.0（2026-10-07 14:34） | 已验证 | <https://github.com/no-phux/phux/pull/1050> · <https://github.com/no-phux/phux/releases/tag/v0.52.0> | 2026-10-11 |
| <a id="thurm"></a>thurm | macOS 终端 | 已发布 | v0.3.0（2026-10-08 04:28） | 已验证 | <https://github.com/nklmilojevic/thurm/pull/68> · <https://github.com/nklmilojevic/thurm/releases/tag/v0.3.0> | 2026-10-11 |
| <a id="wietty"></a>wietty | 终端 | 已发布 | v0.0.17（2026-10-09 23:04） | 已验证 | <https://github.com/kloostermanw/wietty/pull/68> · <https://github.com/kloostermanw/wietty/releases/tag/v0.0.17> | 2026-10-11 |
| <a id="prowl"></a>Prowl | macOS 原生 agent 编排器（经 GhosttyKit 接收） | 已发布 | v2026.10.11（2026-10-11 15:25） | 已验证 | <https://github.com/onevcat/Prowl/pull/887> · <https://x.com/onevcat/status/2109188629885243596> | 2026-10-11 |
| <a id="rove"></a>rove | agent 多路复用器 | 已发布 | v0.9.245（2026-10-10 22:06） | 已验证 | <https://github.com/Sma1lboy/rove/pull/1232> | 2026-10-11 |
| <a id="botmux"></a>botmux | 飞书 / Lark 桥接 AI coding CLI | 已发布 | v3.40.0（2026-10-10 10:32） | 已验证 | <https://github.com/deepcoldy/botmux/pull/1781> | 2026-10-11 |
| <a id="armadra"></a>Armadra | agent 画布 | 已发布 | v0.2.5（2026-10-10 04:55） | 已验证 | <https://github.com/AMA-Link/Armadra/pull/217> | 2026-10-11 |
| <a id="dozer-sandbox"></a>dozer-sandbox | Mac 上给 agent 用的 Linux 沙箱 | 已发布 | v0.32.0（2026-10-09 19:44） | 已验证 | <https://github.com/dozer-sandbox/dozer-sandbox/pull/5> | 2026-10-11 |
| <a id="serverbox"></a>ServerBox（flutter_server_box） | Flutter 终端 / SSH 客户端 | 已发布 | v1.0.1765（2026-10-12 02:32） | 已验证 | <https://github.com/lollipopkit/flutter_server_box/pull/1662> · <https://github.com/lollipopkit/flutter_server_box/releases/tag/v1.0.1765> | 2026-10-21 |
| <a id="diri"></a>diri | 并行 agent 工作台 | 已发布 | v0.9.6（2026-10-09 20:53） | 已验证 | <https://github.com/cristicretu/diri/pull/732> · <https://github.com/cristicretu/diri/releases/tag/v0.9.6> | 2026-10-11 |
| <a id="programa"></a>programa | 基于 Ghostty 的 agent 终端 | 已合并未发版 | —（仅持续移动的 `rolling` 预构建 tag，无版本号） | 已验证 | <https://github.com/darkroomengineering/programa/pull/405> | 2026-10-21 |
| <a id="agent-os"></a>agent-os | agent 工作台（小项目） | 已合并未发版 | — | 已验证 | <https://github.com/saadnvd1/agent-os/pull/100> | 2026-10-21 |
| <a id="zz"></a>zz | 小项目 | 已发布 | v0.17.0（2026-10-18 02:28） | 已验证 | <https://github.com/demfabris/zz/pull/10> · <https://github.com/demfabris/zz/releases/tag/v0.17.0> | 2026-10-21 |
| <a id="toastty"></a>toastty | 小项目 | 已发布 | v0.9.1（2026-10-11 10:38） | 已验证 | <https://github.com/figelwump/toastty/pull/105> · <https://github.com/figelwump/toastty/releases/tag/v0.9.1> | 2026-10-11 |
| <a id="claude-fleet"></a>claude-fleet | agent 工作台（小项目） | 已合并未发版 | PR #2597（滚动 tag `stable` 已包含；无版本号 release） | 已验证 | <https://github.com/verkyyi/claude-fleet/pull/2597> | 2026-10-21 |
| <a id="para-code"></a>para-code | agent 工作台（小项目） | 已发布 | v1.139.1-paracode-165（2026-10-10 19:46） | 已验证 | <https://github.com/MocA-Love/para-code/pull/318> · <https://github.com/MocA-Love/para-code/releases/tag/v1.139.1-paracode-165> | 2026-10-11 |
| <a id="attn"></a>attn | agent 会话管理 | 已合并未发版 | PR #613（合并 2026-10-10 04:30）与 #631（合并 2026-10-11 04:23）；最新 v0.12.0 早于合并 | 已验证 | <https://github.com/SolenesInc/attn/pull/613> · <https://github.com/SolenesInc/attn/pull/631> | 2026-10-21 |
| <a id="cherry"></a>cherry | agent 状态工具（PR 标题：从 7501 取 agent 状态） | 已发布 | v2026.10.12.1（2026-10-13 06:46） | 已验证 | <https://github.com/patrick91/cherry/pull/10> · <https://github.com/patrick91/cherry/releases/tag/v2026.10.12.1> | 2026-10-21 |
| <a id="noctty"></a>noctty | Windows 原生终端（原 winghostty，fork） | 已发布 | v1.3.132（2026-10-16 20:02） | 已验证 | <https://github.com/amanthanvi/noctty/pull/301> · <https://github.com/amanthanvi/noctty/releases/tag/v1.3.132> | 2026-10-21 |
| <a id="monkeyssh"></a>MonkeySSH | Flutter SSH 客户端 | 已发布 | v0.10.0（2026-10-18 15:57） | 已验证 | <https://github.com/depollsoft/MonkeySSH/pull/977> · <https://github.com/depollsoft/MonkeySSH/releases/tag/v0.10.0> | 2026-10-21 |
| <a id="go-term"></a>go-term | go-gui 的终端组件 | 已发布 | v0.16.0（2026-10-12 06:58） | 已验证 | <https://github.com/go-gui-org/go-term/pull/265> · <https://github.com/go-gui-org/go-term/releases/tag/v0.16.0> | 2026-10-21 |
| <a id="agentd"></a>agentd | agent 工作区守护进程 | 已发布 | v0.1.0（2026-10-20 20:50） | 已验证 | <https://github.com/robmorgan/agentd/pull/29> · <https://github.com/robmorgan/agentd/releases/tag/v0.1.0> | 2026-10-21 |
| <a id="tmux-agent-panel"></a>tmux-agent-panel | tmux 面板 | 已关闭 | —（PR #4 closed 未合并） | 已验证 | <https://github.com/ahmedelgabri/tmux-agent-panel/pull/4> | 2026-10-11 |
| <a id="wintty"></a>wintty | Windows 上的 Ghostty 移植 | 已合并未发版 | PR #1316（合并 2026-10-12 09:58；w1.0.0-rc.7 不含） | 已验证 | <https://github.com/deblasis/wintty/pull/1316> | 2026-10-21 |
| <a id="royalterminal"></a>RoyalTerminal | .NET 终端栈（集成 Ghostty VT） | 开发中 | PR open | 已验证 | <https://github.com/royalapplications/RoyalTerminal/pull/121> | 2026-10-21 |
| <a id="luvus"></a>luvus | agent 任务台（mission control） | 开发中 | PR open | 已验证 | <https://github.com/RizRiyz/luvus/pull/498> | 2026-10-21 |
| <a id="cleat"></a>cleat | 会话守护进程 | 已合并未发版 | PR #329（合并 2026-10-13 04:54；无 tag） | 已验证 | <https://github.com/flotilla-org/cleat/pull/329> | 2026-10-21 |
| <a id="tmux"></a>tmux | 多路复用器 | 未支持 | —（issue #5713 于 2026-10-13 15:50 由维护者关闭，无上游提交；DCS passthrough + allow-passthrough on 仍可透传） | 已验证（issue + 本仓库实测；维护者 nicm（2026-10-10 01:51）：“I think between pane titles, OSC 9 progress bars and OSC 133 we have enough coverage of this kind of thing for the moment, let's see if this one takes off.”） | <https://github.com/tmux/tmux/issues/5713> | 2026-10-21 |
| <a id="screen"></a>screen | 多路复用器 | 未支持 | —（pi 文档称不转发） | 自述（pi 文档） | <https://github.com/earendil-works/pi/blob/v1.1.0/packages/coding-agent/docs/terminal-setup.md> | 2026-10-11 |
| <a id="kitty"></a>Kitty | 终端 | 已合并未发版 | master（merge 0e1b7f4812，2026-10-13 10:59；最新 release v0.49.2 发于 2026-10-01，不含） | 已验证（关闭 #10638 时维护者留言（2026-10-13 11:58）：“now implemented in master using 263 ans the id length limit and base64 padding bytes being optional”（原文照录，“ans” 拼写为原始）；即 kitty 的 id 上限为 263 而非规范的 128；PR #10657（ttys3）closed 未合并，实现经维护者 commit 落地） | <https://github.com/kovidgoyal/kitty/issues/10638> · <https://github.com/kovidgoyal/kitty/commit/0e1b7f4812bf297639999a362672c4271e42ed0c> | 2026-10-21 |
| <a id="wezterm"></a>WezTerm | 终端 | 未支持 | —（主分支 commit 与 issue 搜索均无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| <a id="alacritty"></a>Alacritty | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| <a id="windows-terminal"></a>Windows Terminal | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| <a id="zellij"></a>zellij | 多路复用器 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| <a id="iterm2"></a>iTerm2 | 终端 | 未支持 | —（代码与 issue 搜索均无；已有 OSC 21337） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| <a id="xterm-js"></a>xterm.js（VS Code 终端） | 嵌入式终端组件 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| <a id="zed"></a>Zed | 编辑器（终端面板） | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| <a id="warp"></a>Warp | 终端 | 开发中 | PR #16460 open（外部贡献者，2026-10-14 10:00 开）；另有 issue #16407 open（2026-10-11 07:49 开） | 已验证 | [research 笔记](../research/2026-10-09.md) · <https://github.com/warpdotdev/warp/pull/16460> · <https://github.com/warpdotdev/warp/issues/16407> | 2026-10-21 |
| <a id="wave"></a>Wave | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| <a id="rio"></a>Rio | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| <a id="contour"></a>Contour | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| <a id="foot"></a>foot | 终端 | 未确认 | —（issue 搜索无结果，代码未查） | Codeberg issue 搜索无结果，代码未查 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| <a id="orca"></a>Orca | agent 工作台（接收端） | 已发布 | v1.4.232（2026-10-20 14:20） | 已验证 | <https://github.com/stablyai/orca/pull/30261> · <https://github.com/stablyai/orca/pull/30262> | 2026-10-21 |
| <a id="paseo"></a>Paseo | agent 工作台 | 开发中 | PR #6962 open（外部贡献者） | 已验证 | <https://github.com/getpaseo/paseo/pull/6962> | 2026-10-21 |
| <a id="supacode"></a>Supacode | 终端/agent 工作台 | 开发中 | PR #911 open（成员） | 已验证 | <https://github.com/supabitapp/supacode/pull/911> | 2026-10-21 |
| <a id="zmx"></a>zmx | 会话守护进程 | 已关闭 | —（PR #289 closed 未合并） | 已验证 | <https://github.com/neurosnap/zmx/pull/289> | 2026-10-21 |
| <a id="psmux"></a>psmux | Windows 多路复用器 | 已关闭 | —（PR #797 closed 未合并） | 已验证 | <https://github.com/psmux/psmux/pull/797> | 2026-10-21 |
| <a id="ghostel"></a>ghostel | Emacs 终端（libghostty） | 已关闭 | —（PR #740 closed 未合并） | 已验证 | <https://github.com/dakra/ghostel/pull/740> | 2026-10-21 |

### 表 2 · AI agent 与 coding CLI（发送端）

| 名称 | 角色 | 状态 | 版本 | 证据类型 | 来源链接 | 核实日期 |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="claude-code"></a>Claude Code | AI coding agent | 已发布 | v2.1.295（2026-10-09 03:48） | 已验证 | <https://github.com/anthropics/claude-code/releases/tag/v2.1.295> | 2026-10-11 |
| <a id="pi"></a>pi（earendil-works/pi） | AI coding agent | 已发布 | v1.1.0（2026-10-08 06:26） | 已验证 | <https://github.com/earendil-works/pi/releases/tag/v1.1.0> | 2026-10-11 |
| <a id="omp"></a>omp（can1357/oh-my-pi） | AI coding agent | 已发布 | v18.8.7（2026-10-09 21:45，实现 commit fd84fae，7501 首发）；v18.9.0（2026-10-11 16:08）release notes 未提 7501；PR #15113 open | 已验证 | <https://github.com/can1357/oh-my-pi/releases/tag/v18.8.7> · <https://github.com/can1357/oh-my-pi/releases/tag/v18.9.0> | 2026-10-11 |
| <a id="factory-droid"></a>Factory Droid | AI coding agent | 已发布（推断：changelog 未写 OSC 7501 字样） | CLI v0.236.0 · Desktop v0.193.0（2026-10-08） | 推断 | <https://docs.factory.com/changelog/release-notes> | 2026-10-21 |
| <a id="docker-agent"></a>Docker Agent（docker/docker-agent） | AI agent | 已发布 | v1.150.0（2026-10-09 19:39；PR #4544 合并 2026-10-07 22:51） | 已验证 | <https://github.com/docker/docker-agent/releases/tag/v1.150.0> | 2026-10-11 |
| <a id="crush"></a>Crush（charmbracelet/crush） | AI coding agent | 已发布 | v0.98.0（2026-10-09 02:26） | 已验证 | <https://github.com/charmbracelet/crush/pull/4041> · <https://github.com/charmbracelet/crush/releases/tag/v0.98.0> | 2026-10-11 |
| <a id="knightcode"></a>KnightCode | AI coding agent | 已发布 | @knightcodeai/cli@0.15.0（2026-10-08 08:27） | 已验证 | <https://github.com/KnightCodeAI/knightcode/pull/296> · <https://github.com/KnightCodeAI/knightcode/releases/tag/%40knightcodeai%2Fcli%400.15.0> | 2026-10-11 |
| <a id="atomic"></a>atomic（bastani-inc/atomic） | coding agent runtime | 已发布 | 0.9.33（2026-10-11 06:51；#3558 为修复 PR，首个实现 PR 未核实） | 已验证 | <https://github.com/bastani-inc/atomic/pull/3558> | 2026-10-11 |
| <a id="lydakis-agent"></a>agent（lydakis/agent） | 多 agent 守护进程 CLI | 已发布 | v0.2.0（2026-10-11 14:11） | 已验证 | <https://github.com/lydakis/agent/pull/85> | 2026-10-11 |
| <a id="fx"></a>fx（vercel-labs/fx） | coding agent | 已发布 | v0.0.14（2026-10-16 16:27） | 已验证 | <https://github.com/vercel-labs/fx/pull/1181> · <https://github.com/vercel-labs/fx/releases/tag/v0.0.14> | 2026-10-21 |
| <a id="pi-subagents"></a>pi-subagents | pi 扩展（层级 id `subagents/<run>`） | 已发布 | v0.77.0（2026-10-10 13:26） | 已验证 | <https://github.com/nicobailon/pi-subagents/pull/2725> · <https://github.com/nicobailon/pi-subagents/releases/tag/v0.77.0> | 2026-10-11 |
| <a id="yolop"></a>yolop | coding agent（小项目） | 已发布 | v0.20.0（2026-10-10 07:18） | 已验证 | <https://github.com/everruns/yolop/pull/818> · <https://github.com/everruns/yolop/releases/tag/v0.20.0> | 2026-10-11 |
| <a id="rho"></a>rho | coding agent（小项目） | 已发布 | rho-sdk-v5.9.0（2026-10-11 05:01；tag 名为 sdk，CLI 是否同包未确认） | 已验证 | <https://github.com/matthewyjiang/rho/pull/1454> · <https://github.com/matthewyjiang/rho/releases/tag/rho-sdk-v5.9.0> | 2026-10-11 |
| <a id="jazz"></a>jazz | coding agent（小项目） | 已发布 | v0.16.13（2026-10-09 17:37） | 已验证 | <https://github.com/lvndry/jazz/pull/824> · <https://github.com/lvndry/jazz/releases/tag/v0.16.13> | 2026-10-11 |
| <a id="wing-agent"></a>wing-agent | coding agent（小项目） | 已合并未发版 | PR #177 | 已验证 | <https://github.com/lpdink/wing-agent/pull/177> | 2026-10-21 |
| <a id="shikigami"></a>shikigami | coding agent（小项目） | 已合并未发版 | PR #438 | 已验证 | <https://github.com/Sannrox/shikigami/pull/438> | 2026-10-21 |
| <a id="the-last-harness"></a>the-last-harness | coding agent（小项目） | 已发布 | v0.44.0（2026-10-13 05:52） | 已验证 | <https://github.com/diegopetrucci/the-last-harness/pull/749> · <https://github.com/diegopetrucci/the-last-harness/releases/tag/v0.44.0> | 2026-10-21 |
| <a id="haskell-agent"></a>haskell-agent | agent harness（Haskell） | 已合并未发版 | PR #1389（合并 2026-10-11 06:07；无 release） | 已验证 | <https://github.com/digitallyinduced/haskell-agent/pull/1389> | 2026-10-21 |
| <a id="cyrup"></a>cyrup | agent / CLI | 已合并未发版 | PR #221（无 release） | 已验证 | <https://github.com/cyrup-ai/cyrup/pull/221> | 2026-10-21 |
| <a id="tincan"></a>tincan | Mac 消息 / 通讯录应用（小项目） | 未确认 | —（仓库 2026-10-21 访问返回 404，无法复核） | 仓库 2026-10-21 访问返回 404，无法复核 | <https://github.com/AarushSah/tincan/pull/1> | 2026-10-21 |
| <a id="armadra-agent"></a>Armadra Agent | Armadra 画布的 agent 端（发送端） | 已发布 | v0.7.2（2026-10-09 22:35；10-11 版误记为未发版，已更正） | 已验证 | <https://github.com/AMA-Link/armadra-agent/pull/126> · <https://github.com/AMA-Link/armadra-agent/releases/tag/v0.7.2> | 2026-10-21 |
| <a id="prime-agent"></a>prime-agent | AI agent | 开发中 | PR open | 已验证 | <https://github.com/PrimeIntellect-ai/prime-agent/pull/3424> | 2026-10-21 |
| <a id="8gent-code"></a>8gent-code | AI agent | 已发布 | v0.20.0（2026-10-14 07:29） | 已验证 | <https://github.com/8gi-foundation/8gent-code/pull/3738> · <https://github.com/8gi-foundation/8gent-code/releases/tag/v0.20.0> | 2026-10-21 |
| <a id="bub"></a>bub | AI agent | 已合并未发版 | PR #345（合并 2026-10-19 09:36；0.6.0a3 不含） | 已验证 | <https://github.com/bubbuild/bub/pull/345> | 2026-10-21 |
| <a id="wovenmatter"></a>wovenmatter | AI agent | 已发布 | v0.2.7（2026-10-10 23:57） | 已验证 | <https://github.com/wovenmatter/wovenmatter/pull/111> · <https://github.com/wovenmatter/wovenmatter/releases/tag/v0.2.7> | 2026-10-11 |
| <a id="minimax-code"></a>MiniMax Code | AI coding agent | 已合并未发版 | PR #471（合并 2026-10-13 16:02；v0.6.5 不含） | 已验证 | <https://github.com/MiniMax-AI/minimax-code/pull/471> | 2026-10-21 |
| <a id="icode"></a>iCode | 离线开发平台 / agent 工具包 | 已合并未发版 | PR #80（合并 2026-10-16 17:37；v0.30.1 不含） | 已验证 | <https://github.com/openJiuwen-ai/iCode/pull/80> | 2026-10-21 |
| <a id="amp"></a>Amp | AI coding agent | 仅宣布（作者自述，无官方 changelog） | 未确认 | 自述（第三方） | <https://x.com/mitchellh/status/2107894687587795079> | 2026-10-21 |
| <a id="codex-cli"></a>Codex CLI（openai/codex） | AI coding agent | 已发布 | rust-v0.163.0（2026-10-16 05:30） | 已验证 | <https://github.com/openai/codex/pull/52725> · <https://github.com/openai/codex/releases/tag/rust-v0.163.0> | 2026-10-21 |
| <a id="opencode"></a>opencode | AI coding agent | 已合并未发版 | PR #55172（合并 2026-10-14 04:48，经 OpenTUI 0.6.3 setProgramStatus）；#54402 closed 未合并；最新 v1.19.3 与合并提交 diverged，是否已随 release 发出未确认；2026-10-14 #55300 临时回退 OpenTUI 0.6 升级，但 dev 分支 program-status.ts 仍在 | 已验证 | <https://github.com/anomalyco/opencode/pull/54402> · <https://github.com/anomalyco/opencode/issues/54179> · <https://github.com/anomalyco/opencode/pull/55172> · <https://github.com/anomalyco/opencode/pull/55300> · <https://github.com/anomalyco/opencode/pull/54560> | 2026-10-21 |
| <a id="gemini-cli"></a>Gemini CLI | AI coding agent | 未支持 | —（代码 / PR 搜索无；issue #29710 open，2026-10-10 开） | 已验证 | <https://github.com/google-gemini/gemini-cli/issues/29710> | 2026-10-21 |
| <a id="cursor-cli"></a>Cursor CLI | AI coding agent | 未确认（闭源） | —（changelog 未见） | 官方 changelog 未见（闭源） | <https://cursor.com/changelog> | 2026-10-21 |
| <a id="goose"></a>goose | AI agent CLI | 已合并未发版 | PR #12928（合并 2026-10-16 10:47；v1.55.0 不含） | 已验证 | <https://github.com/aaif-goose/goose/pull/12928> | 2026-10-21 |
| <a id="openclaw"></a>OpenClaw | agent TUI | 已合并未发版 | PR #175692（合并 2026-10-18 09:10；v2026.10.5 不含） | 已验证 | <https://github.com/openclaw/openclaw/pull/175692> | 2026-10-21 |
| <a id="deepseek-reasonix"></a>DeepSeek-Reasonix | AI agent TUI | 已发布 | studio-v2.39.0（2026-10-14 09:24） | 已验证 | <https://github.com/esengine/DeepSeek-Reasonix/pull/12976> | 2026-10-21 |
| <a id="dsh-tui"></a>dsh-TUI | agent TUI | 已合并未发版 | PR #1561（合并 2026-10-20 03:18；v0.16.1 不含） | 已验证 | <https://github.com/ccch1mneyyy/dsh-TUI/pull/1561> | 2026-10-21 |
| <a id="qwen-code"></a>Qwen Code | AI coding CLI | 开发中 | PR #13994 open（外部贡献者） | 已验证 | <https://github.com/QwenLM/qwen-code/pull/13994> | 2026-10-21 |
| <a id="hermes-agent"></a>Hermes Agent | AI agent CLI/TUI | 开发中 | PR #140837 open（协作者）；另 #138152 open | 已验证 | <https://github.com/NousResearch/hermes-agent/pull/140837> | 2026-10-21 |
| <a id="cua"></a>cua | computer-use agent | 开发中 | PR #5155 open（协作者） | 已验证 | <https://github.com/trycua/cua/pull/5155> | 2026-10-21 |

### 表 3 · 非 AI CLI（发送端）

| 名称 | 角色 | 状态 | 版本 | 证据类型 | 来源链接 | 核实日期 |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="git-stack"></a>git-stack | git 工作流 CLI | 已发布 | v0.2.0（2026-10-07 19:25） | 已验证 | <https://github.com/DomBlack/git-stack/pull/16> · <https://github.com/DomBlack/git-stack/releases/tag/v0.2.0> | 2026-10-11 |
| <a id="tuist"></a>tuist | Xcode 项目工具 | 已合并未发版 | PR #13956（已进预发布 4.213.0-rc.2，2026-10-16 17:02；未见含它的正式版） | 已验证 | <https://github.com/tuist/tuist/pull/13956> | 2026-10-21 |
| <a id="hugo"></a>Hugo | 静态站点生成器 | 已发布 | v0.168.0（2026-10-14 01:24） | 已验证 | <https://github.com/gohugoio/hugo/pull/15428> · <https://github.com/gohugoio/hugo/releases/tag/v0.168.0> | 2026-10-21 |
| <a id="composer"></a>Composer | PHP 依赖管理 | 开发中 | PR open（同时支持 OSC 9;4） | 已验证 | <https://github.com/composer/composer/pull/13117> | 2026-10-21 |
| <a id="expo-cli"></a>Expo CLI | 开发工具 | 开发中（experiment） | PR open | 已验证 | <https://github.com/expo/expo/pull/51289> | 2026-10-21 |
| <a id="bunny-net-cli"></a>bunny.net CLI | CDN CLI | 已关闭 | —（PR #244 closed 未合并） | 已验证 | <https://github.com/BunnyWay/cli/pull/244> | 2026-10-21 |
| <a id="firebase-tools"></a>firebase-tools | 开发工具 | 已关闭 | —（#11245 / #11246 关闭，计划 fresh implementation 重做） | 已验证 | <https://github.com/firebase/firebase-tools/pull/11245> | 2026-10-11 |
| <a id="terraform-homebrew-poc"></a>Terraform / Homebrew | — | 仅宣布（仅作者 PoC，插件或 fork） | — | 自述（博文） | <https://mitchellh.com/writing/program-status-osc7501> | 2026-10-11 |
| <a id="solana-pay-cli"></a>Solana Pay CLI | 密钥库 auth 提示上报 | 已合并未发版 | PR #509（合并 2026-10-16 21:54；pay-v0.29.0 不含） | 已验证 | <https://github.com/solana-foundation/pay/pull/509> | 2026-10-21 |
| <a id="gradle"></a>Gradle | 构建工具 | 开发中 | PR #39468 open（成员） | 已验证 | <https://github.com/gradle/gradle/pull/39468> | 2026-10-21 |
| <a id="msbuild"></a>MSBuild | .NET 构建 | 开发中 | PR #15263 open（成员） | 已验证 | <https://github.com/dotnet/msbuild/pull/15263> | 2026-10-21 |
| <a id="aspire"></a>Aspire | .NET 应用编排 CLI | 开发中 | PR #20988 open（成员） | 已验证 | <https://github.com/microsoft/aspire/pull/20988> | 2026-10-21 |
| <a id="buildkite-agent"></a>Buildkite Agent | CI agent | 开发中 | PR #4534 open（成员） | 已验证 | <https://github.com/buildkite/agent/pull/4534> | 2026-10-21 |

### 表 4 · TUI 库 / SDK

| 名称 | 角色 | 状态 | 版本 | 证据类型 | 来源链接 | 核实日期 |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="bubble-tea"></a>Bubble Tea | Go TUI 框架 | 已发布 | v2.1.0（2026-10-09 01:40；PR #1845 open：退出/挂起后陈旧记录修复） | 已验证 | <https://github.com/charmbracelet/bubbletea/releases/tag/v2.1.0> | 2026-10-11 |
| <a id="charmbracelet-x"></a>charmbracelet/x（ansi） | Go ANSI 库 | 已合并未发版 | PR #1004（合并 2026-10-09 01:27）；#1005 open（解析器） | 已验证 | <https://github.com/charmbracelet/x/pull/1004> | 2026-10-21 |
| <a id="charmbracelet-ultraviolet"></a>charmbracelet/ultraviolet | Go 终端库 | 已合并未发版 | PR #207；#208 open | 已验证 | <https://github.com/charmbracelet/ultraviolet/pull/207> | 2026-10-21 |
| <a id="libvaxis"></a>libvaxis | Zig TUI 库 | 已合并未发版 | main（ctlseqs.zig 含查询序列） | 已验证 | <https://github.com/rockorager/libvaxis/blob/main/src/ctlseqs.zig> | 2026-10-11 |
| <a id="tuika"></a>tuika | Rust TUI 框架 | 已发布 | v0.13.0（2026-10-08 04:40） | 已验证 | <https://github.com/everruns/tuika/pull/140> · <https://github.com/everruns/tuika/releases/tag/v0.13.0> | 2026-10-11 |
| <a id="libghostty-rs"></a>libghostty-rs | libghostty-vt 的 Rust 绑定 | 已合并未发版 | PR #6（包装回调） | 已验证 | <https://github.com/termio-sh/libghostty-rs/pull/6> | 2026-10-21 |
| <a id="xterm-dart"></a>xterm.dart | Dart 终端组件 | 已合并未发版 | PR #26（7501 + 9;4 + 133） | 已验证 | <https://github.com/lollipopkit/xterm.dart/pull/26> | 2026-10-21 |
| <a id="uncurses"></a>uncurses | 终端 UI 工具库 | 已发布 | v0.0.6（2026-10-11 03:26） | 已验证 | <https://github.com/aymanbagabas/uncurses/pull/89> | 2026-10-11 |
| <a id="opentui"></a>OpenTUI | TS 终端 UI 框架（发送端 API setProgramStatus） | 已发布 | v0.6.3（2026-10-13 16:20） | 已验证 | <https://github.com/anomalyco/opentui/pull/1657> | 2026-10-21 |
| <a id="crossterm"></a>crossterm | Rust 终端库 | 开发中 | PR #1144 open（外部贡献者） | 已验证 | <https://github.com/crossterm-rs/crossterm/pull/1144> | 2026-10-21 |
| <a id="tqdm"></a>tqdm | Python 进度条 | 开发中 | PR #1884 open（外部贡献者） | 已验证 | <https://github.com/tqdm/tqdm/pull/1884> | 2026-10-21 |

<!-- END GENERATED: matrix -->

## 状态定义

| 状态 | 定义 |
| --- | --- |
| 已发布 | 有包含该功能的 release / 版本号，或官方 changelog 明确记载 |
| 已实现（自述） | 官方文档描述已实现，但找不到版本号/release |
| 已合并未发版 | 主分支已合并，但未找到包含该功能的 release |
| 开发中 | open PR / fork 活跃开发 |
| 仅宣布 | 只有帖子 / 口头表态，无代码无版本 |
| 已关闭 | PR / issue 被关闭且未合并 |
| 未支持 | 一手源核实（代码 / issue / 实测）确认当前不支持 |
| 未确认 | 一手源查不到，无法判定 |

证据类型：**已验证** = 一手源可回溯；**自述** = 当事人 / 作者声称；**推断** =
由多条一手源推出（推断均另有标注）。

## 如何复核

用 GitHub CLI 复核各条状态（示例）：

```sh
# PR 是否已合并、何时合并
gh api repos/ghostty-org/ghostty/pulls/14560 \
  --jq '{state, merged, merged_at, merge_commit_sha}'

# 某 PR 是否进了某个 release（比较 merge commit 与 tag）
gh api repos/ghostty-org/ghostty/commits/a4aacd918ba9e79929ff608034c60a4341773ef0 \
  --jq '.sha' # 再用 git merge-base --is-ancestor 对照 tag
# 或直接问 compare API：status 为 behind / identical = 该 release 已包含此合并
gh api repos/OWNER/REPO/compare/TAG...MERGE_SHA --jq .status

# 仓库的最新 release / tag
gh release list --repo earendil-works/pi --limit 3
gh api repos/anthropics/claude-code/releases/tags/v2.1.295 --jq '.published_at'

# 全站搜索新的集成 PR（最有效的一招；结果要人工过滤同名噪音）
gh api "search/issues?q=7501+in:title+is:pr+created:>2026-09-27&per_page=100" --jq '.items[]|[.state,.repository_url,.number,.title]|@tsv'

# 主分支代码里有没有实现（判断「未支持」）
gh api 'search/code?q=repo:wezterm/wezterm+"7501;"' --jq '.total_count'

# kitty：issue 讨论状态（作者已在 issue 中审阅规范）
gh api repos/kovidgoyal/kitty/issues/10638 --jq '{state, updated_at}'
```

注意：X / 推文链接用浏览器复核；「自述」类状态要区分第一方自述与第三方转述。Codex
已随 rust-v0.163.0 发布；opencode 经 OpenTUI `setProgramStatus` 合并（#55172，是否已随
release 发出未确认）；kitty 已在 master 实现（id 上限 263，未发版）；Amp 仍仅有作者
Mitchell Hashimoto 的第三方转述（无官方 changelog）；Tern 仍仅有其开发者
@_can1357 的自述（无公开 release）。
