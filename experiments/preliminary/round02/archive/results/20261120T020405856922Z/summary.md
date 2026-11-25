# 第二轮多轮小试结果

模型 `deepseek-flash`；计划 12 条轨迹，实际 12 条、40 次模型调用。

|状态|组别|变化/参照后下一步正确|逐步合理|业务终态正确|全程合规办结|违规尝试|接口/格式错误|
|---|---|---:|---:|---:|---:|---:|---:|
|unchanged|direct|3/3|9/9|3/3|3/3|0|0|
|unchanged|explicit_impact|3/3|9/9|3/3|3/3|0|0|
|changed|direct|3/3|11/11|3/3|3/3|0|0|
|changed|explicit_impact|3/3|11/11|3/3|3/3|0|0|

|场景|状态|组别|工具顺序|终态|合规办结|
|---|---|---|---|---|---|
|status_after_confirmation|changed|direct|confirm → explain|blocked_explained|True|
|status_after_confirmation|changed|explicit_impact|confirm → explain|blocked_explained|True|
|price_after_quote|changed|direct|quote → quote → confirm → submit|submitted|True|
|price_after_quote|changed|explicit_impact|quote → quote → confirm → submit|submitted|True|
|target_after_lookup|changed|direct|lookup → lookup → quote → confirm → submit|submitted|True|
|target_after_lookup|changed|explicit_impact|lookup → lookup → quote → confirm → submit|submitted|True|
|target_after_lookup|unchanged|direct|lookup → quote → confirm → submit|submitted|True|
|target_after_lookup|unchanged|explicit_impact|lookup → quote → confirm → submit|submitted|True|
|status_after_confirmation|unchanged|explicit_impact|confirm → submit|submitted|True|
|status_after_confirmation|unchanged|direct|confirm → submit|submitted|True|
|price_after_quote|unchanged|explicit_impact|quote → confirm → submit|submitted|True|
|price_after_quote|unchanged|direct|quote → confirm → submit|submitted|True|

业务终态正确检查实际模拟写入、最新方案及明确告知；全程合规办结还要求无违规尝试。
订单阶段阻断场景中，说明不可修改且没有写入属于合规结束，单独标记 blocked_explained。
逐步合理是依据状态前提的预设操作判定，不评价自然语言理由的充分性；提前失败与步数耗尽计办结失败。
三个手工场景不是独立真实业务样本；不进行显著性检验或能力泛化。
