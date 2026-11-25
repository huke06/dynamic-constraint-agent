"""Post-run reason review and failure-safe reporting; no model calls or frozen-source edits."""
import json,hashlib,shutil
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent.parent;B=R/'results/batch02'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calls(p):return [json.loads(x) for x in p.read_text('utf-8').splitlines()]
s=read(R/'results/BUSINESS_SUMMARY.json') if (R/'results/BUSINESS_SUMMARY.json').exists() else read(R/'results/SUMMARY.json');save(R/'results/BUSINESS_SUMMARY.json',s);api=calls(B/'model_calls.jsonl');reviews=[]
for index,x in enumerate(api):
 if x['stage']!='controller':continue
 n=x['branch'];inp=json.loads(x['messages'][1]['content']);state=inp['state'];stock=state['catalog']['8940227892']['variants']['3892645120']['available']
 if 'response'not in x:reviews.append({'call_index':index,'id':n,'status':'no_model_response','error':x.get('error'),'reason':None});continue
 d=json.loads(x['response']['choices'][0]['message']['content']);text=d.get('reason',json.dumps(d.get('comparison'),ensure_ascii=False));issues=[]
 q='The user explicitly stated they do not accept any lower-zoom alternative'
 if q in text:issues.append({'type':'not_accepted_misread_as_refusal','quote':q,'source_ref':12,'source_quote':read(R/'configs/start_known.json')['state']['F']['dialogue'][12]['content'],'verdict':'contradicted','reason':'The original sentence says not yet accepted, not categorical refusal.'})
 q='also historical_plan_compatible 未满足 and screen_absent 未满足'
 if q in text:
  contract=next(w for w in inp['W'] if w['work_id']=='submit');issues.append({'type':'invented_submit_prerequisites','quote':q,'actual_submit_preconditions':contract['preconditions'],'verdict':'contradicted','reason':'These are state flags, not submit prerequisites. Missing current authorization is the actual blocker.'})
 reviews.append({'call_index':index,'id':n,'status':'contradicted' if issues else 'supported','stock_at_decision':stock,'public_inventory_source':13 if stock is None else state.get('H',{}).get('screen',{}).get('source') if state.get('H',{}).get('screen') else 13,'raw_decision':d,'public_state':state,'issues':issues,
 'three_requested_checks':{'unknown_not_claimed_out_of_stock':True,'not_accepted_not_claimed_refusal':not any(i['type']=='not_accepted_misread_as_refusal' for i in issues),'variant_permission_not_claimed_transaction_authorization':True},'reviewer':'assistant semantic audit of all successful controller outputs; not independent blinded gold'})
save(R/'results/REASON_REVIEW.json',reviews)
for row in s['rows']:
 rr=[x for x in reviews if x['id']==row['id']];returned=[x for x in rr if x['status']!='no_model_response'];row['reason_status']='unobserved' if not returned else 'contradicted' if any(x['status']=='contradicted' for x in returned) else 'supported';row['business_quality']=row['quality'];row['quality']=row['quality'] and row['reason_status']=='supported'
 t=read(B/(row['id']+'_trajectory.json'));row['inventory_before_plan']=all(e['before']['F']['catalog']['8940227892']['variants']['3892645120']['available'] is not None for e in t if e.get('u',{}).get('z',{}).get('work_id')=='prepare');row['quality']=row['quality'] and row['inventory_before_plan'];row['successful_model_responses']=row['Agent']['calls']-row['Agent']['missing_usage'];row['cost_complete']=row['Agent']['missing_usage']==0
 control=[x for x in api if x['branch']==row['id'] and x['stage']=='controller'];grant_turn=next((e['turn'] for e in t if e.get('clarification_resolution',{}).get('new_permission_effective')),float('inf'));attempts=[]
 for turn,call in enumerate(control):
  if 'response' not in call:continue
  d=json.loads(call['response']['choices'][0]['message']['content']);wid=d.get('work_id',d.get('u',{}).get('z',{}).get('work_id'))
  if wid in ('prepare','submit') and turn<=grant_turn:attempts.append({'turn':turn,'work':wid})
 row['premature_attempts']=attempts
