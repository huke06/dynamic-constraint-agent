"""Shared neutral clarification and event-triggered controlled user; branch never enters Agent input."""
import json
from copy import deepcopy
import recovery13 as prior
from exchange_core import packed
from engine import Case
PRE_APPLY=Case.apply_user
def apply(c,parsed,ar,ur):
 p=deepcopy(parsed);ctx=getattr(c,'clarification_context',None)
 if ctx and ar==ctx['assistant_ref_expected']:
  resolution=p.get('clarification_resolution',{})
  valid=resolution.get('source_ref')==ur and bool(resolution.get('source_quote')) and resolution['source_quote'] in c.history[ur]['content']
  if not valid or resolution.get('kind')!='new_permission':
   p['permission_update']={'kind':'none'};p['authorization']={'approved':False}
   # Clarification is not a requirements-change channel when its reply has not decided anything.
   if resolution.get('kind')=='information_unclear':p['change']={'present':False}
 PRE_APPLY(c,p,ar,ur)
def clarification(c):
 product=c.core.products['8940227892'];old=product['variants']['3892645120'];assert old['available'] is False
 alternatives=[]
 for vid in ('6384525445','7255224608'):
  v=product['variants'][vid];assert v['available'] is True
  alternatives.append({'item_id':vid,'options':deepcopy(v['options']),'price':v['price'],'available':True,'inventory_source_ref':c.core.product_refs['8940227892']})
 fields={'out_of_stock':{'item_id':'3892645120','options':deepcopy(old['options']),'available':False},'available_alternatives':alternatives,'source_ref':c.core.product_refs['8940227892']}
 prefix='The 30MP, CF card, 10x zoom variant (item 3892645120) exists but is currently out of stock. '
 suffix=' The alternatives listed are in stock. You have not authorized either alternative yet. Would you accept one of them, reject both and keep your current order, or do you need more time? Accepting a variant is not final approval of an exchange plan.'
 if getattr(c,'clarification_outcomes',[]) and c.clarification_outcomes[-1]['outcome']=='information_unclear':
  prefix+='You have not made an explicit decision yet. Please clarify your decision. '
 text=prefix+'Observed alternatives: '+packed(alternatives)+suffix
 return text,fields
class Client(prior.Client):
 def __init__(self,out,responses):
  super().__init__(out);self.responses=responses;self.private_branches={};self.counts={};self.pending={};self.events=[];self.controlled_stream=(out/'controlled_events.jsonl').open('w',encoding='utf-8');self.grounded=(out/'grounded_clarifications.jsonl').open('w',encoding='utf-8')
 def ask(self,branch,category,stage,messages,max_tokens=1400,case=None):
  if stage=='worker' and case:
   wid=json.loads(messages[1]['content'])['u']['z']['work_id'];self.pending[branch]=(wid,case)
   if wid=='clarify':
    text,fields=clarification(case);self.grounded.write(packed({'branch':branch,'assistant_ref':len(case.history),'fields':fields,'text':text,'model_calls':0})+'\n');self.grounded.flush();return text
  if category=='environment_user' and stage=='customer':
   wid,c=self.pending[branch];mode=self.private_branches[branch];count=self.counts.get(branch,0)
   assert c.history[-1]['role']=='assistant','Controlled reply requires an actual delivered assistant question'
   if wid=='clarify':
    if mode=='ambiguous' and count==0:key='ambiguous_first'
    elif mode=='ambiguous':
     assert c.clarification_outcomes and c.clarification_outcomes[-1]['outcome']=='information_unclear','No valid prior ambiguous response followed by actual clarification'
     key='ambiguous_followup'
    else:key=mode
    self.counts[branch]=count+1
   elif wid=='confirm':
    assert mode!='reject' and c.plan and c.goal['alternative_permission']=='6384525445'
    assert c.plan['arguments']=={'order_id':'#W4689314','item_ids':['5996159312'],'new_item_ids':['6384525445'],'payment_method_id':'paypal_8194385'} and str(c.plan['quote']['difference'])=='34.07'
    assert mode!='ambiguous' or count>=2,'Confirmation cannot elicit acceptance before follow-up clarification'
    key='confirm'
   else:raise ValueError('User response only triggered by actual clarification or confirmation')
   reply=deepcopy(self.responses[key]);row={'branch':branch,'trigger_work':wid,'trigger_assistant_ref':len(c.history)-1,'private_response_key':key,'reply':reply,'model_calls':0};self.events.append(row);self.controlled_stream.write(packed(row)+'\n');self.controlled_stream.flush();return reply
  return super().ask(branch,category,stage,messages,max_tokens,case)
 def close(self):self.controlled_stream.close();self.grounded.close();super().close()
def install():Case.apply_user=apply
