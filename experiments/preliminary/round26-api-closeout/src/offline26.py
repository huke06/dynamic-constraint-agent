from run26 import *

class Fixture:
 def json(self,messages,role,trigger,max_tokens=1700):
  payload=json.loads(messages[1]['content'])
  if role=='simulator':
   text=payload['actual_assistant']
   if text.startswith('Please'):
    pos=text.find('{');p=json.JSONDecoder().raw_decode(text[pos:])[0];a=p['arguments'];amt=p.get('refund_amount',p.get('difference'));return {'kind':'proposal','asks':True,'question_quote':'Do you approve','item_ids':a['item_ids'],'pairs':[{'item_id':i,'new_item_id':v,'quote':text} for i,v in zip(a['item_ids'],a.get('new_item_ids',[]))],'payment_method_id':a['payment_method_id'],'payment_quote':a['payment_method_id'],'amount':float(amt),'amount_quote':str(amt)}
   m=re.search(r'do you accept refund method ([\w_]+)',text)
   if m:return {'kind':'refund_permission','asks':True,'question_quote':m.group(0),'active_offers':[{'payment_method_id':m.group(1),'quote':m.group(0),'status':'active'}]}
   m=re.search(r'Proposed SUBSTITUTE (\d+)',text)
   if m:return {'kind':'spec_permission','asks':True,'question_quote':'Do you accept SKU '+m.group(1),'active_offers':[{'variant_id':m.group(1),'quote':m.group(1),'status':'active'}]}
  if role=='semantic' and 'pending' in payload:
   updates=[];refs=[]
   for msg in payload['pending']:
    ref=msg['source_ref'];text=msg['text'];ask=msg['in_response_to'];refs.append(ref)
    if 'withdraw the ENTIRE' in text:kind='withdrawal';z={}
    elif 'change my return scope' in text:kind='scope';z={'item_ids':json.loads(re.search(r'EXACTLY (\[.*?\])',text).group(1))}
    elif 'change the refund method' in text:kind='refund_permission';z={'payment_method_id':re.search(r'change the refund method to ([\w_]+)',text).group(1)}
    elif text.startswith('Use '):kind='refund_permission';z={'payment_method_id':text.split()[1]}
    elif text.startswith('Yes'):kind='approval';z={}
    else:kind='unclear';z={}
    updates.append({'kind':kind,'source_ref':ref,'quote':text,**z})
   return {'updates':updates,'processed_refs':refs}
  return {'analysis':'fixture typed facts only','tradeoffs':[],'not_authorization':True}

def action(w,k,p=None):return {'work_type':k,'object':w.cfg['order_id'],'parameters':p or{},'evidence_refs':[],'expected':'offline contract test','reason':'explicit fixture test'}
def parse_exchange(w):
 updates=[]
 for ref in w.pending:
  text=w.history[ref]['content'];ask=w.asks.get(str(ref))
  if ask and ask['kind']=='confirm' and text.startswith('Yes'):u={'kind':'approval'}
  elif ask and ask['kind']=='clarify' and text.startswith('Replace'):u={'kind':'permission','item_id':ask['object'],'variant_id':ask['offered_variant_id'],'conditional_stock':True}
  elif not ask:u={'kind':'requirement','item_id':w.cfg['scope'][0],'variant_id':w.cfg['changed_target'],'conditional_stock':True}
  else:u={'kind':'none'}
  updates.append({'source_ref':ref,'quote':text,**u})
 w.apply({'updates':updates,'processed_refs':list(w.pending),'needs_clarification':False})
