"""Post-run integrity audit and final documentation, no model calls."""
import json,hashlib,shutil
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent.parent;B=R/'results/batch02'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
f=read(R/'configs/freeze.json');s=read(R/'results/SUMMARY.json');checks={}
old10=R.parent/'10_程序事实核验与续行验证';old11=R.parent/'11_框架自主决策与动态多轮验证';old12=R.parent/'12_程序与模型协同修复及复验'
checks['old01_09_and_proposal_unchanged']=all(sha(Path(p))==v for p,v in read(old10/'results/20261123T001740331845Z/freeze.json')['protected'].items())
checks['old10_unchanged']=all(sha(old10/p)==v for p,v in read(old10/'DELIVERY_MANIFEST.json')['files'].items())
checks['old11_unchanged']=all(sha(old11/p)==v for p,v in read(old11/'results/DELIVERY_MANIFEST.json').items())
checks['old12_unchanged']=all(sha(old12/p)==v for p,v in read(old12/'results/DELIVERY_MANIFEST.json').items())
checks['formal_frozen_inputs_unchanged']=all(sha(R/p)==v for p,v in f['files'].items())
checks['offline_passed']=read(R/'configs/offline.json')['passed']
checks['freeze_before_online']=f['utc']<read(B/'started.json')['utc']
checks['same_complete_start_for_all_four']=len({sha(p) for p in B.glob('*_start.json')})==1 and len(list(B.glob('*_start.json')))==4
api=[json.loads(x) for x in (B/'model_calls.jsonl').read_text('utf-8').splitlines()];ctrl=[x for x in api if x['stage']=='controller']
checks['direct_never_W']=all('W' not in json.loads(x['messages'][1]['content']) for x in ctrl if x['branch'].endswith('_direct'))
checks['candidate_always_W']=all('W'in json.loads(x['messages'][1]['content']) for x in ctrl if x['branch'].endswith('_candidate'))
first=[json.loads(next(x for x in ctrl if x['branch']==row['id'])['messages'][1]['content'])['state'] for row in s['rows']]
checks['identical_first_visible_state']=all(x==first[0] for x in first)
checks['all_old_false_permissions_preserved']=all(x['historical_false_rule_preserved'] for x in s['rows'])
checks['three_new_effective_permissions_and_separate_authorizations']=sum(x['new_effective_permission'] and x['final_authorization'] and x['correct_write'] for x in s['rows'])==3
checks['explicit_rejection_caused_no_write']=next(x for x in s['rows'] if x['id']=='t52_r1_recovery_direct')['safe_refusal_without_write']
checks['current_reply_completion_source_bound']=all(all(o['source_valid'] and o['user_ref']>o['assistant_ref'] and o['user_ref']>12 for o in row['outcomes']) for row in s['rows'])
checks['three_confirmation_field_checks']=len(read(R/'results/CONFIRMATION_CHECKS.json'))==3 and all(x['fields_valid_at_utterance'] for x in read(R/'results/CONFIRMATION_CHECKS.json'))
checks['simulator_rule_shared']=len({json.dumps(json.loads(x['messages'][1]['content'])['policy'],sort_keys=True) for x in api if x['category']=='environment_user'})==1
checks['no_unevaluated_spoken_suffix']=True
for row in s['rows']:
 n=row['id'];start=read(B/(n+'_start.json'));h=read(B/(n+'_final_state.json'))['F']['dialogue'];refs={e['assistant_ref'] for e in read(B/(n+'_trajectory.json')) if 'assistant_ref'in e}
 for i,m in enumerate(h):
  if i>=len(start['state']['F']['dialogue']) and m['role']=='assistant' and m.get('content') and i not in refs:checks['no_unevaluated_spoken_suffix']=False
save(R/'results/AUDIT.json',{'passed':all(checks.values()),'checks':checks});assert all(checks.values())
for name in f['files']:
 d=B/'frozen_inputs'/name;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/name,d)
shutil.copy2(R/'configs/freeze.json',B/'freeze.json')
jobs=[f't52_r{rep}_recovery_{g}' for rep in (1,2) for g in ('direct','candidate')];life={}
for batch in ('batch01','batch02'):
 p=R/'results'/batch;results=read(p/'results.json') if (p/'results.json').exists() else {}
 life[batch]=[{'id':n,'stage':'result_saved' if n in results else 'interrupted_partial' if (p/(n+'_start.json')).exists() else 'not_started','reason':results.get(n,{}).get('error')} for n in jobs]
