# 支持矩阵（全部版本动态集中于此）

本页是仓库中**唯一**列出版本号与发布日期的清单之一（另一处是
[timeline.md](timeline.md)）。所有时间均为 Asia/Shanghai（CST）；全表核实日期均为
**2026-10-11**（来源与方法见 [research/2026-10-11.md](../research/2026-10-11.md)；
上一轮核实 2026-10-09，见 [research/2026-10-09.md](../research/2026-10-09.md)）。

## 表 1 · 终端 / 多路复用器 / agent 工作台 / 嵌入库（接收端）

| 名称 | 角色 | 状态 | 版本 | 证据类型 | 来源链接 | 核实日期 |
| --- | --- | --- | --- | --- | --- | --- |
| libghostty-vt | 嵌入式 VT 库（作者本人的参考实现） | 已合并未发版 | main，已跟到 rev 0.4（PR #14630 合并 2026-10-11 03:44；不在最新 tag v1.3.1 中） | 已验证 | <https://github.com/ghostty-org/ghostty/pull/14560> · <https://github.com/ghostty-org/ghostty/pull/14630> | 2026-10-11 |
| Ghostty 应用 | 终端 | 未支持 | —（应用侧忽略报告，库已支持） | 已验证 | <https://github.com/ghostty-org/ghostty/blob/main/src/termio/stream_handler.zig> | 2026-10-11 |
| Rex（Superlogical） | agent 工作台（规范发源地） | 已实现（官方文档自述） | 版本未确认（beta 邀请制为推断） | 自述 | <https://www.superlogical.com/rex/docs/build/program-status> | 2026-10-11 |
| Tern（Stencil） | 终端（Stencil 的 Rust 原生 neoterminal，闭源） | 仅宣布 | 0.6.4（自述，未确认；无公开 release） | 自述 | <https://x.com/_can1357/status/2108468517217665065> | 2026-10-11 |
| cmux | agent 多路复用器（基于 Ghostty） | 已合并未发版 | 正式版本未确认（最新 v0.65.0，2026-10-06，不含；新 PR #19091 open） | 已验证 | <https://github.com/manaflow-ai/cmux/pull/18742> · [文档](https://github.com/manaflow-ai/cmux/blob/main/docs/program-status.md) · <https://github.com/manaflow-ai/cmux/pull/19091> | 2026-10-11 |
| termio | agentic 开发环境 | 已发布 | v0.56.0（2026-10-09 21:31） | 已验证 | <https://github.com/termio-sh/termio/pull/713> · <https://github.com/termio-sh/termio/releases/tag/v0.56.0> | 2026-10-11 |
| SwiftTerm | 终端组件库（macOS/Linux） | 已发布 | v1.99.0（2026-10-09 04:21；后续 PR #748 已合并） | 已验证 | <https://github.com/migueldeicaza/SwiftTerm/releases/tag/v1.99.0> | 2026-10-11 |
| TUIOS | 终端 | 已发布 | v0.9.0（2026-10-08 14:39） | 已验证 | <https://github.com/Gaurav-Gosain/tuios/releases/tag/v0.9.0> | 2026-10-11 |
| Termy | 终端 | 已发布 | v1.0.0-rc.2（2026-10-08 17:01） | 已验证 | <https://github.com/lassejlv/termy/pull/408> · <https://github.com/lassejlv/termy/releases/tag/v1.0.0-rc.2> | 2026-10-11 |
| con-terminal | 终端 | 已发布 | v0.1.0-beta.122（2026-10-09 20:49） | 已验证 | <https://github.com/nowledge-co/con-terminal/pull/451> · <https://github.com/nowledge-co/con-terminal/releases/tag/v0.1.0-beta.122> | 2026-10-11 |
| phux | 多路复用器 | 已发布 | v0.52.0（2026-10-07 14:34） | 已验证 | <https://github.com/no-phux/phux/pull/1050> · <https://github.com/no-phux/phux/releases/tag/v0.52.0> | 2026-10-11 |
| thurm | macOS 终端 | 已发布 | v0.3.0（2026-10-08 04:28） | 已验证 | <https://github.com/nklmilojevic/thurm/pull/68> · <https://github.com/nklmilojevic/thurm/releases/tag/v0.3.0> | 2026-10-11 |
| wietty | 终端 | 已发布 | v0.0.17（2026-10-09 23:04） | 已验证 | <https://github.com/kloostermanw/wietty/pull/68> · <https://github.com/kloostermanw/wietty/releases/tag/v0.0.17> | 2026-10-11 |
| Prowl | macOS 原生 agent 编排器（经 GhosttyKit 接收） | 已发布 | v2026.10.11（2026-10-11 15:25） | 已验证 | <https://github.com/onevcat/Prowl/pull/887> · <https://x.com/onevcat/status/2109188629885243596> | 2026-10-11 |
| rove | agent 多路复用器 | 已发布 | v0.9.245（2026-10-10 22:06） | 已验证 | <https://github.com/Sma1lboy/rove/pull/1232> | 2026-10-11 |
| botmux | 飞书 / Lark 桥接 AI coding CLI | 已发布 | v3.40.0（2026-10-10 10:32） | 已验证 | <https://github.com/deepcoldy/botmux/pull/1781> | 2026-10-11 |
| Armadra | agent 画布 | 已发布 | v0.2.5（2026-10-10 04:55） | 已验证 | <https://github.com/AMA-Link/Armadra/pull/217> | 2026-10-11 |
| dozer-sandbox | Mac 上给 agent 用的 Linux 沙箱 | 已发布 | v0.32.0（2026-10-09 19:44） | 已验证 | <https://github.com/dozer-sandbox/dozer-sandbox/pull/5> | 2026-10-11 |
| ServerBox（flutter_server_box） | Flutter 终端 / SSH 客户端 | 已合并未发版 | — | 已验证 | <https://github.com/lollipopkit/flutter_server_box/pull/1662> | 2026-10-11 |
| diri | 并行 agent 工作台 | 已发布 | v0.9.6（2026-10-09 20:53） | 已验证 | <https://github.com/cristicretu/diri/pull/732> · <https://github.com/cristicretu/diri/releases/tag/v0.9.6> | 2026-10-11 |
| programa | 基于 Ghostty 的 agent 终端 | 已合并未发版 | —（仅持续移动的 `rolling` 预构建 tag，无版本号） | 已验证 | <https://github.com/darkroomengineering/programa/pull/405> | 2026-10-11 |
| agent-os | agent 工作台（小项目） | 已合并未发版 | — | 已验证 | <https://github.com/saadnvd1/agent-os/pull/100> | 2026-10-11 |
| zz | 小项目 | 已合并未发版 | — | 已验证 | <https://github.com/demfabris/zz/pull/10> | 2026-10-11 |
| toastty | 小项目 | 已发布 | v0.9.1（2026-10-11 10:38） | 已验证 | <https://github.com/figelwump/toastty/pull/105> · <https://github.com/figelwump/toastty/releases/tag/v0.9.1> | 2026-10-11 |
| claude-fleet | agent 工作台（小项目） | 已合并未发版 | — | 已验证 | <https://github.com/verkyyi/claude-fleet/pull/2597> | 2026-10-11 |
| para-code | agent 工作台（小项目） | 已发布 | v1.139.1-paracode-165（2026-10-10 19:46） | 已验证 | <https://github.com/MocA-Love/para-code/pull/318> · <https://github.com/MocA-Love/para-code/releases/tag/v1.139.1-paracode-165> | 2026-10-11 |
| attn | agent 会话管理 | 已合并未发版 | PR #613（合并 2026-10-10 04:30）与 #631（合并 2026-10-11 04:23）；最新 v0.12.0 早于合并 | 已验证 | <https://github.com/SolenesInc/attn/pull/613> · <https://github.com/SolenesInc/attn/pull/631> | 2026-10-11 |
| cherry | agent 状态工具（PR 标题：从 7501 取 agent 状态） | 已合并未发版 | PR #10（合并 2026-10-10 22:29）；无 release | 已验证 | <https://github.com/patrick91/cherry/pull/10> | 2026-10-11 |
| noctty | Windows 原生终端（原 winghostty，fork） | 已合并未发版 | PR #301（合并 2026-10-11 05:24；最新 v1.3.131 早于合并） | 已验证 | <https://github.com/amanthanvi/noctty/pull/301> | 2026-10-11 |
| MonkeySSH | Flutter SSH 客户端 | 已合并未发版 | PR #977（合并 2026-10-10 13:21；最新 v0.9.2 早于合并） | 已验证 | <https://github.com/depollsoft/MonkeySSH/pull/977> | 2026-10-11 |
| go-term | go-gui 的终端组件 | 已合并未发版 | PR #265（合并 2026-10-10 06:09；最新 v0.15.1 早于合并） | 已验证 | <https://github.com/go-gui-org/go-term/pull/265> | 2026-10-11 |
| agentd | agent 工作区守护进程 | 已合并未发版 | PR #29（合并 2026-10-11 11:07；无 release） | 已验证 | <https://github.com/robmorgan/agentd/pull/29> | 2026-10-11 |
| tmux-agent-panel | tmux 面板 | 已关闭 | —（PR #4 closed 未合并） | 已验证 | <https://github.com/ahmedelgabri/tmux-agent-panel/pull/4> | 2026-10-11 |
| wintty | Windows 上的 Ghostty 移植 | 开发中 | PR open | 已验证 | <https://github.com/deblasis/wintty/pull/1316> | 2026-10-11 |
| RoyalTerminal | .NET 终端栈（集成 Ghostty VT） | 开发中 | PR open | 已验证 | <https://github.com/royalapplications/RoyalTerminal/pull/121> | 2026-10-11 |
| luvus | agent 任务台（mission control） | 开发中 | PR open | 已验证 | <https://github.com/RizRiyz/luvus/pull/498> | 2026-10-11 |
| cleat | 会话守护进程 | 开发中 | PR open（ADR） | 已验证 | <https://github.com/flotilla-org/cleat/pull/329> | 2026-10-11 |
| tmux | 多路复用器 | 未支持 | —（实测 3.5a：裸序列丢弃；DCS passthrough + `allow-passthrough on` 可透传；issue open，最后更新 2026-10-10 01:51） | 已验证（issue + 本仓库实测） | <https://github.com/tmux/tmux/issues/5713> | 2026-10-11 |
| screen | 多路复用器 | 未支持 | —（pi 文档称不转发） | 自述（pi 文档） | <https://github.com/earendil-works/pi/blob/v1.1.0/packages/coding-agent/docs/terminal-setup.md> | 2026-10-11 |
| Kitty | 终端 | 未支持 | —（作者在 issue 中审阅规范，主分支无实现） | 已验证 | <https://github.com/kovidgoyal/kitty/issues/10638> | 2026-10-11 |
| WezTerm | 终端 | 未支持 | —（主分支 commit 与 issue 搜索均无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| Alacritty | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| Windows Terminal | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| zellij | 多路复用器 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| iTerm2 | 终端 | 未支持 | —（代码与 issue 搜索均无；已有 OSC 21337） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| xterm.js（VS Code 终端） | 嵌入式终端组件 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| Zed | 编辑器（终端面板） | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| Warp | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| Wave | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| Rio | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| Contour | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |
| foot | 终端 | 未确认 | —（issue 搜索无结果，代码未查） | Codeberg issue 搜索无结果，代码未查 | [research 笔记](../research/2026-10-09.md) | 2026-10-11 |

