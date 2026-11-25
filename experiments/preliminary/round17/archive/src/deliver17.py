"""Post-run audit and reporting. Never calls a model or mutates prior rounds."""
import json,hashlib,shutil
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent.parent;B=R/'results/batch01'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def lines(p):return [json.loads(x) for x in p.read_text('utf-8').splitlines()]
s=read(R/'results/SUMMARY.json');f=read(R/'configs/freeze.json');api=lines(B/'model_calls.jsonl');checks={}
old10=R.parent/'10_程序事实核验与续行验证'
checks['old01_09_and_proposal']=all(sha(Path(p))==v for p,v in read(old10/'results/20261123T001740331845Z/freeze.json')['protected'].items())
checks['old10']=all(sha(old10/p)==v for p,v in read(old10/'DELIVERY_MANIFEST.json')['files'].items())
for folder in ('11_框架自主决策与动态多轮验证','12_程序与模型协同修复及复验','13_条件许可落空后的自主恢复','14_澄清语义与受控回应验证','15_库存证据变化与认知决策对照','16_库存查询结果与后续决策复验'):
 old=R.parent/folder;checks[folder[:2]]=all(sha(old/p)==v for p,v in read(old/'results/DELIVERY_MANIFEST.json').items())
checks['frozen_unchanged']=all(sha(R/p)==v for p,v in f['files'].items());checks['offline']=read(R/'configs/offline.json')['passed'];checks['freeze_before_online']=f['utc']<read(B/'started.json')['utc']
checks['all12_saved']=len(s['rows'])==12;checks['all12_registered']=all(x['registered'] and x['authorization'] and x['speech_pass'] for x in s['rows'])
checks['unknown_public_starts_identical']=len({sha(p) for p in B.glob('*_unknown_*_start.json')})==1
ctrl=[x for x in api if x['stage']=='controller'];first=[]
for n in read(B/'results.json'):
 if '_unknown_'in n:first.append((n,next(x['messages'] for x in ctrl if x['branch']==n)))
checks['unknown_first_messages_identical_per_group']=all(len({json.dumps(msg,sort_keys=True) for n,msg in first if n.endswith('_'+g)})==1 for g in ('direct','candidate'))
a=read(B/'t70_r1_unknown_out_direct_environment.json');b=read(B/'t70_r1_unknown_in_direct_environment.json');a['products']['7765186836']['variants']['9013366374']['available']=True;checks['private_db_only_target_stock_differs']=a==b
checks['direct_no_W']=all('W'not in json.loads(x['messages'][1]['content']) for x in ctrl if x['branch'].endswith('_direct'))
checks['candidate_has_W']=all('W'in json.loads(x['messages'][1]['content']) for x in ctrl if x['branch'].endswith('_candidate'))
checks['query_result_switch']=all(r['post_query_first']==('prepare' if r['condition']=='unknown_in' else 'clarify') for r in s['rows'] if r['condition']!='known_out')
checks['original_permission_only_when_true']=all((r['post_query_permission']=='9013366374')==(r['condition']=='unknown_in') for r in s['rows'] if r['condition']!='known_out')
events=lines(B/'request_events.jsonl');checks['requests_balanced']=sum(x['event']=='request_started' for x in events)==len(api)==sum(x['event']=='request_finished' for x in events)
checks['history_not_in_current_conditions']=all('historical_plan_compatible'not in json.loads(x['messages'][1]['content'])['state']['C'] for x in ctrl)
checks['current_contract_gate_policy_shared']=all(json.loads(x['messages'][1]['content'])['state']['execution_contract_policy']['submit_required_conditions']==['identity','plan_current','authorization_current','not_written'] for x in ctrl)
# Supplementary post-run evidence check; the pre-run snapshot was a controlled fixture,
# not a live service observation. Match it to an actual deterministic simulated query.
import experiment17 as e
from copy import deepcopy
c=e.load('known_out');tools=e.b.RetailTools(e.b.RetailDB.model_validate(deepcopy(e.environment('known_out'))))
checks['known_snapshot_equals_simulated_product_query']=tools.get_product_details(product_id='7765186836').model_dump(mode='json')==c.core.products['7765186836']
checks['each_pair_initial_snapshot_equal']=all(read(B/(f't70_r{rep}_{st}_direct_start.json'))==read(B/(f't70_r{rep}_{st}_candidate_start.json')) for st in ('known_out','unknown_out','unknown_in') for rep in (1,2))
save(R/'results/AUDIT.json',{'passed':all(checks.values()),'checks':checks});assert all(checks.values()),checks
save(R/'results/MODEL_VERSIONS.json',[{'id':x['branch'],'stage':x['stage'],'status':x['status'],'provider_request_id':x.get('provider_request_id'),'diagnostic':x.get('diagnostic'),**{k:x.get('response',{}).get(k) for k in ('model','system_fingerprint','id','created','usage')}} for x in api])
account=[]
for r in s['rows']:
 xs=[x for x in api if x['branch']==r['id']];entry={'id':r['id'],'agent_requests':len(xs),'agent_prompt_tokens':sum(x['usage']['prompt_tokens'] for x in xs),'agent_completion_tokens':sum(x['usage']['completion_tokens'] for x in xs),'provider_cache_hit_tokens':sum(x['usage'].get('prompt_cache_hit_tokens',0) for x in xs),'environment_user_model_tokens':0,'external_evaluator_model_tokens':0,'missing_usage':sum(x.get('usage') is None for x in xs),'executed_work':r['steps'],'program_rejections':len(r['program_rejections'])}
 entry['tool_calls']=sum(1 for q in read(B/(r['id']+'_trajectory.json')) if 'u'in q and q['u']['z']['work_id'] in ('inventory','submit'))
 entry['executor_local_cpu_seconds']=sum(q.get('local_process_cpu_seconds_including_transport',0) for q in read(B/(r['id']+'_trajectory.json')))
 entry['executor_wall_seconds_including_io']=sum(q.get('work_wall_seconds_including_model_and_customer_io',0) for q in read(B/(r['id']+'_trajectory.json')))
 account.append(entry)
