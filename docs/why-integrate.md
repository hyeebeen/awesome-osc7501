# 为什么集成 OSC 7501（重点）

集成动机分析。每条动机附「谁这么说/这么做」的一手来源链接；推断一律标注
「（推断）」。核实日期 2026-10-09（Asia/Shanghai，CST）。状态与版本细节见
[support-matrix.md](support-matrix.md)。

## 1 不再靠读屏猜状态（被引用最多的理由）

**谁这么说/这么做**：作者[发布推文](https://x.com/mitchellh/status/2107577887159386152)
（250+ 编排器各自用启发式检测 Claude Code 状态；Herdr 3 个月约 10 次兼容改动）；
cherry 的 PR 标题直接写「Take agents' state from OSC 7501 program status, not
their screens」（[#10](https://github.com/patrick91/cherry/pull/10)，开发中）；
claude-fleet [#2597](https://github.com/verkyyi/claude-fleet/pull/2597) 把 7501
设为主来源、hook 次之、屏幕分类器只在缺失时补位，并因此跳过截屏与模型调用；
pi-subagents [#2725](https://github.com/nicobailon/pi-subagents/pull/2725) 理由
相同。

**各方得到了什么**：终端/工作台拿到确定性的状态而不是概率猜测；agent 侧删掉
 了脆弱的读屏管道（成本节省见第 6 节）。

## 2 「需要你」时能被感知（注意力管理）

**谁这么说/这么做**：docker-agent
[#4544](https://github.com/docker/docker-agent/pull/4544)：「a terminal tab or
window manager has no way to surface 'this agent needs your attention' without
the user switching back」；tuist [#13956](https://github.com/tuist/tuist/pull/13956)
的 Why 段：长命令与浏览器登录（kind=auth）在用户切走后仍需要关注；Composer
[#13117](https://github.com/composer/composer/pull/13117)：多终端会话（"aka
AI"）更容易监控。

**各方得到了什么**：用户可以安心切走，终端用标签、通知、声音把「回来一下」
变成可推送的事件；`blocked` 的 `kind`（permission/question/auth）让接收端能区分
「要我批准」还是「挂了」。

## 3 多会话 / 多 agent 管理（inbox、侧栏、移动端）

**谁这么说/这么做**：cmux 按 pane 存记录、侧栏按紧急度
blocked > error > working > done 显示（[文档](https://github.com/manaflow-ai/cmux/blob/main/docs/program-status.md)）；
termio [#713](https://github.com/termio-sh/termio/pull/713)：状态由 daemon 产生，
Mac、手机、`termio sessions` CLI 都能看到；Rex 在会话选择器与未聚焦标签头展示，
计划推送到移动 App 与统一 inbox（[规范页](https://www.superlogical.com/rex/docs/build/program-status)）。

**各方得到了什么**：并行 agent 的「状态聚合面」——十个会话一眼分清谁在等谁在
跑；`done/error` 保留、`working/blocked` 自动清理的语义正好匹配 inbox 的阅读
模型。

## 4 跨 SSH / 容器、零集成成本（协议层动机）

**谁这么说/这么做**：作者[博文](https://mitchellh.com/writing/program-status-osc7501)：
PTY 天然跨 SSH 与容器，带外 socket 需要额外桥接；每个程序对每个 inbox 单独
集成是 O(N)（[发布推文](https://x.com/mitchellh/status/2107577887159386152)原话
"O(N) integration problem"）；cmux 文档称 "works over SSH and inside
containers"。

**各方得到了什么**：程序一次实现、到哪都生效（本地、ssh、容器、多路复用器
——只要最终终端支持）；工作台不需要为每个 agent 维护私有接入层。

## 5 库层一次实现、下游全部获得（网络效应）

**谁这么说/这么做**：Bubble Tea、charmbracelet/x、ultraviolet、tuika、libvaxis、
libghostty-vt/libghostty-rs、SwiftTerm、xterm.dart 等库率先实现（各自的
PR/release notes，见[矩阵](support-matrix.md)）；作者称 Claude Code 的支持
"will help hundreds or thousands of downstream applications"
（[推文](https://x.com/mitchellh/status/2108296550405619967)）。

**各方得到了什么**：用这些库写的程序（如 Crush 之于 Bubble Tea）与用这些组件
拼的终端**免费**获得能力，不需要各自再懂一遍转义序列（推断：网络效应，依据是
库的发布说明与下游 PR 的依赖关系）。

## 6 与 harness 互操作 / 统一来源优先级

**谁这么说/这么做**：claude-fleet #2597 的优先级是 7501 > hook > 分类器，并因
7501 在场而跳过截屏与模型调用（省成本）；cmux 的 open PR
[#18683](https://github.com/manaflow-ai/cmux/pull/18683) 与 issue
[#18397](https://github.com/manaflow-ai/cmux/issues/18397) 把状态再暴露给 hooks
与 socket API；Herdr 的（被关）[#5093](https://github.com/herdrdev/herdr/pull/5093)
想提供 JSON pane snapshot 给只读 dashboard。

**各方得到了什么**：harness/编排器得到一个**分层**的状态来源：协议在场时走协议，
不在场才降级到启发式——既省了读屏成本，又保住了旧环境的兜底。

## 7 实现成本低

**谁这么说/这么做**：作者[博文](https://mitchellh.com/writing/program-status-osc7501)：
每个 PoC 不超过十几行；POSIX sh 一行函数即可发送（本仓库
[examples/osc7501.sh](../examples/osc7501.sh) 即为证据：发送端约百行以内、零依赖）。

**各方得到了什么**：集成决策的门槛被压到「一个下午」量级（推断：从大量小项目
在数日内合并 PR 的节奏得出）。

## 8 生态与早期曝光（推断）

**谁这么说/这么做**：Bubble Tea PR #1841 的 Why 只写了「The new multiplexer
Rex supports it」；多名开发者在 X 上求 Rex beta 邀请以测试 7501
（[例一](https://x.com/c100k_/status/2107951967398216188)、
[例二](https://x.com/aporianist/status/2108298666062803020)）；作者称 Claude
Code "had access to Rex and verified through Rex"。

**（推断）**Rex 的 beta 访问与 Superlogical 的影响力是早期采纳的加速器之一：
想测试就得先进 beta，形成了围绕单一接收端的早期发送端群体。

## 网络效应与协议层动机

把「状态」留在带外，每个发送端要对每个接收端单独对接：N 个程序 × M 个
inbox/终端 = **N×M** 条集成路径，且跨 SSH/容器各自造桥。把状态放进终端字节流
后，发送端只实现一次协议、接收端只实现一次解析：**N+M**。（推断：这一
N×M → N+M 的表述是对博文与发布推文所述 O(N) 集成问题的形式化。）这正是库层
（Bubble Tea、libghostty-vt、SwiftTerm…）抢先把两边各做一次的原因：库是网络
效应的放大器，一次实现乘以下游数量。

## 反对与观望

- **tmux**：维护者 nicm「This seems premature. Let's see if any other terminals
  and programs pick it up.」（[#5713](https://github.com/tmux/tmux/issues/5713)，
  2026-10-13 关闭，无上游提交）；实测裸序列被丢弃。
- **Herdr**：issue 与外部 PR 均因流程被关（bugs-only 政策、非白名单贡献者），
  非技术否决；目前仍依赖启发式 + 专用 socket 集成（[作者博文](https://mitchellh.com/writing/program-status-osc7501)
  所述 Herdr 的做法：检测 manifest 与 socket API）。
- **firebase-tools**：两次实现被关闭、计划重做——「每个调用点手工包裹」不可
  维护，要改成从共享 chokepoint 推导状态。
- **主流终端**（WezTerm、iTerm2、Alacritty、Windows Terminal）尚无公开
  动作；kitty 已在 master 实现（id 上限 263，未发版）；Ghostty 应用本身也未展示
  （库已实现）。
- **竞品**：iTerm2 OSC 21337、Orca OSC 9999 语义重叠；协议竞争未定。

## 对不同角色的建议

全部为（推断），基于上文动机与反对意见：

- **agent / CLI 作者**：先加「检测 + 三个状态」（working/blocked/done）就先覆盖
  最常用的状态；退出前务必发 done/error，取消发 idle；不要用 7501 传富文本。
- **终端作者**：接收端可以晚做，但**查询应答与 DA1 时序**要先做对（先答
  7501）；记录生命周期照规范实现，别发明心跳。
- **多路复用器作者**：per-pane 存储是自然模型（参考 cmux）；同时想清楚要不要
  向外层终端转发内层报告——这是规范空白，率先定义者拿话语权。
- **inbox / 工作台作者**：把 7501 设为第一优先级来源、启发式只做兜底（参考
  claude-fleet 的分层）；`blocked` 的 kind 值得直接映射到通知路由。