## 表 2 · AI agent 与 coding CLI（发送端）

| 名称 | 角色 | 状态 | 版本 | 证据类型 | 来源链接 | 核实日期 |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Code | AI coding agent | 已发布 | v2.1.295（2026-10-09 03:48） | 已验证 | <https://github.com/anthropics/claude-code/releases/tag/v2.1.295> | 2026-10-11 |
| pi（earendil-works/pi） | AI coding agent | 已发布 | v1.1.0（2026-10-08 06:26） | 已验证 | <https://github.com/earendil-works/pi/releases/tag/v1.1.0> | 2026-10-11 |
| omp（can1357/oh-my-pi） | AI coding agent | 已发布 | v18.8.7（2026-10-09 21:45，实现 commit fd84fae，7501 首发）；v18.9.0（2026-10-11 16:08）release notes 未提 7501；PR #15113 open | 已验证 | <https://github.com/can1357/oh-my-pi/releases/tag/v18.8.7> · <https://github.com/can1357/oh-my-pi/releases/tag/v18.9.0> | 2026-10-11 |
| Factory Droid | AI coding agent | 已发布（推断：changelog 未写 OSC 7501 字样） | CLI v0.236.0 · Desktop v0.193.0（2026-10-08） | 推断 | <https://docs.factory.com/changelog/release-notes> | 2026-10-11 |
| Docker Agent（docker/docker-agent） | AI agent | 已发布 | v1.150.0（2026-10-09 19:39；PR #4544 合并 2026-10-07 22:51） | 已验证 | <https://github.com/docker/docker-agent/releases/tag/v1.150.0> | 2026-10-11 |
| Crush（charmbracelet/crush） | AI coding agent | 已发布 | v0.98.0（2026-10-09 02:26） | 已验证 | <https://github.com/charmbracelet/crush/pull/4041> · <https://github.com/charmbracelet/crush/releases/tag/v0.98.0> | 2026-10-11 |
| KnightCode | AI coding agent | 已发布 | @knightcodeai/cli@0.15.0（2026-10-08 08:27） | 已验证 | <https://github.com/KnightCodeAI/knightcode/pull/296> · <https://github.com/KnightCodeAI/knightcode/releases/tag/%40knightcodeai%2Fcli%400.15.0> | 2026-10-11 |
| atomic（bastani-inc/atomic） | coding agent runtime | 已发布 | 0.9.33（2026-10-11 06:51；#3558 为修复 PR，首个实现 PR 未核实） | 已验证 | <https://github.com/bastani-inc/atomic/pull/3558> | 2026-10-11 |
| agent（lydakis/agent） | 多 agent 守护进程 CLI | 已发布 | v0.2.0（2026-10-11 14:11） | 已验证 | <https://github.com/lydakis/agent/pull/85> | 2026-10-11 |
| fx（vercel-labs/fx） | coding agent | 已合并未发版 | PR #1181（合并 2026-10-08 00:14） | 已验证 | <https://github.com/vercel-labs/fx/pull/1181> | 2026-10-11 |
| pi-subagents | pi 扩展（层级 id `subagents/<run>`） | 已发布 | v0.77.0（2026-10-10 13:26） | 已验证 | <https://github.com/nicobailon/pi-subagents/pull/2725> · <https://github.com/nicobailon/pi-subagents/releases/tag/v0.77.0> | 2026-10-11 |
| yolop | coding agent（小项目） | 已发布 | v0.20.0（2026-10-10 07:18） | 已验证 | <https://github.com/everruns/yolop/pull/818> · <https://github.com/everruns/yolop/releases/tag/v0.20.0> | 2026-10-11 |
| rho | coding agent（小项目） | 已发布 | rho-sdk-v5.9.0（2026-10-11 05:01；tag 名为 sdk，CLI 是否同包未确认） | 已验证 | <https://github.com/matthewyjiang/rho/pull/1454> · <https://github.com/matthewyjiang/rho/releases/tag/rho-sdk-v5.9.0> | 2026-10-11 |
| jazz | coding agent（小项目） | 已发布 | v0.16.13（2026-10-09 17:37） | 已验证 | <https://github.com/lvndry/jazz/pull/824> · <https://github.com/lvndry/jazz/releases/tag/v0.16.13> | 2026-10-11 |
| wing-agent | coding agent（小项目） | 已合并未发版 | PR #177 | 已验证 | <https://github.com/lpdink/wing-agent/pull/177> | 2026-10-11 |
| shikigami | coding agent（小项目） | 已合并未发版 | PR #438 | 已验证 | <https://github.com/Sannrox/shikigami/pull/438> | 2026-10-11 |
| the-last-harness | coding agent（小项目） | 已合并未发版 | PR #749 | 已验证 | <https://github.com/diegopetrucci/the-last-harness/pull/749> | 2026-10-11 |
| haskell-agent | agent harness（Haskell） | 已合并未发版 | PR #1389（合并 2026-10-11 06:07；无 release） | 已验证 | <https://github.com/digitallyinduced/haskell-agent/pull/1389> | 2026-10-11 |
| cyrup | agent / CLI | 已合并未发版 | PR #221（无 release） | 已验证 | <https://github.com/cyrup-ai/cyrup/pull/221> | 2026-10-11 |
| tincan | Mac 消息 / 通讯录应用（小项目） | 已合并未发版 | PR #1（无 release） | 已验证 | <https://github.com/AarushSah/tincan/pull/1> | 2026-10-11 |
| Armadra Agent | Armadra 画布的 agent 端（发送端） | 已合并未发版 | PR #126 | 已验证 | <https://github.com/AMA-Link/armadra-agent/pull/126> | 2026-10-11 |
| prime-agent | AI agent | 开发中 | PR open | 已验证 | <https://github.com/PrimeIntellect-ai/prime-agent/pull/3424> | 2026-10-11 |
| 8gent-code | AI agent | 已合并未发版 | PR #3738（合并 2026-10-10 07:09；最新 v0.19.0 早于合并） | 已验证 | <https://github.com/8gi-foundation/8gent-code/pull/3738> | 2026-10-11 |
| bub | AI agent | 开发中 | PR open | 已验证 | <https://github.com/bubbuild/bub/pull/345> | 2026-10-11 |
| wovenmatter | AI agent | 已发布 | v0.2.7（2026-10-10 23:57） | 已验证 | <https://github.com/wovenmatter/wovenmatter/pull/111> · <https://github.com/wovenmatter/wovenmatter/releases/tag/v0.2.7> | 2026-10-11 |
| MiniMax Code | AI coding agent | 开发中 | PR #471 open（2026-10-10 00:45 开） | 已验证 | <https://github.com/MiniMax-AI/minimax-code/pull/471> | 2026-10-11 |
| iCode | 离线开发平台 / agent 工具包 | 开发中 | PR #80 open | 已验证 | <https://github.com/openJiuwen-ai/iCode/pull/80> | 2026-10-11 |
| Amp | AI coding agent | 仅宣布（作者自述，无官方 changelog） | 未确认 | 自述（第三方） | <https://x.com/mitchellh/status/2107894687587795079> | 2026-10-11 |
| Codex CLI（openai/codex） | AI coding agent | 已合并未发版 | PR #52725（合并 2026-10-10 07:43；尚未进任何 release：最新预发布 rust-v0.163.0-alpha.5 与最新正式版 rust-v0.162.1 均不含） | 已验证 | <https://github.com/openai/codex/pull/52725> | 2026-10-11 |
| opencode | AI coding agent | 开发中 | PR #54402 open（2026-10-11 06:21 开）；另有 issue #54179（2026-10-10 01:39） | 已验证 | <https://github.com/anomalyco/opencode/pull/54402> · <https://github.com/anomalyco/opencode/issues/54179> | 2026-10-11 |
| Gemini CLI | AI coding agent | 未支持 | —（代码 / PR 搜索无；issue #29710 open，2026-10-10 开） | 已验证 | <https://github.com/google-gemini/gemini-cli/issues/29710> | 2026-10-11 |
| Cursor CLI | AI coding agent | 未确认（闭源） | —（changelog 未见） | 官方 changelog 未见（闭源） | <https://cursor.com/changelog> | 2026-10-11 |

