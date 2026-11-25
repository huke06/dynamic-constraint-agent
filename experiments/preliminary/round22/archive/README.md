# 第22轮材料导航

正式batch01已保存A首步32条、B续行8条，失败不替换。A没有证明候选稳定改善适切性；B发现分析执行契约缺陷，不能产生可靠路径排名。详见结果报告。

- 方案、任务/原题、评分、冻结：configs/PROTOCOL.md、configs/tasks、configs/scoring22.json、configs/FREEZE.json。
- 105排除原因及完整原题：configs/excluded105.json。
- 原始轨迹/状态/请求/用量：results/batch01。
- 汇总：results/RESULTS.md。
- A：results/FIRST_DECISION_PAIRS.md。
- B：results/CONTINUATION_PAIRS.md。
- 完整代表轨迹：results/TRACE_B_t93_conflict_r2_clarify.md；失败轨迹results/TRACE_B_t93_conflict_r1_clarify.md。
- 离线/输入配对/只读审计：results/OFFLINE.json、results/PAIR_AUDIT.json、results/AUDIT.json。
- 理由与事实核验：results/FACT_REVIEW.json、results/batch01/REVIEW_EVIDENCE.json。

experiment22.py为冻结执行器，score22.py为冻结评分；post22.py为事后分析，未进入模型执行。原生工具继承21轮。没有生成偏好标签或训练模型。不得覆盖已存在批次。
