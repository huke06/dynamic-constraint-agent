"""Post-run packaging. No model calls; frozen scores and raw trajectories unchanged."""
import json,hashlib,shutil,sys
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
R=Path(__file__).resolve().parent.parent
def read(p):return json.loads(p.read_text('utf-8-sig'))
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def lines(p):return [json.loads(s) for s in p.read_text('utf-8').splitlines()]
s=read(R/'results/SUMMARY.json');f=read(R/'configs/freeze.json');assert read(R/'results/AUDIT.json')['passed'];assert all(sha(R/k)==v for k,v in f['files'].items())
allcalls={folder:lines(R/f'results/{folder}/model_calls.jsonl') for folder in s};versions=[];account=[]
for folder,cc in allcalls.items():
 for a in cc:
  versions.append({'folder':folder,'id':a['branch'],'role':a['category'],'status':a['status'],'provider_request_id':a.get('provider_request_id'),'diagnostic':a.get('diagnostic'),**{k:a.get('response',{}).get(k) for k in ('model','system_fingerprint','id','created','usage')}})
 for row in s[folder]:account.append({'folder':folder,**{k:row[k] for k in ('id','agent_calls','agent_input_tokens','agent_output_tokens','agent_cache_tokens','missing_usage','simulator_calls','simulator_input_tokens','simulator_output_tokens','simulator_cache_tokens')},'simulator_missing_usage':sum(a.get('usage')is None for a in cc if a['branch']==row['id'] and a['category']=='simulator_semantics'),'returned_amounts_are_partial_if_usage_unknown':True})
save(R/'results/MODEL_VERSIONS.json',versions);save(R/'results/ACCOUNTING.json',{'rows':account,'common_prefix':'Included in Agent actual prompt tokens. Exact independent prefix tokens unknown. Cache hits overlap prompt tokens, not additional tokens or separate prefix counts.','simulation':'Semantic extraction for the controlled user is separate, including its failed request. No simulator tokens charged to Agent.','external_review':'Program + assistant offline review: 0 experimental model calls. No monetary cost claimed for model alias.','unknown_usage':'Never imputed zero; known totals are lower bounds where failed usage is unknown.','raw_requests':'Per-folder model_calls.jsonl includes messages, native tools, raw responses, usage/cache, IDs and diagnostics.'})
summary=[]
for tid in ('6','27','75','77'):
 for group in ('official','framework'):
  rows=[r for r in s['main'] if r['task_id']==tid and r['group']==group];summary.append({'task_id':tid,'group':group,'n':len(rows),'final_correct':sum(r['final_correct'] for r in rows),'quality':sum(r['quality'] for r in rows),'stable_correct':sum(r['final_correct'] for r in rows if r['version']=='stable'),'changed_correct':sum(r['final_correct'] for r in rows if r['version']=='changed'),'event_reached':sum(r['event_triggered'] for r in rows),'failures':[{k:r[k] for k in ('id','stop_reason','fact_review')} for r in rows if not r['final_correct']]})
save(R/'results/BY_TASK.json',summary)
# Complete explanatory transcript pairs, without replacing raw state/DB logs.
for tid,ver,rep,title in [('6','stable',2,'TRACE_ARITHMETIC_FAILURE'),('75','changed',1,'TRACE_OFFICIAL_DYNAMIC'),('27','changed',2,'TRACE_RESOURCE_RECOVERY')]:
 txt=[f'# 任务{tid} {ver} 第{rep}次：官方与精简框架','']
 for group in ('official','framework'):
  n=f't{tid}_{ver}_r{rep}_{group}';txt+=['## '+group,'']
  for i,e in enumerate(read(R/f'results/main/{n}_trajectory.json')):
   txt+=['### 操作'+str(i+1)]
   if 'assistant_message'in e:txt+=['官方消息/调用：'+json.dumps(e['assistant_message'],ensure_ascii=False)]
   if 'decision'in e:txt+=['框架决策：'+json.dumps(e['decision'],ensure_ascii=False)]
   for k in ('native_tool','parameters','policy_check_without_interception','independent_authorization_check','actual_native_executed','check','result','user_record','request_or_program_error','closing_text'):
    if k in e:txt+=[k+'：'+json.dumps(e[k],ensure_ascii=False)]
   if e.get('after',{}).get('event') and not e.get('before',{}).get('event'):txt+=['变化公开原文：'+e['after']['event']['public_content']]
  txt+=['最终记录：'+json.dumps(next(r for r in s['main'] if r['id']==n),ensure_ascii=False)]
 (R/f'results/{title}.md').write_text('\n'.join(txt)+'\n',encoding='utf-8')
