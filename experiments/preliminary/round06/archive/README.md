# 第 06 轮：同状态续行独立复验

已完成 8 条独立续行；见 [结果摘要](RESULTS.md)。申请写入 8/8 正确，但附加审计发现 2 条条件许可提前激活、4 条支付尾号表述错误；不据此生成训练标签。

- [方案](PROTOCOL.md)、[场景配置](scenarios/config.json)、[评分与预算口径](scoring.json)
- [运行脚本](run06.py)、[冻结后分析脚本](analyze06.py)、[开发记录](DEVELOPMENT.md)
- [本批次目录](results/20261122T121121980510Z/)、[冻结清单](results/20261122T121121980510Z/freeze.json)
- [原始模型调用](results/20261122T121121980510Z/model_calls.jsonl)、[机器可读摘要](results/20261122T121121980510Z/summary.json)、[附加证据审计](results/20261122T121121980510Z/posthoc_evidence_review.json)

原始冻结批次禁止再次 execute。复查可运行：

```powershell
$python = 'D:/experimentn/tau2-official/.venv/Scripts/python.exe'
& $python run06.py check
& $python analyze06.py results/20261122T121121980510Z
```

`freeze` 创建新批次，`execute` 必须从该批次 frozen 目录运行；重新运行会发起新模型调用，不属于本轮已有结果。申报书、旧实验均未修改。
