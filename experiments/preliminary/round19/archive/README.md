# 第19轮：官方Agent基线与上下文精简

主实验32条：官方与精简框架均14/16正确，原始失败保留。两处同状态各原/精简续行共4条均正确；输入分别降低50.0%、42.4%。不是框架普遍优于官方的证据。

- results/MAIN_PAIRED_RESULTS.md：官方对精简框架；CONTEXT_PAIRED_RESULTS.md：同状态原/精简成本。
- results/RESULTS.md：回答与归因；BY_TASK.json、MAIN_RESOURCE_PAIRS、CONTEXT_PAIRS/CONTEXT_FIELDS：逐项数据。
- configs/PROTOCOL、prompts19、budget、official_integration、tasks、snapshots、offline、freeze：方案及冻结。
- src/run19：官方原消息/工具循环与框架调度；transport19：共同模型/日志；world19：精简及框架执行；user19：实际话术驱动受控用户；score19：冻结独立评分。复制的18轮World/Ledger是框架依赖，绝不用于拦截官方工具。
- results/main：32条原始请求/响应/每轮状态/用户解释/真实DB；context：4条同状态请求；pilot01/02/03：联调及过度精简失败。
- FACTS/FACT_REVIEW/SPEECH_PACKET/AUTO_FACTS、ACCOUNTING、MODEL_VERSIONS、AUDIT、frozen_inputs、DELIVERY_MANIFEST：核验、分账、哈希。
- TRACE_ARITHMETIC_FAILURE、TRACE_OFFICIAL_DYNAMIC、TRACE_RESOURCE_RECOVERY：完整代表轨迹。

唯一运行环境 D:/experimentn/tau2-official/.venv/Scripts/python.exe。已启动批次不要再次execute覆盖。离线复算：post19 packet→review19→score19→post19 tables→report19；均无模型调用。报告/复核/审计脚本为事后分析，未冒称冻结前存在。旧01–18和申报书只读，无偏好标签或训练。
