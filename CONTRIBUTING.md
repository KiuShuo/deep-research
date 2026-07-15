# 贡献指南

## 开发环境

```bash
uv sync --locked
uv run pytest
```

默认测试排除需要外部服务的集成测试；显式运行集成测试时使用：

```bash
uv run pytest -m integration
```

复制 `.env.example` 为 `.env` 后再填写本地密钥。任何真实密钥都不得提交。

## 分支与任务范围

- AI 开发分支：`agent/<short-description>`；
- 功能分支：`feat/<short-description>`；
- 修复分支：`fix/<short-description>`；
- 文档分支：`docs/<short-description>`。

一个分支只解决一个章节目标或一个明确问题。若实现改变核心状态、工具协议、存储结构、模型供应商策略或部署边界，应先新增 ADR。

## 提交信息

采用 Conventional Commits：

```text
feat: 添加有限步数的 ReAct 执行循环
fix: 停止重试不可重试的 Visit 错误
docs: 定义第 2 章验收标准
test: 覆盖最大步数终止场景
refactor: 拆分模型供应商适配器
chore: 更新开发工具配置
```

类型前缀保留英文，冒号后的提交描述必须使用中文。分支名、代码标识符、协议字段和第三方专有名词可保留英文。

## Pull Request

PR 应保持小而可审查，并包含：

- 变更内容及原因；
- 对用户或后续章节的影响；
- 执行过的验证命令；
- 安全、成本、兼容性或数据迁移风险；
- 已知限制和后续工作。

PR 标题、正文、Review 结论、问题清单和交接报告必须使用中文。

如果 PR 使用多个 AI 工具协作，还必须记录：

- 主实现者、独立审查者和集成责任人；
- 派发时的验收条件；
- 主实现 commit SHA 和审查所基于的 commit SHA；
- ZCode 提出的有效问题、误报和处理结果；
- 是否在独立分支或 worktree 中完成实现与审查；
- 工具未能直接调度、需要人工交接的环节。

多工具协作不得在同一分支或 working tree 中并行编辑。完整流程见 [`docs/ai-collaboration.md`](docs/ai-collaboration.md)。

## AI 协作语言

- Codex 给 Cursor、ZCode 的任务包、补充指令和修复反馈必须使用中文；
- Cursor、ZCode 的计划、过程更新、实现交接和独立审查报告必须使用中文；
- Git 提交、PR 和 Review 中面向协作者的描述性记录必须使用中文；
- 技术上必须保持原样的代码、命令、路径、模型名、协议字段和错误原文可保留英文，并在必要时补充中文说明。

合并前必须通过 CI。默认使用 Squash Merge，确保 `main` 历史按意图演进。

## Definition of Done

任务只有在以下条件全部满足时才算完成：

1. 需求和验收条件已实现；
2. 单元测试覆盖新增行为；
3. Ruff、Mypy、Pytest 全部通过；
4. 文档与实际行为一致；
5. 无密钥和非必要大文件；
6. 对外部调用设置超时、错误处理和预算边界；
7. 变更可由另一位开发者或 AI 根据说明复现。
