# 第09轮：固定起点续行复验

从四个经公开证据核对、冻结的JSON起点进入续行；不再在线采初始语义。16条全部启动并正确写入；5条目录描述矛盾、1条措辞未决，另有1条评审误判。按冻结质量口径，两个known/r2配对可比较投入，其余只分账。

- [方案](PROTOCOL.md) · [起点及依据说明](STARTING_STATES.md) · [结果：观察/原因/缺失证据](RESULTS.md)
- [公开起点](snapshots/public/) · [逐项依据](snapshots/evidence/) · [起点清单](snapshots/manifest.json)
- [08头盔状态构建原始问题](sources/round08_helmet_state_construction.json)
- [冻结批次](results/20261122T132951508463Z/) · [冻结清单](results/20261122T132951508463Z/freeze.json)
- [原始调用](results/20261122T132951508463Z/model_calls.jsonl) · [逐任务配对表](results/20261122T132951508463Z/PAIRED_RESULTS.md) · [逐条评分/投入](results/20261122T132951508463Z/TABLES.md)
- [机器摘要](results/20261122T132951508463Z/summary.json) · [事实与输入边界审计](results/20261122T132951508463Z/claim_review.json)

使用现有`D:/experimentn/tau2-official/.venv/Scripts/python.exe`。已有批次禁止再次execute；只读复查：

```powershell
$python = 'D:/experimentn/tau2-official/.venv/Scripts/python.exe'
& $python review.py results/20261122T132951508463Z
& $python analyze.py results/20261122T132951508463Z
```

public快照中的agent_initial_view是模型可见起点；branch_start另含环境DB和私有用户规则供配对复查，不是Agent输入。私有偏好和评测答案不进入Agent请求。申报书及01–08原件未改，无训练/偏好标签。
