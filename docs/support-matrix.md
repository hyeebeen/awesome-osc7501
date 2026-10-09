# 支持矩阵（全部版本动态集中于此）

本页是仓库中**唯一**列出版本号与发布日期的清单之一（另一处是
[timeline.md](timeline.md)）。所有时间均为 Asia/Shanghai（CST）；全表核实日期均为
**2026-10-09**（来源与方法见 [research/2026-10-09.md](../research/2026-10-09.md)）。

## 表 1 · 终端 / 多路复用器 / agent 工作台 / 嵌入库（接收端）

| 名称 | 角色 | 状态 | 版本 | 证据类型 | 来源链接 | 核实日期 |
| --- | --- | --- | --- | --- | --- | --- |
| libghostty-vt | 嵌入式 VT 库（作者本人的参考实现） | 已合并未发版 | main（不在最新 tag v1.3.1 中） | 已验证 | <https://github.com/ghostty-org/ghostty/pull/14560> | 2026-10-09 |
| Ghostty 应用 | 终端 | 未支持 | —（应用侧忽略报告，库已支持） | 已验证 | <https://github.com/ghostty-org/ghostty/blob/main/src/termio/stream_handler.zig> | 2026-10-09 |
| Rex（Superlogical） | agent 工作台（规范发源地） | 已实现（官方文档自述） | 版本未确认（beta 邀请制为推断） | 自述 | <https://www.superlogical.com/rex/docs/build/program-status> | 2026-10-09 |
| Tern（Stencil） | 终端（Stencil 的 Rust 原生 neoterminal，闭源） | 仅宣布 | 0.6.4（自述，未确认） | 自述 | <https://x.com/_can1357/status/2108468517217665065> | 2026-10-09 |
| cmux | agent 多路复用器（基于 Ghostty） | 已合并未发版 | 正式版本未确认 | 已验证 | <https://github.com/manaflow-ai/cmux/pull/18742> · [文档](https://github.com/manaflow-ai/cmux/blob/main/docs/program-status.md) | 2026-10-09 |
| termio | agentic 开发环境 | 已发布 | v0.56.0（2026-10-09 21:31） | 已验证 | <https://github.com/termio-sh/termio/pull/713> · <https://github.com/termio-sh/termio/releases/tag/v0.56.0> | 2026-10-09 |
| SwiftTerm | 终端组件库（macOS/Linux） | 已发布 | v1.99.0（2026-10-09 04:21；后续 PR #748 已合并） | 已验证 | <https://github.com/migueldeicaza/SwiftTerm/releases/tag/v1.99.0> | 2026-10-09 |
| TUIOS | 终端 | 已发布 | v0.9.0（2026-10-08 14:39） | 已验证 | <https://github.com/Gaurav-Gosain/tuios/releases/tag/v0.9.0> | 2026-10-09 |
| Termy | 终端 | 已发布 | v1.0.0-rc.2（2026-10-08 17:01） | 已验证 | <https://github.com/lassejlv/termy/pull/408> · <https://github.com/lassejlv/termy/releases/tag/v1.0.0-rc.2> | 2026-10-09 |
| con-terminal | 终端 | 已发布 | v0.1.0-beta.122（2026-10-09 20:49） | 已验证 | <https://github.com/nowledge-co/con-terminal/pull/451> · <https://github.com/nowledge-co/con-terminal/releases/tag/v0.1.0-beta.122> | 2026-10-09 |
| phux | 多路复用器 | 已发布 | v0.52.0（2026-10-07 14:34） | 已验证 | <https://github.com/no-phux/phux/pull/1050> · <https://github.com/no-phux/phux/releases/tag/v0.52.0> | 2026-10-09 |
| thurm | macOS 终端 | 已发布 | v0.3.0（2026-10-08 04:28） | 已验证 | <https://github.com/nklmilojevic/thurm/pull/68> · <https://github.com/nklmilojevic/thurm/releases/tag/v0.3.0> | 2026-10-09 |
| wietty | 终端 | 已发布 | v0.0.17（2026-10-09 23:04） | 已验证 | <https://github.com/kloostermanw/wietty/pull/68> · <https://github.com/kloostermanw/wietty/releases/tag/v0.0.17> | 2026-10-09 |
| ServerBox（flutter_server_box） | Flutter 终端 / SSH 客户端 | 已合并未发版 | — | 已验证 | <https://github.com/lollipopkit/flutter_server_box/pull/1662> | 2026-10-09 |
| diri | 并行 agent 工作台 | 已合并未发版 | —（PR #732 / #737） | 已验证 | <https://github.com/cristicretu/diri/pull/732> | 2026-10-09 |
| programa | 基于 Ghostty 的 agent 终端 | 已合并未发版 | — | 已验证 | <https://github.com/darkroomengineering/programa/pull/405> | 2026-10-09 |
| agent-os | agent 工作台（小项目） | 已合并未发版 | — | 已验证 | <https://github.com/saadnvd1/agent-os/pull/100> | 2026-10-09 |
| zz | 小项目 | 已合并未发版 | — | 已验证 | <https://github.com/demfabris/zz/pull/10> | 2026-10-09 |
| toastty | 小项目 | 已合并未发版 | — | 已验证 | <https://github.com/figelwump/toastty/pull/105> | 2026-10-09 |
| claude-fleet | agent 工作台（小项目） | 已合并未发版 | — | 已验证 | <https://github.com/verkyyi/claude-fleet/pull/2597> | 2026-10-09 |
| para-code | agent 工作台（小项目） | 已合并未发版 | — | 已验证 | <https://github.com/MocA-Love/para-code/pull/318> | 2026-10-09 |
| attn | agent 会话管理 | 开发中 | PR open | 已验证 | <https://github.com/SolenesInc/attn/pull/613> | 2026-10-09 |
| cherry | agent 状态工具（PR 标题：从 7501 取 agent 状态） | 开发中 | PR open | 已验证 | <https://github.com/patrick91/cherry/pull/10> | 2026-10-09 |
| tmux-agent-panel | tmux 面板 | 开发中 | PR open | 已验证 | <https://github.com/ahmedelgabri/tmux-agent-panel/pull/4> | 2026-10-09 |
| wintty | Windows 上的 Ghostty 移植 | 开发中 | PR open | 已验证 | <https://github.com/deblasis/wintty/pull/1316> | 2026-10-09 |
| tmux | 多路复用器 | 未支持 | —（实测 3.5a：裸序列丢弃；DCS passthrough + `allow-passthrough on` 可透传） | 已验证（issue + 本仓库实测） | <https://github.com/tmux/tmux/issues/5713> | 2026-10-09 |
| screen | 多路复用器 | 未支持 | —（pi 文档称不转发） | 自述（pi 文档） | <https://github.com/earendil-works/pi/blob/v1.1.0/packages/coding-agent/docs/terminal-setup.md> | 2026-10-09 |
| Kitty | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-09 |
| WezTerm | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-09 |
| Alacritty | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-09 |
| Windows Terminal | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-09 |
| zellij | 多路复用器 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-09 |
| iTerm2 | 终端 | 未支持 | —（代码与 issue 搜索均无；已有 OSC 21337） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-09 |
| xterm.js（VS Code 终端） | 嵌入式终端组件 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-09 |
| Zed | 编辑器（终端面板） | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-09 |
| Warp | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-09 |
| Wave | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-09 |
| Rio | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-09 |
| Contour | 终端 | 未支持 | —（主分支代码搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-09 |
| foot | 终端 | 未确认 | —（issue 搜索无结果，代码未查） | Codeberg issue 搜索无结果，代码未查 | [research 笔记](../research/2026-10-09.md) | 2026-10-09 |

