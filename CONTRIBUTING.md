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
feat: add bounded ReAct execution loop
fix: stop retrying non-retryable visit errors
docs: define chapter 2 acceptance criteria
test: cover maximum-step termination
refactor: separate model provider adapter
chore: update development tooling
```

## Pull Request

PR 应保持小而可审查，并包含：

- 变更内容及原因；
- 对用户或后续章节的影响；
- 执行过的验证命令；
- 安全、成本、兼容性或数据迁移风险；
- 已知限制和后续工作。

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
