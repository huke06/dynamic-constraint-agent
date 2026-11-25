"""Round24 adapters only. Round23 v2 modules remain byte-for-byte frozen."""
import os, sys, json, time, hashlib, re
from pathlib import Path
from copy import deepcopy
from decimal import Decimal
sys.dont_write_bytecode = True
E=Path(__file__).resolve().parents[1]; R=E.parents[2]
V=R/'experiments/preliminary/round23-framework-loop/versions/v2'
os.environ['DCA_EXPERIMENT_DIR']=str(V)
sys.path[:0]=[str(R/'src'),str(R/'src/dynamic_constraint_agent_v2/compat')]
from construct20 import read,save,sha
import baseline_runner as b
from transport20 import Transport
from dynamic_constraint_agent_v2.state_model import BusinessState
from dynamic_constraint_agent_v2.decision import choose
from dynamic_constraint_agent_v2.execution import execute
from dynamic_constraint_agent_v2.evaluation import outcome
from runner20 import semantic, POLICY
from exchange_core import packed
from world20 import dump
from tau2.agent.llm_agent import LLMAgent
from tau2.data_model.message import AssistantMessage,UserMessage,ToolMessage,ToolCall,MultiToolMessage

EXTRACT='''You ONLY extract what this ACTUAL assistant speech says, not what would be correct. Return JSON {"kind":"proposal|clarification|stop|other","asks":boolean,"question_quote":"literal substring asking approval or permission", "pairs":[{"item_id":"original purchased ID", "new_item_id":"replacement ID", "quote":"literal substring supporting this mapping"}],"offers":[{"item_id":"original ID", "variant_id":"replacement ID", "quote":"literal offered ID substring"}],"difference":number or null,"amount_quote":"literal substring", "payment_method_id":"ID or null", "payment_quote":"literal substring", "stop_quote":"literal substring"}. A complete proposal lists all items, signed new-minus-original net amount and payment, asks final approval. A negative difference/refund is negative; charge is positive. Natural prose and JSON plan text are equally valid. Clarification asks specification willingness, not final transaction approval. If complete proposal contains unpermitted substitutes, still extract proposal; environment will evaluate. Do not invent missing IDs, quote, amount or approval. Program JSON rows and arguments support mappings. A question about original payment counts original-payment quote. Stop only if assistant explicitly terminates, not merely says do not submit yet.'''

def job(w,k,v=None):
 i=w.cfg['scope'][0]
 return {'work_type':k,'object':w.item(i)['product_id'] if k=='query' else i if k in ('analyze','clarify') else w.cfg['order_id'],'parameters':{'variant_id':v} if v else {},'evidence_refs':[],'expected':'obtain the defined result and feed it back','reason':'predeclared executable first work, not an autonomous model choice'}

def build_case(tid,oid,scope):
 db=read(b.DATA/'db.json');o=db['orders'][oid];u=db['users'][o['user_id']];products={};targets={};opts={}
 for idx,i in enumerate(scope):
  item=next(x for x in o['items'] if x['item_id']==i);p=db['products'][item['product_id']];products[item['product_id']]=p
  vs=sorted([v for v in p['variants'].values() if v['available'] and v['item_id']!=i],key=lambda v:(v['price'],v['item_id']))
  v=vs[-1] if idx==0 else vs[0];targets[i]=v['item_id'];opts[i]=v['options']
 cfg={'task_id':tid,'tier':'controlled_exchange','order_id':oid,'user_id':o['user_id'],'scope':scope,'targets':targets,'initial_options':opts,'payment_method_id':o['payment_history'][0]['payment_method_id'],'initial_catalogues':True,'change_type':'none','environment':{'orders':{oid:o},'users':{o['user_id']:u},'products':products}}
 cfg['initial_message']=f"I am {o['user_id']}, email {u['email']}. In delivered order {oid} exchange ONLY original-to-replacement mapping {packed(targets)}, options {packed(opts)}. Other items stay unchanged. Use original payment {cfg['payment_method_id']}. These specifications are permitted only if in stock and within my signed whole-amount cap. Different specifications need new permission. After that, show ALL current items, exact combined new-minus-old difference and original payment for independent final approval. Initial preferences are negotiable; stock, cap, scope and separate final approval are hard."
 return cfg

