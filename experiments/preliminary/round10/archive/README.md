# 第10轮：程序事实核验与续行验证

已完成旧09的16条离线重评分及8条新配对续行。新8条全部正确写入；话术2支持、1矛盾、5待核实，0个完整质量可比新配对。申报书和01–09原件未改，不训练、不生成偏好标签。

阅读顺序：

1. [结果摘要](RESULTS.md)／[方案](PROTOCOL.md)／[新评分规则](FACT_RULES.md)。
2. [旧16条逐条复核](offline_v2/OFFLINE_TABLE.md)，原冻结分在offline_v2/original_09_scores。
3. [冻结清单](FREEZE_MANIFEST.md)，机器哈希results/20261123T001740331845Z/freeze.json。
4. 新批[逐任务配对表](results/20261123T001740331845Z/PAIRED_RESULTS.md)、[逐条质量/事实](results/20261123T001740331845Z/FACT_REVIEW.md)、[工作及开销](results/20261123T001740331845Z/WORK_PROGRESS.md)。
5. [冻结后问题](POST_FREEZE_ISSUES.md)／[开发记录](DEVELOPMENT.md)。

原始数据位于results/20261123T001740331845Z；Agent/用户/原评审请求与原始响应model_calls.jsonl，新外部提取evaluation/model_calls.jsonl。逐话术原抽取、语义补丁、程序值及证据来源都保存。程序来源补审与冻结评分分开，不覆写原judge。

## 脚本与复现

Python使用D:\experimentn\tau2-official\.venv\Scripts\python.exe。运行需沿用本机既有模型配置；不在文档抄录密钥。frozen/run.py禁止重复execute已启动批次。仅重算已有数据可运行：

```powershell
& 'D:\experimentn\tau2-official\.venv\Scripts\python.exe' '.\results\20261123T001740331845Z\frozen\score_facts.py' --batch '.\results\20261123T001740331845Z' --out '.\results\20261123T001740331845Z\evaluation'
& 'D:\experimentn\tau2-official\.venv\Scripts\python.exe' '.\report.py' '.\results\20261123T001740331845Z'
& 'D:\experimentn\tau2-official\.venv\Scripts\python.exe' '.\verify_delivery.py'
```

上述重算无API调用；不要对已存在提取目录再加--extract。若以后修改事实规则/业务代码，需要新目录或另行冻结，不得写回本批。私有模拟偏好只用于用户模拟/结果核验，不能作为起点解析或Agent事实证据。