## 表 2 · AI agent 与 coding CLI（发送端）

| 名称 | 角色 | 状态 | 版本 | 证据类型 | 来源链接 | 核实日期 |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Code | AI coding agent | 已发布 | v2.1.295（2026-10-09 03:48） | 已验证 | <https://github.com/anthropics/claude-code/releases/tag/v2.1.295> | 2026-10-09 |
| pi（earendil-works/pi） | AI coding agent | 已发布 | v1.1.0（2026-10-08 06:26） | 已验证 | <https://github.com/earendil-works/pi/releases/tag/v1.1.0> | 2026-10-09 |
| omp（can1357/oh-my-pi） | AI coding agent | 已发布 | v18.8.7（2026-10-09 21:45；实现 commit fd84fae） | 已验证 | <https://github.com/can1357/oh-my-pi/releases/tag/v18.8.7> | 2026-10-09 |
| Factory Droid | AI coding agent | 已发布（推断：changelog 未写 OSC 7501 字样） | CLI v0.236.0 · Desktop v0.193.0（2026-10-08） | 推断 | <https://docs.factory.com/changelog/release-notes> | 2026-10-09 |
| Docker Agent（docker/docker-agent） | AI agent | 已发布 | v1.150.0（2026-10-09 19:39；PR #4544 合并 2026-10-07 22:51） | 已验证 | <https://github.com/docker/docker-agent/releases/tag/v1.150.0> | 2026-10-09 |
| Crush（charmbracelet/crush） | AI coding agent | 已发布 | v0.98.0（2026-10-09 02:26） | 已验证 | <https://github.com/charmbracelet/crush/pull/4041> · <https://github.com/charmbracelet/crush/releases/tag/v0.98.0> | 2026-10-09 |
| KnightCode | AI coding agent | 已发布 | @knightcodeai/cli@0.15.0（2026-10-08 08:27） | 已验证 | <https://github.com/KnightCodeAI/knightcode/pull/296> · <https://github.com/KnightCodeAI/knightcode/releases/tag/%40knightcodeai%2Fcli%400.15.0> | 2026-10-09 |
| fx（vercel-labs/fx） | coding agent | 已合并未发版 | PR #1181（合并 2026-10-08 00:14） | 已验证 | <https://github.com/vercel-labs/fx/pull/1181> | 2026-10-09 |
| pi-subagents | pi 扩展（层级 id `subagents/<run>`） | 已合并未发版 | PR #2725（合并 2026-10-07 08:53） | 已验证 | <https://github.com/nicobailon/pi-subagents/pull/2725> | 2026-10-09 |
| yolop | coding agent（小项目） | 已合并未发版 | PR #818 | 已验证 | <https://github.com/everruns/yolop/pull/818> | 2026-10-09 |
| rho | coding agent（小项目） | 已合并未发版 | PR #1454 | 已验证 | <https://github.com/matthewyjiang/rho/pull/1454> | 2026-10-09 |
| jazz | coding agent（小项目） | 已合并未发版 | PR #824 | 已验证 | <https://github.com/lvndry/jazz/pull/824> | 2026-10-09 |
| wing-agent | coding agent（小项目） | 已合并未发版 | PR #177 | 已验证 | <https://github.com/lpdink/wing-agent/pull/177> | 2026-10-09 |
| shikigami | coding agent（小项目） | 已合并未发版 | PR #438 | 已验证 | <https://github.com/Sannrox/shikigami/pull/438> | 2026-10-09 |
| the-last-harness | coding agent（小项目） | 已合并未发版 | PR #749 | 已验证 | <https://github.com/diegopetrucci/the-last-harness/pull/749> | 2026-10-09 |
| prime-agent | AI agent | 开发中 | PR open | 已验证 | <https://github.com/PrimeIntellect-ai/prime-agent/pull/3424> | 2026-10-09 |
| 8gent-code | AI agent | 开发中 | PR open | 已验证 | <https://github.com/8gi-foundation/8gent-code/pull/3738> | 2026-10-09 |
| bub | AI agent | 开发中 | PR open | 已验证 | <https://github.com/bubbuild/bub/pull/345> | 2026-10-09 |
| wovenmatter | AI agent | 开发中 | PR open | 已验证 | <https://github.com/wovenmatter/wovenmatter/pull/111> | 2026-10-09 |
| Amp | AI coding agent | 仅宣布（作者自述，无官方 changelog） | 未确认 | 自述（第三方） | <https://x.com/mitchellh/status/2107894687587795079> | 2026-10-09 |
| Codex CLI（openai/codex） | AI coding agent | 仅宣布（作者称有 in-progress PR，上游未找到） | — | 自述（第三方） | <https://x.com/mitchellh/status/2107894687587795079> · [第三方 fork PR](https://github.com/JJLiebig/codex/pull/230) | 2026-10-09 |
| opencode | AI coding agent | 仅宣布（作者自述，未找到 PR） | — | 自述（第三方） | <https://x.com/mitchellh/status/2107894687587795079> | 2026-10-09 |
| Gemini CLI | AI coding agent | 未支持 | —（代码 / PR 搜索无） | 已验证 | [research 笔记](../research/2026-10-09.md) | 2026-10-09 |
| Cursor CLI | AI coding agent | 未确认（闭源） | —（changelog 未见） | 官方 changelog 未见（闭源） | <https://cursor.com/changelog> | 2026-10-09 |

