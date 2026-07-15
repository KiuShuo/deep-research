# Architecture Decision Records

ADR 用于记录会影响多个章节、多个模块或长期维护方式的重要决策。

需要 ADR 的典型情况：

- 引入或替换 Agent 框架；
- 改变核心状态或工具协议；
- 选择存储、队列、搜索服务或模型供应商；
- 改变训练、部署或评估策略；
- 接受一个短期不能消除的重要技术债。

文件名格式：`NNNN-short-title.md`。状态使用 `Proposed`、`Accepted`、`Superseded` 或 `Rejected`。

模板：

```markdown
# NNNN. 决策标题

- Status: Proposed
- Date: YYYY-MM-DD

## Context

为什么需要决策。

## Decision

选择什么。

## Consequences

正面影响、代价和风险。

## Alternatives

考虑过但未采用的方案。
```