save(R/'results/ACCOUNTING.json',{'rows':account,'notes':['All model calls are Agent decision/semantic parsing. Controlled simulator and assistant review make no experimental model requests.','Shared policy and state prefixes are included in returned prompt usage. Exact prefix-specific token use is not reported by provider and is unknown, not subtracted or charged to simulator.','Provider cache-hit token count is a separate overlapping provider statistic, not common-prefix overhead.','Executor wall time and local process CPU are recorded; pure program-only overhead is not separately isolated. Tool calls count actual inventory queries and exchange writes; prepare/screen are local computation.']})
save(R/'results/ACTUAL_PROMPTS.json',{'post_run_export_of_frozen_source':True,'first_messages':{x['branch']:next(y['messages'] for y in ctrl if y['branch']==x['branch']) for x in ctrl},'all_messages_in':'batch01/model_calls.jsonl','frozen_definition':'src/experiment11.py shared direct/candidate prompts + src/experiment17.py policy + src/helmet17.py compact state, recorded in configs/freeze.json'})
for p in f['files']:
 dest=B/'frozen_inputs'/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/p,dest)
shutil.copy2(R/'configs/freeze.json',B/'freeze.json')
quality=sum(x['quality'] for x in s['rows']);reason_counts=Counter(x['status'] for x in read(R/'results/REASONS.json'))
report=f'''# 第17轮结果：头盔任务跨任务机制复验

## 观察到什么

正式单批计划12条，启动12、保存12、正确登记12；必要约束、当前方案独立授权、发言事实核验均12/12。无未启动、提前停止、未办结或模型请求异常。执行前程序拒绝2次，均保留在原轨迹，没有替补。完整质量（另含决策理由及预期准确性）{quality}/12；两条有前提误读，另一条的退款时点预期待核实。

**第16轮的查询后切换在头盔题复现。** 两组各两次均先查库存；查到缺货后第一决策均clarify，查到有货后第一决策均prepare。两个待核实条件的公开完整起点和同组首次messages一致，私有数据库只改目标规格available。false使原source11条件许可不生效，用户实际接受黑/L后取得新许可；true激活原蓝/M许可，不重复询问规格接受，但仍prepare→confirm→submit，独立请求当前完整方案授权。

known_out两次：候选组首个模型选择都是clarify；直接组首个选择都是inventory，以“许可要求available=true，所以必须获取当前库存”为由请求查询。程序指出已有有效库存证据、inventory在当前阶段不适用；下一次直接组改clarify并完成办理。首次选择、被拒绝工作与首个实际执行工作在配对表分别列出。两组首个实际执行工作都是澄清，不能据此把首次决策说成相同。

没有人选择screen缓存整理。本轮已知状态直接组的重复查询未执行，不等同第16轮合法的screen整理。screen属于本地分析已有缓存，inventory是实际获取正式库存结果；不得把它们当作相同工作来跨轮比较。

登记的业务状态均为exchange requested，表示申请已登记，不代表实物换货或退款到账。缺货两条件使用1665571435黑/L/高通风，价196.89，相对原197.33差额−0.44；有货使用9013366374蓝/M/高通风，价219.88，差额+22.55。原商品3358616356、订单#W3947049、原Visa credit_card_7901829（7312）保持一致。逐条数据库与工具结果、许可来源和当前授权指纹已核对。

## 前提和理由复核

54次成功决策全部混排去组别/条件名后按共同判据语义审阅，判定{dict(reason_counts)}。REVIEW_PACKET与单独映射、REASON_REVIEW及REASONS保留原句、时点状态、来源和判定。覆盖同义表述而非仅扫关键词。比较格式仍可能暴露组别，复核者知道任务，且没有独立金标准，因此只是部分遮蔽。

R008、R036（known_out直接组两次）原句均承认available=false，却推导“so current inventory must be obtained”。最新ref12已经确定缺货，当前障碍是该许可条件不成立和替代许可未取得，不是缺少库存观察；程序工作适用性拒绝后两次都恢复。该问题是许可生效条件和信息缺口混淆，不能说成模型完全没读到false，也不能把任何主动刷新都判错。

本批未发现把“尚未接受”说成明确拒绝、把历史兼容性当submit额外必要条件，或把规格许可当最终授权。历史信息仍在独立historical_information中；提交实际契约只检查identity/plan_current/authorization_current/not_written。当前状态、共用提示和程序核验提供一致反馈。不能从本轮无此类误读断言已普遍修复，第16轮到17轮同时改变任务与状态表达，无法单独归因。

R050（unknown_out直接组第2次）的内部expected称“the $0.44 refund is issued”。差额和换货申请登记有证据，但工具不证明退款实际到账；按冻结歧义规则保留待核实。这不是已经对用户发出的退款到账承诺，也没有影响正确写入。该配对保守地不参与投入排名。

所有实际澄清/确认话术以发言前工具记录核验，明确exists但out of stock，unknown则待核实；未把尚未接受说成拒绝。确认展示当前商品、规格、库存、差额、原支付，并由新用户原话独立授权；旧批准仅历史，未复用为提交授权。FACTS逐条保存程序结果，原始状态中的实际契约检查在P.actual_contract_checks，拒绝详情在trajectory。

## 可能由什么造成

两种查询结果直接改变程序计算的条件许可与可准备规格，模型之后选择不同工作有逐步证据支持；两组查询后路线相同，未观察到候选额外缩短流程。已知缺货时显式候选及其前提可能帮助候选组直接定位许可缺口，直接组也能利用共享拒绝反馈恢复。这是机制解释，尚不能证明候选导致收益。继承接口仅在库存未知时提供inventory契约，已知状态的拒绝是该接口工作适用性规则，不是基准业务禁止再次查询；直接组不预看完整候选契约，这种前提暴露差异也可能解释其多一次选择，不能把它全部归为认知能力收益。详见configs/EVIDENCE_INDEX。

## 投入与请求诊断

实际请求{s['attempts']}次，全部成功；缺失usage {s['missing_usage']}，服务总返回词元{s['returned_tokens']}。实际返回模型/指纹为{s['versions']}，逐次版本/请求编号在MODEL_VERSIONS。程序拒绝与请求异常分别计账，不算服务失败，也不隐去消耗。

仅3/6配对满足两侧完整质量且用量完整：unknown_out第1次、unknown_in第1/2次。它们工作步数差均0，D−C词元分别−3588、−2481、−2446；候选多出的比较文本和输入也消耗词元。其余不计算投入差。ACCOUNTING分别列Agent输入/输出、提供方缓存命中、工具调用、程序拒绝；模拟用户为本地受控脚本、外部语义复核未调用实验模型，两者模型用量0。公共前缀计入Agent输入，提供方未给独立前缀词元拆分，故单独数值未知，不虚构扣除。同时保留执行器局部CPU与含模型/用户IO的总耗时，未独立拆出纯程序计算开销。

统一预算24请求尝试/60000返回词元软阈值/9实际工作/12决策机会；SDK与应用自动重试0。未超预算、未中途修改冻结实现、无开发轨迹混入正式批次。沿用16轮异常分类日志；本批没有实际服务故障，不能据此宣称所有异常路径线上验证。

## 还需什么证据

每组合两次、一个改编头盔起点、静态库存和固定用户接受回复，只能支持小规模跨任务机制观察。需要独立复核理由、更多不同表达/拒绝/含糊回复、随机顺序及独立批次，才能判断候选收益和适用范围。已有第16轮相机和本轮头盔的相同查询后切换，但不是自由Agent整体对照，也不做训练或偏好标签。

用户原话为受控改编：本轮明确撤销原70后续黑色硬要求，保留高通风硬要求、蓝/M偏好和库存条件许可，未冒称原基准用户原句。起点最新库存是可复现模拟工具结果的fixture，已与真实模拟get_product_details逐字段比对，非现实商城库存。较早蓝/M有货证据保留在历史，最新ref12覆盖为false/null；不使用未来结果解释查询前发言。三值状态按原始UTF-8保存，终端编码显示差异不作为模型输入缺陷。

AUDIT核对起点、首次提示、数据库单变量差异、旧授权失效、查询后许可激活、写入结果和冻结完整性；第01–16轮与申报书原件哈希均未变。预先冻结的是协议/执行/提示源码，report/review/deliver为事后审阅脚本，实际提示另导出ACTUAL_PROMPTS，不冒称事后导出文件是预冻结文件。
'''
(R/'results/RESULTS.md').write_text(report,encoding='utf-8')
(R/'README.md').write_text('''# 第17轮：业务前提区分与跨任务复验

一批12条正确登记；9条完整质量通过，2条前提误读，1条退款时点预期待核实。查到缺货后澄清、查到有货后准备原规格方案，两个组两次均复现。

- configs/PROTOCOL.md、offline.json、freeze.json：预定方案、离线校验、冻结清单。
- src/helmet17.py：头盔起点/共享输入/受控交互；experiment17.py：正式运行；tests17.py：离线校验。
- results/RESULTS.md、PAIRED_RESULTS.md、TRACE_UNKNOWN_OUT.md、TRACE_UNKNOWN_IN.md：结果及两条完整续行。
- results/batch01：实际请求/反馈/每轮状态/环境/写入数据库；frozen_inputs包含原冻结副本。
- results/REASONS.json、REASON_REVIEW.json、FACTS.json、ACCOUNTING.json、AUDIT.json：分维度复核与投入；ACTUAL_PROMPTS.json是事后导出的实际提示，原始提示逐次保存在model_calls。

执行环境D:/experimentn/tau2-official/.venv/Scripts/python.exe。不要重复execute已启动批次。report17.py、deliver17.py可离线重算，无模型调用；复核语义判定由review_finalize17.py记录。src继承了一批旧模块，旧命名脚本只是依赖留存，活动入口仅上述17轮文件。旧目录只读，无训练或偏好标签。
''',encoding='utf-8')
save(R/'results/DELIVERY_MANIFEST.json',{str(p.relative_to(R)):sha(p) for p in R.rglob('*') if p.is_file() and '__pycache__'not in p.parts and p.name!='DELIVERY_MANIFEST.json'})
print({'audit':checks,'quality':quality,'reason_counts':dict(reason_counts),'attempts':s['attempts']})
