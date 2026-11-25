# 第09轮：固定起点续行复验结果

## 观察到了什么

### 从核对后的共同起点进入3.1.4比较

计划16条，实际16条全部启动并正确写入申请，未启动0、提前停止0、工作异常0、评审缺失0。没有在线初始语义采样、响应重放或失败替补。两任务的8个实际配对完整系统起点哈希均相同。

四个公开快照依据给定对话、规则与已观察工具记录构造，包含state、Agent初始视图、候选工作、预算和可直接恢复的JSON runtime。头盔硬要求是黑色、高通风，优先项为尺寸M；备选L仍未获许可。相机硬要求30MP/CF、10x优先；备选5x也未获许可。两unknown状态保留原指定候选的available=null，底层DB与known一致，没有用私有模拟信息补齐未知观察。

逐字段依据见STARTING_STATES.md、scenarios/public及snapshots/evidence。头盔尺寸归属由新用户ref11、“The size is too small and you want medium ...”的ref0、旧M方案ref9和目录ref8共同支持。不是依评测答案选字段。online只恢复已核对的快照，不重做这项解释。

第08轮两次原始输出、请求、response id和字段差异保存在sources/round08_helmet_state_construction.json：preferred_options.ventilation=medium应为preferred_options.size=M。此错误单列申报书3.1.1状态构建问题；本轮固定起点排除它作为续行比较的干扰，不宣称已经修好或验证了在线状态构建模型。

公开起点构造不读scenarios/private；私有用户规则只进environment_user/外部评审，预期结果只进评分。实际124个Agent请求通过阶段/字段白名单审计，无initial_semantics或受限字段。改变私有偏好/答案不改变公开起点的离线检查通过。用户在真实模拟回复中透露备选许可，才是后续Agent的合法公开依据。完整branch_start含模拟DB/私有规则用于配对审计，它不是模型输入；实际输入以model_calls.jsonl为准。

### 冻结、模型与独立性

批次`results/20261122T132951508463Z`；冻结13:29:51 UTC，开始13:30:14，结束13:33:58（2026-11-22）。离线先核对状态、库存差、可行首步、提交不可用、16格恢复一致及许可/新授权边界后冻结。代码、场景、快照/依据、评分和预算先哈希再调用；执行期间未修改实现。

沿用08模型请求：deepseek-flash、temperature=0、thinking=false、retries=0、timeout=60；每后缀Agent24调用、60000 total tokens、9工作，输出上限不变。172次实际返回均为`deepseek-flash`，fingerprint=`bc19ba97cbe016479903222bb1578db6`，未返回更细权重版本。响应ID全部唯一，与04–08无交集，replayed=0。温度0及相同指纹不意味着固定服务端随机种子。

01–08及当前申报书、官方数据/工具和冻结包的保护哈希前后相同。本轮都是公开基准模拟数据；原始给定前缀是受控情境，不是本轮模型从零办出的完整任务。52沿用原公开action的旧计划，不另外断言它与原自然语言需求逐处一致。

### 写入、用户目标、许可、新授权分别核对

|任务|计划/启动|未启动/提前停止|正确申请写入|目标及硬约束|库存许可及来源|新方案授权及来源|
|---|---:|---:|---:|---:|---:|---:|
|70 头盔|8/8|0/0|8|8|8|8|
|52 相机|8/8|0/0|8|8|8|8|

头盔每条实际写入3358616356→1665571435（L/黑/高通风），退款0.44，原Visa credit_card_7901829，last_four=7312。相机每条5996159312→6384525445（30MP/CF/5x），追加34.07，PayPal paypal_8194385。每轨迹恰好一次官方exchange_delivered_order_items，DB状态均为exchange requested。正确“办结”指申请正确入库，不是换货实物已履约。

四条unknown/clarify续行均先存用户条件规则、保持许可unknown，查询available=true后生效；许可和最终批准引用各自的原话/ref，不用旧许可充当交易授权。16条都重新确认当前方案、金额和支付后才提交。旧整体授权在起点已失效。已有规则可复用，没有因为旧句不是当前回复再次阻断办理。

### 逐条表述质量与原始评分

32条worker话术均对照发言时完整目录/库存、原商品价格、金额/支付与工具结果。冻结原始strict_pass为15/16；补充审计发现5条目录描述矛盾、1条目录措辞未决，并确认1条外部评审误判。不能将15/16直接当作完整表述准确率。原分不覆写，精确原句、ref、response id和事实见claim_review.json/fact_findings.json。