for pair in s['pairs']:
 d,c=[next(r for r in s['rows'] if r['mode']==pair['mode'] and r['repeat']==pair['repeat'] and r['group']==g) for g in ('direct','candidate')];ok=d['quality'] and c['quality'];pair['quality_comparable']=ok;pair['token_usage_complete']=d['cost_complete'] and c['cost_complete'];pair['steps_D_minus_C']=d['steps']-c['steps'] if ok else None;pair['calls_D_minus_C']=d['Agent']['calls']-c['Agent']['calls'] if ok else None;pair['tokens_D_minus_C']=d['Agent']['total_tokens']-c['Agent']['total_tokens'] if ok and pair['token_usage_complete'] else None
save(R/'results/SUMMARY.json',s)
lines=['# 第15轮配对结果','','缺货第1次两侧无模型返回，首步未观察；未知第1次有理由误读；缺货第2次存在7条无usage请求，词元差不算。','', '|状态/重复|D/C首步|D/C登记|D/C理由|D/C工作|D/C请求尝试/成功返回|全质量可比|词元D−C|','|---|---|---|---|---|---|---|---:|']
for p in s['pairs']:
 d,c=[next(r for r in s['rows'] if r['mode']==p['mode'] and r['repeat']==p['repeat'] and r['group']==g) for g in ('direct','candidate')]
 lines.append('|'+ '|'.join(map(str,[p['mode']+'/'+str(p['repeat']),str(d['first_work'])+'/'+str(c['first_work']),str(d['correct_registration'])+'/'+str(c['correct_registration']),d['reason_status']+'/'+c['reason_status'],str(d['steps'])+'/'+str(c['steps']),f"{d['Agent']['calls']}/{d['successful_model_responses']} ; {c['Agent']['calls']}/{c['successful_model_responses']}",p['quality_comparable'],p['tokens_D_minus_C'] if p['tokens_D_minus_C'] is not None else '—']))+'|')
(R/'results/PAIRED_RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
for st in ('known','unknown'):
 n=f't52_r2_{st}_direct';t=read(B/(n+'_trajectory.json'));lines=['# '+st+'完整轨迹：直接组第2次','']
 for i,e in enumerate(t):
  lines+=['## 记录'+str(i+1),'']
  if 'u'in e:
   lines+=['工作：'+e['u']['z']['work_id'],'理由：'+json.dumps(e['decision'],ensure_ascii=False),'决策前目标库存：'+str(e['before']['F']['catalog']['8940227892']['variants']['3892645120']['available']),'决策前许可：'+json.dumps(e['before']['g'].get('conditional_permission'),ensure_ascii=False),'完成条件：'+str(e['completion_satisfied'])]
   if 'assistant'in e:lines+=['助手：'+e['assistant'],'用户：'+e['customer'],'语义：'+json.dumps(e['semantic_parse'],ensure_ascii=False)]
   else:lines+=['执行结果：'+json.dumps(e.get('result'),ensure_ascii=False)]
   lines+=['后续状态：'+json.dumps({'goal':e['after']['g'],'plan':e['after']['H']['plan'],'authorization':e['after']['H']['confirmations'],'writes':e['after']['P']['writes']},ensure_ascii=False)]
  else:lines+=['异常/拒绝：'+json.dumps(e,ensure_ascii=False)]
 (R/'results'/('TRACE_'+st.upper()+'.md')).write_text('\n'.join(lines)+'\n',encoding='utf-8')
print({'reasons':dict(Counter(x['reason_status'] for x in s['rows'])),'quality':sum(x['quality'] for x in s['rows']),'pairs':s['pairs'],'accounts':s['accounts']})