def prepare():
 tasks=read(b.DATA/'tasks.json')
 for tid in ('80','23'):
  cfg=read(R/f'experiments/preliminary/round21/archive/configs/stage2/{tid}/case.json');save(E/f'configs/A/{tid}/case.json',cfg)
 cfg=read(V/'configs/tasks/29/case.json');save(E/'configs/A/29/case.json',cfg)
 cfg=build_case('39','#W5285031',['4063058357','2235648106'])
 w=BusinessState(cfg,'stable',None);w.initialize_constraints(10000);ds=sorted(Decimal(str(v['whole_difference'])) for v in w.comparison()['negotiable']);cap=(ds[0]+w.difference())/2
 assert ds and cap<w.difference();cfg['cap']=str(cap);cfg['adaptation']='Untouched original task39 is identity/address business; controlled two-item exchange subtask of its delivered order. This is not official-task success. No task39 model debugging before formal batch.';save(E/'configs/A/39/case.json',cfg)
 for tid in ('80','23','29','39'):
  save(E/f'configs/A/{tid}/original_task.json',next(x for x in tasks if x['id']==tid));save(E/f'configs/A/{tid}/adaptation.json',{'task':tid,'business':'controlled exchange continuation','original_retained':True,'event':{'80':'none','23':'resource after actual complete approval','29':'user requirement after actual complete approval','39':'initial cap conflict, no injected event'}[tid]})
 for tid in ('26','35'):
  for f in ('case.json','original_task.json','subtask.json'):
   save(E/f'configs/B/{tid}/{f}',read(V/f'configs/tasks/{tid}/{f}'))
 states=[{'id':'26_capacity','task':'26','priorities':['capacity','color','material']},{'id':'26_appearance','task':'26','priorities':['color','material','capacity']},{'id':'35_waterproof','task':'35','priorities':['waterproof','color','battery life']}]
 # Check exact option names against the actual catalogue before freeze.
 p=read(E/'configs/B/35/case.json');first=p['scope'][0];keys=p['initial_options'][first];states[-1]['priorities']=[k for k in ['waterproof','color'] if k in keys]+[k for k in keys if k not in ('waterproof','color')]
 save(E/'configs/B/states.json',states)
 save(E/'configs/model_budget.json',read(V/'configs/runtime.json'))
 save(E/'configs/official_source.json',{'file':str(b.REPO/'src/tau2/agent/llm_agent.py'),'sha256':sha(b.REPO/'src/tau2/agent/llm_agent.py'),'loop':'unmodified LLMAgent.generate_next_message; completion transport patched only; native tools unchanged'})

class SharedWorld(BusinessState):
 def reply(self,kind,ar,detail):
  # The same speech->extract->program adjudicate path serves BOTH groups.
  rec=respond(self,self.history[ar]['content'],ar)
  if self.group=='framework' and kind=='confirm':
   self.asks[str(rec['user_ref'])]={'kind':'confirm','assistant_ref':ar,'proposal':deepcopy(detail)}
  self.sim_records.append(rec)
  return rec['user_ref']

def snapshot(cfg,version,t,group='framework',cap=None,preferences=None):
 cfg=deepcopy(cfg)
 if preferences:
  cfg['initial_message']+=' SOFT preference priority, highest first: '+packed(preferences)+'. Preserve the CURRENT initially requested value for the highest priority if feasible; lower priorities may be negotiated. These are soft, not a refusal of an explicitly proposed in-stock/cap-compliant offer. I may explicitly accept a tradeoff, but still evaluate how well it preserves these priorities.'
 w=SharedWorld(cfg,version,t);w.group=group;w.sim_records=[];w.policy=POLICY;w.initialize_constraints(cap if cap is not None else cfg.get('cap',10000));return w

def quoted(text,s):return isinstance(s,str) and bool(s) and s in text

def reply_record(w,ar,text,kind,detail=None,approved=False):
 ref=len(w.history);w.history.append({'role':'user','content':text})
 if w.group=='framework':w.pending.append(ref)
 if kind=='clarify':w.asks[str(ref)]={'kind':'clarify','assistant_ref':ar,**detail}
 if approved:
  w.env_approvals.append({'arguments':deepcopy(detail['arguments']),'difference':detail['difference'],'source_ref':ref,'assistant_ref':ar,'quote':text,'epoch':w.env_epoch,'valid':True})
 w.env_records.append({'ask_kind':kind,'assistant_ref':ar,'user_ref':ref,'reply':text,'approved':approved})
 if approved:w.trigger()
 return {'reply':text,'user_ref':ref,'kind':kind,'approved':approved}

