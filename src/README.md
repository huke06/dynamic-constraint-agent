# 框架版本

- `dynamic_constraint_agent_v2/`：当前第23轮验收版本。
- `dynamic_constraint_agent/`：第23轮v1冻结原实现，因严格事实审核未通过而保留，不作默认验收结论。

两个版本分别维护状态约束与建模、认知决策、任务执行与反馈。compat是与已有RetailTools、Ledger、模型传输对接的边界，不是另一个官方Agent实现。原始官方Agent基线没有被替换成项目helper。