save(R/'results/LIFECYCLE.json',life)
report='''# 第13轮：条件许可落空后的自主恢复

## 起点与实现

使用任务52公开历史改编共同起点。实验新增用户原话为“If item 3892645120 ... is in stock, I accept that variant. I have not accepted any lower-zoom alternative. Please check stock before making a plan.”，不是冒称基准原始逐字对话。先把这一规格的先前库存观察设为未知，绑定source12条件许可；再实际调用模拟RetailTools.get_product_details，ref13确认完整目录中该规格存在且available=false，同时6384525445（30MP/CF/5x）和7255224608（30MP/CF/3x）均true。最后一次官方查询原样保存在configs/start_evidence.json；此前未知掩蔽为实验的观测设置，不冒充未改动的真实服务返回。

初始旧许可保留，条件false，因此alternative_permission仍unknown；替代品库存已有证据，但无用户许可、新方案或当前授权。配置start.json同时保存公共状态/视图和可恢复运行时，不包含私有fallback答案；私有规则仅供用户模拟和评测。两组四次完整起点及首次可见状态相同。程序可选工作同时包括直接澄清和整理缓存，避免人为拒绝合理分析路径。

第12轮完成条件permission_rule_acquired只返回bool(conditional_permission)，确实能被旧许可自动满足。新current_reply_clarification_resolved逐次begin上下文；只有本轮原话/来源有效且取得另一个规格的新许可，或本轮明确拒绝，才完成澄清。旧许可不能自动通过；信息不明确则completion=false，允许继续问。同意新规格不授权完整交易；prepare之后仍必须confirm，再由程序核验当前方案指纹才能submit。

离线复现旧缺陷，并验证四个必需行为及新许可/明确拒绝/不明确三分支。正式线上观察到3次new_permission、1次explicit_rejection、0次information_unclear；不明确分支只有离线证据。许可条件满足性仍由程序读取已有有效库存判断，不由模型承诺“有货”。

## 正式结果

正式批次batch02，共4条，无替补。直接组第1次screen→clarify后收到明确拒绝，正确保留原订单、没有申请和授权；直接组第2次screen→clarify→prepare→confirm→submit，登记成功。候选组两次均clarify→prepare→confirm→submit，登记成功。全部旧false规则和source12原句留存于permission_history。

成功3条均5996159312→6384525445，30MP/CF/5x，差额+$34.07，原PayPal paypal_8194385，工具状态exchange requested。它表示换货申请正确登记，不能说实际换货或收费已完成。三条的必要约束、当前方案新授权、源引用及实际写入均通过；3次程序确认的规格、库存、价格差额和支付字段均由发言前证据支持。

首步选择在两次重复中一致：直接组先screen，候选组先clarify。候选组实际comparison指出整理只能提供候选摘要，不能解决用户许可缺口；直接组识别了3892645120缺货，但把整理缓存视作下一步。两者均为允许的合理工作，不把缓存整理本身计为错误或重复查询。

**真正解除恢复障碍的是本轮用户对6384525445的明确新许可**：候选组两次source15、直接组第2次source16；库存已在ref13有效查询中为true，程序复核后立即使该新条件许可生效。screen没有改变许可状态，没有获得新的外部库存；它只整理已有依据。随后prepare形成+$34.07新方案，confirm获得另一条用户批准，submit绑定当前方案及该批准。接受变体与最终交易授权分别核对。完整成功轨迹见FULL_TRACE.md，含实际话术误述和所有状态变化，不隐去瑕疵。

## 对话事实、意图与模拟用户分开

工具可核实事实为3条supported、1条pending。3892645120均被正确说成缺货而非不存在；5x/3x库存与价格有依据。候选组第2次的“other 30MP CF-card variants”排除了前文已讨论的3892645120，模型抽取却当作绝对目录全集，原始程序判矛盾；按冻结的语义标注规则改为范围待核实，因为现有selector不能表达other排除集。保留原抽取，不把合法的相对范围误说成确凿话术错误，也不强推通过。

四条澄清均出现“Since you've said you don't accept a lower zoom”。用户只说尚未接受任何低倍替代，并没有一概拒绝低倍规格。**四条用户偏好/许可表述均不准确**。这是模型语义错误，与工具库存真值不同；工具事实supported不能洗掉它。语义审阅来自本助手，非独立盲审，原句对照在SUMMARY.json。

直接组第1次模拟用户进一步拒绝了所有低倍替代，偏离统一私有模拟规则“若有货可接受且仅接受6384525445”。两组收到的模拟规则完全相同，但模型用户实际遵循情况并不完全一致。Agent尊重该实际拒绝停止提交是正确的；这条不能简单算作无法理解false条件，更不能用它证明候选组成功率较高。共同的话术误述可能影响用户回复，但本轮没有隔离因果。

因此两次配对均没有两侧达到完整相同质量标准，不计算步骤/调用/词元收益差。绝对记账和路径仍保存。候选组2次登记、直接组1次登记1次拒办，是本批观察；首步差异重复一致，而直接组最终结果不一致，且受模拟偏离干扰。不能据此生成组间偏好标签或训练数据。

## 证据边界与下一步

已验证：旧许可不生效时可重新澄清；新完成条件确实依本轮回复，保留旧许可不会自动完成；新的变体许可可复用已有有效库存生效；完整方案另获授权才能登记；用户拒绝时不错误提交。

尚需复验：澄清话术对“尚未接受”和“拒绝接受”的区分；模拟用户遵守固定私有规则的稳定性；信息不明确时实际追问的在线分支；独立语义审阅；更多同质量配对。显式候选两次都更直接选择许可澄清，可以追溯到comparison和当前缺口，但尚不能宣称整体质量/恢复成功率或投入有稳定收益。每组只有2次，底层库存静态且仅单商品，适用范围有限。

## 冻结、开发记录与投入

batch01为开发诊断批次，四条结果均已保存：直接组两条被继承菜单反复拒绝而未办结，候选组两条登记。排查发现菜单因旧许可存在而屏蔽screen，人为拒绝了合理的分析首步。发现后保留原冻结代码及全部四条结果，停止使用该设计作正式对照；并非声称运行中的四条都被进程中断。两组共同开放一次可选缓存整理后另冻，正式batch02四条全部独立新采样。没有把开发样本混入正式配对，也没有删除开发失败。排除依据是共享菜单缺陷，不是按哪组赢选择数据。

正式及开发账户分别如下（模拟用户/外评均不计入Agent）：

|批次/账户|调用|输入|输出|合计词元|
|---|---:|---:|---:|---:|
'''
for label,accounts in [('正式',s['accounts']),('开发',s['development_accounts'])]:
 for name,a in accounts.items():report+=f"|{label}/{name}|{a['calls']}|{a['prompt_tokens']}|{a['completion_tokens']}|{a['total_tokens']}|\n"
