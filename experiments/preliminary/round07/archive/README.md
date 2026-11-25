# 对照校验与跨任务小试

先复核06，再建立独立修订版，离线校验后冻结运行任务70（头盔）和52（相机）的受控续行。未修改申报书或01–06。

- [设计复核](REVIEW06.md) · [方案](PROTOCOL.md) · [评分维度](scoring.json) · [结果与局限](RESULTS.md)
- [场景目录](scenarios/) · [开发记录](DEVELOPMENT.md)
- [冻结批次](results/20261122T123400300210Z/) · [原始请求响应](results/20261122T123400300210Z/model_calls.jsonl)
- [逐条表格](results/20261122T123400300210Z/TABLES.md) · [机器可读摘要](results/20261122T123400300210Z/summary.json) · [附加证据审计](results/20261122T123400300210Z/posthoc_review.json)

16个计划组合：12后缀启动、10正确写入、2来源校验失败；另4组合初始化未通过。均保留，不替补，不训练。部分模型评审通过的表述在附加审计中发现错误，不能把原strict_pass当作完整金标准。

现有环境：`D:/experimentn/tau2-official/.venv/Scripts/python.exe`。只读分析可重新运行：

```powershell
$python = 'D:/experimentn/tau2-official/.venv/Scripts/python.exe'
& $python analyze.py results/20261122T123400300210Z
& $python posthoc_review.py results/20261122T123400300210Z
```

`run.py check`离线；`run.py freeze`会创建新冻结包，模型调用须执行该包内的`run.py execute`。本批次禁止再次execute或补采。后续修订必须另立版本。
