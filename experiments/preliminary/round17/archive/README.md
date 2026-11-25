# 第17轮：业务前提区分与跨任务复验

一批12条正确登记；9条完整质量通过，2条前提误读，1条退款时点预期待核实。查到缺货后澄清、查到有货后准备原规格方案，两个组两次均复现。

- configs/PROTOCOL.md、offline.json、freeze.json：预定方案、离线校验、冻结清单。
- src/helmet17.py：头盔起点/共享输入/受控交互；experiment17.py：正式运行；tests17.py：离线校验。
- results/RESULTS.md、PAIRED_RESULTS.md、TRACE_UNKNOWN_OUT.md、TRACE_UNKNOWN_IN.md：结果及两条完整续行。
- results/batch01：实际请求/反馈/每轮状态/环境/写入数据库；frozen_inputs包含原冻结副本。
- results/REASONS.json、REASON_REVIEW.json、FACTS.json、ACCOUNTING.json、AUDIT.json：分维度复核与投入；ACTUAL_PROMPTS.json是事后导出的实际提示，原始提示逐次保存在model_calls。

执行环境D:/experimentn/tau2-official/.venv/Scripts/python.exe。不要重复execute已启动批次。report17.py、deliver17.py可离线重算，无模型调用；复核语义判定由review_finalize17.py记录。src继承了一批旧模块，旧命名脚本只是依赖留存，活动入口仅上述17轮文件。旧目录只读，无训练或偏好标签。
