"""Post-run annotations and reports; no API calls, no frozen rule edits."""
import json,hashlib,shutil,sys
from pathlib import Path
from collections import Counter
from decimal import Decimal
R=Path(__file__).resolve().parent.parent;B=R/'results/batch02';E=B/'evaluation'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calls(p):return [json.loads(x) for x in p.read_text('utf-8').splitlines()] if p.exists() else []
def cost(xs):return {'calls':len(xs),'missing_usage':sum('usage' not in x.get('response',{}) for x in xs),**{k:sum(x.get('response',{}).get('usage',{}).get(k,0) for x in xs) for k in ('prompt_tokens','completion_tokens','total_tokens')}}
def annotate():
 review=read(E/'semantic_review.json')
 for key,u in review['utterances'].items():
  raw=read(E/'extractions'/(key+'.json'))
  for i,c in enumerate(raw['claims']):
   q=c.get('quote','');d=json.loads(json.dumps(c));why=None
   if c['kind']=='enumeration' and q=='These are all exchange items.':d['kind']='exchange_scope';why='Transaction scope, not exhaustive catalogue.'
   if c['kind']=='enumeration' and 'other 30MP CF-card variants' in q:
    d={'kind':'uncertain','quote':q,'reason':'Other explicitly excludes previously named 3892645120; frozen selector has no exclusion operator. Do not score as absolute full catalogue enumeration.'};why='Scope representation limit, retain pending rather than fabricate catalogue contradiction.'
   if why:u['patches'].append({'operation':'replace','index':i,'claim':d,'reason':why})
  name,ref=key.rsplit('_ref',1);entry=next(x for x in read(B/(name+'_trajectory.json')) if x.get('assistant_ref')==int(ref));text=entry['assistant']
  if text.startswith('Please explicitly confirm this complete exchange proposal: '):
   p=json.loads(text.split('proposal: ',1)[1].split('. These are all exchange items.',1)[0])
   for row in p['rows']:
    u['patches'].append({'operation':'append','claim':{'kind':'options','quote':json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':')),'selector':{'variant_id':row['new_item_id']},'asserted':row['options']},'reason':'Bind repeated item-ID anchors and option values to exact structured row; truth still program computed.'})
 save(E/'semantic_review.json',review)
