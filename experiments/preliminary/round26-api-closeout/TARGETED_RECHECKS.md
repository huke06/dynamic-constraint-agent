# 定向修复：逐批保留

均为原失败涉及题目的独立重新采样；不与原A01合并成成功率。修复前后模型采样有波动，不能只挑成功版本替换原分数。

|冻结版本/批次|轨迹|正确|未办结|
|---|---|---|---|
|simfix1/recheck01|4|4||
|simfix2/recheck01|2|2||
|simfix2/recheck_R55|2|1|A_R_55_r1_official:budget_exhausted|
|simfix3/recheck01|4|3|A_E_EDB05_r2_official:None|
|simfix4/recheck01|2|2||
|statefix1/recheck01|6|4|A_R_RDB01_r1_framework:loop_limit, A_R_RDB02_r1_framework:loop_limit|
|statefix2/recheck01|2|1|A_R_RDB01_r1_framework:loop_limit|
|statefix2/recheck_RDB02|2|2||
|statefix3/recheck01|6|5|A_R_RDB01_r2_framework:loop_limit|