## 表 3 · 非 AI CLI（发送端）

| 名称 | 角色 | 状态 | 版本 | 证据类型 | 来源链接 | 核实日期 |
| --- | --- | --- | --- | --- | --- | --- |
| git-stack | git 工作流 CLI | 已发布 | v0.2.0（2026-10-07 19:25） | 已验证 | <https://github.com/DomBlack/git-stack/pull/16> · <https://github.com/DomBlack/git-stack/releases/tag/v0.2.0> | 2026-10-09 |
| tuist | Xcode 项目工具 | 已合并未发版 | PR #13956（合并 2026-10-08 17:02；含 blocked kind=auth） | 已验证 | <https://github.com/tuist/tuist/pull/13956> | 2026-10-09 |
| Hugo | 静态站点生成器 | 开发中 | PR open（与 OSC 9;4 并发） | 已验证 | <https://github.com/gohugoio/hugo/pull/15428> | 2026-10-09 |
| Composer | PHP 依赖管理 | 开发中 | PR open（同时支持 OSC 9;4） | 已验证 | <https://github.com/composer/composer/pull/13117> | 2026-10-09 |
| Expo CLI | 开发工具 | 开发中（experiment） | PR open | 已验证 | <https://github.com/expo/expo/pull/51289> | 2026-10-09 |
| bunny.net CLI | CDN CLI | 开发中 | PR open | 已验证 | <https://github.com/BunnyWay/cli/pull/244> | 2026-10-09 |
| firebase-tools | 开发工具 | 已关闭 | —（#11245 / #11246 关闭，计划 fresh implementation 重做） | 已验证 | <https://github.com/firebase/firebase-tools/pull/11245> | 2026-10-09 |
| Terraform / Homebrew | — | 仅宣布（仅作者 PoC，插件或 fork） | — | 自述（博文） | <https://mitchellh.com/writing/program-status-osc7501> | 2026-10-09 |

