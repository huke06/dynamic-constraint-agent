"""Post-run semantic type annotations and reports, no API calls."""
import json,hashlib,sys
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parent.parent;B=ROOT/'results/batch01';E=B/'evaluation'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def annotate():
 r=read(E/'semantic_review.json')
 for key,u in r['utterances'].items():
  raw=read(E/'extractions'/(key+'.json'))
  for i,c in enumerate(raw['claims']):
   q=c.get('quote','');d=json.loads(json.dumps(c));reason=None
   if c['kind']=='order_status' and q=='nothing has changed on your order yet':
    d={'kind':'write','quote':q,'asserted':False};reason='Context explicitly says earlier exchange never submitted; no literal status enum asserted.'
   if c['kind']=='difference' and 'earlier $22.55' in q:
    d['selector']={'variant_id':'9013366374'};reason='Earlier refers to original public blue proposal, not new black fallback.'
   if c['kind']=='price' and ('variant_id' in c or 'old_item_id' in c):
    d['selector']={k:c[k] for k in ('variant_id','old_item_id') if k in c};reason='Move explicitly quoted item binding into typed selector; no fact value changed.'
   if reason:u['patches'].append({'operation':'replace','index':i,'claim':d,'reason':reason})
 save(E/'semantic_review.json',r)
def report():
 from score_facts import evaluate
 evaluate(B,E,None)
 raw=read(B/'results.json');scored=read(E/'rescored.json')['rows'];calls=[json.loads(x) for x in (B/'model_calls.jsonl').read_text('utf-8').splitlines()]
 external=[json.loads(x) for x in (E/'model_calls.jsonl').read_text('utf-8').splitlines()]
 def cost(data):return {'calls':len(data),**{k:sum(x.get('response',{}).get('usage',{}).get(k,0) for x in data) for k in ('prompt_tokens','completion_tokens','total_tokens')}}
 rows=[]
 for s in scored:
  n=s['id'];t=read(B/(n+'_trajectory.json'));r=raw[n];dec=[x for x in calls if x['branch']==n and x['stage']=='controller'];f=read(B/(n+'_final_state.json'))
  first=json.loads(dec[0]['response']['choices'][0]['message']['content']);firstid=first.get('work_id',first.get('u',{}).get('z',{}).get('work_id'))
  facts=s['factual_status'] if s['utterances'] else 'no_utterance_not_assessed'
  rows.append({'id':n,'write':r['R_write'],'goal':r['R_goal'],'necessary_constraints':r['C_hard'] and r['C_authorization_program'] and r['C_permission_state'],
    'facts':facts,'quality':s['quality_pass'],'first_proposed':firstid,'first_executed':next((e['u']['z']['work_id'] for e in t if 'u' in e),None),
    'steps':r['steps'],'rejections':sum('rejection' in x for x in t),'cost':cost([x for x in calls if x['branch']==n and x['category']=='agent']),
    'event_triggered':n.endswith('_direct') and 'dynamic' in n and (B/(n+'_event.json')).exists() or (B/(n+'_event.json')).exists(),
    'stop_reason':r.get('error'),'work_sequence':[e['u']['z']['work_id'] for e in t if 'u' in e],
    'stock_queries':sum(e.get('u',{}).get('z',{}).get('work_id')=='inventory' for e in t),
    'intent_wording_note':'Calls preferred 10x a requirement; observable wording error, even though final chosen alternative was permitted.' if n=='t52_r1_unknown_candidate' else None})
 pairs=[];table=['# 第11轮配对结果','','D=直接决策，C=候选决策；事实P=待核实、X=矛盾、S=已抽取事实支持、N=没有话术。工作数含实际执行，拒绝次数单列。质量不可比不计算资源差。','','|任务/状态|D/C首次提议|D/C写入|D/C必要约束|D/C话术|D/C工作数|D/C拒绝|质量可比|投入差|','|---|---|---|---|---|---|---|---|---|']
 for tid,st in [('70','known'),('70','unknown'),('52','known'),('52','unknown'),('70','dynamic')]:
  d,c=[next(r for r in rows if r['id']==f't{tid}_r1_{st}_{g}') for g in ('direct','candidate')]
  equal=read(B/(d['id']+'_start.json'))==read(B/(c['id']+'_start.json'))
  comparable=d['quality'] and c['quality'] and not(d['intent_wording_note'] or c['intent_wording_note'])
  pairs.append({'task':tid,'state':st,'complete_start_equal':equal,'quality_comparable':comparable,'token_difference_D_minus_C':d['cost']['total_tokens']-c['cost']['total_tokens'] if comparable else None})
  table.append(f"|{tid}/{st}|{d['first_proposed']}/{c['first_proposed']}|{d['write']}/{c['write']}|{d['necessary_constraints']}/{c['necessary_constraints']}|{d['facts']}/{c['facts']}|{d['steps']}/{c['steps']}|{d['rejections']}/{c['rejections']}|{comparable}|{'—' if not comparable else d['cost']['total_tokens']-c['cost']['total_tokens']}|")
 (ROOT/'results/PAIRED_RESULTS.md').write_text('\n'.join(table)+'\n',encoding='utf-8')
 accounts={k:cost([x for x in calls+external if x['category']==k]) for k in sorted({x['category'] for x in calls+external})}
 save(ROOT/'results/SUMMARY.json',{'rows':rows,'pairs':pairs,'accounts':accounts,'model_versions':dict(Counter(str(x.get('response',{}).get('model'))+' / '+str(x.get('response',{}).get('system_fingerprint')) for x in calls+external))})
 # Full dynamic failure trace; no success fabricated.
 n='t70_r1_dynamic_direct';t=read(B/(n+'_trajectory.json'));lines=['# 完整动态轨迹：头盔直接组（未办结）','','起点使用原任务公开身份/目录和已准备的蓝色M高通风旧方案；原始搜索非在线重采样。在线重新请求确认。保留历史原确认元数据，但当前授权标为stale，必须取得新回复。','']
 for i,e in enumerate(t):
  lines+=['## 记录'+str(i+1),'']
  if 'event' in e:
   ev=e['event'];lines+=['用户事件：'+ev['user_message']['content'],f"原句来源ref{ev['source']}；解析：{json.dumps(ev['semantic_parse'],ensure_ascii=False)}",'变化后旧plan='+str(ev['after']['H']['plan'])+'；确认='+str(ev['after']['H']['confirmations']),
    '保留F字段：'+','.join(k for k,v in ev['before']['F'].items() if ev['after']['F'].get(k)==v)]
  elif 'u' in e:
   lines+=['工作：'+e['u']['a']+' / '+e['u']['z']['work_id'],'模型决策：'+json.dumps(e['decision'],ensure_ascii=False),'执行前检查：已通过；完成契约='+str(e['completion_satisfied'])]
   if 'assistant' in e:lines+=['助手：'+e['assistant'],'用户：'+e['customer'],'语义更新：'+json.dumps(e['semantic_parse'],ensure_ascii=False)]
  else:lines+=['拒绝/停止：'+str(e.get('rejection',e.get('error'))),'原始模型选择见该轨迹对应model_calls.jsonl的controller请求/响应。']
 lines+=['','事件后未查询库存、未形成新方案、未取得新授权、未写入。旧授权未被用于提交。候选组因反复确认、语义层未认定有效授权，预算耗尽，事件未触发；该组实际完整记录另存。']
 (ROOT/'results/DYNAMIC_TRACE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 # Verify all old files against previously delivered manifests, plus frozen new inputs.
 prior=ROOT.parent/'10_程序事实核验与续行验证';oldfreeze=read(prior/'results/20261123T001740331845Z/freeze.json')
 protected=all(sha(Path(p))==v for p,v in oldfreeze['protected'].items())
 old10=all(sha(prior/p)==v for p,v in read(prior/'DELIVERY_MANIFEST.json')['files'].items())
 freeze=read(ROOT/'configs/freeze.json');unchanged=all(sha(ROOT/p)==v for p,v in freeze['files'].items())
 audit={'old01_09_and_proposal_unchanged':protected,'old10_unchanged':old10,'frozen_inputs_unchanged':unchanged,'all_five_pairs_complete_start_equal':all(p['complete_start_equal'] for p in pairs),'trajectories':len(rows),'writes':sum(r['write'] for r in rows),'no_training':True}
 save(ROOT/'results/AUDIT.json',audit);assert protected and old10 and unchanged and audit['all_five_pairs_complete_start_equal']
 print(json.dumps({'rows':rows,'accounts':accounts,'audit':audit},ensure_ascii=False,indent=2))
if __name__=='__main__':
 if sys.argv[1]=='annotate':annotate()
 else:report()