def adjudicate(w,text,ar,p):
 """Literal speech extraction is untrusted. Numerical/native facts are deterministic."""
 permitted=w.oracle;scope=w.cfg['scope'];checks={};kind=p.get('kind');ask=p.get('asks') and quoted(text,p.get('question_quote'))
 mapping={}
 for x in p.get('pairs',[]):
  if x.get('item_id') in scope and quoted(text,x.get('quote')) and x.get('new_item_id') in x['quote'] and x.get('item_id') in x['quote']:mapping[x['item_id']]=x['new_item_id']
 # JSON argument arrays have separated original and new IDs; pair quote may span them.
 if kind=='proposal' and ask:
  checks['scope']=set(mapping)==set(scope) and len(p.get('pairs',[]))==len(scope)
  args={'order_id':w.cfg['order_id'],'item_ids':scope,'new_item_ids':[mapping.get(i) for i in scope],'payment_method_id':p.get('payment_method_id')}
  payquote=p.get('payment_quote','')
  if quoted(text,payquote) and ('original' in payquote.lower() or w.cfg['payment_method_id'] in payquote):args['payment_method_id']=w.cfg['payment_method_id'] if p.get('payment_method_id') in (None,w.cfg['payment_method_id']) else p['payment_method_id']
  checks['payment']=quoted(text,payquote) and args['payment_method_id']==w.cfg['payment_method_id'];delta=Decimal('0');valid=True
  for i,v in mapping.items():
   row=w.variant(i,v)
   if not row or row['available'] is not True or v==i:valid=False
   else:delta+=Decimal(str(row['price']))-Decimal(str(w.item(i)['price']))
  checks['stock']=valid and checks['scope'];checks['cap']=delta<=w.cap
  checks['amount']=quoted(text,p.get('amount_quote')) and isinstance(p.get('difference'),(int,float)) and Decimal(str(p['difference']))==delta
  checks['literal_amount']=any(abs(Decimal(s))==abs(delta) for s in re.findall(r'-?\d+\.\d+',p.get('amount_quote','')))
  checks['spec_permission']=checks['scope'] and all(mapping[i]==permitted[i] for i in scope)
  if all(checks.values()):
   q={'arguments':args,'difference':float(delta)}
   rec=reply_record(w,ar,'Yes, I approve exactly that complete combined proposal for all listed exchange items at the stated net difference and original payment. Those are all items I want exchanged.','confirm',q,True)
   return {**rec,'checks':checks,'extraction':p}
  rec=reply_record(w,ar,'I have not approved this transaction. Please correct '+', '.join(k for k,v in checks.items() if not v)+'. If a different specification is needed, ask my specification permission first. Then show all current items, correct signed combined difference and original payment for separate final approval.','correction')
  return {**rec,'checks':checks,'extraction':p}
 if kind=='clarification' and ask:
  offers=p.get('offers',[])
  # Actual order of offers, not catalogue sort or a hidden best answer.
  offers=sorted(offers,key=lambda x:text.find(x.get('quote','')))
  for x in offers:
   i=x.get('item_id');v=x.get('variant_id')
   if i not in scope or i!=scope[0] or not quoted(text,x.get('quote')) or not v or v not in x['quote'] or v==i:continue
   if not w.feasible(v):continue
   w.oracle[i]=v
   if w.group=='official':
    w.targets[i]=v;w.core.requirements[i]=deepcopy(w.variant(i,v)['options'])
   detail={'object':i,'offered_variant_id':v}
   rec=reply_record(w,ar,f'Replace my CURRENT request for original item {i} with SKU {v}, if in stock and whole signed difference <= {w.cap}. This supersedes the previous requested SKU for this item. Other items stay as agreed. This is specification permission only; show the complete new proposal for separate final approval.','clarify',detail)
   return {**rec,'extraction':p,'accepted_offer':v}
  rec=reply_record(w,ar,'I have not accepted any new specification. Please ask about a specific observed in-stock substitute within my hard whole-amount limit. Keep the other items unchanged.','correction');return {**rec,'extraction':p}
 if kind=='stop' and quoted(text,p.get('stop_quote')):
  # A clearly voluntary handoff is not a successful exchange in these solvable tasks.
  w.stopped=True;return {**reply_record(w,ar,'Please keep the order unchanged.','stop'),'extraction':p}
 return {**reply_record(w,ar,'Please follow my latest request. Ask about specific alternatives if necessary, then present the complete correct proposal and ask my final approval before writing.','correction'),'extraction':p}