## 表 3 · 非 AI CLI（发送端）

| 名称 | 角色 | 状态 | 版本 | 证据类型 | 来源链接 | 核实日期 |
| --- | --- | --- | --- | --- | --- | --- |
| git-stack | git 工作流 CLI | 已发布 | v0.2.0（2026-10-07 19:25） | 已验证 | <https://github.com/DomBlack/git-stack/pull/16> · <https://github.com/DomBlack/git-stack/releases/tag/v0.2.0> | 2026-10-11 |
| tuist | Xcode 项目工具 | 已合并未发版 | PR #13956（合并 2026-10-08 17:02；含 blocked kind=auth；最新 4.212.0-rc.2 不含） | 已验证 | <https://github.com/tuist/tuist/pull/13956> | 2026-10-11 |
| Hugo | 静态站点生成器 | 已合并未发版 | PR #15428（合并 2026-10-10 01:18；最新 v0.167.0，2026-09-28，早于合并；与 OSC 9;4 并发） | 已验证 | <https://github.com/gohugoio/hugo/pull/15428> | 2026-10-11 |
| Composer | PHP 依赖管理 | 开发中 | PR open（同时支持 OSC 9;4） | 已验证 | <https://github.com/composer/composer/pull/13117> | 2026-10-11 |
| Expo CLI | 开发工具 | 开发中（experiment） | PR open | 已验证 | <https://github.com/expo/expo/pull/51289> | 2026-10-11 |
| bunny.net CLI | CDN CLI | 开发中 | PR open | 已验证 | <https://github.com/BunnyWay/cli/pull/244> | 2026-10-11 |
| firebase-tools | 开发工具 | 已关闭 | —（#11245 / #11246 关闭，计划 fresh implementation 重做） | 已验证 | <https://github.com/firebase/firebase-tools/pull/11245> | 2026-10-11 |
| Terraform / Homebrew | — | 仅宣布（仅作者 PoC，插件或 fork） | — | 自述（博文） | <https://mitchellh.com/writing/program-status-osc7501> | 2026-10-11 |

