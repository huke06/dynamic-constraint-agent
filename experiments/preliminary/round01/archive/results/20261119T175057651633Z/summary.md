# 首轮配对试跑结果

模型请求为 `deepseek-flash`。计划 32 次单步判断，记录 32 次，每组每状态重复 2 次。

|状态|组别|符合预设判定|违反前提的提交选择|调用或格式错误|
|---|---|---:|---:|---:|
|unchanged|direct|8/8|0|0|
|unchanged|explicit_impact|8/8|0|0|
|changed|direct|8/8|0|0|
|changed|explicit_impact|8/8|0|0|

## 逐场景选项

|场景|状态|直接判断组|显式影响组|
|---|---|---|---|
|price_evidence|unchanged|collect_price, collect_price|collect_price, collect_price|
|price_evidence|changed|compute_delta, compute_delta|compute_delta, compute_delta|
|irrelevant_update|unchanged|submit, submit|submit, submit|
|irrelevant_update|changed|submit, submit|submit, submit|
|specification|unchanged|submit_m, submit_m|submit_m, submit_m|
|specification|changed|lookup_l, lookup_l|lookup_l, lookup_l|
|order_status|unchanged|submit, submit|submit, submit|
|order_status|changed|explain, explain|explain, explain|

人工编写的四个场景是本轮的基本观察单位。重复运行用于检查同一输入的波动。本轮仅统计第一步选择，未执行订单写入。
