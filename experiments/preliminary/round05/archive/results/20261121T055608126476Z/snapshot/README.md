# 只增加一个库存证据相邻状态

以第四轮完整快照为已知状态锚点。业务目标、规则、实际库存、用户私有偏好、公共策略/工作执行器及预算不变；仅将一个可用 RGB/clicky 替代品的公开 available=true 观察改为未知。规格、价格、其他库存和原确认仍保留。

这是显式的受控观察视图，不声称官方工具当时返回了 null。历史工具返回、程序缓存和判断在构造前一致处理。实际数据库从不改动，调用原官方 get_product_details 后才获得库存事实。

新增状态只运行两个首步：库存查询与询问接受范围，后续共同策略续行。旧已知状态不重新采样；离线验收会用新代码逐条重放旧状态的 22 条模型请求，保证已知状态没有被新查询能力改变。

- `baseline_runner.py`、`baseline_engine.py`、`exchange_core.py`：第四轮冻结源码的原样副本。
- `engine.py`：仅新增未知库存条件、实际官方查询及未知匹配的保持。
- `run.py`：一个观察干预、两分支、旧锚点与相邻状态的成本差比较。
- `checks.py`：泄漏、查询真实性、条件许可、分支隔离与旧状态兼容性自检。
- `protocol.md`：冻结的干预与解释边界。

```powershell
Set-Location 'D:/experimentn/Codex工作区/实验/05_库存证据相邻状态'
$env:PYTHONIOENCODING = 'utf-8'
$python = 'D:/experimentn/tau2-official/.venv/Scripts/python.exe'
& $python run.py --check
& $python run.py
```

Agent、客户模拟和外部评测分列，前缀另列；每分支一次，不预设价值必须反转。不修改第四轮、其他旧实验和申报文件。
