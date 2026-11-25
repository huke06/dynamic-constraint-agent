# 复现与版本边界

## 当前框架

本地使用`D:/experimentn/tau2-official/.venv/Scripts/python.exe`及同一DeepSeek API模型别名。原生工具来自本地τ²-bench checkout。可通过`DCA_TAU2_ROOT`指定其他原生仓库位置，`DEEPSEEK_API_KEY`提供凭据。未设置环境密钥时仅在当前机器兼容既有凭据解析器；仓库不包含该凭据或会话文件。不要将密钥写进配置或提交。

在其他机器，先安装本地τ²-bench及其依赖，并按各冻结runtime.json的SDK版本准备环境。当前目录结构有意保留两个版本；v1原实现/冻结记录不改写，v2是修复后独立源码和实验目录。

```powershell
$env:DCA_TAU2_ROOT = 'D:/experimentn/tau2-official'
# DEEPSEEK_API_KEY 应由本地环境设置，不写入此文件
& 'D:/experimentn/tau2-official/.venv/Scripts/python.exe' tests/test_framework_loop.py -v
& 'D:/experimentn/tau2-official/.venv/Scripts/python.exe' tests/test_framework_loop_v2.py -v
```

两个回归命令在独立进程运行，避免历史compat同名模块共享全局路径。测试不调用API，采用真实模拟RetailTools及固定语义夹具；实际语义模型行为由联调和正式批次另验收。

当前入口`experiments/preliminary/round23-framework-loop/versions/v2/run23.py`。prepare读取本地公开benchmark构造受控配置；freeze必须有离线通过记录且不能覆盖旧冻结；old先跑8条旧题；new必须有OLD_GATE.json通过记录。所有结果目录create-only。再次采样应复制到新的实验版本/批次，不删除已存在目录绕过保护。

正式批次已经结束时，report23.py为事后汇总，读取原始文件不调用模型。完整原始文件在RAW_ARCHIVES清单所指位置，Git只收摘要、评测表、代表轨迹及配置；从Git克隆后若要重建所有旧表，需要恢复对应原始档案。不能因Git没有大日志而声称原始证据不存在，也不能声称仅凭摘要可以重建所有词元或请求。

## 历史01–22轮

归档脚本`tools/archive_preliminary.py`以只读方式从`DCA_HISTORICAL_ROOT`（默认D:/experimentn/Codex工作区/实验）复制可复现材料。每轮保留原始相对结构、源码中的绝对路径和冻结清单原字节。历史脚本应在原路径依赖得到恢复时重放；并未承诺在新的archive目录中直接运行所有早期版本。源档案、已复制文件SHA256、未入Git的大文件/敏感候选及原始日志体积分别登记。

本轮官方Agent端到端受控对照不在采样范围，第21轮的定位与证据保持单列。别名相同不代表服务提供了可核验、不可变的后端权重版本；实际返回model字段、响应ID和SDK版本才是已记录事实。请求失败用量未知时不补零。费用不能由总输入降幅直接推出，须看命中/未命中字段和实际计费规则。
