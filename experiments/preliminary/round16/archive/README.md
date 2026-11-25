# 第16轮：库存查询结果与后续决策独立复验

一批12条全部正确登记；7条完整质量通过，5条理由有误。两组两次均在查到缺货后澄清替代，查到有货后准备原10x方案并独立确认。请求异常0；诊断分类已离线注入验证。

- [配对表](results/PAIRED_RESULTS.md)、[结果说明](results/RESULTS.md)、[查到缺货轨迹](results/TRACE_UNKNOWN_OUT.md)、[查到有货轨迹](results/TRACE_UNKNOWN_IN.md)。
- configs/PROTOCOL.md、offline.json、start_known/unknown.json、prompts.json、private_responses.json、freeze.json：预定规则、快照、提示、回复及冻结。
- src/logging16.py：共享诊断；experiment16.py：12条自主运行和受控当前方案批准；tests16.py：异常分类/库存分支/独立授权离线验证；report16.py：事后评分和理由审阅；deliver16.py：汇总与完整性审计。
- results/batch01：request_events/model_calls（请求开始/完成、诊断、usage）、controlled_events、程序话术；每轨迹start/environment/trajectory/final_state/database。环境独立于公开快照。
- SUMMARY.json、REASONS.json、FACTS.json、MODEL_VERSIONS.json、AUDIT.json保存所有维度；frozen_inputs完整留存原冻结副本。复制业务模块和scenarios/snapshots资源位于src，原目录只读。

Python D:/experimentn/tau2-official/.venv/Scripts/python.exe。不要重复execute已启动批次。仅report16.py和deliver16.py可离线重算，无API调用；改执行/评分应另冻。没有训练或偏好标注。
