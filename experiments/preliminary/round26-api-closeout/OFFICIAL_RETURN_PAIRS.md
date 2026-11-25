# return 官方同批配对

数值顺序：官方 / 框架。原始A01成绩不变；“末次定向复验”只是工程定位索引，并非统一修订版的新同批成绩。具体版本见results/A_PAIRS.json。成本结论仅使用RESULTS.md另列的同批、同质量配对。

|基础题/重复/情形|原始正确|末次定向复验正确|末次严格质量|末次Agent调用|输入/输出|命中/未命中|模拟调用|质量可比|
|---|---|---|---|---|---|---|---|---|
|R_14_r1/stable|True / True|True / True|True / True|2 / 1|10908/298 / 823/79|9856/1052 / 0/823|1 / 1|True|
|R_28_r1/stable|True / True|True / True|True / True|2 / 1|10880/278 / 832/79|9856/1024 / 0/832|1 / 1|True|
|R_30_r1/evidence|False / True|True / True|True / True|3 / 2|15390/360 / 3270/156|14972/418 / 2940/330|1 / 1|True|
|R_31_r1/evidence|False / True|True / True|True / True|3 / 2|15624/479 / 3362/157|15104/520 / 3072/290|1 / 1|True|
|R_54_r1/scope|True / True|True / True|True / True|3 / 2|17474/557 / 2082/255|16000/1474 / 384/1698|2 / 2|True|
|R_54_r2/scope|True / True|True / True|True / True|3 / 2|17702/720 / 2082/240|17152/550 / 1664/418|2 / 2|True|
|R_73_r1/scope|True / True|True / True|True / True|3 / 2|17800/761 / 2174/252|16384/1416 / 384/1790|2 / 2|True|
|R_51_r1/conflict|False / True|True / True|True / True|3 / 5|17245/603 / 8682/617|16640/605 / 5760/2922|2 / 2|True|
|R_55_r1/conflict|False / True|False / True|False / False|20 / 5|179693/6477 / 8617/645|175996/3697 / 5248/3369|20 / 3|False|
|R_82_r1/withdraw|True / True|True / True|True / False|2 / 2|11401/337 / 4441/191|10112/1289 / 1536/2905|2 / 1|False|
|R_89_r1/withdraw|True / True|True / True|True / False|2 / 2|11176/322 / 4267/189|9984/1192 / 1536/2731|2 / 1|False|
|R_RDB01_r1/payment|True / False|True / True|True / True|4 / 8|23428/652 / 4971/244|22656/772 / 2688/2283|2 / 2|True|
|R_RDB01_r2/payment|True / False|True / False|True / False|3 / 31|17129/543 / 19438/447|16512/617 / 11904/7534|2 / 2|False|
|R_RDB02_r1/payment|True / False|True / True|True / True|3 / 2|17086/575 / 1176/196|16512/574 / 256/920|2 / 2|True|