def check():
 passed=[]
 def ok(n,b):assert b,n;passed.append(n)
 ms=read(E/'configs/TASKS.json');prior=read(E/'configs/PRIOR_USAGE.json');ok('20 independent unused orders',len(ms)==20 and len({m['order_id'] for m in ms})==20 and not set(prior['orders'])&{m['order_id'] for m in ms});ok('8 exchange 12 return',Counter(m['business'] for m in ms)=={'return':12,'exchange':8});ok('4 repeats fixed',len(read(E/'configs/REPEATS.json'))==4)
 t=Fixture()
 for m in ms:
  cfg=read(E/f'configs/tasks/{m["id"]}/case.json');w=snapshot(cfg,t,'framework');o=snapshot(cfg,t,'official');ok(m['id']+' same public start',w.history==o.history and w.tools.db==o.tools.db)
  if w.business=='exchange':
   ok(m['id']+' cap equal monetary precision',w.cap==money(w.cap) and str(w.cap) in w.history[w.cap_ref]['content'])
   if cfg['scenario']=='evidence':ok(m['id']+' no initial inventory leak',all(x['CURRENT_EFFECTIVE_SPECIFICATION']['stock'] is None for x in w.model_state()['objects']))
   if not cfg['initial_catalogues']:
    for pid in cfg['environment']['products']:w.observe('get_product_details',{'product_id':pid},dump(w.tools.get_product_details(product_id=pid)))
   if not w.feasible():
    v=w.comparison()['negotiable'][0]['variant_id'];ok(m['id']+' conflict clarification',exchange_execute(w,forced(w,'clarify',{'variant_id':v}),t,[])['allowed']);parse_exchange(w)
   for k in ('prepare','confirm'):ok(m['id']+' '+k,exchange_execute(w,action(w,k),t,[])['allowed'])
   parse_exchange(w)
   if cfg['change_type']!='none':
    ok(m['id']+' old approval invalid after change',not w.current_auth())
    if not w.feasible():
     v=w.comparison()['negotiable'][0]['variant_id'];ok(m['id']+' changed clarification',exchange_execute(w,forced(w,'clarify',{'variant_id':v}),t,[])['allowed']);parse_exchange(w)
    for k in ('prepare','confirm'):ok(m['id']+' fresh '+k,exchange_execute(w,action(w,k),t,[])['allowed'])
    parse_exchange(w)
   ok(m['id']+' native exchange write',exchange_execute(w,action(w,'submit'),t,[])['allowed']);ok(m['id']+' exact native end',evaluate(w)['correct'])
   continue
  if cfg['initial_missing']:
   ok(m['id']+' two actual missing evidence choices',not w.observed.get('get_order_details') and not w.observed.get('get_user_details') and return_dispatch(w).route=='decision_model')
   for tool,args in [('get_user_details',{'user_id':cfg['user_id']}),('get_order_details',{'order_id':cfg['order_id']})]:w.observe(tool,args,dump(w.tools.use_tool(tool,**args)))
  if cfg['scenario']=='conflict':
   ok(m['id']+' invalid refund gate',not w.feasible() and not return_execute(w,action(w,'submit'),t,[])['allowed']);method=w.legal_methods()[0];ok(m['id']+' legal permission execution',return_execute(w,action(w,'clarify',{'payment_method_id':method}),t,[])['allowed']);w.interpret(t,[])
  ok(m['id']+' prepare complete',return_execute(w,action(w,'prepare'),t,[])['allowed']);ok(m['id']+' no authorization cannot submit',not return_execute(w,action(w,'submit'),t,[])['allowed']);ok(m['id']+' confirm actual response',return_execute(w,action(w,'confirm'),t,[])['allowed'])
  if cfg['event']['kind']!='none':ok(m['id']+' old approval invalidated',not w.current_auth() and not w.env_valid(w.args()))
  w.interpret(t,[])
  if cfg['event']['kind']=='withdraw':
   ok(m['id']+' withdrawn stop',return_execute(w,action(w,'stop'),t,[])['allowed']);ok(m['id']+' unchanged DB',evaluate(w)['correct']);continue
  if cfg['event']['kind']!='none':
   ok(m['id']+' fresh complete plan',return_execute(w,action(w,'prepare'),t,[])['allowed']);ok(m['id']+' reconfirm',return_execute(w,action(w,'confirm'),t,[])['allowed']);w.interpret(t,[])
  ok(m['id']+' native return write',return_execute(w,action(w,'submit'),t,[])['allowed']);ok(m['id']+' native fields and authorization',evaluate(w)['correct'])
 for s in read(E/'configs/DPO_CHECKPOINTS.json'):
  a=snapshot(s['cfg'],t,'framework');b=snapshot(s['cfg'],t,'framework');ok(s['id']+' same branch starts',a.export()==b.export())
  for k in s['first_works']:
   z=snapshot(s['cfg'],t,'framework');d=forced(z,k,s['clarify_parameters']);fb=(exchange_execute if z.business=='exchange' else return_execute)(z,d,t,[]);ok(s['id']+' '+k+' executable first work',fb['allowed'] and bool(fb['result']))
 # Known round24 failure examples: real cap question and rejected earlier SKU.
 cfg=read(E/'configs/DPO_CHECKPOINTS.json')[0]['cfg'];w=snapshot(cfg,t,'official');text='Does the negative cap mean minimum refund or maximum refund?';p={'kind':'constraint_question','asks':True,'question_quote':text};rec=adjudicate(w,text,len(w.history),p);ok('cap clarification receives numeric <= answer','<=' in rec['reply'] and not rec['approved'])
 text='SKU 2698416822 is rejected and not allowed. Do you accept SKU 1240311797?';p={'kind':'spec_permission','asks':True,'question_quote':'Do you accept SKU 1240311797?','active_offers':[{'variant_id':'2698416822','quote':'2698416822','status':'active'},{'variant_id':'1240311797','quote':'1240311797','status':'active'}],'rejected_offer_ids':[]};rec=adjudicate(w,text,len(w.history),p);ok('earlier rejected candidate not permission',rec.get('accepted_offer')=='1240311797')
 cfg=read(E/'configs/PILOT_RETURN.json');w=snapshot(cfg,t,'official');text='Which refund methods does policy permit?';rec=adjudicate(w,text,len(w.history),{'kind':'constraint_question','asks':True,'question_quote':text});ok('refund rule question answered','original payment' in rec['reply'] and not rec['approved'])
 cfg=deepcopy(cfg);cfg['event']={'kind':'none'};w=snapshot(cfg,t,'official');amt=w.amount();text=f"Return {packed(w.scope)}, **Refund amount:** ${amt:.2f}, **Refund method:** {w.payment}. Do you approve?";p={'kind':'proposal','asks':True,'question_quote':'Do you approve?','item_ids':w.scope,'payment_method_id':w.payment,'payment_quote':'Refund method: '+w.payment,'amount':-float(amt),'amount_quote':'Refund amount: $'+str(amt)};rec=adjudicate(w,text,len(w.history),p);ok('return refund magnitude is not signed exchange delta',rec['approved']);ok('Markdown-equivalent quote is accepted',contains(text,p['amount_quote']))
 w=snapshot(cfg,t,'official');text='I will not proceed until you approve.';rec=adjudicate(w,text,len(w.history),{'kind':'stop','stop_quote':text});ok('conditional hold is not termination',not w.stopped)
 for text in ['I will not register any return.','Your order will remain unchanged.','I will not submit the request.']:
  w=snapshot(cfg,t,'official');w.oracle_withdrawn=True;rec=adjudicate(w,text,len(w.history),{'kind':'stop','stop_quote':text});ok('actual withdrawal acknowledgement '+text,w.stopped and w.terminal_reason=='withdrawal_acknowledged')
 w=snapshot(cfg,t,'framework');ok('return program rejection falls back to model',return_dispatch(w,False).route=='decision_model')
 f=read(a2.V/'configs/FREEZE.json');ok('old v2 remains byte-identical',all(sha(R/k)==v for k,v in f['files'].items()))
 save(E/'results/OFFLINE.json',{'passed':True,'count':len(passed),'checks':passed});print({'passed':True,'count':len(passed)})
if __name__=='__main__':check()
