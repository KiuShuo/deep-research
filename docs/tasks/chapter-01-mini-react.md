# 第 1 章任务包：Mini ReAct Agent

## 任务信息

- 任务名称：实现带最大步数限制的 Mini ReAct Agent
- 主实现者：Cursor
- 独立审查者：ZCode（低风险试运行，只读首审）
- 集成责任人：Codex
- 基线：`main` / `7d551bb`
- 实现分支：`agent/chapter-01-mini-react`
- 实现 worktree：`/Users/liushuo/Documents/github/deep-research-worktrees/chapter-01-cursor`

开始前完整阅读：

- `AGENTS.md`
- `README.md`
- `docs/architecture.md`
- `docs/roadmap.md`
- `docs/ai-collaboration.md`
- `docs/adr/0001-learning-first-layered-architecture.md`

## 目标

实现第 1 章可运行、可观察、可单元测试的最小 ReAct 循环。默认 Demo 不依赖网络或 API Key，通过脚本化模型和 stub Search 展示：模型提出搜索动作、程序执行工具、观察回填上下文、模型继续搜索或给出最终答案。

本章只建立最小机制，不提前实现第 2 章状态机/检查点或第 3 章完整工具网关。

## 范围内

1. 在 `src/deep_research/` 中实现可复用的 Mini ReAct 核心；
2. 使用依赖注入或 `Protocol` 隔离模型与 Search，使单元测试不访问网络；
3. 支持显式 `search("query")` 和 `final("answer")` 动作；
4. 记录结构化步骤，至少包含步骤号、模型输出、动作、查询和观察；
5. 使用明确的 `completed` 与 `max_steps` 终止原因；
6. 实现内存 stub Search，对未知查询返回稳定、可解释的 fallback；
7. 提供 `demos/chapter_01/` 入口、章节说明、运行命令、预期输出、限制和下一章演进方向；
8. 默认 Demo 使用确定性的脚本化模型，复制仓库后无需 API Key 即可运行；
9. 如果增加 OpenAI 兼容的真实模型模式，必须是可选适配器，不得成为测试或默认 Demo 的前置条件。

## 范围外

- 真实 Search、Visit、Scholar 或 Python 工具；
- 通用 Tool Registry、重试、缓存和并发；
- 检查点、持久化、长期记忆和任务恢复；
- FastAPI、数据库、Web UI、Docker 和训练流程；
- LangChain、LangGraph 或其他会隐藏 ReAct 循环的大型 Agent 框架；
- 展示或依赖模型的隐藏思维链。Demo 只输出结构化动作、观察、答案和终止原因。

## 行为约定

### 步数语义

- 一次模型响应计为一步；
- `max_steps` 必须为正整数，否则构造或运行时立即拒绝；
- 在第 `max_steps` 步返回 `final(...)` 时应正常完成；
- 在第 `max_steps` 步执行非终止动作后，不得再调用模型，返回 `max_steps`；
- 达到预算时不得伪造最终答案。

### 动作语义

- `search("query")`：调用一次 stub Search，并把结构化观察追加到下一轮模型上下文；
- `final("answer")`：不调用 Search，立即返回 `completed`；
- 空查询、空答案和无法解析的动作必须产生明确、可测试的错误或终止结果，不得静默当成成功；
- 解析器不得执行模型返回的任意 Python、Shell 或动态表达式。

### 可观察结果

运行结果至少暴露：

- 原始问题；
- 已执行步骤；
- 最终答案（没有则为 `None`）；
- 终止原因；
- 使用步数。

Demo 输出至少展示：`Action`、`Observation`、最终答案和终止原因。

## 建议结构

以下结构用于约束依赖边界，文件名可在不改变职责的前提下微调：

```text
src/deep_research/
├── agents/react.py
├── core/models.py
├── llms/                  # 可选真实模型适配器
└── tools/stub_search.py

demos/chapter_01/
├── README.md
└── main.py

tests/unit/
├── test_react_agent.py
└── test_stub_search.py
```

不要为了目录完整性创建没有行为的占位模块。

## 验收条件

1. 默认 Demo 能从仓库根目录运行，至少经历两次 Search 后输出最终答案；
2. 正常路径返回 `completed`，步骤、Search 调用顺序和最终答案可断言；
3. 无限请求 Search 的脚本化模型在准确的步数边界返回 `max_steps`，且没有额外模型或工具调用；
4. 第 `max_steps` 步给出最终答案时仍返回 `completed`；
5. 非法 `max_steps`、空动作参数和未知动作具有确定行为及测试；
6. stub Search 的命中和 fallback 均有测试；
7. 单元测试不读取 `.env`、不访问真实网络、不依赖真实模型；
8. 公共 API 完整类型标注，Ruff、Mypy 和 Pytest 全部通过；
9. 文档说明本章与教程示例的对应关系，以及刻意保留的简化；
10. 没有引入第 2–8 章范围或不必要的新依赖。

## 必须运行的验证

```bash
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run mypy src tests
uv run pytest
uv run python demos/chapter_01/main.py
git diff --check
```

## Cursor 交付格式

完成后不要合并，不要强推，不要改写历史。提交到当前实现分支，并报告：

```text
分支：
commit SHA：
修改文件及目的：
新增/更新测试：
实际验证命令及结果：
已知限制和未验证项：
依赖、配置、数据结构或外部接口变化：
```

## ZCode 首轮审查要求

ZCode 在 Cursor 提交之后开始，只读取本任务包、仓库规范、实现 diff 和测试结果。首轮不得修改文件，重点验证：

- 正常完成、最大步数和最后一步完成的边界；
- 是否出现额外模型或 Search 调用；
- 空参数、未知动作和解析安全；
- 观察是否确实进入下一轮上下文；
- 测试是否断言行为，而不是仅检查程序可以运行；
- Demo 输出和文档是否与实现一致。

每个问题必须给出严重级别、文件位置、复现输入、实际结果、预期结果和证据；证据不足时标记为“待验证”。
