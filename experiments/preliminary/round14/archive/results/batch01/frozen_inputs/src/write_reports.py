"""Render reports from saved evidence, never calls models."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent; B=R/'results/20261123T001740331845Z'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,s):p.write_text(s,encoding='utf-8')
S=read(B/'summary.json'); E=read(B/'evaluation/rescored.json'); F=read(B/'freeze.json')
lines=['# 第10轮逐条质量与事实核验','','同一工具事实只使用发言前已观察证据。pending不是已证明错误，也不是通过。原始提取与补丁分开保存。','',
       '|轨迹|正确写入|用户目标|必要约束/许可/最终授权|话术|全质量|','|---|---|---|---|---|---|']
for r in E['rows']:
    lines.append('|'+ '|'.join(map(str,[r['id'],r['R_write'],r['R_goal'],r['necessary_constraints'],r['factual_status'],r['quality_pass']]))+'|')
for r in E['rows']:
    lines+=['','## '+r['id'],'']
    problems=[]
    for u in r['utterances']:
        for c in u['claims']:
            if c['status'] in ('pending','contradicted'):
                problems.append(f"- ref{u['ref']} **{c['status']}**：{c['claim']['quote']}\n  程序值={json.dumps(c.get('expected'),ensure_ascii=False)}；来源={c.get('source_refs')}；{c['reason']}。")
        if u.get('coverage_missing'):problems.append('- 覆盖待核实：'+json.dumps(u['coverage_missing'],ensure_ascii=False))
    lines+=problems or ['已审阅、抽取的事实均获当时证据支持。该结论不等于自然语言穷尽证明。']
    final=read(B/(r['id']+'_final_state.json')); p=final['g']['conditional_permission']; h=final['H']['confirmations'][-1]
    lines+=['',f"条件许可原句（ref{p['source']}）：{p['source_quote']}",f"许可触发：{p['sat']}；库存来源ref{p['inventory_source']}。",
            f"本轮完整方案/最终回复：ref{h['assistant_ref']} / ref{h['user_ref']}。回复原句：{h['source_quote']}",
            f"原judge strict={r['old_strict_pass']}；冻结新裁决={r['arbitration']}。"]
write(B/'FACT_REVIEW.md','\n'.join(lines)+'\n')
lines=['# 工作产物、复核及独立开销','','这里逐条记账，不对未通过相同质量门槛的路径计算资源收益。review是程序复核，不是额外LLM调用；无记录变化也不直接等同无价值重复。','',
       '|轨迹|工作序列|工作数|review/无记录变化|库存查询/写入|Agent调用|Agent输入/输出/合计词元|','|---|---|---:|---|---|---:|---|']
for r in S['rows']:
    final=read(B/(r['id']+'_final_state.json')); start=read(B/(r['id']+'_start.json'))
    reviews=final['P']['review_audit'][len(start['state']['P']['review_audit']):]
    nochange=sum(not x['changed_record_keys'] for x in reviews); a=r['Agent']
    lines.append(f"|{r['id']}|{' → '.join(r['work_sequence'])}|{r['work_steps']}|{len(reviews)} / {nochange}|{r['tools']['inventory_queries']} / {r['tools']['exchange_writes']}|{a['calls']}|{a['prompt_tokens']} / {a['completion_tokens']} / {a['total_tokens']}|")
for r in E['rows']:
    lines+=['','## '+r['id'],'','|步|工作|完成契约|新增产物|程序review|','|---:|---|---|---|---:|']
    for p in r['work_progress']:
        lines.append(f"|{p['step']}|{p['work']}|{p['contract_completed']}|{', '.join(p['new_artifacts'])}|{p['review_calls']}|")
lines+=['','所有路径均保留已核实身份、同商品目录、原订单/原价和原支付依据；不因颜色或存储变更重新查询全部事实。旧方案及其交易授权失效，新许可绑定自己的原句，prepare重算当前报价，confirm取得独立新授权。unknown的许可先登记，取得库存true后才生效；known直接用有效缓存触发。','',
        'screen只整理已有目录及库存证据，无新外部观察；inventory调用官方get_product_details并保存原始结果，同时产生候选摘要。二者不是同一具体工作。known先澄清不再单独screen；unknown两侧都只有一次inventory。prepare、confirm按各自契约复核，保留所有复核及其changed_record_keys，未以任意权重计“工作价值”。']
write(B/'WORK_PROGRESS.md','\n'.join(lines)+'\n')
accounts=['|账户|调用|输入词元|输出词元|合计词元|','|---|---:|---:|---:|---:|']
for k,a in S['accounts'].items():accounts.append(f"|{k}|{a['calls']}|{a['prompt_tokens']}|{a['completion_tokens']}|{a['total_tokens']}|")
report='''# 第10轮结果：程序事实核验与续行验证

## 观察到什么

本轮完成第09轮16条旧轨迹的独立复核，以及8条新续行。对应申报书3.1.4的固定同状态候选续行比较：仅指定不同首步，随后使用共同续行策略。不是3.2框架自主选择首步的效果实验。业务决策、执行、工具和用户模拟实现保持09；评分只在办理后运行。

旧16条实际写入、目标、约束和授权均通过。旧冻结strict为15通过/1未通过；新规则为10条话术获支持、5条有矛盾、1条待核实，全质量10条通过。相对旧strict有6条从通过变为未通过（5矛盾、1待核实），1条从未通过变为通过。旧分逐字节原样归档，不覆盖原件。逐条理由见offline_v2/OFFLINE_TABLE.md，原句、程序值及来源见per_trajectory。

旧相机典型错误：t52_r2_unknown_clarify把30MP/CF/10x说成“不存在”。完整目录含3892645120，available=false；因此“存在但无货”有程序证据，“不存在”与目录冲突。旧头盔t70_r2_unknown_inventory中，ref12的正式查询1665571435.available=true，评审却明确写成null；程序检出该评审断言错误，原话事实支持，纠正新分，不把评审错误算作办理失败。

新8条全部启动并写入正确换货申请，无初始化中止、未启动、提前停止或模型提取失败。头盔4条：原3358616356换1665571435，黑色/L/高通风，条件许可已生效，差额−$0.44，原Visa ending7312（credit_card_7901829）。相机4条：原5996159312换6384525445，30MP/CF/5x，明确获准降低首选变焦，差额+$34.07，原PayPal paypal_8194385。最终完整方案均重新授权；写入结果均为exchange requested。这是申请正确登记，不能说实物换货或退款已完成。

|任务|新续行|正确写入/目标/必要约束|话术支持|矛盾|待核实|全质量通过|
|---|---:|---|---:|---:|---:|---:|
|70 头盔|4|4/4 均通过|1|0|3|1|
|52 相机|4|4/4 均通过|1|1|2|1|
|合计|8|8/8 均通过|2|1|5|2|

头盔known先整理缓存路径把不存在的M/黑/高通风说成“not available”，依事前规则保留歧义，不能擅自认定无货或不存在；unknown先澄清在库存尚未知时说“no available ... right now”，证据不足。相机unknown先查询明确说“none combine 10x with 30MP + CF”，与目录矛盾；宽范围“10x variants unavailable”及available语境下的no-item范围则保留待核实。逐条见本批FACT_REVIEW.md，不把5条pending说成5条已证实错误。

新头盔unknown先查询的原judge也未通过，但这次不是简单把true读成null：它承认ref12=true，却把整个observation封装当作自生成摘要，忽略其中official_tool/get_product_details及official_result。冻结评分已按正式结果支持ref16库存说法；该路径仍因另一处无匹配SKU的库存措辞pending，不能直接升为全质量通过。补充程序来源审计见JUDGE_PROVENANCE_AUDIT.json，原judge完整保留。冻结提取器只表示库存值断言，未自动表示来源合法性断言，该覆盖边界单列。

## 工作是否推进，和投入是否可比

所有已完成工作均满足自身契约。screen只建立缓存候选摘要，属于准备性产物；clarify建立用户许可规则，inventory补充新官方库存依据，prepare建立当前方案，confirm绑定本轮回复，submit写入申请。许可的获取、生效及交易授权分开，不能用话术错误直接推定整步毫无业务推进。

两项任务的known先澄清均执行4工作（clarify→prepare→confirm→submit），先整理均5工作，多一个screen；澄清后没有再做screen。unknown两侧均5工作，inventory/clarify顺序相反，其余相同；各查询库存1次。先澄清获得“若有货则接受”后，由查询触发许可；先查询先消除库存未知，再澄清用户接受范围。两种顺序本批都成功写入。

新4个配对均至少一侧话术未通过/待核实，故**没有质量可比配对，不作资源差排名或收益结论**。绝对记账仍保存于WORK_PROGRESS.md和summary.json；PAIRED_RESULTS.md的差值留空，不用失败/待核实路径的较低成本证明优势。

旧09按新规则复核后只有3个质量可比配对：头盔known第2次，先整理比先澄清多1工作/1 Agent调用/5261词元；相机known第2次多1工作/1调用/3703词元；头盔unknown第2次工作和调用相同，先查询少404词元但多1次程序review。相机unknown两次均不可比。它们是历史参照，不与本批凑成已验证的重复收益；原始和重评分并列。

缓存整理是已有证据上的本地计算；库存查询获得新的外部观察。跨状态不能把两者当成同一干预。review次数及无记录变化的复核另列，不等同额外模型调用，也不直接推断无必要。

## 投入分账及模型记录

'''+ '\n'.join(accounts)+'''

所有usage均实际返回，无缺失。Agent总词元213990，模拟用户20491及外部评测均未计入Agent。公共起点由已核对JSON直接加载，新增公共前缀解析调用为0；其历史与规则进入各请求的输入词元，已包含在Agent输入201532中。服务不返回公共前缀子段的独立usage，不能假报其词元为0、重复计入或凭估算扣除缓存。保留原始usage及缓存字段。

本批事实提取16次、评审证据提取1次；离线v1开发33次、v2统一校验33次另列，旧16条离线复核没有新业务Agent调用。语义抽取由本助手逐话术审阅，标注成本无法审计计量，未记为0；既不是独立人工金标准，也不是全自动事实理解。新16句话术12个类型/实体/范围/遗漏补丁逐条附理由和原提取哈希，无真值或通过分数覆盖。JSON与原响应均保留。

新业务86次+新评分17次，以及离线66次实际响应均返回model=deepseek-flash，system_fingerprint=bc19ba97cbe016479903222bb1578db6；旧09的172次响应也为此标识。逐调用id/created/model/fingerprint见returned_models_all.json及旧原记录。该服务未提供更细权重版本号，不能据相同别名和fingerprint保证后端权重完全不变。temperature=0、thinking=false、retries=0、timeout60；每条预算仍24次Agent调用/60000词元/9工作。

程序CPU及elapsed见program_timing.json：仅量化日志重放、比较和JSON IO，不含导入、模型调用或作者审阅。复算输出逐字节一致。

## 可能由什么造成

known少一步整理与当前菜单契约有关：澄清可直接读取已观察目录并取得许可，后续无需单独screen。此现象与09的结构观察相符，但不能据本批不等质量的配对宣布总收益成立。unknown在共同后续策略下最终都需用户许可与一次正式库存查询，因此顺序不同、工作数相同；更复杂分支、用户拒绝、库存变化可能改变结果，本批未测试。

话术失准可能来自模型压缩候选集时混淆“目录全集”和“可用子集”，或把未知简写成无货。评审错误可能来自工具结果以observation封装而非独立role=tool呈现。上述是机制解释，不是已隔离验证的因果结论。模型提取自身也出现目标规格错提为存在性否定、原报价错绑新SKU、30MP上下文范围漏绑等；均在保留原响应后按冻结语义审阅程序标注。尚存歧义保持pending，不能靠最终成功结果修正过去话术。

## 还需什么证据，哪些可进入3.2

任务70/52 × known/unknown四类固定起点已有公开依据、合法可开展的两候选、配对起点一致性和可追溯写入证据，可作为3.2框架对照的**诊断场景与候选集合**：known用screen/clarify，unknown用inventory/clarify。若指“主收益比较已就绪”，本批四类均未达质量可比重复门槛，不能宣称任何首步已获稳定收益证据。

优先可保留known两任务检验省略缓存整理的结构假设；unknown头盔保留顺序及条件许可触发诊断；unknown相机还需澄清目录存在性/可用性话术边界。均应先处理剩余语义范围与评审来源覆盖，再独立冻结，获得同任务同状态至少两组质量可比的新配对。3.2还需让框架真正自主选择首步并与同模型基线比较，而不是继续只强制首步。此处不据结果生成偏好标签。

本轮只有2个单商品任务、单一模拟许可规则、底层静态库存、新批每格1次；作者参与语义校准，未有独立复核。known的工作数现象可重现，但整体成本方向没有新的合格重复。样本与评测边界均不足以外推多商品、库存再变化、用户修改最终方案或一般业务收益。

## 完整性与开发/冻结结果边界

冻结UTC 2026-11-23T00:17:41.573614+00:00，业务启动00:18:19.938823+00:00；先完成旧16条复核及两类离线自检，再冻结，再启动新8条。冻结代码、规则和数据未改；11个业务/恢复/接口模块及work/scores/rollout与09一致，四组完整起点与09对应起点一致。939个受保护文件（含申报书、01–09、基准及依赖）哈希保持，DELIVERY_AUDIT.json通过。

v1开发提取、修订及统一v2旧样本再抽取全部保留，见DEVELOPMENT.md、development_v1、offline_v1；它们不混入冻结后新结果。冻结后只进行预先规定的语义标注、结果汇总和独立来源审计，没有修订业务或评分代码，没有替补采样。尚未覆盖的宽范围混合库存及来源断言问题见POST_FREEZE_ISSUES.md，保持本批原样。

config.json中sampling文字仍遗留“16 planned”，execution_order文字含r2；实际控制字段repeats=1、冻结PROTOCOL及执行循环均为8，结果也恰为8。离线检查中某些旧测试描述含16次恢复，指继承自09的离线检查，不是新在线数。旧离线派生表rule_version沿用早期10_v1字符串；冻结规则/源码及实质算法为v10.2，原始提取与语义补丁可重算。以上元数据瑕疵照录，不修改冻结清单以掩盖。

本轮使用公开τ²-bench零售模拟数据，申报书和01–09原件保持；没有训练、偏好标签或真实交易。
'''
write(R/'RESULTS.md',report)
write(R/'POST_FREEZE_ISSUES.md','''# 冻结后发现及保留边界

1. **描述元数据遗留。** 冻结config sampling文字仍写16，execution_order文字含r2；实际repeats=1及PROTOCOL规定8，执行8。离线派生rescore版本字符串遗留10_v1，但v2代码/规则/原始提取/补丁均已冻结；不回填修改冻结文件。
2. **混合库存集合的有限表示。** 对某些“the 10x variants are unavailable”，stock提取为多SKU组，而程序发现库存不一致时返回pending，尚不把不明确的量词/上下文强推成全称或存在断言。明确定义范围后可用exists/available或逐SKU核验；当前原输出留档，不在本批追改规则消除pending。它限制事实覆盖，并不说明已有确定单SKU的true/false无法核验。
3. **来源断言覆盖不足。** 冻结judge提取器只表示available值。新judge承认ref12=true却否认其中official_result来源，自动结构断言列表未捕获这类来源命题。独立程序读取原封装作JUDGE_PROVENANCE_AUDIT，原评审及冻结分数不改；未来若扩展表示，应另冻。原冻结话术评分已经使用正式结果，所以不因judge否认该封装而撤销证据。
4. **语义审阅仍需作者。** 16条新话术均读过，12个补丁保存原句与哈希，无真值覆盖；不是独立金标准。pending保留。完整政策句和多义范围不等于已被有限事实本体穷尽。报告不把2条supported夸大为全自动自然语言正确证明。

本文件是冻结后的发现与适用范围说明，不是另一个暗中修订的实验批次。未追加续行、替补失败、回放API响应或训练。
''')
write(R/'FREEZE_MANIFEST.md',f'''# 冻结与交付清单

- 冻结批次：results/{B.name}，UTC {F['utc']}。
- 机器冻结清单：本批freeze.json，{len(F['files'])}个冻结文件、{len(F['protected'])}个受保护文件哈希。
- 已冻结方案/规则：frozen/PROTOCOL.md、FACT_RULES.md、scoring.json、config.json。
- 固定起点和原话依据：frozen/snapshots/public、snapshots/evidence、STARTING_STATES.md。
- 公开场景、模拟DB、私有评测分开：frozen/scenarios/public、initial_database.json、scenarios/private；私有内容不进Agent。
- 评分：frozen/fact_verifier.py、claim_contract.py、score_facts.py；原09评分legacy_scoring09.json保留。
- 预检：frozen/offline_check.json、fact_selfcheck.json、offline_validation/validation.json；原09复核分另存。
- 新运行：frozen/run.py execute，8条；不复用响应，不替补，不中途修订。
- 原始记录：本批model_calls.jsonl、各_start/_trajectory/_final_state/_result.json；新评分evaluation/model_calls.jsonl及extractions。
- 语义审阅：evaluation/semantic_review.json及根review_live_annotations.py，按冻结规则做数据标注；原抽取永存。
- 最终审计：DELIVERY_AUDIT.json、integrity_after.json、ACTUAL_WRITES.json、JUDGE_PROVENANCE_AUDIT.json。
- 描述元数据瑕疵与剩余覆盖边界见根POST_FREEZE_ISSUES.md；不修改冻结清单。

方案、代码、场景、数据及预算先冻结，新8条全部完成后再评分。根报告/汇总脚本属于冻结后交付，不冒充预注册文件。
''')
write(R/'README.md',f'''# 第10轮：程序事实核验与续行验证

已完成旧09的16条离线重评分及8条新配对续行。新8条全部正确写入；话术2支持、1矛盾、5待核实，0个完整质量可比新配对。申报书和01–09原件未改，不训练、不生成偏好标签。

阅读顺序：

1. [结果摘要](RESULTS.md)／[方案](PROTOCOL.md)／[新评分规则](FACT_RULES.md)。
2. [旧16条逐条复核](offline_v2/OFFLINE_TABLE.md)，原冻结分在offline_v2/original_09_scores。
3. [冻结清单](FREEZE_MANIFEST.md)，机器哈希results/{B.name}/freeze.json。
4. 新批[逐任务配对表](results/{B.name}/PAIRED_RESULTS.md)、[逐条质量/事实](results/{B.name}/FACT_REVIEW.md)、[工作及开销](results/{B.name}/WORK_PROGRESS.md)。
5. [冻结后问题](POST_FREEZE_ISSUES.md)／[开发记录](DEVELOPMENT.md)。

原始数据位于results/{B.name}；Agent/用户/原评审请求与原始响应model_calls.jsonl，新外部提取evaluation/model_calls.jsonl。逐话术原抽取、语义补丁、程序值及证据来源都保存。程序来源补审与冻结评分分开，不覆写原judge。

## 脚本与复现

Python使用D:\\experimentn\\tau2-official\\.venv\\Scripts\\python.exe。运行需沿用本机既有模型配置；不在文档抄录密钥。frozen/run.py禁止重复execute已启动批次。仅重算已有数据可运行：

```powershell
& 'D:\\experimentn\\tau2-official\\.venv\\Scripts\\python.exe' '.\\results\\{B.name}\\frozen\\score_facts.py' --batch '.\\results\\{B.name}' --out '.\\results\\{B.name}\\evaluation'
& 'D:\\experimentn\\tau2-official\\.venv\\Scripts\\python.exe' '.\\report.py' '.\\results\\{B.name}'
& 'D:\\experimentn\\tau2-official\\.venv\\Scripts\\python.exe' '.\\verify_delivery.py'
```

上述重算无API调用；不要对已存在提取目录再加--extract。若以后修改事实规则/业务代码，需要新目录或另行冻结，不得写回本批。私有模拟偏好只用于用户模拟/结果核验，不能作为起点解析或Agent事实证据。
''')
print('Reports written')
