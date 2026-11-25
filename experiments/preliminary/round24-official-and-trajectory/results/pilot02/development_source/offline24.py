from run24 import *

def check():
 tests=[]
 def ok(name,p):
  assert p,name
  tests.append(name)
 for tid in ('80','23','29','39'):
  cfg=read(E/f'configs/A/{tid}/case.json');a=snapshot(cfg,'changed' if tid in ('23','29') else 'stable',None,'framework');b=snapshot(cfg,a.version,None,'official')
  ok(tid+' identical business history/database',a.history==b.history and a.tools.db==b.tools.db)
  ok(tid+' no private simulator branch in messages',all('env_approvals' not in m.get('content','') for m in a.history))
  if tid=='39':ok('fresh conflict feasible alternatives',not a.feasible() and bool(a.comparison()['negotiable']))
  else:
   p=a.core.compile(a.args());args=a.args();delta=a.difference();text='Approve complete plan '+packed(args)+' signed difference '+str(delta)+' original payment '+cfg['payment_method_id']+'?'
   pairs=[{'item_id':i,'new_item_id':v,'quote':text} for i,v in zip(args['item_ids'],args['new_item_ids'])]
   ext={'kind':'proposal','asks':True,'question_quote':'Approve complete plan','pairs':pairs,'difference':float(delta),'amount_quote':str(delta),'payment_method_id':cfg['payment_method_id'],'payment_quote':'original payment '+cfg['payment_method_id']}
   a.history.append({'role':'assistant','content':text});b.history.append({'role':'assistant','content':text});ra=adjudicate(a,text,len(a.history)-1,ext);rb=adjudicate(b,text,len(b.history)-1,ext)
   ok(tid+' natural full proposal equal approval',ra['approved'] and rb['approved'])
   ok(tid+' equal event exposure',a.change==b.change and a.history==b.history)
   if tid in ('23','29'):ok(tid+' old authorization invalidated',not a.env_valid(args) and not b.env_valid(args))
   wrong=deepcopy(ext);wrong['difference']=float(delta)+1;z=snapshot(cfg,'stable',None);z.history.append({'role':'assistant','content':text});ok(tid+' wrong amount not approved',not adjudicate(z,text,len(z.history)-1,wrong)['approved'])
 cfg=read(E/'configs/A/39/case.json')
 for group in ('framework','official'):
  w=snapshot(cfg,'stable',None,group);offers=w.comparison()['negotiable'];vs=offers[:2];i=cfg['scope'][0];text='For original '+i+', do you accept '+ ' or '.join(v['variant_id'] for v in vs)+' as specification only?'
  p={'kind':'clarification','asks':True,'question_quote':'do you accept','offers':[{'item_id':i,'variant_id':v['variant_id'],'quote':v['variant_id']} for v in vs]};w.history.append({'role':'assistant','content':text});res=adjudicate(w,text,len(w.history)-1,p)
  ok(group+' multichoice explicit reply matches internal permission',res.get('accepted_offer')==w.oracle[i] and w.oracle[i] in res['reply'])
  ok(group+' specification is not authorization',not w.env_valid(w.expected_args()))
  z=snapshot(cfg,'stable',None,group);z.history.append({'role':'assistant','content':text});bad=deepcopy(p)
  for offer in bad['offers']:offer['item_id']=scope_other=cfg['scope'][1]
  fixed=adjudicate(z,text,len(z.history)-1,bad);ok(group+' semantic wrong object resolved by unique visible catalogue membership',fixed['program_resolved_original_item']==i and z.oracle[i]==fixed['accepted_offer'])
  z=snapshot(cfg,'stable',None,group);z.history.append({'role':'assistant','content':'I will stop.'});r=adjudicate(z,'I will stop.',len(z.history)-1,{'kind':'stop','stop_quote':'I will stop.'});ok(group+' terminal no write',z.stopped and not z.writes)
 for s in read(E/'configs/B/states.json'):
  cfg=read(E/f'configs/B/{s["task"]}/case.json');a=snapshot(cfg,'stable',None,cap=cfg['caps']['conflict'],preferences=s['priorities']);b=snapshot(cfg,'stable',None,cap=cfg['caps']['conflict'],preferences=s['priorities'])
  ok(s['id']+' exact same paired starts',a.export()==b.export())
  ok(s['id']+' priorities visible to decision and analysis',all(p in packed(a.model_state()) for p in s['priorities']) and packed(s['priorities']) in a.model_state()['objects'][0]['CURRENT_EFFECTIVE_SPECIFICATION']['literal_user_source'])
  c=a.comparison();ok(s['id']+' both first works executable',c['status']=='no_exact_match' and bool(c['negotiable']) and all(a.feasible(v['variant_id']) for v in c['negotiable']))
  ok(s['id']+' no premature submit',not a.current_auth() and not a.env_valid(a.args()))
 # Fixed v2 untouched before any API call.
 f=read(V/'configs/FREEZE.json');ok('round23 v2 frozen bytes unchanged',all(sha(R/k)==v for k,v in f['files'].items()))
 out={'passed':True,'count':len(tests),'checks':tests,'scope':'adjudicator contracts use explicit extraction fixtures; actual semantic extraction additionally checked by separate pilot'};save(E/'results/OFFLINE.json',out);print(out)

if __name__=='__main__':check()