|轨迹|写入/目标/许可/授权|冻结strict|额外证据复核|
|---|---|---|---|
|t70_r1_known_screen|通过|true|未检出所列矛盾|
|t70_r1_known_clarify|通过|true|虚构black/M/low目录选项|
|t70_r1_unknown_clarify|通过|true|未检出所列矛盾|
|t70_r1_unknown_inventory|通过|true|不存在的M/黑/高组合称not in stock，语义未决|
|t70_r2_unknown_inventory|通过|false|库存查询实际true，评审误读null；原分保留|
|t70_r2_unknown_clarify|通过|true|未检出所列矛盾|
|t70_r2_known_clarify|通过|true|未检出所列矛盾|
|t70_r2_known_screen|通过|true|未检出所列矛盾|
|t52_r1_known_screen|通过|true|将目录10x只归于SD，否认已有30MP/CF/10x|
|t52_r1_known_clarify|通过|true|未检出所列矛盾|
|t52_r1_unknown_clarify|通过|true|含无货项的10x排他列举仍漏30MP/CF/10x|
|t52_r1_unknown_inventory|通过|true|声称没有10x组合含30MP/CF|
|t52_r2_unknown_inventory|通过|true|未检出所列矛盾|
|t52_r2_unknown_clarify|通过|true|明确将30MP/CF/10x说成目录不存在|
|t52_r2_known_clarify|通过|true|明确列3892645120存在但无货，未检出矛盾|
|t52_r2_known_screen|通过|true|按有货语境解释，无直接矛盾|

头盔目录black/M只有3264130640（medium ventilation、无货），没有black/M/low。相机3892645120明确存在，规格30MP/CF/10x，但available=false；“没有有货匹配”不能改称“目录没有该规格”。对有上下文限定的available简写不强判全目录断言；头盔not in stock是否会误导为“SKU存在但无货”保持uncertain，不伪造确定错误。

本次未检出支付ID冒充尾号、PayPal冒充银行卡或明确错误业务状态值。工具结果全部exchange requested；多数话术仅要求确认或说提交后不可改，并未明确告知这个具体状态，不能把“无状态矛盾”写成“每条均正确通知状态”。实际写入不抵消目录描述问题。

外部误判单列：t70_r2_unknown_inventory的trajectory第1步、history ref12均是官方查询结果true，派生候选和后续状态也为true；评审却说ref12是null并否认已查询。查证后保留该false原分，不重新调用judge、不在同批次放宽冻结比较门槛。因此其配对仍不作原口径成本排名；这不是办理路径真的缺库存证据。

### 首步之后发生了什么，两次是否一致

两个任务的每个组合在两次重复中都形成相同工作结构：

- known/screen：screen→clarify→prepare→confirm→submit。
- known/clarify：clarify→prepare→confirm→submit；没有prepare后又screen。
- unknown/inventory：inventory→clarify→prepare→confirm→submit。
- unknown/clarify：clarify→inventory→prepare→confirm→submit；条件许可可随查询生效。

这是轨迹结构与实际写入的一致性，不是表述质量一致性。16条都没有同名工作重复，未耗尽预算；prepare仍有候选过滤和Ledger.prepare两次review，confirm仍做一次review。known每条4次review；unknown/inventory每条5次；unknown/clarify中3条为4次、相机r2为5次，均有明细。共同安全复算未被包装成新增信息，也未为制造差别删去。

identity/profile/scope/payment的值、版本、来源在16条均保持；known目录也保持，unknown只刷新缺失商品库存依据。续行语义仍由LLM提取，12条把接受备选同时写入change块，偏好/硬要求的表示不完全一致；固定起点不保证之后每次状态更新都无语义偏移。最终选项是用户明确接受的备选，但对后续再次变化的影响尚未验证。

### 先质量，再比较资源

差值为“库存依据先行”减去“澄清先行”；—为不可比，不是零差。逐任务配对文件PAIRED_RESULTS.md包含全部8对及起点哈希核对。

|任务/状态/重复|能否按冻结口径比较|工作差|review差|Agent调用差|Agent词元差|
|---|---|---:|---:|---:|---:|
|70 known r1|否：目录描述矛盾|—|—|—|—|
|70 known r2|是|+1|0|+1|+5261|
|70 unknown r1|否：目录措辞未决|—|—|—|—|
|70 unknown r2|否：原评审分量失败，误判已单列|—|—|—|—|
|52 known r1|否：目录描述矛盾|—|—|—|—|
|52 known r2|是|+1|0|+1|+3703|
|52 unknown r1|否：两侧目录描述问题|—|—|—|—|
|52 unknown r2|否：一侧目录描述问题|—|—|—|—|

两个合格的known第二重复均看到：先澄清省去单独缓存整理及一次控制器调用，程序review数量不变。头盔5261词元、相机3703词元是当前两次单独配对的局部差值，不是单任务两次都经过同质量验证的收益复现。

unknown首步次序之后仍都进入prepare、confirm、submit，实际写入一致；目录表述或评审问题使本轮没有满足冻结全部质量条件的unknown配对，故不计算其资源差、不判先查或先问优劣。业务结局相同有观察价值，但不能因此忽略对用户说错事实。

