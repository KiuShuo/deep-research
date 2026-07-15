# 第 1 章 Demo：Mini ReAct Agent

对应教程：[为什么需要 Deep Research](https://www.wushixiongai.com/projects/deep-research/c/01-why-deep-research)。

本 Demo 用**脚本化模型**和**内存 stub Search**展示最小 ReAct 循环：模型提出 `search` / `final` 动作，程序执行工具并把观察回填上下文，直到给出答案或触达步数上限。

## 与教程的对应关系

| 教程概念 | 本仓库实现 |
| --- | --- |
| Think → Act → Observe | `MiniReActAgent.run` 显式循环 |
| Search 工具 | `StubSearch`（无网络） |
| 最大步数预算 | `max_steps` + `TerminationReason.MAX_STEPS` |
| 可观察轨迹 | `AgentResult.steps`（步骤号、动作、查询、观察） |

刻意保留的简化（留给后续章节）：

- 无检查点 / 持久化（第 2 章）
- 无通用 Tool Registry、Visit、Scholar、Python（第 3 章）
- 无真实模型与真实搜索（可选适配器，非本 Demo 前置条件）

## 运行

在仓库根目录：

```bash
uv run python demos/chapter_01/main.py
```

不需要 API Key，也不访问网络。

## 预期输出

- 至少两次 `Action: search(...)` 及对应 `Observation`
- 一次最终答案
- `Termination: completed`

## 限制

- 模型回复是写死的脚本，不会随问题变化
- Search 只命中 Demo 内置 knowledge；未知查询返回稳定 fallback
- 动作解析只接受 `search("...")` / `final("...")`，不执行任意代码

## 下一章方向

第 2 章会把隐式消息列表升级为显式状态机、演进报告和检查点恢复，对照普通 ReAct 与 IterResearch 的上下文规模。
