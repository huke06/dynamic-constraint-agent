# 第24轮导航

两项任务独立留档，保留第23轮v2冻结与全部原记录。

- [总结果](RESULTS.md)、[官方同批配对](OFFICIAL_PAIRS.md)
- A修订版执行/冻结/原始结果：versions/a2；初始A01在results/A01保留，不能和a2合并估计效果。原A01配对另存results/A01_OFFICIAL_PAIRS.md。
- B1：[12条可审阅SFT示例](results/B1/SFT_EXAMPLES.jsonl)、[筛选与缺口](results/B1/README.md)、SCREENING.json与PARTITIONS.json。
- B2：[续行与偏好表](CONTINUATION_PREFERENCES.md)、[DPO候选](results/DPO_CANDIDATES.json)、results/B01保存12条续行原始位置。
- 大批原始文件在原位置及独立归档保留，见RAW_ARCHIVES.json；代表完整轨迹以FULL_TRACE.md结尾。只有messages是当时模型输入；事后评价元数据不能拼入训练输入。

src/run24.py及versions/a2/src/run24a2.py只连接冻结框架与实验环境；post24*.py、finalize24.py为事后评审/归档，不进入Agent。实际小模型训练尚未进行。