report+='''
正式和开发已记录响应的usage均无缺失；开发四条都有完整结果，未将开发开销并入正式Agent。3次程序确认话术生成0模型调用；用户模拟、语义提取仍按实计。公共起点离线构造包含真实模拟查询，单次逻辑起点记录1次正式查询，离线测试还会在独立DB副本上重复验证。它们不是Agent在线查询；本批线上无需再查库存。公共前缀新增模型解析调用0，提示中的历史与规则已包含Agent输入，不冒称其独立词元为0。作者语义标注没有独立时间计量。

预算及模型与12轮一致，返回model/fingerprint见SUMMARY.json。7次事实抽取原请求/响应保留；补丁只调整类型/引用/范围和实体，不写事实真值。冻结执行源码及配置完整保存在batch02/frozen_inputs；评分用原有fact_verifier/score_facts，旧strict_pass只是继承占位False，不作为最终指标。analyze13.py/deliver13.py为事后标注汇总，非冻结前执行策略。

原01–12和申报书哈希保持；AUDIT.json校验通过。无偏好标签或训练。全部拒办、待核实和开发排查结果保留。
'''
(R/'results/RESULTS.md').write_text(report,encoding='utf-8')
(R/'README.md').write_text('''# 第13轮：条件许可落空后的自主恢复

正式batch02四条：候选组两次登记；直接组一次登记、一次收到用户拒绝后安全停止。首步两次均直接组screen、候选组clarify。四条都误述“尚未接受”为“不接受”，无质量可比配对，不做收益排名。

- [配对表](results/PAIRED_RESULTS.md)、[结果与局限](results/RESULTS.md)、[完整实际轨迹](results/FULL_TRACE.md)。
- configs/PROTOCOL.md、config.json、prompts.json、start.json、start_evidence.json、offline.json、freeze.json：方案、共同起点及其来源、离线断言和冻结。
- src/experiment13.py构造真实模拟工具起点并运行四条；recovery13.py修复本轮澄清完成判定；tests13.py离线覆盖。其余执行/事实核验模块本地复制沿用，资源scenarios/snapshots保留原相对布局，原目录只读。
- results/batch02保存原始model_calls.jsonl、program_confirmations.jsonl、各start/trajectory/final_state/result；evaluation保存原始事实抽取、哈希绑定语义补丁和逐条程序值。
- results/SUMMARY.json含每条许可/拒绝结果、授权、写入、用户表述误差、模拟偏离及分账；CONFIRMATION_CHECKS.json独立核验3个程序确认；AUDIT.json完整性；LIFECYCLE.json开发与正式启动/停止位置。
- results/batch01为已完成的开发诊断批，仅作缺陷记录，不并入正式结果。

Python为D:/experimentn/tau2-official/.venv/Scripts/python.exe。已启动execute禁止重复运行。重算只需src/score_facts.py --batch results/batch02 --out results/batch02/evaluation（不加--extract）；src/analyze13.py report不调用API。勿反复运行annotate追加重复补丁。任何执行修订另冻，不覆写本批。无训练和偏好标签。
''',encoding='utf-8')
print({'audit':checks,'lifecycle':{k:dict(Counter(x['stage'] for x in v)) for k,v in life.items()}})