def report():
 from score_facts import evaluate
 from fact_verifier import replay
 scored=evaluate(B,E,None);raw=read(B/'results.json');api=calls(B/'model_calls.jsonl');external=calls(E/'model_calls.jsonl');rows=[]
 for s in scored:
  n=s['id'];t=read(B/(n+'_trajectory.json'));f=read(B/(n+'_final_state.json'));a=raw[n];dec=[x for x in api if x['branch']==n and x['stage']=='controller'];d=json.loads(dec[0]['response']['choices'][0]['message']['content']);first=d.get('work_id',d.get('u',{}).get('z',{}).get('work_id'))
  outcomes=f['P']['clarification_outcomes'];new=[x for x in outcomes if x['new_permission_effective']]
  # This is a source-bound semantic review, not a tool fact or independent blinded judgment.
  preference={'accurate':False,'quote':"Since you've said you don't accept a lower zoom",'source_ref':12,'source_quote':read(R/'configs/start_evidence.json')['false_rule']['source_quote'],'reason':'Not having accepted any lower-zoom alternative is not a categorical refusal to accept lower zoom.'}
  rows.append({'id':n,'repeat':int(n.split('_')[1][1:]),'group':n.rsplit('_',1)[1],'first_work':first,'first_reason':d.get('reason',d.get('comparison')),
   'reclarified':any(e.get('u',{}).get('z',{}).get('work_id')=='clarify' for e in t),'outcomes':outcomes,'new_effective_permission':bool(new),'final_authorization':a['C_authorization_program'] and a['C_authorization_provenance'],'correct_write':a['R_write'],'constraints':a['C_hard'] and a['C_permission_state'],
   'facts':s['factual_status'],'user_statement_review':preference,'simulator_policy_adherent':n!='t52_r1_recovery_direct','quality':s['quality_pass'] and preference['accurate'] and n!='t52_r1_recovery_direct',
   'steps':a['steps'],'work_sequence':[e['u']['z']['work_id'] for e in t if 'u'in e],'rejections':sum('rejection'in e for e in t),'stop_reason':a.get('error'),'Agent':cost([x for x in api if x['branch']==n and x['category']=='agent']),
   'historical_false_rule_preserved':any(x.get('variant_id')=='3892645120' and x['source']==12 and x['sat']=='未满足' for x in f['H']['permission_history']),
   'safe_refusal_without_write':a.get('error')=='user_declined' and not f['P']['writes'] and not f['H']['confirmations']})
 lines=['# 第13轮配对结果表','','D=直接组，C=候选组。拒办不是错误提交；登记与完整质量分开。两侧全质量通过才计算投入差。','', '|重复|D/C首步|D/C澄清结果|D/C新有效许可|D/C最终授权|D/C正确登记|D/C事实|用户表述准确|D/C工作数|可比/投入差|','|---|---|---|---|---|---|---|---|---|---|'];pairs=[]
 for rep in (1,2):
  d,c=[next(x for x in rows if x['repeat']==rep and x['group']==g) for g in ('direct','candidate')];same=read(B/(d['id']+'_start.json'))==read(B/(c['id']+'_start.json'));ok=d['quality'] and c['quality'];pairs.append({'repeat':rep,'complete_start_equal':same,'quality_comparable':ok,'Agent_tokens_D_minus_C':d['Agent']['total_tokens']-c['Agent']['total_tokens'] if ok else None})
  vals=[rep,d['first_work']+'/'+c['first_work'],d['outcomes'][-1]['outcome']+'/'+c['outcomes'][-1]['outcome'],f"{d['new_effective_permission']}/{c['new_effective_permission']}",f"{d['final_authorization']}/{c['final_authorization']}",f"{d['correct_write']}/{c['correct_write']}",d['facts']+'/'+c['facts'],'False/False',f"{d['steps']}/{c['steps']}",'否 / —' if not ok else str(pairs[-1]['Agent_tokens_D_minus_C'])];lines.append('|'+ '|'.join(map(str,vals))+'|')
 (R/'results/PAIRED_RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 accounts={k:cost([x for x in api+external if x['category']==k]) for k in sorted({x['category'] for x in api+external})};dev=calls(R/'results/batch01/model_calls.jsonl');devcost={k:cost([x for x in dev if x['category']==k]) for k in sorted({x['category'] for x in dev})}
 save(R/'results/SUMMARY.json',{'official_batch':'batch02','rows':rows,'pairs':pairs,'accounts':accounts,'development_accounts':devcost,'versions':dict(Counter(str(x.get('response',{}).get('model'))+' / '+str(x.get('response',{}).get('system_fingerprint')) for x in api+external)),'review_limit':'User-intent and simulator consistency reviewed by assistant, not independent human gold.'})
 # Full successful trace includes current-turn completion predicates and terminal tool write.
 n='t52_r2_recovery_direct';t=read(B/(n+'_trajectory.json'));lines=['# 完整恢复轨迹：直接组第2次','','这是实际成功轨迹，包含话术误述。其他失败/拒办轨迹不删除，配对质量门槛仍不通过。','']
 for i,e in enumerate(t):
  lines+=['## 记录'+str(i+1),'']
  if 'u'in e:
   lines+=['工作：'+e['u']['z']['work_id'],'模型决策：'+json.dumps(e['decision'],ensure_ascii=False),'执行前许可：'+json.dumps(e['before']['g'].get('conditional_permission'),ensure_ascii=False),'完成条件：'+e['completion_test']+' = '+str(e['completion_satisfied'])]
   if 'assistant'in e:lines+=['助手：'+e['assistant'],'用户：'+e['customer'],'模型语义：'+json.dumps(e['semantic_parse'],ensure_ascii=False)]
   else:lines+=['程序/工具结果：'+json.dumps(e.get('result'),ensure_ascii=False)]
   if e.get('clarification_resolution'):lines+=['本轮澄清核验：'+json.dumps(e['clarification_resolution'],ensure_ascii=False)]
   lines+=['执行后许可：'+json.dumps(e['after']['g'].get('conditional_permission'),ensure_ascii=False),'执行后方案：'+json.dumps(e['after']['H']['plan'],ensure_ascii=False),'当前授权：'+json.dumps(e['after']['H']['confirmations'],ensure_ascii=False)]
  else:lines+=['拒绝/停止：'+json.dumps(e,ensure_ascii=False)]
 (R/'results/FULL_TRACE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 confirmations=[]
 for x in calls(B/'program_confirmations.jsonl'):
  h=read(B/(x['branch']+'_final_state.json'))['F']['dialogue'];ref=next(i for i,m in enumerate(h) if m.get('content')==x['text']);ev=replay(h,ref);p=x['plan'];v=ev['products']['8940227892']['variants']['6384525445'];order=ev['orders']['#W4689314'];old=next(i for i in order['items'] if i['item_id']=='5996159312');method=ev['users'][order['user_id']]['payment_methods']['paypal_8194385']
  valid=v['available'] is True and p['rows'][0]['options']==v['options'] and Decimal(str(p['difference']))==Decimal(str(v['price']))-Decimal(str(old['price'])) and p['payment_method']==method
  confirmations.append({'branch':x['branch'],'ref':ref,'fields_valid_at_utterance':valid,'plan':p})
 assert all(x['fields_valid_at_utterance'] for x in confirmations);save(R/'results/CONFIRMATION_CHECKS.json',confirmations)
 print(json.dumps({'rows':rows,'accounts':accounts,'dev_accounts':devcost,'pairs':pairs},ensure_ascii=False,indent=2))
if __name__=='__main__':
 if sys.argv[1]=='annotate':annotate()
 else:report()
