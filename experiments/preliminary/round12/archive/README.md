# 第12轮：程序与模型协同修复及复验

正式batch03共12条，全部正确登记；整条事实5支持/4矛盾/3待核实。仅确认前动态配对两侧质量通过，不以12条登记成功代替全质量通过。

- [结果说明](results/RESULTS.md)、[唯一配对结果表](results/PAIRED_RESULTS.md)、[完整动态轨迹](results/DYNAMIC_TRACE.md)。
- 预定方案及实际提示词：configs/PROTOCOL.md、prompts.json；离线断言configs/offline.json；正式冻结configs/freeze.json。
- 主要实现：src/repairs12.py（三接口）、experiment12.py（两组自主运行）、tests12.py（离线）。执行器/工具/事实核验副本保留旧相对资源布局，scenarios/snapshots在src下，原目录只读。
- 正式原始数据results/batch03：每轨迹start/trajectory/final_state/result，model_calls.jsonl，program_confirmations.jsonl，动态_event.json。
- evaluation中保留原始事实抽取、程序核验、语义补丁和偏好审阅；14次程序确认另见results/CONFIRMATION_FACTS.json。
- results/PROGRAM_CHECKS.json为从记录的执行前状态及冻结契约重建的核验审计；真实运行拒绝反馈直接在轨迹及后续controller提示中，二者标明区别。
- results/SUMMARY.json含逐行路径、质量、开销和唯一可比配对；EVENT_AUDIT.json、AUDIT.json和LIFECYCLE.json含完整性、事件及开发停止位置。
- batch01/02均为开发中止，保存当时冻结文件与调用，不并入正式结果，也不抹掉开销。

Python使用D:/experimentn/tau2-official/.venv/Scripts/python.exe。禁止对已启动批次重复execute。仅重算已有抽取可运行src/score_facts.py --batch results/batch03 --out results/batch03/evaluation，不加--extract；report12.py仅离线汇总。语义标注脚本需原始提取与既有review配合，不反复运行追加重复补丁。修订执行逻辑需要新冻结，不写回本批。
