# 第20轮实验导航

本轮已完成离线检查、联调、冻结、第一阶段32条及第二阶段36条正式运行。旧实验和申报书未改。正式批次发现的模拟接口缺陷原样保留，不做替补或训练。

- 方案与预算：configs/PROTOCOL.md、configs/budget.json。
- 任务及原题：configs/tasks.json、configs/stage1、configs/stage2。
- 冻结：configs/freeze_stage1.json、configs/freeze_stage2.json。
- 结果与局限：results/RESULTS.md、results/DEVIATIONS.md。
- 第一阶段逐次配对：results/STAGE1_PAIRED_RESULTS.md。
- 第二阶段逐次配对：results/STAGE2_PAIRED_RESULTS.md。
- 严格可比成本：results/COMPARABLE_COSTS.md。
- 完整动态配对：results/DYNAMIC_PAIR_stage1_t0_r1.md；results/DYNAMIC_PAIR_stage2_t29_r2.md；失败示例results/DYNAMIC_PAIR_stage2_t23_r1.md。
- 原始请求、逐轮状态、工具与数据库：results/stage1、results/stage2。
- 分项核验与归因：results/stage1_scores.json、results/stage2_scores.json、results/fact_review.json、results/FEEDBACK_AUDIT.json。
- 逐条质量分项表：results/QUALITY_COMPONENTS.md。
- 请求及角色用量：results/REQUEST_DIAGNOSTICS.json、results/ACCOUNTING.json。
- 只读/起点/冻结审计：results/AUDIT.json。

运行器位于src/runner20.py、src/official20.py，预冻结共享实现为world20.py、exchange_core.py、transport20.py、prompts20.py；评分与推进规则score20.py。analysis20.py、finalize20.py仅为正式运行后的分析代码，不进入冻结Agent执行实现。用本地tau2-official/.venv/Scripts/python.exe执行finalize20.py可重建分析，不调用模型。正式原始数据有防覆盖保护。