## 表 4 · TUI 库 / SDK

| 名称 | 角色 | 状态 | 版本 | 证据类型 | 来源链接 | 核实日期 |
| --- | --- | --- | --- | --- | --- | --- |
| Bubble Tea | Go TUI 框架 | 已发布 | v2.1.0（2026-10-09 01:40；PR #1845 open：退出/挂起后陈旧记录修复） | 已验证 | <https://github.com/charmbracelet/bubbletea/releases/tag/v2.1.0> | 2026-10-11 |
| charmbracelet/x（ansi） | Go ANSI 库 | 已合并未发版 | PR #1004（合并 2026-10-09 01:27）；#1005 open（解析器） | 已验证 | <https://github.com/charmbracelet/x/pull/1004> | 2026-10-11 |
| charmbracelet/ultraviolet | Go 终端库 | 已合并未发版 | PR #207；#208 open | 已验证 | <https://github.com/charmbracelet/ultraviolet/pull/207> | 2026-10-11 |
| libvaxis | Zig TUI 库 | 已合并未发版 | main（ctlseqs.zig 含查询序列） | 已验证 | <https://github.com/rockorager/libvaxis/blob/main/src/ctlseqs.zig> | 2026-10-11 |
| tuika | Rust TUI 框架 | 已发布 | v0.13.0（2026-10-08 04:40） | 已验证 | <https://github.com/everruns/tuika/pull/140> · <https://github.com/everruns/tuika/releases/tag/v0.13.0> | 2026-10-11 |
| libghostty-rs | libghostty-vt 的 Rust 绑定 | 已合并未发版 | PR #6（包装回调） | 已验证 | <https://github.com/termio-sh/libghostty-rs/pull/6> | 2026-10-11 |
| xterm.dart | Dart 终端组件 | 已合并未发版 | PR #26（7501 + 9;4 + 133） | 已验证 | <https://github.com/lollipopkit/xterm.dart/pull/26> | 2026-10-11 |
| uncurses | 终端 UI 工具库 | 已发布 | v0.0.6（2026-10-11 03:26） | 已验证 | <https://github.com/aymanbagabas/uncurses/pull/89> | 2026-10-11 |

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
已有上游合并 PR（#52725，尚未进 release），opencode 已有 open PR（#54402）；Amp 仍
仅有作者 Mitchell Hashimoto 的第三方转述（无官方 changelog）；Tern 仍仅有其开发者
@_can1357 的自述（无公开 release）。
