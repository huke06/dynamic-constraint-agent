# 第14轮：澄清语义与受控回应验证

正式6条：接受2条正确登记，拒绝2条正确停止且DB不变，含糊2条先追问再登记。三组配对均通过预先冻结的质量标准。各分支单次观察，未训练或生成偏好标签。

- [配对表](results/PAIRED_RESULTS.md)、[完整含糊轨迹](results/AMBIGUOUS_TRACE.md)、[结果说明](results/RESULTS.md)。
- configs/PROTOCOL.md、start.json、start_evidence.json、private_responses.json、prompts.json、offline.json、freeze.json：方案、公共起点来源、私有受控回复、实际提示、离线检查及冻结。
- src/interface14.py：共同中性澄清、来源/许可防护和按实际问题触发的受控用户；experiment14.py运行；tests14.py离线；grade14.py事前冻结分支评分。复制执行/状态模块保留旧相对资源布局（scenarios/snapshots位于src），旧目录只读。
- results/batch01/model_calls.jsonl：所有真实模型决策及语义请求/响应；controlled_events.jsonl：每次问题触发的用户回复；grounded_clarifications.jsonl及program_confirmations.jsonl：程序原话、字段及来源。
- 每轨迹start/trajectory/final_state/database/result，保留完整状态和最终DB；SUMMARY.json为最终分支评分，FACT_CHECKS.json为发言前事实证据核对，MODEL_VERSIONS.json为实际返回版本，AUDIT.json为保护与边界审计。
- 完整冻结输入副本results/batch01/frozen_inputs，原冻结哈希configs/freeze.json。deliver14.py是事后汇总，不冒充预注册。

Python为D:/experimentn/tau2-official/.venv/Scripts/python.exe。禁止重复execute已启动批次；仅离线重算可运行src/grade14.py，再运行src/deliver14.py，均无API调用。修改执行/回复/评分必须另行冻结，不覆写本批。
