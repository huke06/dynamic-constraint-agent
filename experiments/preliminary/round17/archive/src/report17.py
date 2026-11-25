"""Post-run implementation of frozen protocol criteria; reason semantics reviewed by assistant."""
import json,hashlib,shutil
from pathlib import Path
from decimal import Decimal
from collections import Counter
from fact_verifier import replay
R=Path(__file__).resolve().parent.parent;B=R/'results/batch01'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calls(p):return [json.loads(x) for x in p.read_text('utf-8').splitlines()]
mapping=read(R/'results/REVIEW_MAPPING.json');semantic_reviews=read(R/'results/REASON_REVIEW.json')['items'];raw=read(B/'results.json');api=calls(B/'model_calls.jsonl');rows=[];reviews=[];speech=calls(B/'grounded_clarifications.jsonl');confirm=calls(B/'program_confirmations.jsonl');facts=[]
for n,r in raw.items():
 t=read(B/(n+'_trajectory.json'));f=read(B/(n+'_final_state.json'));env=read(B/(n+'_environment.json'));h=f['F']['dialogue'];controllers=[x for x in api if x['branch']==n and x['stage']=='controller'];ds=[]
 for x in controllers:
  if x['status']!='success':continue
  d=json.loads(x['response']['choices'][0]['message']['content']);state=json.loads(x['messages'][1]['content'])['state'];text=d.get('reason',json.dumps(d.get('comparison'),ensure_ascii=False));issues=[]
  review=next(v for v in semantic_reviews if mapping[v['code']]['call_index']==api.index(x));issues=review['issues']
  rr={'id':n,'decision_index':len(ds),'stock':state['catalog']['7765186836']['variants']['9013366374']['available'],'raw_decision':d,'public_state':state,'issues':issues,'status':review['status'],'review_code':review['code'],'judgment_evidence':review['evidence'],'reviewer':'assistant reviewed all controller outputs, not independent blinded gold'};reviews.append(rr);ds.append(rr)
 for x in [x for x in speech if x['branch']==n]:
  ref=x['assistant_ref'];ev=replay(h,ref);prod=ev['products']['7765186836'];ok=prod['variants']['9013366374']['available']==x['fields']['target']['available'] and h[ref]['content']==x['text']
  for v in [x['fields']['alternative']]:ok=ok and prod['variants'][v['item_id']]['available'] is True and prod['variants'][v['item_id']]['options']==v['options'] and Decimal(str(prod['variants'][v['item_id']]['price']))==Decimal(str(v['price']))
  facts.append({'id':n,'ref':ref,'kind':'clarify','supported':bool(ok)})
 for x in [x for x in confirm if x['branch']==n]:
  ref=next(i for i,m in enumerate(h) if m.get('content')==x['text']);ev=replay(h,ref);p=x['plan'];row=p['rows'][0];v=ev['products']['7765186836']['variants'][row['new_item_id']];o=ev['orders']['#W3947049'];original=next(i for i in o['items'] if i['item_id']==row['item_id']);method=ev['users'][o['user_id']]['payment_methods'][p['arguments']['payment_method_id']]
  ok=v['available'] is True and row['options']==v['options'] and Decimal(str(row['new_price']))==Decimal(str(v['price'])) and Decimal(str(p['difference']))==Decimal(str(v['price']))-Decimal(str(original['price'])) and method==p['payment_method'];facts.append({'id':n,'ref':ref,'kind':'confirm','supported':bool(ok)})
 writes=f['P']['writes'];biz=False;auth=False;chosen=None;difference=None
 if len(writes)==1:
  w=writes[0];a=w['arguments'];chosen=a['new_item_ids'][0];difference=w['result']['exchange_price_difference'];v=env['products']['7765186836']['variants'][chosen];orig=next(i for i in env['orders']['#W3947049']['items'] if i['item_id']=='3358616356');con=f['H']['confirmations'][-1]
  auth=w['gate']['allowed'] and w['gate']['confirmation_sources']==[con['assistant_ref'],con['user_ref']] and con['source_quote'] in h[con['user_ref']]['content']
  biz=a['item_ids']==['3358616356'] and a['payment_method_id']=='credit_card_7901829' and chosen==f['g']['alternative_permission'] and v['available'] is True and v['options']['ventilation']=='high' and chosen==('9013366374' if '_unknown_in_' in n else '1665571435') and read(B/(n+'_database.json'))['orders']['#W3947049']==w['result'] and w['gate']['fingerprint']==f['H']['plan']['quote']['fingerprint'] and Decimal(str(difference))==Decimal(str(v['price']))-Decimal(str(orig['price'])) and w['result']['status']=='exchange requested' and auth
 completed=[e for e in t if 'u'in e];inv=next((e for e in completed if e['u']['z']['work_id']=='inventory'),None);post=None
 if inv:post=next((e for e in completed if e['turn']>inv['turn']),None)
 local=[x for x in facts if x['id']==n];coverage={x['ref'] for x in local}=={e['assistant_ref'] for e in completed if 'assistant_ref'in e};factpass=coverage and all(x['supported'] for x in local)
 reasonpass=bool(ds) and all(x['status']=='supported' for x in ds);requests=[x for x in api if x['branch']==n];usage=[x['usage'] for x in requests if x.get('usage') is not None]
 rows.append({'id':n,'condition':'_'.join(n.split('_')[2:-1]),'repeat':int(n.split('_')[1][1:]),'group':n.rsplit('_',1)[1],'first':completed[0]['u']['z']['work_id'] if completed else None,'first_model_choice':ds[0]['raw_decision'] if ds else None,'first_selected':(ds[0]['raw_decision'].get('work_id') or ds[0]['raw_decision'].get('selected_work_id') or ds[0]['raw_decision'].get('selected') or ds[0]['raw_decision'].get('u',{}).get('z',{}).get('work_id')) if ds else None,'program_rejections':[e['diagnostic'] for e in t if e.get('kind')=='program_rejection'],'post_query_first':post['u']['z']['work_id'] if post else None,'post_query_permission':inv['after']['g']['alternative_permission'] if inv else None,'post_query_rule':inv['after']['g'].get('conditional_permission') if inv else None,'registered':bool(biz),'necessary_constraints':bool(biz),'user_goal_satisfied':bool(biz),'authorization':bool(auth),'chosen':chosen,'difference':difference,'speech_pass':factpass,'reason_pass':reasonpass,'quality':bool(biz and auth and factpass and reasonpass and not r['error']),'steps':r['steps'],'attempts':len(requests),'success_responses':sum(x['status']=='success' for x in requests),'missing_usage':len(requests)-len(usage),'returned_tokens':sum(x['total_tokens'] for x in usage),'error':r['error'],'sequence':[e['u']['z']['work_id'] for e in completed]})
