# 起点依据索引（运行后整理，不是新增冻结输入）

冻结定义在src/helmet17.py、src/scenarios/public/task70.json及configs/freeze.json；实际完整起点逐条保存于results/batch01/*_start.json。本索引只帮助复核，不改变快照。

|事项|公开依据|当前处理|
|---|---|---|
|身份|对话ref2身份查询结果|sofia_hernandez_5364保留|
|原支付|ref4用户资料、ref6原订单支付记录|credit_card_7901829，Visa末四位7312|
|订单和可换货状态|ref6订单工具结果|#W3947049，delivered，原商品3358616356|
|目录和价格|ref8商品工具结果；最新ref12模拟观察|原197.33、目标219.88、黑/L替代196.89；规格均存在|
|历史蓝/M方案及授权|ref9完整旧方案、ref10批准|保留历史；新条件ref11明确不是新交易授权，当前授权stale，plan清空|
|当前用户条件|ref11受控改编原句，全文见helmet17.QUOTE|高通风硬要求，蓝/M偏好；9013366374有货才接受；其他规格尚未接受，非明确拒绝|
|当前库存|ref12：known_out为false，两个unknown为null|最新记录覆盖ref8的历史库存；后续实际查询才揭示false或true|
|可用替代|ref12保留1665571435 black/L/high，available=true|在实际询问前没有该规格用户许可|
|授权和支付规则|src/scenarios/official_policy.md Exchange delivered order|同一产品的有货规格；原订单delivered；确认全部换货商品、差额及支付；提交后exchange requested|

ref12是受控模拟结果fixture，不是现实商城实时数据。运行后另用真正的模拟get_product_details逐字段验证known快照；两个unknown的私有DB仅目标available不同，公开快照及同组首次messages完全一致。分支标签、未来回复和评分不进入模型输入。

inventory在继承实现中只在inventory_unknown()为真时生成，对应identity及inventory_query_needed契约。已知状态没有该工作；程序返回work_applicability拒绝，而非从历史兼容性增加提交门禁。这是本实验工作接口范围，不能解释成τ²-bench一般禁止刷新已知库存。直接组不预看完整候选契约，可能因此需要一次反馈；该限制影响对组间首次选择差异的解释。
