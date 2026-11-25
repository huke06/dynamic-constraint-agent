# 第13轮：条件许可落空后的自主恢复

正式batch02四条：候选组两次登记；直接组一次登记、一次收到用户拒绝后安全停止。首步两次均直接组screen、候选组clarify。四条都误述“尚未接受”为“不接受”，无质量可比配对，不做收益排名。

- [配对表](results/PAIRED_RESULTS.md)、[结果与局限](results/RESULTS.md)、[完整实际轨迹](results/FULL_TRACE.md)。
- configs/PROTOCOL.md、config.json、prompts.json、start.json、start_evidence.json、offline.json、freeze.json：方案、共同起点及其来源、离线断言和冻结。
- src/experiment13.py构造真实模拟工具起点并运行四条；recovery13.py修复本轮澄清完成判定；tests13.py离线覆盖。其余执行/事实核验模块本地复制沿用，资源scenarios/snapshots保留原相对布局，原目录只读。
- results/batch02保存原始model_calls.jsonl、program_confirmations.jsonl、各start/trajectory/final_state/result；evaluation保存原始事实抽取、哈希绑定语义补丁和逐条程序值。
- results/SUMMARY.json含每条许可/拒绝结果、授权、写入、用户表述误差、模拟偏离及分账；CONFIRMATION_CHECKS.json独立核验3个程序确认；AUDIT.json完整性；LIFECYCLE.json开发与正式启动/停止位置。
- results/batch01为已完成的开发诊断批，仅作缺陷记录，不并入正式结果。

Python为D:/experimentn/tau2-official/.venv/Scripts/python.exe。已启动execute禁止重复运行。重算只需src/score_facts.py --batch results/batch02 --out results/batch02/evaluation（不加--extract）；src/analyze13.py report不调用API。勿反复运行annotate追加重复补丁。任何执行修订另冻，不覆写本批。无训练和偏好标签。
