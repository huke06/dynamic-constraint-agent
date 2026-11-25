# 第15轮：库存证据变化与认知决策对照

正式batch02计划8条，6条登记、2条请求异常未取得决策；理由另有2条误读。库存变化使第2次重复中两组首步都改变；不能仅以最终登记判定理由正确。

- [配对表](results/PAIRED_RESULTS.md)、[结果](results/RESULTS.md)、[已知轨迹](results/TRACE_KNOWN.md)、[待核实轨迹](results/TRACE_UNKNOWN.md)。
- configs/PROTOCOL.md、start_known/unknown.json、reference14.json、offline.json、prompts.json、private_responses.json、freeze.json：设计、来源、派生状态与冻结。
- src/evidence15.py重放两起点和未知话术；experiment15.py运行；tests15.py泄露/前提离线验证；grade15.py冻结业务规则。复制的执行/工具资源沿用原相对布局scenarios/snapshots，旧目录只读。
- results/batch02原始messages/响应、用户事件、程序话术、逐轮状态、最终DB、异常及结果；frozen_inputs为冻结副本。
- SUMMARY.json为含理由的最终质量；BUSINESS_SUMMARY.json保留业务评分；REASON_REVIEW.json含原始理由及证据；MODEL_VERSIONS.json含实际返回与异常；AUDIT.json和LIFECYCLE.json包含完整性及启动/停止。
- batch01是对象映射缺陷开发批，不并入正式比较。grade15_reporting/analyze15/deliver15仅事后报告，不调用业务API、不改冻结执行。

Python D:/experimentn/tau2-official/.venv/Scripts/python.exe。已启动批次不得重复execute。仅离线重算可用grade15_reporting.py，再analyze15.py（后者保留首次BUSINESS_SUMMARY），不生成训练标签。改执行/评分应另冻，不写回本批。
