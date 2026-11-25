# exchange 官方同批配对

数值顺序：官方 / 框架。原始A01成绩不变；“末次定向复验”只是工程定位索引，并非统一修订版的新同批成绩。具体版本见results/A_PAIRS.json。成本结论仅使用RESULTS.md另列的同批、同质量配对。

|基础题/重复/情形|原始正确|末次定向复验正确|末次严格质量|末次Agent调用|输入/输出|命中/未命中|模拟调用|质量可比|
|---|---|---|---|---|---|---|---|---|
|E_EDB01_r1/stable|True / True|True / True|True / True|2 / 1|14656/562 / 793/80|11904/2752 / 128/665|1 / 1|True|
|E_EDB02_r1/stable|True / True|True / True|True / True|3 / 1|21885/586 / 790/81|18816/3069 / 128/662|1 / 1|True|
|E_EDB03_r1/evidence|True / True|True / True|True / True|4 / 3|26290/701 / 6996/278|23808/2482 / 3456/3540|1 / 1|True|
|E_EDB04_r1/evidence|True / True|True / True|True / True|4 / 2|27928/800 / 3804/183|24832/3096 / 1792/2012|1 / 1|True|
|E_EDB05_r1/resource|False / True|True / True|True / True|7 / 4|66019/2259 / 7883/469|63488/2531 / 4224/3659|5 / 3|True|
|E_EDB05_r2/resource|False / True|True / True|True / True|12 / 4|120281/3519 / 7883/429|116608/3673 / 2688/5195|8 / 3|True|
|E_EDB06_r1/resource|True / True|True / True|False / True|7 / 4|54270/1190 / 6259/432|50432/3838 / 2048/4211|4 / 3|False|
|E_EDB07_r1/requirement|True / True|True / True|True / True|6 / 2|47594/1044 / 2511/264|43392/4202 / 256/2255|2 / 2|True|
|E_EDB08_r1/conflict|True / True|True / True|False / True|5 / 5|40227/1781 / 12151/913|36992/3235 / 3584/8567|3 / 2|False|
|E_EDB08_r2/conflict|True / True|True / True|True / True|4 / 3|30562/1236 / 5882/348|29824/738 / 5376/506|2 / 2|True|
