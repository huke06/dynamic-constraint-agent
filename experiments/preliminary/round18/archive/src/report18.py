"""Post-run document assembly; no models, no score/decision rule changes."""
import json,hashlib,shutil,sys
from pathlib import Path
from datetime import datetime,timezone
from importlib.metadata import version,PackageNotFoundError
R=Path(__file__).resolve().parent.parent
def read(p):return json.loads(p.read_text('utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return [json.loads(x) for x in p.read_text('utf-8').splitlines()]
s=read(R/'results/SUMMARY.json');xp=read(R/'results/EXPLORATORY.json');api=rows(R/'results/main/model_calls.jsonl');ep=rows(R/'results/exploratory/model_calls.jsonl');f=read(R/'configs/freeze.json')
audit=read(R/'results/AUDIT.json');prefix_checks=[]
for tid in ('6','27','75','77'):
 for rep in (1,2):
  for group in ('free','framework'):
   aa=read(R/f'results/main/t{tid}_stable_r{rep}_{group}_trajectory.json');bb=read(R/f'results/main/t{tid}_changed_r{rep}_{group}_trajectory.json');ha=next(e['after']['history'] for e in aa if e.get('decision',{}).get('action')=='confirm' and e['check']['allowed']);hb=next(e['after']['history'] for e in bb if e.get('decision',{}).get('action')=='confirm' and e['check']['allowed']);prefix_checks.append(ha==hb[:len(ha)])
audit['checks']['actual_prechange_public_dialogue_identical_across_versions']=all(prefix_checks);assert all(prefix_checks);save(R/'results/AUDIT.json',audit)
# Preserve a second complete paired repeat from the task with observed differences.
text=['# 登山靴27变化版第2次：两组完整续行','原始完整每轮状态位于main对应trajectory.json；下列按顺序呈现所有尝试、反馈、用户交互与授权。','']
for group in ('free','framework'):
 n=f't27_changed_r2_{group}';text+=['## '+group,'']
 for i,e in enumerate(read(R/f'results/main/{n}_trajectory.json')):
  text+=['### 第'+str(i+1)+'次尝试','模型：'+json.dumps(e.get('decision'),ensure_ascii=False),'执行核验：'+json.dumps(e.get('check'),ensure_ascii=False),'实际结果：'+json.dumps(e.get('result'),ensure_ascii=False)]
  for ref in (e.get('assistant_ref'),e.get('user_ref')):
   if ref is not None:text+=[e['after']['history'][ref]['role']+'：'+e['after']['history'][ref]['content']]
  if e['after']['event'] and not e['before']['event']:text+=['实际变化：'+json.dumps(e['after']['event'],ensure_ascii=False)]
  text+=['执行后证据：'+json.dumps({'desired':e['after']['desired'],'permission_source':e['after']['permission_source'],'records':e['after']['ledger']['records']},ensure_ascii=False)]
(R/'results/TRACE_TASK27_REPEAT2.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
acc=read(R/'results/ACCOUNTING.json')
for row in acc['primary']:
 rs=next(r for r in s['rows'] if r['id']==row['id']);row['shared_initial_real_simulated_queries']=4;row['shared_driver_event_queries']=int(rs['event_triggered'] and rs['change_type']=='resource');row['agent_model_request_wall_seconds']=sum(a['seconds'] for a in api if a['branch']==row['id'])
acc['executor_time_note']='world.execute wall/CPU covers local tool and controlled-user execution, not model request time; model request elapsed seconds are separately recorded. Full framework-only overhead is not isolated.'
acc['exploratory']=[{k:r[k] for k in ('id','continuation_steps','prefix_steps','calls','prompt_tokens','completion_tokens','returned_tokens','missing_usage')} for r in xp['rows']]
save(R/'results/ACCOUNTING.json',acc)
explines=['# 探索性：同状态直接决策 vs 显式候选','','不计入32条主实验，不作偏好标签。基础状态来自预定主实验框架组第1次事件后的实际快照；两分支完整起点逐字相同，只有提示是否提供候选不同。','', '|状态|直接/候选首步|续行步骤|请求|直接词元|候选词元|两侧质量|','|---|---|---|---|---:|---:|---|']
for tid in ('6','75'):
 a,b=[next(r for r in xp['rows'] if r['id']==f'diag_t{tid}_{g}') for g in ('state_direct','framework')];explines.append('|'+ '|'.join(map(str,[tid,a['first_after_change']['action']+'/'+b['first_after_change']['action'],str(a['continuation_steps'])+'/'+str(b['continuation_steps']),str(a['calls'])+'/'+str(b['calls']),a['returned_tokens'],b['returned_tokens'],str(a['quality'])+'/'+str(b['quality'])]))+'|')
explines+=['','台灯两分支都澄清后重拟方案；耳机两分支都先拟新方案。未观察到候选列表额外减少步骤/请求，候选输入增加词元。两状态各仅一对，且未包含主实验出现最明显差异的登山靴状态，不能据此把其差异归因于状态维护、前提核验或候选中的任何单一因素。','框架提示要求独立comparison字段，但本轮所有145次模型响应均未提供该字段；冻结校验器只强制action/reason/claims。因此确认的是“获得候选及前提后的选择”，不能声称已观测或验证模型逐项比较过程。','候选额外输入只在framework分支，state_direct保留同样显式状态和共同检查。尚未做“有无状态×有无检查×有无候选”的因子实验。']
(R/'results/EXPLORATORY.md').write_text('\n'.join(explines)+'\n',encoding='utf-8')
proof={}
for tid in ('6','75'):
 a=read(R/f'results/exploratory/diag_t{tid}_state_direct_start.json');b=read(R/f'results/exploratory/diag_t{tid}_framework_start.json');proof[tid]={'starts_identical':a==b,'common_snapshot_sha256':sha(R/f'results/exploratory/t{tid}_common_snapshot.json'),'both_same_as_common':a==read(R/f'results/exploratory/t{tid}_common_snapshot.json')}
save(R/'results/BRANCH_REPRODUCIBILITY.json',proof);assert all(v['starts_identical'] and v['both_same_as_common'] for v in proof.values())
for name in f['files']:
 dest=R/'results/frozen_inputs'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/name,dest)
shutil.copy2(R/'configs/freeze.json',R/'results/frozen_inputs/freeze.json')
packages={}
for pkg in ('openai','pydantic','litellm','toml'):
 try:packages[pkg]=version(pkg)
 except PackageNotFoundError:packages[pkg]='not found in this interpreter'
save(R/'results/ENVIRONMENT.json',{'python':sys.version,'executable':sys.executable,'packages':packages,'recorded_after_run':True,'external_source_hashes_in':'configs/freeze.json read_only_sources','model_versions':s['versions']})
report=f'''# 第18轮：动态约束下完整框架对照结果

## 主结果：最终办理没有拉开差异

4个独立基础任务，稳定/变化两版本，两组各两次，共32条正式新轨迹；全部启动并保留。两组各16/16最终正确：各14次正确登记换货申请、2次在撤回后正确停止且数据库不变。稳定版各8/8正确；变化版各8/8正确。没有未到触发点、提前预算停止、未办结或正式替补。

“正确登记”均为真实RetailTools返回exchange requested，与数据库一致；不是实物换货或退款到账。28次写入逐项核对规格、原订单/商品、原支付、精确差额、有效用户许可和当前完整方案独立授权。4次撤回结果核对无写入、明确停止和全DB未变。主实验不存在“底层拦住非法提交后把不写入当成功”的情况：实际不当提交尝试为0，但存在3次未推进业务的澄清对象错误，另行记录。

主配对表在PAIRED_RESULTS.md，按任务和变化类型分别见BY_TASK.md/JSON、BY_CHANGE_TYPE.json。独立题数是4，不是32；资源变化2题，规格修改与撤回各1题。两次重复采用新请求，温度0不等于提供方完全确定。

## 按任务观察

|基础题|稳定版两组两次|变化版两组两次|实际差异与波动|
|---|---|---|---|
|6 台灯|均prepare→confirm→submit，3步|均clarify→prepare→confirm→submit恢复，全程6步|两组都先问1569765161，用户实际回复许可9190635437；工作路线无组间差异。框架稳定第2次有一处理由门槛误述，第1次没有|
|27 登山靴|均3步正确登记|均最终使用6159919747并新授权，6个成功工作|自由组两次首次clarify错误指向缺货原规格8277474082；分别拒绝2次、1次后恢复，模型请求8/7次；框架均6次，直接问其他规格（两次对象不同）|
|75 耳机|均3步正确登记|两组都首先prepare9580569596，再独立confirm、submit，全程5步|没有复用旧4063058357授权；路线相近，重复方向一致|
|77 香水|均3步正确登记|两组收到撤回后第一步均stop，全程3步，无写入|两次方向一致；停止也是正确完成，不把它当失败|

变化只在实际第一次完整方案确认之后、首次提交之前触发。16条变化轨迹全部达到该阶段，资源变化向两组公开同一真实模拟商品查询结果；规格/撤回发送相同用户原话。所有16条变化轨迹的身份、用户资料、订单和支付依据保持有效，旧方案/授权影响及新来源在每轮before/after和event_snapshot可追溯。变化版没有被模型提早知道；同题两版本同组的实际首次messages逐字相同。

资源事件已经给出完整最新库存，因此模型无需再查就可澄清；本批没有Agent主动query。耳机新规格原先已观察有货且模拟库存没有变化，因此允许沿用有效库存依据，不机械要求重查。共同接口仍允许任意阶段重新查询，没有第17轮已知库存不能查询的适用性限制。缓存整理、重新查询和用户许可是不同工作，本轮未把它们混为收益。

## 中间错误：与最终正确分开

结构化事实断言508条，3条冲突都在自由组登山靴变化轨迹：两次初始prepare错误断言已有当前交易授权，第1次获得替代规格许可后又错误断言已有最终授权。用户原话明确两者均不是最终批准，程序证据能确定这些错误。实际模型仍请求了完整方案确认，所以没有造成错误提交；不能以最终正确覆盖断言问题。

全部145次原始自然理由（主实验131、探索14）另作语义复核，4处问题保留原句与契约：J005/J103/J138对应自由组3次澄清对象错误，把询问其他规格的预期作用绑定到同一个缺货原规格；其中J138收到明确拒绝后仍重复。库存缺货和旧授权失效判断本身正确，不能误报成未读懂缺货或违规提交。

J135属于框架组台灯稳定版第2次：原句“confirm/submit remain unauthorized until independent approval”把confirm也说成需要先获独立批准。共同契约要求confirm有当前已准备方案，并由它获得批准；只有submit需要最终授权。实际随后仍正确confirm，这是一处理由中的额外前提，非执行失败。

未发现把尚未接受说成明确拒绝、把未知库存说成缺货、把存在但无货说成不存在，或把历史兼容性增加为提交门槛。程序生成的52次主实验澄清/确认话术均通过时点证据核验。另用继承的fact_verifier.replay按assistant_ref排除未来记录，独立重放主实验52次及探索6次话术，核对目录存在性、当时库存、Decimal差额和支付，58次均通过，详见FACTS.json。自然理由复核为同一助手阅读、混排遮蔽标识；进度核查时已看过部分具名轨迹，且表达可暴露来源，不是独立完全盲审。SEMANTIC_ITEMS/REVIEW_PACKET保留所有语义判定和证据，程序claims与话术评分在SUMMARY逐条保留，二者不互相覆盖。

冻结完整质量标准下自由组14/16、框架组15/16；稳定版自由8/8、框架7/8，变化版自由6/8、框架8/8。三个受影响轨迹不是三个独立业务题，也不是最终失败。该小差异不足以宣称总体优势，单条语言判定还需独立复核。

## 同等质量后的投入

13/16配对两侧完整质量且用量完整，步骤及请求数差都为0；这些配对自由组词元均较少，F−K范围−18479至−7411，合计−143489。其余3配对不计算资源差：登山靴变化两次及台灯稳定第2次。登山靴8/7对6次请求只是过程记录，不拿不等质量配对作效率收益结论。

正式主批131次请求全部成功，服务返回总词元833870，缺失usage0。自由组原始总计67次/329655词元，框架64次/504215词元；这些原始总量包含不等质量记录，不作总体投入排名。框架显式状态、出处和候选增加输入，是较高词元的可能直接来源；本轮未分解纯程序成本与其后续影响。

Agent输入/输出、提供方缓存命中、初始公共工具记录和外部库存事件查询在ACCOUNTING分别列出：初始每条4次真实模拟查询，共128次；资源事件驱动8次，Agent提交28次，没有Agent主动库存查询。公共前缀已包含在Agent输入，提供方没有独立前缀token拆分，单独值未知。受控用户及本地外部语义复核不调用实验API，模型用量0；不把模拟用户词元计进Agent。执行器局部CPU/耗时与模型请求耗时分列，纯框架模块开销未独立隔离。

实际返回模型/指纹deepseek-flash / bc19ba97cbe016479903222bb1578db6，131次一致；探索14次亦单独记录。别名与指纹不保证后端权重可永久复现。温度、重试和预算两组相同，最大单轨迹返回57107词元，未触发60000软阈值；无超时、网络/服务/解析异常，日志接口仍保留这些分类、脱敏和可用请求编号。程序3次拒绝另记，不伪装成服务失败或抹去请求开销。

## 探索诊断与原因解释

EXPLORATORY.md记录两个预定事件状态的“显式状态直接决策 vs 显式候选”各一次续行，共4条，不进主实验。台灯两分支均4个新工作/4请求，耳机均3/3，全部正确；候选没有减少工作，词元各多1935、1365。完整起点逐字一致，BRANCH_REPRODUCIBILITY、exploratory/common_snapshot、start/messages/trajectory保留可复现分支，供后续研究使用，无偏好标签。

观察到：主结果相近；登山靴完整框架更少出现错误澄清对象和授权断言，其余动态路线相近。可能原因：显式当前许可、失效记录和候选前提帮助定位操作对象；共享底层反馈也帮助自由组恢复。还需证据：本轮同时改变状态维护与候选呈现，没有拆出各因素；两状态诊断都表现相近且未覆盖最明显差异的登山靴，不能定位收益来自状态维护、检查还是候选选择。

此外，框架提示要求comparison字段，但所有145次响应均未提供，冻结校验只强制action/reason/claims。故本轮验证了候选输入后的选择，不声称已观测逐项比较的计算过程。未事后修改提示或补跑成功样本；该限制和旧plan缓存字段仍保留历史值、靠契约指纹判效的实现细节，留待下一轮改进。

## 范围、留档与后续证据

这是本地公开基准模拟数据上的受控续行比较，非τ²-bench原始私有用户全流程得分。四题的原题和改编分别存configs/tasks；改编明确处理范围和规格、使用原支付：台灯差额初始+12.07/替代+15.29；靴初始−23.99/替代−0.81；耳机初始+16.85/新规格+30.89；香水−10.48。原题返回、偏好细节等未覆盖的部分不冒称已完成。

自由组也获得同一报价、澄清/确认辅助和隐藏底层业务检查，因此是相同工具条件下的自由决策对照，并非没有程序辅助的裸模型。受控用户提供固定自然表达及同源结构化语义，本轮不证明任意自然语言解析能力；库存更新完整公开、任务单商品且容易观察、用户配合、任务和版本运行顺序固定，都限制外推。每组合仅两次，未做显著性或普遍收益判断。

第16轮相机52、第17轮头盔70共24条旧写入回归通过，旧理由错误原样保留。68项离线检查通过后冻结，再执行唯一32条主批及单列4条探索；未替补失败。AUDIT核对旧01–17目录、申报书和基准数据源码3081个只读文件，均未变化；冻结输入逐项哈希一致。冻结清单、实际请求和原始轨迹全部保存，事后评分语义审阅与报告脚本明确区分。当前不训练、不生成偏好标签。

至少两套解释差异的完整对照轨迹：TRACE_TASK27.md（第1次，两组）和TRACE_TASK27_REPEAT2.md（第2次，两组）；另有TRACE_TASK6与TRACE_TASK75展示相近路径。后续需要独立语义复核、更多基础任务和用户表达，并对状态维护/前提反馈/候选单独消融，才能判断整体框架的收益和适用范围。
'''
(R/'results/RESULTS.md').write_text(report,encoding='utf-8')
(R/'README.md').write_text('''# 第18轮：动态约束下完整框架对照

4道基础题×稳定/变化×自由/框架×两次=32条正式轨迹。两组最终均16/16正确（各14次登记、2次正确停止）；完整质量自由14/16、框架15/16。无最终成功率差异；中间错误与投入单列。探索4条不计入主实验。

- results/RESULTS.md：主结论与局限；PAIRED_RESULTS.md：16组配对；BY_TASK.md/JSON、BY_CHANGE_TYPE.json：按基础题与类型。
- results/TRACE_TASK27.md、TRACE_TASK27_REPEAT2.md：两次登山靴完整对照；TRACE_TASK6/75.md：相近路线。
- configs/PROTOCOL.md、budget/prompts/tasks、offline/additional_offline、freeze.json：方案、原题/改编、离线、冻结。
- src/construct18/world18/run18/score18：冻结构造、依赖状态、共享执行、运行、程序评分；复用exchange_core/logging16/fact_verifier资源。score18使用同一最新观察/Decimal逻辑，语言审阅与模板事实另列。
- results/main：32条start/trajectory/final/event快照、原始model_calls和request_events；用户与真正工具结果均在history。原始文件不改。
- results/exploratory、EXPLORATORY.md/JSON：同状态分支、提示及续行；BRANCH_REPRODUCIBILITY.json：逐字起点校验。
- SEMANTIC_ITEMS/REVIEW_PACKET/MAPPING、SUMMARY、ACCOUNTING、MODEL_VERSIONS、AUDIT、ENVIRONMENT、frozen_inputs、DELIVERY_MANIFEST：复核和复现。

运行环境 D:/experimentn/tau2-official/.venv/Scripts/python.exe。setup18→run18 freeze→execute→diagnostic；已运行批次不可再次execute覆盖。离线复算可运行review18→score18→post18 deliver→report18，不产生模型请求。review/post/report是事后分析，不冒称冻结时存在。旧01–17和申报书只读，无训练或偏好标签。
''',encoding='utf-8')
dev=R/'results/DEVELOPMENT.md';dev.write_text(dev.read_text('utf-8') if '第一次误用系统Python' in dev.read_text('utf-8') else dev.read_text('utf-8')+'\n事后自然理由复核第一次误用系统Python，因缺少toml而终止；改用已规定虚拟环境后完成。没有修改冻结代码或重新请求模型。第一次离线汇总在自然理由未完成时将完整质量置pending，因此暂计0；语义审阅完成后按同一冻结规则离线重算为29/32，不是正式批次替换。\n',encoding='utf-8')
assert all(sha(R/p)==v for p,v in f['files'].items())
save(R/'results/DELIVERY_MANIFEST.json',{'utc':datetime.now(timezone.utc).isoformat(),'files':{str(p.relative_to(R)):sha(p) for p in R.rglob('*') if p.is_file() and '__pycache__'not in p.parts and p.name!='DELIVERY_MANIFEST.json'}})
print({'primary':len(s['rows']),'correct':sum(r['final_correct'] for r in s['rows']),'quality':sum(r['quality'] for r in s['rows']),'exploratory':len(xp['rows']),'frozen_unchanged':True})