### 实际投入分账

下表仅记账，不对不合格配对排资源优劣。每条Agent都在24调用/60000词元/9工作预算内。具体输入/输出及模拟用户、外部评审账见TABLES.md与summary.json。

|任务|轨迹（顺序r1后r2）|Agent调用/总词元|
|---|---|---:|
|70|r1 known screen|8 / 28227|
|70|r1 known clarify|7 / 23668|
|70|r1 unknown clarify|8 / 28788|
|70|r1 unknown inventory|8 / 28080|
|70|r2 unknown inventory|8 / 27939|
|70|r2 unknown clarify|8 / 28343|
|70|r2 known clarify|7 / 23498|
|70|r2 known screen|8 / 28759|
|52|r1 known screen|8 / 27187|
|52|r1 known clarify|7 / 22796|
|52|r1 unknown clarify|8 / 28033|
|52|r1 unknown inventory|8 / 27577|
|52|r2 unknown inventory|8 / 27069|
|52|r2 unknown clarify|8 / 27322|
|52|r2 known clarify|7 / 23539|
|52|r2 known screen|8 / 27242|

|账目|调用|输入|输出|total tokens|
|---|---:|---:|---:|---:|
|续行Agent|124|403350|24717|428067|
|固定起点预处理的在线模型调用|0|0|0|0|
|模拟用户|32|38455|2829|41284|
|外部评审|16|99410|4631|104041|
|全部API（不能称为Agent总开销）|172|541215|32177|573392|

头盔Agent217302，相机210765。输入含供应商缓存词元；无usage缺失。固定前缀的实际prompt片段仍包含在每次输入词元中，不作免费扣除。公开起点程序构造记录约0.260秒墙时、0.219秒本地CPU，人工/作者核对没有可审计成本计量，未编造为0。不能把取消初始采样的本轮总量与08未启动头盔的总量直接作效率提升比较。

正式新工具调用为8次库存查询、16次换货申请写入；缓存整理及内存review另计。首次缓存工作不产生新世界观察，实际查询有新工具依据；跨状态不能当成相同动作。

## 可能原因是什么

1. 固定并核对公开起点，把3.1.1字段归属故障与3.1.4续行价值比较分离，可能解释本轮头盔能稳定启动。它是实验控制改变，不是LLM状态理解能力提升或端到端框架优势。
2. known时worker本来能读完整目录；得到具体许可后直接准备，显式screen不再必要。每项工作之后再调共同控制器的设计，使一次很便宜的程序整理伴随一次额外模型调用；资源差与工作粒度、提示上下文相关，不可全归因业务计算本身。
3. unknown两路径均须库存和许可，顺序改变了何时形成条件规则、何时更新匹配结论。内部复核次数还受LLM把备选接受写成change还是permission影响。现有记录不足以从这些耦合中推出一个首步稳定更优。
4. 目录存在、库存可得、用户许可是不同判断。worker同时看到全目录和只列有货选项的程序摘要，可能把过滤后的摘要误当完整目录；第一步先整理也未保证不会发生这种语言错误。需消融和更多任务才能确定原因。
5. 外部评审可能混淆原始null观察和后来带嵌套official_result的true记录。本轮证据明确显示一次这样的误判，也显示多次目录描述遗漏；因此其布尔值不能独立担任业务事实真值。

## 还缺什么证据

本轮每任务known只剩一次完整质量可比配对，unknown没有满足冻结双门槛的配对；没有同任务、同状态的两次完整质量比较来确认资源方向稳定。需要更多预注册重复，并事先确定模型评审与工具事实冲突时的独立裁决规则，不能事后静默提分或筛掉坏话术。

仍需检查许可接受与硬要求/偏好更新的边界、真实无货/库存再变、用户在最终确认时改变条件、未变第二商品及多单流程等；本轮在线只覆盖两个静态单商品模拟世界。还需独立人工或可审查标注明确“目录不存在”和“当前不可买”的措辞边界。质量稳定前不判断总体收益或适用范围，不生成偏好训练标签。本轮不追加样本、不改冻结实现。

## 交付与完整性

方案PROTOCOL.md；起点说明STARTING_STATES.md；公开快照/Agent视图/runtime与逐项依据在snapshots；08字段问题原始输出在sources。scenarios/public与private明确分开，前者构造起点，后者仅模拟与评测。run.py及snapshots.py负责冻结、恢复和编排；Agent业务模块、提示、规则、工具、预算沿用08。

实际执行副本为批次frozen，freeze.json列全部哈希。原始model_calls、16份start/trajectory/final_state/result及results.json均保留；PAIRED_RESULTS.md、TABLES.md、summary.json为配对/分账；claim_review/fact_findings为补充证据；returned_models及delivery_audit为版本/完整性核对。修改仅限09新目录与冻结后只读分析产物，申报书及01–08保持原样。
