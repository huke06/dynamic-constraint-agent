# 轨迹样本与读取验收

本目录止步数据导出和校验，无模型训练。36条SFT（train24/validation2/test10）；2个DPO候选（train1/test1）。基础题划分在configs/PARTITIONS.json，同题分支/重复不跨划分。

- `sft_train.jsonl`、`sft_validation.jsonl`、`sft_test.jsonl`：messages格式，最后一条为实际模型的下一工作JSON。来源、请求行号、response_id、SHA256与后续判定在SFT_MANIFEST.json。
- `SFT_SCREENING.json`：所有新自主决策的筛选结果与未通过原因；AUTOMATIC_AND_FORCED.json单列程序及强制首步，不能当自主模型示范。
- `dpo_train.jsonl`、`dpo_test.jsonl`（validation为空）：prompt/chosen/rejected格式。DPO_MANIFEST.json保留同起点、实际首步对象、两次支持及划分；dpo_all仅供审阅，不能整个用于训练。
- DPO候选首步由实验预注册，后续由实际API模型续行；不是自主生成的teacher回答。两对只支持这两个具体对象/偏好的比较，不支持工作类型的普遍优劣。
- `VALIDATION_REPORT.json`为独立本地进程实际读取结果。它验证格式/来源/输入边界/划分与已审阅判定，不能替代对开放语义的独立人工盲审。

离线重建：依次运行src/review26.py、post26.py、export26.py、validate26.py。需要RAW_ARCHIVES.json所列原始日志仍在原路径，24轮旧12例的来源也保持可访问；单独克隆仓库没有大批日志，不应冒称可在缺失来源时重算验收。

SFT覆盖query6、analyze4、clarify16、prepare3、confirm4、submit3。其中旧24轮12条，新26轮24条；按需自动步骤不凑成新的自主提交样本。容量优先理由误读、撤回引用不准、未办结/程序修正及未知用量分支均另留诊断，不收相应正示范。