def respond(w,text,ar):
 payload={'actual_assistant':text,'scope_original_ids':w.cfg['scope'],'order_id':w.cfg['order_id']}
 p=w.t.json([{'role':'system','content':EXTRACT},{'role':'user','content':packed(payload)}],'simulator','actual_speech_interpretation',max_tokens=2100)
 return adjudicate(w,text,ar,p)

def typed(m):
 if m['role']=='user':return UserMessage(role='user',content=m['content'])
 if m['role']=='tool':return ToolMessage(role='tool',id=m['tool_call_id'],content=m['content'])
 return AssistantMessage(role='assistant',content=m.get('content'),tool_calls=[ToolCall(id=a['id'],name=a['function']['name'],arguments=json.loads(a['function']['arguments'])) for a in m.get('tool_calls',[])] or None)

def roll(out,n,cfg,version,t,group='framework',first=None,cap=None,preferences=None):
 w=snapshot(cfg,version,t,group,cap,preferences);t.world=w;t.branch=n;trace=[];error=None;start=time.perf_counter();save(out/(n+'_start.json'),w.export());save(out/(n+'_visible_start.json'),w.model_state(True) if group=='framework' else w.history)
 repeated={};agent=None
 if group=='official':
  agent=LLMAgent(list(w.tools.get_tools().values()),POLICY,llm=b.MODEL,llm_args={'temperature':0,'max_tokens':1700,'num_retries':0});h=[typed(m) for m in w.history];state=agent.get_init_state(h[:-1]);incoming=h[-1]
 try:
  if first:
   v=w.comparison()['negotiable'][0]['variant_id'] if first=='clarify' else None;execute(w,job(w,first,v),t,trace)
  for tick in range(35):
   if w.writes or w.stopped:break
   if min(w.remaining_budget.values())<=0:error='budget_exhausted';break
   if group=='framework':
    if w.pending:semantic(w,t,trace);continue
    d=choose(w,t,'candidate');trace.append({'module':'cognitive_decision','model_output':d,'state':w.model_state(True)});e=execute(w,d,t,trace)
    if not e['allowed']:
     key=packed([d,e['reason']]);repeated[key]=repeated.get(key,0)+1
     if repeated[key]>=3:error='repeated_same_rejection';break
   else:
    before=w.export();msg,state=agent.generate_next_message(incoming,state);ar=len(w.history);raw={'role':'assistant','content':msg.content}
    if msg.tool_calls:raw['tool_calls']=[{'id':a.id,'type':'function','function':{'name':a.name,'arguments':packed(a.arguments)}} for a in msg.tool_calls]
    w.history.append(raw)
    if msg.tool_calls:
     outputs=[]
     for tc in msg.tool_calls:
      check={'independent_valid_authorization':w.env_valid(tc.arguments)} if tc.name=='exchange_delivered_order_items' else None;err=None
      try:
       result=dump(w.tools.use_tool(tc.name,**tc.arguments));w.history.append({'role':'tool','tool_call_id':tc.id,'content':packed(result)});w.core.observe(tc.name,tc.arguments,result,len(w.history)-1)
       if tc.name=='exchange_delivered_order_items':w.writes.append({'arguments':tc.arguments,'result':result,'independent':check})
       if tc.name=='transfer_to_human_agents':w.stopped=True
      except Exception as ex:err=str(ex);result={'error':err};w.history.append({'role':'tool','tool_call_id':tc.id,'content':packed(result)})
      w.remaining_budget['operations']-=1;trace.append({'module':'native_execution','model_original':msg.model_dump(mode='json'),'native_tool':tc.name,'parameters':tc.arguments,'before':before,'independent_submit_check':check,'actual_executed':err is None,'native_error':err,'result':result,'after':w.export()});outputs.append(ToolMessage(role='tool',id=tc.id,content=packed(result),error=err is not None))
     incoming=MultiToolMessage(role='tool',tool_messages=outputs)
    else:
     rec=respond(w,msg.content or '',ar);w.sim_records.append(rec);w.remaining_budget['operations']-=1;trace.append({'module':'native_speech','text':msg.content,'model_original':msg.model_dump(mode='json'),'user_result':rec,'before':before,'after':w.export()})
     if w.event_export:
      state.messages.append(UserMessage(role='user',content=rec['reply']));incoming=UserMessage(role='user',content='Public inventory/user update: '+w.change['public_text'])
     else:incoming=UserMessage(role='user',content=rec['reply'])
   if w.event_export:trace.append({'module':'public_change','event':w.event_export});w.event_export=None
   save(out/(n+'_trace.json'),trace)
  if not w.writes:error=error or ('stopped_without_write' if w.stopped else 'loop_limit')
 except Exception as ex:
  from logging16 import sanitize
  error=type(ex).__name__+': '+sanitize(ex,getattr(t.sdk,'secret',None));trace.append({'module':'failure','error':error})
 final=w.export();save(out/(n+'_trace.json'),trace);save(out/(n+'_final.json'),final);save(out/(n+'_simulator.json'),w.sim_records)
 result={'id':n,'task':cfg['task_id'],'group':group,'first':first,'error':error,'event_triggered':bool(w.change),'seconds':time.perf_counter()-start,**outcome(final)};print(result,flush=True);return result