pairs=[];table=['# 第17轮配对表','','D直接/C候选。理由错误不以办结覆盖；质量不等或usage不完整不比较投入。','', '|条件/重复|D/C首步|D/C查询后首步|D/C正确登记|D/C必要约束|D/C当前授权|D/C事实话术|D/C理由全通过|D/C步骤|质量可比|词元D−C|','|---|---|---|---|---|---|---|---|---|---|---:|']
for state in ('known_out','unknown_out','unknown_in'):
 for rep in (1,2):
  d,c=[next(x for x in rows if x['condition']==state and x['repeat']==rep and x['group']==g) for g in ('direct','candidate')];ok=d['quality'] and c['quality'] and not(d['missing_usage'] or c['missing_usage']);p={'condition':state,'repeat':rep,'comparable':ok,'steps_D_minus_C':d['steps']-c['steps'] if ok else None,'tokens_D_minus_C':d['returned_tokens']-c['returned_tokens'] if ok else None};pairs.append(p)
  table.append('|'+ '|'.join(map(str,[state+'/'+str(rep),str(d['first_selected'])+'/'+str(c['first_selected'])+'; 执行 '+str(d['first'])+'/'+str(c['first']),str(d['post_query_first'])+'/'+str(c['post_query_first']),str(d['registered'])+'/'+str(c['registered']),str(d['necessary_constraints'])+'/'+str(c['necessary_constraints']),str(d['authorization'])+'/'+str(c['authorization']),str(d['speech_pass'])+'/'+str(c['speech_pass']),str(d['reason_pass'])+'/'+str(c['reason_pass']),str(d['steps'])+'/'+str(c['steps']),ok,p['tokens_D_minus_C'] if ok else '—']))+'|')
(R/'results/PAIRED_RESULTS.md').write_text('\n'.join(table)+'\n',encoding='utf-8');save(R/'results/REASONS.json',reviews);save(R/'results/FACTS.json',facts);save(R/'results/SUMMARY.json',{'rows':rows,'pairs':pairs,'diagnostics':dict(Counter(x.get('diagnostic',{}).get('kind','success') for x in api)),'attempts':len(api),'missing_usage':sum(x.get('usage') is None for x in api),'returned_tokens':sum((x.get('usage') or {}).get('total_tokens',0) for x in api),'versions':dict(Counter(str(x.get('response',{}).get('model'))+' / '+str(x.get('response',{}).get('system_fingerprint')) for x in api if 'response'in x))})
for state in ('unknown_out','unknown_in'):
 n=f't70_r1_{state}_direct';t=read(B/(n+'_trajectory.json'));lines=['# '+state+'完整轨迹：直接组第1次','']
 for e in t:
  if 'u'not in e:lines+=['拒绝/异常：'+json.dumps(e,ensure_ascii=False)];continue
  lines+=['## '+e['u']['z']['work_id'],'','模型理由：'+json.dumps(e['decision'],ensure_ascii=False),'执行前许可：'+json.dumps(e['before']['g'].get('conditional_permission'),ensure_ascii=False)]
  if 'assistant'in e:lines+=['助手：'+e['assistant'],'用户：'+e['customer'],'语义：'+json.dumps(e['semantic_parse'],ensure_ascii=False)]
  else:lines+=['执行结果：'+json.dumps(e.get('result'),ensure_ascii=False)]
  lines+=['程序实际契约：'+json.dumps(e['after']['P'].get('actual_contract_checks',[])[-1:] ,ensure_ascii=False),'执行前库存证据：'+json.dumps({'target':e['before']['F']['catalog']['7765186836']['variants']['9013366374'],'source':e['before']['g'].get('conditional_permission',{}).get('inventory_source')},ensure_ascii=False),'执行后许可：'+json.dumps(e['after']['g'].get('conditional_permission'),ensure_ascii=False),'执行后当前授权：'+json.dumps(e['after']['H']['confirmations'],ensure_ascii=False)]
 (R/'results'/('TRACE_'+state.upper()+'.md')).write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'rows':[{k:x[k] for k in ('id','first','post_query_first','registered','quality','chosen','difference')} for x in rows],'pairs':pairs},ensure_ascii=False,indent=2))
