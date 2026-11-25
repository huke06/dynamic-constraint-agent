"""Post-run reporting only; no business or evaluator API calls."""
import json,hashlib,sys
from pathlib import Path
from collections import Counter
from decimal import Decimal
R=Path(__file__).resolve().parent.parent;B=R/'results/batch03';E=B/'evaluation'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def calls(p):return [json.loads(x) for x in p.read_text('utf-8').splitlines()] if p.exists() else []
def cost(xs):return {'calls':len(xs),'missing_usage':sum('usage' not in x.get('response',{}) for x in xs),**{k:sum(x.get('response',{}).get('usage',{}).get(k,0) for x in xs) for k in ('prompt_tokens','completion_tokens','total_tokens')}}
def main():
 scored=read(E/'rescored.json')['rows'];raw=read(B/'results.json');api=calls(B/'model_calls.jsonl');evapi=calls(E/'model_calls.jsonl');rows=[];audits=[]
 preferences=read(E/'preference_review.json') if (E/'preference_review.json').exists() else {}
 for s in scored:
  n=s['id'];t=read(B/(n+'_trajectory.json'));f=read(B/(n+'_final_state.json'));start=read(B/(n+'_start.json'));a=raw[n]
  sequence=[e['u']['z']['work_id'] for e in t if 'u'in e];c=[x for x in api if x['branch']==n and x['category']=='agent']
  pref=preferences.get(n,{'status':'pending','reason':'not independently reviewed'})
  rule_states=[]
  for e in t:
   for state in (e.get('before'),e.get('after')):
    if state:
     r=state['g'].get('conditional_permission')
     if r:rule_states.append({'source':r['source'],'variant':r['variant_id'],'sat':r['sat'],'quote':r['source_quote']})
  false_recovery=any(e.get('u',{}).get('z',{}).get('work_id')=='clarify' and e['before']['g'].get('conditional_permission',{}).get('sat')=='未满足' for e in t)
  for i,e in enumerate(t):
   if 'u'in e:
    wid=e['u']['z']['work_id'];keys={'screen':['identity','catalog','screen_absent','alternative_inventory'],'inventory':['identity','inventory_query_needed'],'clarify':['identity','user_channel'],'prepare':['identity','catalog','alternative_permission','selection_available','not_written','alternative_inventory'],'confirm':['plan_current','user_channel','not_written'],'submit':['identity','plan_current','authorization_current','not_written']}[wid]
    audits.append({'branch':n,'entry':i,'work':wid,'interpretation':'post-run reconstruction from recorded pre-state and frozen selected-work contract, not a new check fed to model','prerequisites':{k:e['before']['C'][k] for k in keys if k in e['before']['C']},'completed':e['completion_satisfied'],'changed_F_fields':[k for k in e['before']['F'] if e['before']['F'][k]!=e['after']['F'].get(k)],'model_decision':e['decision']})
  rows.append({'id':n,'correct_write':a['R_write'],'necessary_constraints':a['C_hard'] and a['C_permission_state'],'current_authorization':a['C_authorization_program'] and a['C_authorization_provenance'],
   'facts':s['factual_status'] if s['utterances'] else 'no_utterance','preference':pref,'quality':s['quality_pass'] and pref['status']=='accurate',
   'work_sequence':sequence,'steps':a['steps'],'rejections':sum('rejection'in x for x in t),'repeated_rejections':sum(x.get('repeat_of_previous_rejection',False) for x in t),'Agent':cost(c),'stop_reason':a.get('error'),
   'false_permission_reclarified':false_recovery,'permission_states':rule_states,'inventory_queries':sequence.count('inventory'),'event_triggered':(B/(n+'_event.json')).exists()})
 pairs=[];lines=['# 第12轮正式批次配对表','','每格1次。—表示未达到相同质量门槛，不计算资源差；未登记行的约束/授权False表示尚未满足办结前提。','', '|任务/状态|直接/候选登记|必要约束|当前授权|事实话术|偏好表述|工作数|拒绝数|可比|Agent词元差D−C|','|---|---|---|---|---|---|---|---|---|---:|']
 for tid,st in [('70','known'),('70','unknown'),('52','known'),('52','unknown'),('70','postchange'),('70','dynamic')]:
  d,c=[next(x for x in rows if x['id']==f't{tid}_r1_{st}_{g}') for g in ('direct','candidate')];equal=read(B/(d['id']+'_start.json'))==read(B/(c['id']+'_start.json'));ok=d['quality'] and c['quality']
  pair={'task':tid,'state':st,'complete_start_equal':equal,'comparable':ok,'Agent_tokens_D_minus_C':d['Agent']['total_tokens']-c['Agent']['total_tokens'] if ok else None,'steps_D_minus_C':d['steps']-c['steps'] if ok else None,'calls_D_minus_C':d['Agent']['calls']-c['Agent']['calls'] if ok else None};pairs.append(pair)
  vals=[tid+'/'+st,f"{d['correct_write']}/{c['correct_write']}",f"{d['necessary_constraints']}/{c['necessary_constraints']}",f"{d['current_authorization']}/{c['current_authorization']}",d['facts']+'/'+c['facts'],d['preference']['status']+'/'+c['preference']['status'],f"{d['steps']}/{c['steps']}",f"{d['rejections']}/{c['rejections']}",ok,pair['Agent_tokens_D_minus_C'] if ok else '—'];lines.append('|'+ '|'.join(map(str,vals))+'|')
 (R/'results/PAIRED_RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 accounts={k:cost([x for x in api+evapi if x['category']==k]) for k in sorted({x['category'] for x in api+evapi})}
 development={}
 for batch in ('batch01','batch02'):
  items=calls(R/'results'/batch/'model_calls.jsonl');development[batch]={k:cost([x for x in items if x['category']==k]) for k in sorted({x['category'] for x in items})}
 save(R/'results/SUMMARY.json',{'official_batch':'batch03','rows':rows,'pairs':pairs,'accounts':accounts,'development_all_categories_separate':development,'versions':dict(Counter(str(x.get('response',{}).get('model'))+' / '+str(x.get('response',{}).get('system_fingerprint')) for x in api+evapi))})
 save(R/'results/PROGRAM_CHECKS.json',audits)
 # Verify every deterministic confirmation against evidence available when spoken.
 from fact_verifier import replay
 checks=[]
 for x in calls(B/'program_confirmations.jsonl'):
  n=x['branch'];p=x['plan'];h=read(B/(n+'_final_state.json'))['F']['dialogue'];ref=next(i for i,m in enumerate(h) if m.get('content')==x['text']);evidence=replay(h,ref);valid=True;total=Decimal('0')
  for item in p['rows']:
   matches=[v for prod in evidence['products'].values() for vid,v in prod['variants'].items() if vid==item['new_item_id']]
   valid=valid and len(matches)==1 and matches[0]['available'] is True and matches[0]['options']==item['options'] and Decimal(str(matches[0]['price']))==Decimal(str(item['new_price']))
   originals=[i for o in evidence['orders'].values() for i in o['items'] if i['item_id']==item['item_id']]
   valid=valid and len(originals)==1 and Decimal(str(originals[0]['price']))==Decimal(str(item['old_price']))
   total+=Decimal(str(item['new_price']))-Decimal(str(item['old_price']))
  method=p['payment_method'];profiles=[u for u in evidence['users'].values() if method['id'] in u['payment_methods']]
  valid=valid and total==Decimal(str(p['difference'])) and len(profiles)==1 and profiles[0]['payment_methods'][method['id']]==method
  checks.append({'branch':n,'assistant_ref':ref,'program_fields_supported_at_utterance':bool(valid),'plan':p,'cost_model_calls':0})
 save(R/'results/CONFIRMATION_FACTS.json',checks);assert all(x['program_fields_supported_at_utterance'] for x in checks)
 # Full end-to-end trace of the actual dynamic run; failures, if any, retained.
 n='t70_r1_dynamic_direct';t=read(B/(n+'_trajectory.json'));lines=['# 确认前起点完整动态轨迹：直接组','','见每轮原始before/after JSON；下列为完整话术、决策、反馈及事件。身份/目录搜索沿用公开历史。','']
 for i,e in enumerate(t):
  lines+=['## 记录'+str(i+1),'']
  if 'event'in e:
   v=e['event'];lines+=['用户变更：'+v['user_message']['content'],'旧方案：'+str(v['before']['H']['plan']),'变化后plan='+str(v['after']['H']['plan'])+'；confirmations='+str(v['after']['H']['confirmations']),'保留F：'+','.join(k for k,z in v['before']['F'].items() if v['after']['F'].get(k)==z)]
  elif 'u'in e:
   lines+=['工作：'+e['u']['a']+'/'+e['u']['z']['work_id'],'模型依据：'+json.dumps(e['decision'],ensure_ascii=False),'完成契约：'+str(e['completion_satisfied'])]
   if 'assistant'in e:lines+=['助手：'+e['assistant'],'用户：'+e['customer'],'模型语义解析：'+json.dumps(e['semantic_parse'],ensure_ascii=False)]
   else:lines+=['工具/执行结果：'+json.dumps(e.get('result'),ensure_ascii=False)]
  else:lines+=['拒绝/错误：'+json.dumps(e,ensure_ascii=False)]
 lines+=['','最终记录：'+json.dumps(raw[n],ensure_ascii=False)]
 (R/'results/DYNAMIC_TRACE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 print(json.dumps({'rows':[{k:r[k] for k in ('id','correct_write','facts','quality','steps','false_permission_reclarified','rejections')} for r in rows],'pairs':pairs,'accounts':accounts,'development':development},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
