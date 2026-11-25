# 第11轮：框架自主决策与动态多轮验证

已完成10条新轨迹：固定起点8条，动态题2条。固定起点5条正确登记换货申请，动态两条均未办结。所有未办结轨迹、拒绝、原始响应和停止原因保留。未生成偏好标签或训练模型。

- 预定方案、预算及冻结：[configs/PROTOCOL.md](configs/PROTOCOL.md)、configs/config.json、configs/offline.json、configs/fact_selfcheck.json、configs/freeze.json。
- 主要新实现：src/experiment11.py；src其他模块、scenarios及snapshots是第10轮执行器和公开起点的本地副本，保留其原模块相对资源布局。原始事实核验逻辑fact_verifier.py、score_facts.py未改。
- [结果说明](results/RESULTS.md)、[唯一配对表](results/PAIRED_RESULTS.md)、[完整动态失败轨迹](results/DYNAMIC_TRACE.md)。
- 原始数据：results/batch01/model_calls.jsonl、各_start/_trajectory/_final_state/_result.json，动态用户事件_event.json。
- 外部事实抽取、原始响应、程序值及语义标注：results/batch01/evaluation/。程序独立重放发言前官方工具结果，模型只提取说法。
- 机器摘要与审计：results/SUMMARY.json、results/AUDIT.json。申报书及01–10原始文件哈希均保持。

运行Python为D:/experimentn/tau2-official/.venv/Scripts/python.exe。已启动批次禁止再次execute。冻结后新脚本summarize11.py只作类型/实体标注和报告，不调用业务模型。旧目录只读。源文件中的旧轮号注释不代表本轮重新执行那些旧脚本。
