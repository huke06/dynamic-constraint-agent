# 原始A01：全部预选题配对

数值顺序为官方/框架；20个基础订单，预定4题复验另列，不能将重复当独立题。定向修复不替换此表。

|业务/任务/重复|情形|正确终态|事实/理由审阅|事件实际触发|同质量可比|Agent请求|输入|输出|缓存命中/未命中|耗时秒（端到端）|
|---|---|---|---|---|---|---|---|---|---|---|
|return/A_R_14_r1|stable|True / True|supported / supported|False / False|True|2 / 1|10908 / 823|298 / 79|9856/1052 / 0/823|10.68 / 2.94|
|return/A_R_28_r1|stable|True / True|supported / supported|False / False|True|2 / 1|10880 / 832|278 / 79|9856/1024 / 0/832|6.18 / 3.75|
|return/A_R_30_r1|evidence|False / True|simulator_bias / supported|False / False|False|8 / 2|48480 / 3270|2166 / 155|46592/1888 / 1536/1734|31.11 / 4.79|
|return/A_R_31_r1|evidence|False / True|simulator_bias / supported|False / False|False|20 / 2|178924 / 3362|7446 / 158|174720/4204 / 1536/1826|97.71 / 4.69|
|return/A_R_54_r1|scope|True / True|supported / supported|True / True|True|3 / 2|17474 / 2082|557 / 255|16000/1474 / 384/1698|9.3 / 6.35|
|return/A_R_54_r2|scope|True / True|supported / supported|True / True|True|3 / 2|17702 / 2082|720 / 240|17152/550 / 1664/418|11.25 / 9.3|
|return/A_R_73_r1|scope|True / True|supported / supported|True / True|True|3 / 2|17800 / 2174|761 / 252|16384/1416 / 384/1790|11.67 / 7.78|
|return/A_R_51_r1|conflict|False / True|simulator_bias / pending|False / False|False|20 / 5|182968 / 8679|6897 / 618|178304/4664 / 3200/5479|87.94 / 10.86|
|return/A_R_55_r1|conflict|False / True|simulator_bias / supported|False / False|False|20 / 5|184574 / 8505|7054 / 569|179968/4606 / 3200/5305|82.96 / 11.97|
|return/A_R_82_r1|withdraw|True / True|supported / pending|True / True|False|2 / 2|11401 / 4441|337 / 191|10112/1289 / 1536/2905|5.75 / 4.71|
|return/A_R_89_r1|withdraw|True / True|supported / pending|True / True|False|2 / 2|11176 / 4267|322 / 189|9984/1192 / 1536/2731|7.0 / 5.13|
|return/A_R_RDB01_r1|payment|True / False|supported / program_or_semantic_failure|True / True|False|3 / 2|17260 / 4222|627 / 259|16000/1260 / 1792/2430|11.13 / 4.95|
|return/A_R_RDB01_r2|payment|True / False|supported / program_or_semantic_failure|True / True|False|3 / 2|17188 / 4222|583 / 291|16640/548 / 3840/382|8.55 / 4.9|
|return/A_R_RDB02_r1|payment|True / False|supported / program_or_semantic_failure|True / True|False|3 / 2|17264 / 4188|704 / 261|15872/1392 / 1536/2652|9.94 / 4.55|
|exchange/A_E_EDB01_r1|stable|True / True|supported / supported|False / False|True|2 / 1|14656 / 793|562 / 80|11904/2752 / 128/665|7.33 / 3.92|
|exchange/A_E_EDB02_r1|stable|True / True|supported / supported|False / False|True|3 / 1|21885 / 790|586 / 81|18816/3069 / 128/662|10.97 / 4.49|
|exchange/A_E_EDB03_r1|evidence|True / True|supported / supported|False / False|True|4 / 3|26290 / 6996|701 / 278|23808/2482 / 3456/3540|12.37 / 8.05|
|exchange/A_E_EDB04_r1|evidence|True / True|supported / supported|False / False|True|4 / 2|27928 / 3804|800 / 183|24832/3096 / 1792/2012|10.67 / 5.67|
|exchange/A_E_EDB05_r1|resource|False / True|simulator_bias / supported|True / True|False|2 / 4|15758 / 7883|653 / 457|12160/3598 / 2048/5835|8.79 / 13.84|
|exchange/A_E_EDB05_r2|resource|False / True|simulator_bias / supported|True / True|False|2 / 4|15761 / 7883|650 / 454|14720/1041 / 7168/715|9.54 / 14.89|
|exchange/A_E_EDB06_r1|resource|True / True|simulator_bias / supported|True / True|False|7 / 4|54270 / 6259|1190 / 432|50432/3838 / 2048/4211|25.15 / 15.53|
|exchange/A_E_EDB07_r1|requirement|True / True|supported / supported|True / True|True|6 / 2|47594 / 2511|1044 / 264|43392/4202 / 256/2255|17.28 / 9.18|
|exchange/A_E_EDB08_r1|conflict|True / True|contradicted / supported|False / False|False|5 / 5|40227 / 12151|1781 / 913|36992/3235 / 3584/8567|49.3 / 14.86|
|exchange/A_E_EDB08_r2|conflict|True / True|supported / supported|False / False|True|4 / 3|30562 / 5882|1236 / 348|29824/738 / 5376/506|17.84 / 9.75|
