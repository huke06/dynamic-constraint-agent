# A：同状态首步配对

每格保留原始选择与执行核验，质量含对象、推进和理由；不按动作相同评分。

|题/状态/重复|直接选择→执行|候选选择→执行|严格首步质量|
|---|---|---|---|
|91/unknown/1|query:3801771308 → True|query:3801771308 → True|True / True|
|91/unknown/2|query:3801771308 → True|query:3801771308 → True|True / True|
|91/known/1|prepare:#W3239882 → True|prepare:#W3239882 → True|True / True|
|91/known/2|prepare:#W3239882 → True|prepare:#W3239882 → True|True / True|
|102/full_authorized/1|submit:#W3445693 → True|submit:#W3445693 → True|True / True|
|102/full_authorized/2|submit:#W3445693 → True|submit:#W3445693 → True|True / True|
|102/withdrawn/1|confirm:#W3445693 → True|confirm:#W3445693 → True|True / True|
|102/withdrawn/2|confirm:#W3445693 → True|confirm:#W3445693 → True|True / True|
|93/conflict/1|prepare:#W4073673 → False|prepare:#W4073673 → False|False / False|
|93/conflict/2|prepare:#W4073673 → False|prepare:#W4073673 → False|False / False|
|93/feasible/1|prepare:#W4073673 → True|prepare:#W4073673 → True|True / True|
|93/feasible/2|analyze:2216662955 → False|prepare:#W4073673 → True|False / True|
|98/spec_only/1|confirm:#W3916020 → True|confirm:#W3916020 → True|True / True|
|98/spec_only/2|confirm:#W3916020 → True|confirm:#W3916020 → True|True / True|
|98/full_authorized/1|submit:#W3916020 → True|submit:#W3916020 → True|True / True|
|98/full_authorized/2|submit:#W3916020 → True|submit:#W3916020 → True|True / True|