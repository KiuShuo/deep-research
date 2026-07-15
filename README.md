# Deep Research 学习与 Demo 项目

本仓库用于跟随[八章 Deep Research 教程](https://www.wushixiongai.com/projects/deep-research/c/01-why-deep-research)学习，并逐章沉淀可运行的 Demo、实验记录与测试。

## 学习路线

| 章节 | 主题 | 状态 |
| --- | --- | --- |
| 01 | 为什么需要 Deep Research | 待开始 |
| 02 | Agent 执行框架：ReAct → IterResearch | 待开始 |
| 03 | 工具集设计：Search / Visit / Scholar / Python | 待开始 |
| 04 | 多轮对话与长程记忆管理 | 待开始 |
| 05 | 训练数据构造：种子 → 轨迹 → 增强 | 待开始 |
| 06 | 多阶段训练：Agentic CPT → SFT → GRPO | 待开始 |
| 07 | 工程化上线：推理优化、并发与成本 | 待开始 |
| 08 | 评估：研究类任务没标准答案，怎么定义「好」 | 待开始 |

整体主线是：规划 → 多步检索 → 交叉验证 → 综合成带引用的报告。

## 项目结构

```text
.
├── demos/                  # 按章节组织的可运行 Demo
├── docs/                   # 架构、路线图和 ADR
├── src/deep_research/      # 可复用的核心实现
├── tests/                  # 自动化测试
├── AGENTS.md               # AI 开发规范
├── CONTRIBUTING.md         # 分支、提交和 PR 规范
├── .env.example            # 环境变量模板
└── pyproject.toml          # Python 项目与工具配置
```

## 开发规范

- AI 代理开始任务前必须阅读 [`AGENTS.md`](AGENTS.md)。
- 分层与模块边界见 [`docs/architecture.md`](docs/architecture.md)。
- 每章验收标准见 [`docs/roadmap.md`](docs/roadmap.md)。
- 分支、提交和 PR 规则见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。
- 跨模块的重要决策使用 [`docs/adr/`](docs/adr/) 记录。
- Cursor、ZCode 与 Codex 的职责、交接和审查流程见 [`docs/ai-collaboration.md`](docs/ai-collaboration.md)。

## 本地开发

项目使用 Python 3.11+ 和 [uv](https://docs.astral.sh/uv/) 管理依赖。

```bash
cp .env.example .env
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src tests
```

将真实 API Key 仅写入本地 `.env`；该文件已被 Git 忽略。

## 提交约定

- 每章的学习与 Demo 使用独立提交，便于回看演进过程。
- 可复用逻辑放在 `src/deep_research/`，章节入口和实验放在 `demos/`。
- 提交前至少运行测试和静态检查。
