"""Post-run delivery/integrity/archive only; no API imports or calls."""
import json,hashlib,shutil,re
from pathlib import Path
from collections import Counter
E=Path(__file__).resolve().parents[1];R=E.parents[2];A2=E/'versions/a2';V=R/'experiments/preliminary/round23-framework-loop/versions/v2'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calls(out):return [json.loads(l) for l in (out/'model_calls.jsonl').read_text('utf-8').splitlines()]
def totals(cs):
 return {'requests':len(cs),'input':sum(c['usage']['prompt_tokens'] for c in cs if c.get('usage')),'output':sum(c['usage']['completion_tokens'] for c in cs if c.get('usage')),'cache_hit':sum(c['usage'].get('prompt_cache_hit_tokens',0) for c in cs if c.get('usage')),'cache_miss':sum(c['usage'].get('prompt_cache_miss_tokens',0) for c in cs if c.get('usage')),'unknown_usage':sum(c.get('usage') is None for c in cs),'failed':sum(c['status']!='success' for c in cs),'seconds':sum(c['seconds'] for c in cs),'roles':dict(Counter(c['role'] for c in cs))}

def main():
 phases=[(name,E/'results'/name) for name in ('pilot01','pilot02','pilot03','A01','B01')]+[('a2/'+name,A2/'results'/name) for name in ('pilot04','A01')]
 accounting={};allc=[];raw=[];ext=Path('D:/experimentn/research-raw-archives/round24-official-and-trajectory')
 for phase,out in phases:
  cs=calls(out);allc+=cs;accounting[phase]={'agent':totals([c for c in cs if c['role']!='simulator']),'simulator':totals([c for c in cs if c['role']=='simulator']),'trajectory_count':len(read(out/'OUTCOMES.json'))}
  for f in out.iterdir():
   if not f.is_file() or not (f.suffix=='.jsonl' or f.name.endswith(('_start.json','_trace.json','_final.json','_simulator.json')) or f.name=='OUTCOMES.json'):continue
   dest=ext/f.relative_to(E);dest.parent.mkdir(parents=True,exist_ok=True)
   if not dest.exists():shutil.copyfile(f,dest)
   assert sha(f)==sha(dest)
   raw.append({'source':str(f),'archive':str(dest),'sha256':sha(f),'bytes':f.stat().st_size})
 save(E/'RAW_ARCHIVES.json',{'originals_preserved':True,'external_archive_root':str(ext),'files':raw,'total_bytes':sum(f['bytes'] for f in raw)})
 save(E/'results/GLOBAL_ACCOUNTING.json',{'phases':accounting,'all':totals(allc),'returned_models':dict(Counter(c.get('response',{}).get('model','none') for c in allc)),'external_judge_api_calls':0,'orchestration_chat_cost':'unknown, excluded','formal_trajectories':44,'development_trajectories':12,'no_training':True})
 freezes={}
 for p in (V/'configs/FREEZE.json',E/'configs/FREEZE.json',A2/'configs/FREEZE.json'):
  f=read(p);assert all(sha(R/k)==v for k,v in f['files'].items());freezes[str(p.relative_to(R))]={'sha256':sha(p),'files':len(f['files']),'unchanged':True}
 starts={}
 for scope,base,tasks in [('A01',E,('80','23','29','39')),('A2',A2,('80','23','29','43'))]:
  for tid in tasks:
   for rep in (1,2):
    prefix=f'A_t{tid}_r{rep}_';out=base/'results/A01';equal=read(out/(prefix+'official_start.json'))==read(out/(prefix+'framework_start.json'));assert equal;starts[scope+'/'+prefix]=equal
 for s in read(E/'configs/B/states.json'):
  for rep in (1,2):
   prefix=f'B_{s["id"]}_r{rep}_';out=E/'results/B01';equal=read(out/(prefix+'analyze_start.json'))==read(out/(prefix+'clarify_start.json'));assert equal;starts['B/'+prefix]=equal
 # Actual Agent inputs never contain simulator oracle/configured future event keys.
 leaks=[]
 for c in allc:
  if c['role']=='simulator':continue
  text=json.dumps(c['messages'],ensure_ascii=False)
  if any(k in text for k in ('environment_only','env_approvals','changed_target','change_type')):leaks.append(c['branch'])
 assert not leaks
 # Audit A2 resource event is a genuine tool-role message in the actual next request.
 event_inputs=[]
 for rep in (1,2):
  n=f'A_t23_r{rep}_official';cs=[c for c in calls(A2/'results/A01') if c['branch']==n and c['role']=='cognitive'];first=cs[1]
  tail=first['messages'][-3:];assert [m['role'] for m in tail]==['user','assistant','tool'];r=json.loads(tail[-1]['content']);assert r['variants']['8926329222']['available'] is False
  event_inputs.append({'id':n,'response_id':first['response']['id'],'roles':[m['role'] for m in tail],'tool_result_sha256':hashlib.sha256(tail[-1]['content'].encode()).hexdigest(),'observed_unavailable':True})
 save(E/'results/INTEGRITY_AUDIT.json',{'freezes':freezes,'equal_paired_starts':starts,'actual_A2_event_inputs':event_inputs,'Agent_future_key_leaks':leaks,'raw_archive_hashes_match':True,'new_after_freeze_files':'post24.py/post24a2.py/finalize24.py are post-run only, never imported by execution'})
 # Retain the original A01 table, expose the current A2 table at the top level.
 if not (E/'results/A01_OFFICIAL_PAIRS.md').exists():shutil.copyfile(E/'OFFICIAL_PAIRS.md',E/'results/A01_OFFICIAL_PAIRS.md')
 shutil.copyfile(A2/'OFFICIAL_PAIRS.md',E/'OFFICIAL_PAIRS.md')
 b=read(E/'results/B01/SCORES.json');a=read(A2/'results/A01/SCORES.json');pairs=read(A2/'results/A_PAIRS.json');eligible={n for p in pairs if p['comparable'] for n in p['ids']}
 cmp={}
 for g in ('official','framework'):
  rs=[s for s in a if s['group']==g and s['id'] in eligible];cmp[g]={k:sum(s['agent'][k] for s in rs) for k in ('calls','input','output','cache_hit','cache_miss','seconds')};cmp[g]['wall_seconds']=sum(s['seconds'] for s in rs)
 save(E/'results/A2_COMPARABLE_ACCOUNTING.json',cmp)
 # Candidate references contain visible input separately from evaluation-only snapshots.
 cands=read(E/'results/DPO_CANDIDATES.json')
 for c in cands:
  sid=c['state'];n=f'B_{sid}_r1_analyze';out=E/'results/B01';tr=read(out/(n+'_trace.json'));other=read(out/(f'B_{sid}_r1_clarify_trace.json'))
  c.update(first_work_instructions={'analyze':tr[0]['model_original_choice'],'clarify':other[0]['model_original_choice']},source_visible_snapshot=str(out/(n+'_visible_start.json')),visible_input_sha256=sha(out/(n+'_visible_start.json')),repetitions=[{'analyze':f'B_{sid}_r{rep}_analyze','clarify':f'B_{sid}_r{rep}_clarify'} for rep in (1,2)],qualification='Full work+object+offered SKU and common continuation are compared, not a universal work-type ranking. Inferior soft preference is scored, not filtered as hard failure. No chosen/rejected training pairs emitted.')
 save(E/'results/DPO_CANDIDATES.json',cands)
 # Retained evidence: unaffected requirement, original source, identity/payment and old approval.
 state_evidence=[]
 for tid in ('23','29'):
  for rep in (1,2):
   n=f'A_t{tid}_r{rep}_framework';tr=read(A2/'results/A01'/(n+'_trace.json'));ix=next(i for i,e in enumerate(tr) if e['module']=='public_change');ev=tr[ix]['event'];cfg=ev['state']['cfg'];unchanged=cfg['scope'][1];key='requirement:'+unchanged
   nextsem=next(e for e in tr[ix+1:] if e['module']=='semantic_update');before=ev['before_records'];after=nextsem['after']['core']['records']
   state_evidence.append({'id':n,'event':ev['state']['change'],'unaffected_original_item':unchanged,'unaffected_requirement_same':before[key]==after[key],'identity_value_same':before['identity']['value']==after['identity']['value'],'payment_value_same':before['payment']['value']==after['payment']['value'],'before_targets':ev['state']['targets'],'after_semantic_targets':nextsem['after']['targets'],'old_authorization_after_event':ev['after_records'].get('authorization'),'current_complete_write':read(A2/'results/A01'/(n+'_final.json'))['writes']})
 assert all(s['unaffected_requirement_same'] and s['identity_value_same'] and s['payment_value_same'] for s in state_evidence)
 save(E/'results/STATE_TRANSITIONS.json',state_evidence)
 make_report(a,b,cmp,accounting,raw,cands)
 print({'formal':44,'development':12,'API_requests':len(allc),'archive_files':len(raw),'archive_mb':round(sum(x['bytes'] for x in raw)/1e6,2),'comparable_A2_pairs':len(eligible)//2})

def make_report(a,b,cmp,accounting,raw,cands):
 totals_api=sum(v['agent']['requests']+v['simulator']['requests'] for v in accounting.values());o=cmp['official'];f=cmp['framework'];sft=[json.loads(l) for l in (E/'results/B1/SFT_EXAMPLES.jsonl').read_text('utf-8').splitlines()]
 text=f'''# 第24轮：官方对照与轨迹样本验收

## 本轮完成了什么

A与B均已完成计划内采样与逐条审阅。**当前A以独立冻结a2为主：两组各8/8正确登记；在6个控制与质量可比配对中，双方均通过，未显示办理质量差异。** 全批事实/授权/运行严格质量官方6/8、框架8/8，但43题恢复过程受模拟回应和输入精度偏差影响，不能据这两条宣称框架的恢复成功率或成本收益。 B有12条正确登记，其中9条达到事实/来源/运行完整口径；26题形成两个有业务依据、方向相反的稳定路径偏好候选，35暂不验收。

本轮实际保留：初始A01正式16条、修订A2正式16条、B01正式12条，共**44条正式轨迹**，另有三批初始联调10条和a2联调2条。没有把旧正式失败改称联调、删除或替补，没有把跨版本合并为更大的独立样本。第23轮v2以及本轮两个冻结hash均核对无变化。框架仍是同一份状态约束与建模、认知决策、任务执行与反馈，不是另修后的决策器。

## A：控制、偏差和官方循环

官方运行本地原生LLMAgent.generate_next_message与RetailTools，completion仅换成共同API传输和日志；不向它提供项目状态摘要、候选、prepare辅助、模板确认或项目提交门禁。完整框架用冻结23v2的candidate入口，每轮由模型选工作，确定性核验/算价/模板/反馈在框架侧。不能把这些程序分工解释为模型单独推理提升。模型仍deepseek-flash、temperature0、thinking disabled，预算40次Agent请求、180000已知词元、24操作、35轮，重试规则统一。实际返回别名/model/responseID/cache原字段保留；别名不代表可核验的固定权重修订。

初始A01（80/23/29/39）保留在results/A01。离线先过50项、联调检查多选和批准，正式后仍发现资源事件来源形式不一致：官方得到用户转述JSON，框架得到真实工具记录。官方先查询有来源核实理由，原23两对不作成本证据。39第二次还有正确方案被提取器伪造引文误拒。原39第二次评分按列表顺序误判scope，独立canonical成对映射复核另表纠正，原OUTCOMES不覆盖。细节在[偏差记录](results/DEVIATIONS.md)。

a2在新目录修实验环境，58项离线和旧23两条联调后重新冻结：资源更新实际assistant-call/tool-result角色链原样交两组；要求变化仍是实际user原话。正式为80稳定、23库存变化、29用户改一项要求、43初始cap冲突，各组两次。43没有参与本轮模型调试；39已见，不再作为新题。43原题是身份/地址业务，本轮从其公开已交付订单抽相机与键盘做受控换货；原题、改编配置分别留档，不能称原题benchmark成功。其他题也为固定办理阶段的受控续行。

模拟用户由实际话术触发同一个提取器，程序核对当时可见目录/库存、literal SKU、原支付、Decimal整单差额与cap。新规格许可和完整交易批准分开；变化只由真实完整旧方案批准触发。两组每个配对完整起点一致；a2实际下一请求中的资源记录已核对为tool角色，不是用户粘贴。所有写入都可追到当次完整批准和正确映射，没有未授权工具尝试。配对表见[OFFICIAL_PAIRS.md](OFFICIAL_PAIRS.md)，详细SCORES与原提取在versions/a2/results。

本批停止于首次实际写入，状态是exchange requested，不表示实物换货或退款到账。官方写入后的自然语言回执没有继续采样；投入不包含它，不能与21轮含回执、且框架自动连续推进的口径直接比较。

## A：观察到什么、哪些原因仍不能分开

|题|结果与关键首步（a2）|能支持什么|
|---|---|---|
|80稳定|双方两次均正确，官方自然语言完整方案→批准→原生提交；框架prepare→confirm→解析→submit|前提齐备时双方可办；v2细分步骤有额外模型往返|
|23资源|双方收到同源tool更新后，首个业务工作均是澄清行李箱6301799585的替代许可；官方在新许可后再查一次库存，框架利用已有有效证据|原A01的“先重新查 vs 先澄清”差别在统一来源后消失；不能把旧差别当作框架收益。后续刷新可理解为核对“if still in stock”，不自动判无效|
|29要求变化|官方先查水管product6679515468，再完整拟案；框架先解释当前新消息，首个业务工作prepare新整单|双方都保留登山靴8277474082、身份和原支付，并重新取得完整授权。显式状态留下可审计的来源/失效链；官方仅按历史与参数核验，不补造状态维护记录|
|43冲突|框架一次analyze→clarify，一次直接clarify，均先取得相机6700049080许可；官方两次把-27.65误判满足<=-56.105，用户拒绝后继续|程序核定的cap与前提能帮助框架避免不可行拟案。但两次官方还受到后述模拟偏差，恢复时长/成功差不能单独归因|

框架三个模块的证据在[STATE_TRANSITIONS.json](results/STATE_TRANSITIONS.json)：变化影响A的库存/要求、旧完整授权失效；B的requirement值和来源、identity/payment值保留；新许可进入当前目标后，拟案与提交绑定当前方案。没有重复解释已处理用户消息。工具结果、模型原始选择、程序核验/规范化、实际执行、下一轮状态分别保存。a2未出现程序拒绝造成的“拦住了所以看似成功”；本批不能估计拦截的总体收益。这是全框架外部比较，不是模块消融，不能分别估计三个模块的因果效应。

**仍有模拟偏差。** 官方43题询问“cap是最低还是最高退款”时，脚本没有回答这个真实问题，仍要求它提出具体SKU；第二次还把说明中已被Agent否定的6700049080当成当前offer，尽管最后仅问9391733462。最终实际用户明确接受6700049080、独立批准该完整方案，数据库与这些实际回复一致，所以最终登记可核验；但中间许可不符合预定实际提问触发范围。两次43官方均保留并排除质量/成本配对。其最初cap方向错误发生在模拟偏差之前，仍是模型错误；不能把全部问题算给模型或全部算给模拟器。不再继续抽新批替换失败。

另外，冻结v2的cap原话格式化为两位小数，而构造的43阈值是-56.105，框架状态显示全精度、官方初始原话显示-56.10；初始39同样存在-151.155/-151.16差异。逐个枚举实际有货规格后没有可行性分类翻转，官方-27.65方向错误也不能由0.005解释；但数值输入并非严格相同，43不能称作完全受控的组间机制证据。POSTRUN_CHECKS.json明确保留该限制。后续应在构造时先统一合法货币精度，再冻结，不改本批数据。

## A：同质量后的投入

a2仅80/23/29共6配对可比较：官方→框架请求**{o['calls']}→{f['calls']}**，输入**{o['input']}→{f['input']}**，输出**{o['output']}→{f['output']}**；缓存命中{o['cache_hit']}→{f['cache_hit']}、未命中{o['cache_miss']}→{f['cache_miss']}。请求耗时{o['seconds']:.2f}→{f['seconds']:.2f}秒；含程序/模拟交互的续行时间{o['wall_seconds']:.2f}→{f['wall_seconds']:.2f}秒，只作本地描述。

框架读得更少，但模型请求更多，输出和未命中输入并未随总输入下降，**本轮没有总投入更低的证据**。v2为测每次认知选择暂停自动推进，不能把它当21轮按需调度器。官方cognitive日志角色包含原生完整循环，不是纯认知分项。认知、语义、模拟分开记账；公共前缀以实际消息/原生观察次数单列，供应商未单独返回其词元，不从Agent实际输入中重复减扣，详见A2_COMPARABLE_ACCOUNTING与GLOBAL_ACCOUNTING。时间含I/O和共享服务波动，不作推理速度因果估计。

## B1：哪些可作为示范

回到23轮52候选及原始API请求，筛出**{len(sft)}条可审阅示例**：[SFT_EXAMPLES.jsonl](results/B1/SFT_EXAMPLES.jsonl)。包括93/26的许可澄清（获取用户信息），以及拟案、完整确认和提交。每条记录原始messages、原始决策、对象、依据、完成条件、source/responseID/hash、实际允许执行和后续严格结果；程序纠正后的动作不伪装成模型原始成功。

重要修正是来源读取：23的trace.state有可变引用，预算/analysis_feedback可能在后续被修改。本轮12条都使用原始逐次序列化model_calls请求重建输入，不使用已变动的trace.state，不给模型拼入后续结果。未来字段只在事后审阅元数据。消息本身可单独取出作为训练格式，尚未训练。

原候选**没有库存query或自主analyze**。澄清只能覆盖获取用户许可；强制分析首步在FORCED_ANALYSIS_REVIEW中单列，不混成自主SFT。分析类正例仍缺，不能为了覆盖三类而造一条。52条去留在SCREENING；12条中拟议训练93/29共7，验证102共2，保留测试26共3；35也整体保留测试。只是按基础题登记计划，实际训练未开始，示例文件内的保留测试行必须过滤；这些已被API实验查看的题不是独立盲测，后续仍需新测试题与独立复核。

## B2：用户偏好让路径评价反转

3个起点×analyze/clarify×两次=12条，全部硬约束、当次完整授权和登记通过。比较首步由实验指定，后续共同candidate策略，不冒称首步是模型自主选择。偏好写在初始用户原话，真实输入可查；硬条件是stock、cap、同产品、scope、原支付与独立授权，属性可协商。评分固定为硬约束→办结→公开优先级保持向量→投入。这里严格质量指事实/授权/日志，不包含“偏好最优”，否则会先过滤掉需要比较的较差选择。

|起点|两次路径评价|业务依据|
|---|---|---|
|26容量优先|先澄清胜，两次一致|先澄清1240311797保留1L，[1,0,0]；先分析随后选择2698416822保留白色/塑料却改1.5L，[0,1,1]。容量在先，不能按保留属性个数反过来判|
|26颜色/材质优先|先分析胜，两次一致|同样两个最终SKU，向量变为分析[1,1,0]、澄清[0,0,1]。先分析虽多2次调用，仍保留更高优先的属性|
|35实际为颜色/续航/防水优先|暂不定偏好候选|分析保留红色+防水，澄清保留红色但不防水；然而两次分析金额参照含糊/错误，一条澄清有日志异常，不能跳过质量门槛|

26容量优先时，局部分析确实识别了容量优先，但认知选择仍挑2698416822；第一次甚至说放弃最高优先容量是“best tradeoff”。这是**认知决策中的价值排序问题**，不是属性事实、许可或授权不满足。较低偏好路径被用户实际明确接受并合法办结，不等于原软偏好已自动抹去。允许这种劣路径进入比较，才有有业务依据的负候选；不把这段理由当SFT好示范。第二次分析路径还重复prepare一次。

35的状态名waterproof及协议文字不准确，实际冻结JSON与用户输入优先级是color、battery life、water resistance，按实际顺序报告；原文件不改。分析第一次说“-16.22 versus current requested item”，数值是相对原购并含水管的整单差额、参照含糊；第二次说cap相对当前请求价格321.18，参照错误。第二次澄清在正确写入后保存trace出现OSError Errno22，后续保存了异常和最终状态，根因未确定；不是网络或用户模拟异常。两条重复prepare及全部调用都保留。

[偏好表](CONTINUATION_PREFERENCES.md)和[DPO_CANDIDATES.json](results/DPO_CANDIDATES.json)只有26的**两个状态候选**，不是两道独立任务，也不是chosen/rejected训练响应对。保存相同可见快照、具体对象/报价SKU、两个强制工作及各自续行。方向针对这些具体绑定和共同策略，不是“分析总优于澄清”或反之；澄清SKU由字面首个可行选提供，可能偶然合用户偏好，尚未优化其报价选择策略。若直接澄清同一个更合偏好的报价，分析路径的优势可能消失，本批不证明分析本身必要。需补该分支来分开工作类型与报价参数的作用，且需要独立复核，不能自动训练。

## 账本、归档和阶段决定

全部阶段{totals_api}次实际API请求，含额外A修订和所有联调，Agent/模拟用户分开；模拟回复自然语言由实际交互触发，提取器用量记模拟，不混进Agent。无缺失usage；实际模型、传输失败和解析事件按原始日志统计。一个程序日志I/O异常另列，不能算请求失败。编排聊天开销未知、外部评审API为0。

{len(raw)}份原始文件仍在原位，并复制到D:/experimentn/research-raw-archives/round24-official-and-trajectory，SHA逐一一致，见[RAW_ARCHIVES.json](RAW_ARCHIVES.json)。Git收代码、冻结、配置、摘要、评分、示例和代表轨迹；完整请求/状态批量文件通过清单恢复。申报书、21及以前原目录、23冻结和原记录均保持原样。

结论按两问分别是：第一，框架提供可审计的来源/局部失效/前提和授权绑定，并能推动后续工作；在同源库存事件后官方同样直接澄清，在稳定及局部变更也能正确办理，不能声称框架普遍优胜。第二，可从真实请求得到有限的好示范，可从公开软偏好得到稳定且反向的路径候选；仍缺自主查询/分析正例，不能扩成已验收训练集。

下一步先修用户模拟的约束问题回答和“当前offer/已否定备选”语义边界，加入本批反例；另版修局部分析的当前整单差额/明确冲突原因，并把软优先级显式送到下一步选择以核验偏好排序。保留现有候选，补独立审阅与新的查询/分析轨迹，模型确定后再做实际小模型训练。不要用这批已看过的题继续充当未见测试。

代表轨迹：[A2官方资源恢复](versions/a2/A_t23_r1_official_FULL_TRACE.md)、[A2框架同状态恢复](versions/a2/A_t23_r1_framework_FULL_TRACE.md)、[B26先分析](B_26_appearance_r1_analyze_FULL_TRACE.md)、[B26先澄清](B_26_appearance_r1_clarify_FULL_TRACE.md)。每份含全部工作、实际原话、程序核验、状态更新和逐调用用量。
'''
 (E/'RESULTS.md').write_text(text,encoding='utf-8')
 marker='### 2026-11-25 · 第24轮：官方同批对照与轨迹样本验收'
 entry=f'''\n\n{marker}

- **实际批次。** 固定23v2，完成初始A01正式16、独立修订A2正式16、B01正式12，共44正式，另12联调；旧正式保留，不当联调或合并估收益。A2为80/23/29/43，43为未用于本轮调试的公开订单受控换货改编。
- **A结果与控制。** A2两组均8/8正确登记，严格质量官方6/8、框架8/8。资源事件统一原生tool来源后，双方第一业务工作都澄清；初始A01的额外先查询不能算框架收益。43初始cap方向错误是模型错误，但后续cap澄清未获适当回应、第二次当前offer解析偏离，故不比较其恢复成本/因果收益。6个可比配对请求{o['calls']}→{f['calls']}、输入{o['input']}→{f['input']}，框架未命中输入和调用更多，不支持总投入降低。两组均保留29另一商品依据、使用新完整授权。
- **B1。** 从23原52候选回到实际请求，12条可审阅示例；23trace.state可变引用的后续变化不能当决策输入，改用逐次序列化API请求还原。覆盖许可澄清和操作，库存query/自主analyze仍缺，强制分析单列，不造正例。按基础题登记拟议划分，未训练。
- **B2。** 12条硬结果正确，事实/来源/运行9条通过。26容量优先两次澄清优、颜色/材质优先两次分析优；更少调用不压过更高优先属性，只有两个同题状态的DPO候选，不是独立两题或可训练chosen/rejected。35参照问题及一条日志I/O异常保留，未定候选。
- **账本与决定。** 全阶段{totals_api}次API含Agent与模拟分别记账。三份冻结hash一致，原始档案与副本hash清单保留。先补模拟约束澄清/被否定备选边界与分析事实输入，再核验认知优先级排序、补查询/分析示范及独立复核；实际训练等模型确定后。\n- **证据。** [第24轮报告](../experiments/preliminary/round24-official-and-trajectory/RESULTS.md)、同目录OFFICIAL_PAIRS.md、CONTINUATION_PREFERENCES.md、results/B1与完整轨迹。
'''
 log=R/'docs/research_log.md'
 if marker not in log.read_text('utf-8'):
  with log.open('a',encoding='utf-8') as f0:f0.write(entry)
 original=Path('D:/experimentn/Codex工作区/实验/研究计划与实验日志.md')
 if marker not in original.read_text('utf-8-sig'):
  with original.open('a',encoding='utf-8') as f0:f0.write(entry.replace('../experiments/preliminary/round24-official-and-trajectory/RESULTS.md',str(E/'RESULTS.md').replace('\\','/')))
 index=R/'experiments/preliminary/README.md';idx=index.read_text('utf-8')
 if '|24 ' not in idx:
  idx+='\n|24 官方同批对照与轨迹样本验收|固定23v2；A资源来源差异修订后双方均先澄清，终局相当；模拟约束回应仍有限。12条SFT示例有查询/分析覆盖缺口；26公开软优先级改变使两次路径评价稳定反向，35待核实。无训练。|[结果](round24-official-and-trajectory/RESULTS.md)|仓库内独立A/B冻结与原始归档清单|\n';index.write_text(idx,encoding='utf-8')
 readme=R/'README.md';s=readme.read_text('utf-8').replace('01–23轮前期探索索引','01–24轮前期探索索引')
 if '第24轮官方对照' not in s:s=s.replace('- [研究定位]', '- [第24轮官方对照与轨迹验收](experiments/preliminary/round24-official-and-trajectory/RESULTS.md)\n- [研究定位]')
 readme.write_text(s,encoding='utf-8')

if __name__=='__main__':main()
