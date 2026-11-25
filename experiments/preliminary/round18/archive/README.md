# 第18轮：动态约束下完整框架对照

4道基础题×稳定/变化×自由/框架×两次=32条正式轨迹。两组最终均16/16正确（各14次登记、2次正确停止）；完整质量自由14/16、框架15/16。无最终成功率差异；中间错误与投入单列。探索4条不计入主实验。

- results/RESULTS.md：主结论与局限；PAIRED_RESULTS.md：16组配对；BY_TASK.md/JSON、BY_CHANGE_TYPE.json：按基础题与类型。
- results/TRACE_TASK27.md、TRACE_TASK27_REPEAT2.md：两次登山靴完整对照；TRACE_TASK6/75.md：相近路线。
- configs/PROTOCOL.md、budget/prompts/tasks、offline/additional_offline、freeze.json：方案、原题/改编、离线、冻结。
- src/construct18/world18/run18/score18：冻结构造、依赖状态、共享执行、运行、程序评分；复用exchange_core/logging16/fact_verifier资源。score18使用同一最新观察/Decimal逻辑，语言审阅与模板事实另列。
- results/main：32条start/trajectory/final/event快照、原始model_calls和request_events；用户与真正工具结果均在history。原始文件不改。
- results/exploratory、EXPLORATORY.md/JSON：同状态分支、提示及续行；BRANCH_REPRODUCIBILITY.json：逐字起点校验。
- SEMANTIC_ITEMS/REVIEW_PACKET/MAPPING、SUMMARY、ACCOUNTING、MODEL_VERSIONS、AUDIT、ENVIRONMENT、frozen_inputs、DELIVERY_MANIFEST：复核和复现。

运行环境 D:/experimentn/tau2-official/.venv/Scripts/python.exe。setup18→run18 freeze→execute→diagnostic；已运行批次不可再次execute覆盖。离线复算可运行review18→score18→post18 deliver→report18，不产生模型请求。review/post/report是事后分析，不冒称冻结时存在。旧01–17和申报书只读，无训练或偏好标签。
