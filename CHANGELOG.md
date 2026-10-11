# Changelog

本仓库遵循「每次迭代一条」的记录方式；核实方法见
[research/](research/) 笔记。

## Unreleased

- README「30 秒看懂」加入流向图、检测时序图、字节分段 SVG 与状态图（中英同步，deep-dive 同步）
- 新增 docs/why.md：动机、前后对比、社区声音（X/HN/GitHub）、现实意义与前景

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
