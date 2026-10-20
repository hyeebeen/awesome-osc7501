# Changelog

本仓库遵循「每次迭代一条」的记录方式；核实方法见
[research/](research/) 笔记。

## 2026-10-21

- **数据迁移**：支持矩阵从 docs/support-matrix.md 的手写表格迁移到
  `data/integrations.yml`（单一事实源，121 个条目），配 JSON Schema
  （`data/schema.json`）与校验器 `scripts/validate.py`（schema、id 唯一、
  url 可达、entry url == 首个 source）；`data/resources.yml` 同构维护
  精选清单（15 条）；JSON 导出 `data/integrations.json` /
  `data/resources.json`。
- **生成器**：`scripts/build.py` 从 yml 确定性生成 support-matrix 四张表
  （带稳定锚点）、JSON 导出与 README 支持概览/单测计数（`--check` 可验
  幂等）；`scripts/check.sh` / Makefile 固化 CI 序列；
  `scripts/migrate_matrix.py` 留存迁移溯源。
- **矩阵全量复核**（方法见 [research/2026-10-21.md](research/2026-10-21.md)）：
  100 → 121 行。kitty master 已实现（id 上限 263 而非规范 128，已合并未
  发版）；tmux #5713 关闭（维持未支持）；Codex rust-v0.163.0、cmux v0.65.1、
  Hugo v0.168.0、ServerBox、zz、cherry、noctty、MonkeySSH、go-term、agentd、
  fx、the-last-harness、8gent-code、Armadra Agent 共 14 行转已发布；
  wintty/cleat/bub/MiniMax Code/iCode/opencode 转已合并未发版；bunny.net CLI
  关闭；Warp 转开发中；tincan 仓库 404 转未确认；新增 goose、OpenClaw、
  OpenTUI、DeepSeek-Reasonix、Orca、Gradle、MSBuild、tqdm、crossterm 等
  21 行。校验器计数：released=51、merged-unreleased=26、in-progress=17、
  closed=6、unsupported=14、announced=3、unconfirmed=3、
  implemented-self-reported=1。
- **时间线/文档**：补 2026-10-13 至 10-20 事件（kitty master、tmux 关闭、
  Codex/Hugo/OpenTUI/Orca 发版、goose/OpenClaw 合并）；deep-dive/why/
  why-integrate/practice 中与新一轮事实相悖的旧表述（kitty issue 仍 open、
  Codex 未发版、tmux 观望等）已更新。
- **agent 友好**：新增 `AGENTS.md`（数据流、字段表、状态/证据枚举、核验
  方法、规则与 AI 贡献政策，README/CONTRIBUTING 均已链接）；`build.py`
  整文件生成 `llms.txt`（无标记，计数/日期/研究笔记链接随数据自动更新，
  `--check` 覆盖）；`.github/ISSUE_TEMPLATE/` 新增 new-integration 与
  status-change 两个 issue 表单（分类/状态下拉与 schema 枚举一致）。

## 2026-10-11

- **规范 rev 0.4**（Revision history 日期 2026-10-10）：删除 terminfo
  （`Pst`）整节；检测回复可带 `states=` / `kinds=` 支持列表（裸 `?`
  永远等于原五个 state、三个 kind）；控制字符拒收补「单行值」理由；
  `app` 定位为标识符（`title` 才是展示名）。全仓库文档同步到 rev 0.4。
- **examples**：解析器与单测覆盖 rev 0.4 回复列表（单测增至 49 个）；
  `detect.sh` 解析 `states=`/`kinds=` 并处理 DA1 竞态；新增
  `fake_terminal.py` 假终端挂具（v04 / bare / da1 / silent 四种回复模式）。
- **docs**：deep-dive / practice 同步 rev 0.4；「规范未说清之处」更新，
  新增 id 长度上限问题（128 < 8×32+7，规范未解释，未修）；why.md 措辞
  匿名化。
- **矩阵**：全部条目于 2026-10-11 重新核实，扩至 100 行；新增 Codex CLI
  （已合并未发版）、opencode（开发中）、Prowl 等一批新集成方。
- **时间线**：增补 2026-10-10 至 2026-10-11 事件——kitty issue #10638
  审阅触发 rev 0.4、Ghostty PR #14630、opencode PR #54402、Prowl 与
  omp v18.9.0 等发布。
- README「30 秒看懂」加入流向图、检测时序图、字节分段 SVG 与状态图
  （中英同步，deep-dive 同步）；新增 docs/why.md（动机、前后对比、
  社区声音、现实意义与前景）；正文与支持概览更新到 rev 0.4 与
  2026-10-11 核实口径。

## 2026-10-09

- **examples**：新增 OSC 7501 示例套件——POSIX sh 函数库（`osc7501.sh`）、
  字节级演示（`bytes-demo.sh`）、命令包装器（`wrap.sh`）、特性检测
  （`detect.sh`）、带完整校验的 Python 增量解析器与 39 个单测
  （`osc7501_parser.py` / `test_osc7501_parser.py`）、tmux 3.5a DCS passthrough
  四象限实验（`tmux-passthrough.sh`）；新增 `examples/RUNLOG.md` 记录真实运行
  输出。
- **docs**：新增文档两层结构——核心（协议）+ 重点（生态与实践）：
  - `README.md`（awesome list + 协议核心摘要 + 精选清单 + 支持概览）
  - `README.en.md`（英文摘要）
  - `docs/deep-dive.md`（协议深度解读：字节格式、设计取舍、实现机制、安全
    边界、时间/空间/变量/反/空）
  - `docs/why-integrate.md`（集成动机分析，按证据组织）
  - `docs/practice.md`（实践指南，引用 RUNLOG 真实输出）
  - `docs/support-matrix.md`（79 个条目的状态/版本/证据矩阵）
  - `docs/timeline.md`（2026-09-28 至 2026-10-09 的时间线）
  - `research/2026-10-09.md`（本轮核实方法、查询记录、五条线索核实、实验）
- **仓库基建**：`CONTRIBUTING.md`（收录标准）、`LICENSE`（CC0-1.0）、
  `.markdownlint-cli2.jsonc`。
- 核实基准：规范 rev 0.3；全部条目核实日期 2026-10-09（CST）。