def verify():
 for fp in (V/'configs/FREEZE.json',E/'configs/FREEZE.json'):
  assert all(sha(R/k)==v for k,v in read(fp)['files'].items()),str(fp)+' changed'

def freeze():
 assert read(E/'results/OFFLINE.json')['passed'];p=E/'configs/FREEZE.json';assert not p.exists()
 files={str(x.relative_to(R)):sha(x) for folder in (E/'src',E/'configs') for x in folder.rglob('*') if x.is_file() and '__pycache__' not in x.parts}
 save(p,{'files':files,'round23_v2_freeze':sha(V/'configs/FREEZE.json'),'utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()})

def batch(which):
 if which.startswith('pilot'):
  assert all(sha(R/k)==v for k,v in read(V/'configs/FREEZE.json')['files'].items())
 else:verify()
 out=E/'results'/which;out.mkdir(exist_ok=False)
 if which.startswith('pilot'):
  for p in (E/'src').glob('*.py'):(out/'development_source').mkdir(exist_ok=True);(out/'development_source'/p.name).write_bytes(p.read_bytes())
 t=Transport(out);t.install();rows=[]
 if which.startswith('pilot'):
  cases=[('80','stable'),('23','changed')]
  for tid,ver in cases:
   for g in ('official','framework'):
    n=f'pilot_t{tid}_{g}';rows.append(roll(out,n,read(E/f'configs/A/{tid}/case.json'),ver,t,g));save(out/'OUTCOMES.json',rows)
 elif which=='A01':
  for tid in ('80','23','29','39'):
   for rep in (1,2):
    for g in (('official','framework') if rep==1 else ('framework','official')):
     n=f'A_t{tid}_r{rep}_{g}';rows.append(roll(out,n,read(E/f'configs/A/{tid}/case.json'),'changed' if tid in ('23','29') else 'stable',t,g));save(out/'OUTCOMES.json',rows)
 elif which=='B01':
  for s in read(E/'configs/B/states.json'):
   cfg=read(E/f'configs/B/{s["task"]}/case.json');cap=cfg['caps']['conflict']
   for rep in (1,2):
    for first in (('analyze','clarify') if rep==1 else ('clarify','analyze')):
     n=f'B_{s["id"]}_r{rep}_{first}';rows.append(roll(out,n,cfg,'stable',t,'framework',first,cap,s['priorities']));save(out/'OUTCOMES.json',rows)
 t.close()

if __name__=='__main__':
 command=sys.argv[1]
 if command=='prepare':prepare()
 elif command=='freeze':freeze()
 else:batch(command)