## 表 4 · TUI 库 / SDK

| 名称 | 角色 | 状态 | 版本 | 证据类型 | 来源链接 | 核实日期 |
| --- | --- | --- | --- | --- | --- | --- |
| Bubble Tea | Go TUI 框架 | 已发布 | v2.1.0（2026-10-09 01:40；PR #1845 open：退出/挂起后陈旧记录修复） | 已验证 | <https://github.com/charmbracelet/bubbletea/releases/tag/v2.1.0> | 2026-10-09 |
| charmbracelet/x（ansi） | Go ANSI 库 | 已合并未发版 | PR #1004（合并 2026-10-09 01:27）；#1005 open（解析器） | 已验证 | <https://github.com/charmbracelet/x/pull/1004> | 2026-10-09 |
| charmbracelet/ultraviolet | Go 终端库 | 已合并未发版 | PR #207；#208 open | 已验证 | <https://github.com/charmbracelet/ultraviolet/pull/207> | 2026-10-09 |
| libvaxis | Zig TUI 库 | 已合并未发版 | main（ctlseqs.zig 含查询序列） | 已验证 | <https://github.com/rockorager/libvaxis/blob/main/src/ctlseqs.zig> | 2026-10-09 |
| tuika | Rust TUI 框架 | 已发布 | v0.13.0（2026-10-08 04:40） | 已验证 | <https://github.com/everruns/tuika/pull/140> · <https://github.com/everruns/tuika/releases/tag/v0.13.0> | 2026-10-09 |
| libghostty-rs | libghostty-vt 的 Rust 绑定 | 已合并未发版 | PR #6（包装回调） | 已验证 | <https://github.com/termio-sh/libghostty-rs/pull/6> | 2026-10-09 |
| xterm.dart | Dart 终端组件 | 已合并未发版 | PR #26（7501 + 9;4 + 133） | 已验证 | <https://github.com/lollipopkit/xterm.dart/pull/26> | 2026-10-09 |

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

# 仓库的最新 release / tag
gh release list --repo earendil-works/pi --limit 3
gh api repos/anthropics/claude-code/releases/tags/v2.1.295 --jq '.published_at'

# 全站搜索新的集成 PR（最有效的一招；结果要人工过滤同名噪音）
gh api "search/issues?q=7501+in:title+is:pr+created:>2026-09-27&per_page=100" --jq '.items[]|[.state,.repository_url,.number,.title]|@tsv'

# 主分支代码里有没有实现（判断「未支持」）
gh api 'search/code?q=repo:wezterm/wezterm+"7501;"' --jq '.total_count'
gh api 'search/code?q=repo:kovidgoyal/kitty+"7501;"' --jq '.total_count'
```

注意：X / 推文链接用浏览器复核；「自述」类状态要区分第一方自述与第三方转述
（本表中 Amp / Codex / opencode 为作者 Mitchell Hashimoto 的第三方转述；Tern
为其开发者 @_can1357 的自述；均无对应官方发布记录）。