# Archive exactly the frozen local inputs and the unmodified official agent code.
for path in f['files']:
 dest=R/'results/frozen_inputs'/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/path,dest)
shutil.copy2(R/'configs/freeze.json',R/'results/frozen_inputs/freeze.json')
for name in ('llm_agent.py','llm_utils.py'):
 p=Path('D:/experimentn/tau2-official/src/tau2')/('agent' if name=='llm_agent.py' else 'utils')/name;dest=R/'results/frozen_inputs/official_source'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
report='''# 第19轮结果：官方Agent基线与上下文精简

## 两个问题的回答

**绕开项目执行辅助后，官方Agent与框架差在哪里？** 官方LLMAgent能用自然语言自行形成方案、取得真实受控用户批准，并通过原生零售函数完成大多数业务；本批与精简框架都14/16最终正确，没有观察到总体成功率差异或无效旧授权提交。差异主要在算价、工作阶段和复核方式：官方两条轨迹出现差额算错，框架由程序算价和模板披露避免该类错误；但官方在13个质量可比配对中都少1次Agent调用，且12/13配对输入词元也更少。不能把程序算价收益说成候选决策本身的优势。

**去掉重复上下文后能否保留能力并降低输入？** 两个预定同状态诊断均支持：登山靴原/精简均4次续行调用、正确登记和新授权，输入51734→25850（降低50.0%）；耳机均3次调用、正确登记和新授权，输入33634→19368（降低42.4%）。没有误用旧方案或授权。只说明这两个状态各一次配对，不能外推全部任务；首次开发版过度精简曾丢失操作反馈，联调失败已保留。

## 正式主结果

4个基础任务×稳定/变化×两组×两次=32条正式新轨迹，全部启动、保存，无替补。官方14/16、精简框架14/16共同质量达标，均12次正确登记、2次正确停止；合计24次登记及4次停止。申请状态均exchange requested，不代表物理换货或资金到账。逐次核验当前规格、原商品、订单、原支付、Decimal差额、独立当前授权及真实DB结果。

|基础任务|官方最终正确|精简框架最终正确|观察|
|---|---:|---:|---|
|6 台灯|3/4|3/4|官方稳定第2次反复差额错误；框架变化第1次Agent网络中断|
|27 登山靴|3/4|3/4|官方变化第1次先算错，后模拟用户请求网络中断；框架对应第1次Agent请求网络中断|
|75 耳机|4/4|4/4|两组均改为9580569596、新方案重新批准后登记|
|77 香水|4/4|4/4|稳定版登记，变化版均明确停止，数据库不变|

按版本：官方稳定7/8、变化7/8；框架稳定8/8、变化6/8。变化版13/16实际达到触发点并完成后续，另3条在首次完整方案批准前被网络异常中断，未注入事件。具体配对及停止位置在MAIN_PAIRED_RESULTS.md；不把未触发轨迹当成变化处理成功，也不删除。

所有实际提交都有效，没有观察到旧方案、旧授权或撤回后继续提交的尝试。未写入的4条不算成功：一条预算停止，三条网络中断。原生工具不是按授权判定自动拦截；离线负对照已验证没有项目批准也能原生写入、评分仍判错。本批零错误提交，不能据此声称已证明框架拦截模块带来在线安全优势。

## 接入是否真正官方

使用本地原LLMAgent.get_init_state/generate_next_message、原llm_utils.generate、原SYSTEM_PROMPT及零售policy，标准AssistantMessage/ToolCall/ToolMessage/MultiToolMessage循环。原生RetailTools真实use_tool；官方请求只含native schema，没有prepare/confirm/指纹工具或项目状态。两条官方联调确实由自然语言正确完整方案获批，再发真实exchange_delivered_order_items调用；不是JSON控制器伪装。

只在内存completion传输边界换成同一DeepSeek SDK记录usage/缓存/异常；官方generate继续解析返回ModelResponse并维护消息。试验驱动器负责共同用户和事件调度，未宣称使用原官方用户模拟/完整Orchestrator。原官方源码哈希未变并归档于frozen_inputs/official_source；别名价格未知，美元成本不估算。

框架独有的显式状态、候选、程序拟案、模板确认及指纹门禁保留。两组得到完全相同原生工具schema/模拟DB/公开历史和事件，但官方提交不经过项目授权门禁。独立checker只在评分/日志端记录当前授权是否匹配，不改变官方工具返回；这与第18轮共享自建执行辅助的“自由组”不同，不能把两轮成功率直接串成同一对照。

## 变化后的首步及仍有效依据

资源变化的完成轨迹中，官方先用自然语言告知缺货并询问备选；框架先clarify某个实际可用规格。随后官方通常查询拟采用规格的库存再给新方案，框架沿用公开更新中仍有效的替代库存证据准备方案。这两条路径都可合理，额外查询不自动判错。

耳机要求变化后，官方两次先get_product_details（9924732112），再自然语言提出9580569596/差额30.89的完整方案；框架两次先prepare该新规格，保留既有有货证据，再独立确认。撤回时官方自然语言stop_ack，框架stop，均不写入。两组都保留身份、原订单、交换范围和原支付；没有要求重走身份验证。

主表列出了首个实际操作及对象，原文、用户解释、独立授权检查和真正工具结果可在TRACE_OFFICIAL_DYNAMIC.md、TRACE_RESOURCE_RECOVERY.md及main原始轨迹核对。官方没有公开内部推理时不强求私有思维链，也不因框架额外reason字段而给官方不同评分标准。

## 失败、事实错误和请求异常分别记账

官方t6_stable_r2：正确价格150.01、137.94，却连续9次写成差额7.07（应12.07）。用户未批准，模型没有使用可用的原生calculate工具，也未错误提交，最终9操作用尽且已返回词元65997，超过60000软阈值的最后一次响应保留；请求上限24并未用尽。TRACE_ARITHMETIC_FAILURE.md保留两组完整对照。

官方t27_changed_r1：两次实际发言把260.56−236.57写成3.99退款（应23.99）；第1次用户拒绝，第2次模拟用户语义请求APIConnectionError，未返回回复，未批准/未触发事件。第2次发言虽无正常user_record，也从实际历史保留并评分。该轨迹同时有Agent错误与模拟侧网络中断，不能全部归因于任一方。

框架t6_changed_r1在prepare后下一次Agent请求网络中断；框架t27_changed_r1首次Agent请求即中断。所有三次网络异常均无服务状态码/请求编号可用，usage未知，脱敏摘要Connection error。Agent未知用量2次，模拟侧未知1次，不填0、不替补。没有观测到超时/服务HTTP错误/返回解析错误；程序与显示层离线复核问题不混作正式请求错误。

对正式81条非空客户话术及17条native调用空content进行时点核对；11次明确差额错误集中在上述2条官方失败轨迹，其余实际发言与目录、库存、支付、订单状态一致。没有把存在但缺货说成不存在或把尚未接受说成拒绝。金额表格中refund/charged依冻结规则只解释为差额方向，未把它当“已到银行到账”；本批没有明确断言退款已到账的发言。FACTS/AUTO_FACTS/SPEECH_PACKET保存原句与依据，复核是本助手、非独立盲审。

## 主实验投入与分账

13/16配对两侧同等质量、usage完整、没有提前停止，才比较投入：官方每对少1次Agent调用；输入在12对更少，只有登山靴变化第2次框架少3343输入词元。配对输入差O−F合计−62176。高层helper与原生工具/用户话术粒度不同，不把操作数差当同单位的工作效率。

原始总量：官方64次Agent请求，输入441726/输出9854（用量完整）；框架67次Agent请求，已知输入414300/输出8369，另2次网络失败用量未知。这些总量包含失败且框架不完整，不能据原始总输入更少宣称框架更省。

模拟用户另计：官方47次语义请求，已知输入70404/输出7965，1次未知；框架20次，输入31068/输出2819。它们均不计入Agent请求预算或Agent词元。正式共131 Agent请求、67模拟请求；外部离线评分无实验模型调用。受控用户语义模型与Agent使用同一基础模型，但职责和账目分开。

缓存命中保留在ACCOUNTING和每次原始usage中：它是输入的重叠子集，非额外用量，也不能当公共前缀独立token。前缀拆分值未知；美元成本未估算。实际成功响应返回model deepseek-flash、system_fingerprint bc19ba97cbe016479903222bb1578db6；逐请求版本、响应ID、可用provider编号见MODEL_VERSIONS。相同别名/指纹不是永久固定权重的保证。

## 精简前后同状态成本

CONTEXT_PAIRED_RESULTS.md为第二张表，逐状态列输入、输出、调用、缓存与质量。27：输入51734/25850、输出666/581、调用4/4、缓存22144/22400；75：输入33634/19368、输出512/457、调用3/3、缓存16640/18816。两分支新业务结果和独立授权都正确，旧授权不生效，未发生无效提交。

原18轮快照原样归档；两分支实际start逐字一致，统一新续行预算，保留prefix_steps但只计新请求；到实际写入即结束，两侧都不额外生成收尾。相同本轮提示、native schema、用户规则与执行器，只改变payload表示；不是拿18轮旧词元与19轮新词元直接比。实际字段和字符数在CONTEXT_FIELDS，完整messages/tools在context/model_calls。

原字段为interaction_history/framework_state/candidate_work/remaining_budget，精简字段为current_goal/current_change/affected_judgments/missing_preconditions/相关规格与候选/证据索引/短操作反馈等。程序完整存储目录和历史；已请求的原生结果或选定证据只在下一轮提供一次。六个业务候选及门槛仍由同一函数产生；取证入口两侧共同提示都可用，精简表示额外显式列出，本批四条诊断均未调用，不能把该包宣称为纯删除某一目录字段的单因素消融。

开发联调pilot02因没有已完成工作反馈而连续查询至预算停止；pilot03补回短反馈/正式来源/条件状态后7步正确结束。失败保留，未进入32条正式。本轮精简保留执行反馈是必要设计观察，但单个开发修复不能给出因果或普遍收益证明。

## 局限与复现

四道受控单商品续行，不是原τ²-bench全部私有用户任务得分；每组合两次、成本诊断每状态一对，顺序固定，不能做普遍收益判断。用户回复较结构化，含明确SKU；模拟语义提取有潜在误读，虽本批无确认的解析偏离，仍需独立复核。对不合格方案的用户反馈只统一要求正确完整方案，不逐项指出错额，可能放大重复算错；后续可同规则复验更具体反馈。真实用户自由语言的状态抽取未验证。

证据按需交付接口已做事后零模型本地补测：指定ref的原记录能交付下一请求，随后清空；本批4条成本诊断没有在线调用取证，因此不能宣称已验证所有缺口检索场景。SUPPLEMENTAL_CHECKS和local_negative_controls还保存了无授权原生写入/框架拦截两条本地负对照，独立评分均判不正确，它们不是正式轨迹或新模型样本。

框架状态对当前控制消息消费同源结构化语义，程序负责引用/依赖/条件/金额/授权绑定，模型选择工作和对象。未将受控模块的结果解释成通用认知能力。需要更多任务、其他模型、独立语义审阅及真实用户表达，才判断适用范围。暂不训练、不生成偏好标签。

32项离线检查、官方/框架联调、最终冻结及唯一正式32条均留档，4条成本诊断单列。AUDIT核对3303个旧实验/申报书/官方源码文件未变，冻结输入未变；原始失败不回改。README列出入口和复算顺序，frozen_inputs保存冻结材料和官方原代码，DELIVERY_MANIFEST提供全部交付哈希。
'''
(R/'results/RESULTS.md').write_text(report,encoding='utf-8')
(R/'README.md').write_text('''# 第19轮：官方Agent基线与上下文精简

主实验32条：官方与精简框架均14/16正确，原始失败保留。两处同状态各原/精简续行共4条均正确；输入分别降低50.0%、42.4%。不是框架普遍优于官方的证据。

- results/MAIN_PAIRED_RESULTS.md：官方对精简框架；CONTEXT_PAIRED_RESULTS.md：同状态原/精简成本。
- results/RESULTS.md：回答与归因；BY_TASK.json、MAIN_RESOURCE_PAIRS、CONTEXT_PAIRS/CONTEXT_FIELDS：逐项数据。
- configs/PROTOCOL、prompts19、budget、official_integration、tasks、snapshots、offline、freeze：方案及冻结。
- src/run19：官方原消息/工具循环与框架调度；transport19：共同模型/日志；world19：精简及框架执行；user19：实际话术驱动受控用户；score19：冻结独立评分。复制的18轮World/Ledger是框架依赖，绝不用于拦截官方工具。
- results/main：32条原始请求/响应/每轮状态/用户解释/真实DB；context：4条同状态请求；pilot01/02/03：联调及过度精简失败。
- FACTS/FACT_REVIEW/SPEECH_PACKET/AUTO_FACTS、ACCOUNTING、MODEL_VERSIONS、AUDIT、frozen_inputs、DELIVERY_MANIFEST：核验、分账、哈希。
- TRACE_ARITHMETIC_FAILURE、TRACE_OFFICIAL_DYNAMIC、TRACE_RESOURCE_RECOVERY：完整代表轨迹。

唯一运行环境 D:/experimentn/tau2-official/.venv/Scripts/python.exe。已启动批次不要再次execute覆盖。离线复算：post19 packet→review19→score19→post19 tables→report19；均无模型调用。报告/复核/审计脚本为事后分析，未冒称冻结前存在。旧01–18和申报书只读，无偏好标签或训练。
''',encoding='utf-8')
(R/'results/DEVELOPMENT.md').write_text('''# 开发与正式批次边界

pilot01：官方6稳定/27变化均用自然语言完整方案获批并真实native换货。pilot02：首版精简丢失已完成查询反馈，27变化重复query至9操作预算，零写入；完整失败保留。开发加入短操作反馈、正式来源/条件许可与业务终态，pilot03同题正确7步结束。

正式前增加框架直用native提交的独立尝试日志及按需原始结果一次性交付，并保留预运行清单pre_run_freeze_review；最终32项检查通过后生成用于正式的freeze。未在正式中改实现或替补失败。共同用户支持基于正确自然语言完整方案批准，规格许可与最终授权可在同一句中分别满足，避免强迫官方走项目helper。

main只启动一次，32条全部保存；context只启动一次4条。main有2次Agent网络失败、1次模拟侧网络失败，全部保留。用户语义输出和实际话术留档，不根据后续结果改回复。

事后review19在写完事实文件后，终端GBK无法打印Unicode减号导致显示错误；UTF-8文件不受影响。后续使用UTF-8显示，评分离线重算未请求模型。最初完整质量pending时不做投入比较；语义核对完成后按同一冻结规则生成最终两表。

post/review/report/audit为事后分析，不改变冻结执行或程序评分规则。语义复核同一助手、非独立盲审。无训练与偏好标签。
''',encoding='utf-8')
from importlib.metadata import version,PackageNotFoundError
packages={}
for package in ('openai','pydantic','litellm','toml'):
 try:packages[package]=version(package)
 except PackageNotFoundError:packages[package]='unknown'
save(R/'results/ENVIRONMENT.json',{'python':sys.version,'executable':sys.executable,'packages':packages,'recorded_after_run':True,'official_sources':'frozen_inputs/official_source; hashes in configs/freeze.json'})
save(R/'results/DELIVERY_MANIFEST.json',{'utc':datetime.now(timezone.utc).isoformat(),'files':{str(p.relative_to(R)):sha(p) for p in R.rglob('*') if p.is_file() and '__pycache__'not in p.parts and p.name!='DELIVERY_MANIFEST.json'}})
print({'formal':len(s['main']),'context':len(s['context']),'main_correct':sum(r['final_correct'] for r in s['main']),'frozen_unchanged':True})
