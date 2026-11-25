# 第08轮：同任务配对复验

一次冻结批次，计划16个组合：头盔两次公共语义字段误绑定，8槽位未启动；相机8条续行均正确写入，2条状态话术矛盾、1条目录措辞未决。仅相机第二重复的两个配对可用于质量相当的资源比较。不补采、不训练、不生成偏好标签。

- [上线前方案](PROTOCOL.md) · [结果：观察/原因/所需证据](RESULTS.md) · [开发记录](DEVELOPMENT.md)
- [预算配置](config.json) · [评分](scoring.json) · [原场景](scenarios/)
- [冻结批次](results/20261122T125916414502Z/) · [冻结清单](results/20261122T125916414502Z/freeze.json)
- [原始调用](results/20261122T125916414502Z/model_calls.jsonl) · [逐条表](results/20261122T125916414502Z/TABLES.md) · [逐任务配对表](results/20261122T125916414502Z/PAIRED_RESULTS.md)
- [机器摘要](results/20261122T125916414502Z/summary.json) · [逐字事实审计](results/20261122T125916414502Z/claim_review.json)

使用`D:/experimentn/tau2-official/.venv/Scripts/python.exe`。离线`run.py check`；已执行冻结包禁止再次execute。只读复查：

```powershell
$python = 'D:/experimentn/tau2-official/.venv/Scripts/python.exe'
& $python review08.py results/20261122T125916414502Z
& $python analyze.py results/20261122T125916414502Z
```

01–07和申报书受保护清单前后哈希一致。新修订必须另冻版本，不覆盖本批次。
