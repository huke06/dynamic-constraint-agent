# 面向动态多约束业务办理的 Agent 认知决策方法与应用

围绕原申报书2.1的两个问题，研究动态业务状态如何支持认知决策，以及执行反馈如何支持决策评价和后续学习。当前处于前期探索和三个模块闭环验收，不是已经完成的训练方法或标准基准总分。

- [01–24轮前期探索索引](experiments/preliminary/README.md)
- [第23轮结果与版本边界](experiments/preliminary/round23-framework-loop/RESULTS.md)
- [第24轮官方对照与轨迹验收](experiments/preliminary/round24-official-and-trajectory/RESULTS.md)
- [研究定位](docs/research_basis.md)、[研究计划与日志](docs/research_log.md)
- [复现说明](docs/REPRODUCIBILITY.md)

## 源码与证据

当前验收版本是`src/dynamic_constraint_agent_v2/`；`state_model.py`、`decision.py`、`execution.py`分别对应状态约束与建模、认知决策、任务执行与反馈。`compat/`继承历史原生零售工具/来源跟踪/传输接口。`src/dynamic_constraint_agent/`保留第23轮v1，便于核对冻结来源，不能当作已验收默认版本。

`tests/`保存回归。`experiments/preliminary/round01`至`round22`保存原样复制的代码/配置/摘要与代表证据，每轮ARCHIVE.json标明原始路径和复制hash。大批原始请求、状态及轨迹不直接加入Git，位置与完整性清单在第23轮RAW_ARCHIVES.json及历史ARCHIVE.json。历史目录没有移动或重写；绝对路径依赖保留为历史记录。

模型配置与实际返回信息均随批次记录。凭据只在本地环境使用，未纳入仓库。正式失败、流程偏差、并列与反转保留。只有通过来源、事实、授权、可执行性及重复稳定性审查的记录才列作学习**候选**，目前没有训练或自动发布偏好标签。
