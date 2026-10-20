# 贡献指南

欢迎贡献！本仓库是 awesome list + 深度解读的混合体，所以收录标准比普通
awesome list 更严。

## 收录标准

1. **一手源**：只收录能回溯到一手源的事实——规范/提案原文、实现源码与 PR、
   作者本人文章与帖子、已集成方的官方 changelog/release。社区转述与二手新闻
   不作为状态依据（可以放进「文章与讨论」，但不用于判定支持状态）。
2. **状态必须附来源与核实日期**：每个支持/计划中/未支持的说法都要有链接与
   「核实日期（Asia/Shanghai，标 CST）」。
3. **版本号只进矩阵与时间线**：`docs/support-matrix.md` 与 `docs/timeline.md`
   是唯一出现版本号与发布日期的地方（research 笔记除外）。README、deep-dive、
   why-integrate、practice 里只写状态类别（已发布 / 已合并未发版 / 开发中 /
   仅宣布 / 已关闭 / 未支持 / 未确认），需要版本号时链接到矩阵。
4. **不收录未核实条目**：查不到就写「未确认」，不要猜；没有官方 release 的
   「即将发布」一律按自述处理并标注。
5. **推断必须标注**：由多条一手源推出的结论标「（推断）」；区分第一方自述与
   第三方转述。
6. **不编造**：不新增未见于来源的版本号、日期、star 数、PR 号。

## 流程

1. 先读 [research/](research/) 里最近一期的笔记与「下一轮待查」清单，从缺口
   续做。
2. 核实新条目时：在 `research/<日期>.md` 记录方法与查询记录（gh 命令、代码
   搜索、原帖链接），再更新矩阵、时间线与 README 概览计数。
3. 示例类贡献必须在真实环境跑过，并把输出追加到 `examples/RUNLOG.md`。
4. 批量复核状态（只读）：`python3 scripts/recheck.py --format md` 用 GitHub
   API 重查 merged-unreleased / in-progress 等状态条目的 PR/issue 与 release，
   输出仅为建议，人工确认后再改 `data/integrations.yml`（`--fail-on-change`
   时有差异退出码 2；CI 每周一自动跑）。
5. 运行 `markdownlint-cli2 "**/*.md"` 保证 0 错误。
6. 在 `CHANGELOG.md` 记一条。

## markdownlint

```sh
markdownlint-cli2 "**/*.md"
```

配置见 `.markdownlint-cli2.jsonc`（仅关闭 MD013 行长、MD033 行内 HTML）。

## 许可

贡献即同意以 [CC0-1.0](LICENSE) 发布。
