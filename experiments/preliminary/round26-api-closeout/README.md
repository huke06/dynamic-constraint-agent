# 第26轮在线API收束

先读[RESULTS](RESULTS.md)。根PROTOCOL为原草案，正式细化/偏离预先记在configs/EXECUTION_PROTOCOL.md；FREEZE.json为正式执行文件与配置的SHA256。旧代码不覆盖，受影响定向修复在versions下分别冻结。

目录：src执行与离线核验；configs题目/模型/提示/规则；results全批原始及独立评分；versions修复原件与定向重跑；samples训练格式和来源验收。原始大日志另见RAW_ARCHIVES.json，原路径保留。

环境：D:/experimentn/tau2-official/.venv/Scripts/python.exe、当地tau2-official原生工具/LLMAgent与既有API环境。凭据不入仓库。正式目录采用create-only，已有批次不会覆盖；重新采样必须独立命名并记录新冻结。

本轮计划76正式全部完成；另冻定向复验30正式，原失败保留。没有模型训练、没有上传原始日志或推送远程仓库。
