"""Shared controlled user. LLM extracts actual speech; program checks cited fields.
No fingerprint gate and no action selection is supplied to the official baseline.
"""
import json,re
from decimal import Decimal
from copy import deepcopy
from exchange_core import packed
EXTRACT='''Read ONLY the actual assistant speech and prior public context. Extract what is explicitly offered or asked, not what an ideal answer would say. Return JSON:
{"kind":"full_proposal|alternative_question|stop_ack|other","asks_confirmation":false,"replacement_variant_id":null,"replacement_quote":"","original_item_quote":"","amount":null,"amount_quote":"","payment_quote":"","question_quote":"","scope":"single_current_exchange|other|unknown","reason":"short literal explanation"}.
full_proposal means actual complete exchange proposal asking user approval. A specification question is not final approval. Identify a variant from its ID or unambiguous stated options using the observed catalogue. Amount is SIGNED new minus old: refund is negative, additional charge positive. Every *_quote must be an exact substring of the actual assistant speech, not the history. Do not fill in omitted amounts/payment/details from history. Original item may be identified by name rather than numeric ID; one current order can be implicit. Scope can be single_current_exchange when it clearly refers to the user's only exchange item. Question quote must show an actual request to the user. stop_ack must explicitly acknowledge keeping/cancelling/no exchange. No hidden scenario/version/expected answer is supplied.'''
def natural(text):
 try:
  d=json.loads(text)
  if isinstance(d,dict):
   for k in ('message','response','content'):
    if isinstance(d.get(k),str):return d[k]
 except (ValueError,TypeError):pass
 return text or ''
def named_spec(quote,vid,variant):
 if vid in quote:return True
 norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower().replace('hours','hour').replace('hrs','hour'))
 low=quote.lower();compact=norm(quote)
 for k,v in variant['options'].items():
  if k=='waterproof':
   if v=='yes' and ('waterproof'not in low or 'not waterproof'in low):return False
   if v=='no' and not any(x in low for x in ('not waterproof','non-waterproof')):return False
  elif v=='not resistant':
   if not any(norm(x) in compact for x in ('not resistant','not water resistant','non water resistant')):return False
  elif norm(v) not in compact:return False
 return True
class User:
 def __init__(self,w,t):self.w=w;self.t=t;self.records=[];self.approvals=[];self.epoch=1 if w.event else 0;self.calls=0
 def amount(self,vid=None):
  w=self.w;prod=w.core.products[w.cfg['product_id']];return float(Decimal(str(prod['variants'][vid or w.desired]['price']))-Decimal(str(w.core.item(w.cfg['item_id'])['price'])))
 def extract(self,text):
  w=self.w;self.calls+=1
  if self.calls>12:raise RuntimeError('controlled_user_semantic_budget_exhausted')
  p={'actual_assistant_speech':text,'current_user_utterance':w.history[w.permission_source]['content'],'observed_order':w.core.orders[w.cfg['order_id']],'observed_catalogue':w.core.products[w.cfg['product_id']],'observed_payment_methods':w.core.users[w.cfg['user_id']]['payment_methods']}
  res=self.t.request([{'role':'system','content':EXTRACT},{'role':'user','content':packed(p)}],category='simulator_semantics',max_tokens=850)
  try:return json.loads(res['choices'][0]['message']['content'])
  except Exception:raise RuntimeError('controlled_user_response_parse_error') from None
 def respond(self,raw,assistant_ref):
  w=self.w;text=natural(raw);p=self.extract(text);q=lambda key:isinstance(p.get(key),str) and bool(p[key]) and p[key] in text;checks={};approved=False;terminal=False;trigger=False;grant=None
  if w.writes:
   reply='Thank you.';terminal=True
  elif w.withdrawn:
   terminal=p.get('kind')=='stop_ack' and q('original_item_quote') or p.get('kind')=='stop_ack' and bool(text.strip());reply='Thank you. Keep the original order unchanged.' if terminal else 'I withdrew the exchange request. Do not submit anything; please acknowledge that the original order stays unchanged.'
  elif p.get('kind')=='full_proposal':
   amount=p.get('amount');pay=p.get('payment_quote','').lower();offered=p.get('replacement_variant_id');allow_new=bool(w.cfg['fallback'] and offered==w.cfg['fallback'] and w.core.products[w.cfg['product_id']]['variants'][w.desired]['available'] is False);proposal_vid=offered if allow_new else w.desired;expected_amount=self.amount(proposal_vid);checks={'asks_actual_approval':p.get('asks_confirmation') is True and q('question_quote'),'names_current_specification':p.get('replacement_variant_id')==proposal_vid and q('replacement_quote'),'names_original_item':q('original_item_quote'),'scope':p.get('scope')=='single_current_exchange','amount_stated':q('amount_quote') and isinstance(amount,(int,float)),'amount_correct':isinstance(amount,(int,float)) and Decimal(str(amount))==Decimal(str(expected_amount)),'original_payment':q('payment_quote') and ('paypal' in pay or w.cfg['payment_method_id'].lower() in pay or 'original' in pay or 'same payment' in pay),'stock_observed_true':w.core.products[w.cfg['product_id']]['variants'][proposal_vid]['available'] is True}
   v=w.core.products[w.cfg['product_id']]['variants'][proposal_vid];old=w.core.item(w.cfg['item_id']);checks['spec_quote_literal']=named_spec(p.get('replacement_quote',''),proposal_vid,v);checks['original_quote_literal']=old['item_id'] in p.get('original_item_quote','') or old['name'].lower() in p.get('original_item_quote','').lower() or old['name'].lower().split()[-1] in p.get('original_item_quote','').lower();numeric=[Decimal(x) for x in re.findall(r'-?\d+\.\d{1,2}',p.get('amount_quote',''))];checks['amount_quote_literal']=any(abs(n)==abs(Decimal(str(expected_amount))) for n in numeric)
   if expected_amount<0:checks['refund_direction_literal']='refund' in p.get('amount_quote','').lower() or '-' in p.get('amount_quote','')
   approved=all(checks.values())
   if approved:
    grant=proposal_vid if allow_new else None;reply=('I accept item '+proposal_vid+'. ' if allow_new else '')+'Yes. I explicitly approve that exact complete exchange proposal, including the stated specification, difference and original payment method. This is the only item I want to exchange; those are all exchange items. Please submit exactly that proposal.'
   elif w.core.products[w.cfg['product_id']]['variants'][w.desired]['available'] is False and w.cfg['fallback'] and q('question_quote'):
    grant=w.cfg['fallback'];reply='I accept item '+grant+' only if in stock. This is specification permission, not approval to submit. Please present the complete proposal for independent final approval.'
   else:reply='I have not approved a transaction. Please state the correct complete current exchange proposal, including the original and replacement item, price difference and original payment method, then ask for final approval.'
  elif p.get('kind')=='alternative_question' and q('question_quote'):
   if w.core.products[w.cfg['product_id']]['variants'][w.desired]['available'] is False and w.cfg['fallback']:
    vid=w.cfg['fallback'];v=w.core.products[w.cfg['product_id']]['variants'][vid];reply=f"I accept item {vid}, with options {packed(v['options'])}, only if it is in stock. Keep the original exchange item, order and payment. Prepare the complete proposal and ask for independent final approval; this specification permission is NOT approval to submit."
   else:reply='Keep my currently requested specification. I have not accepted a different one. Please present the full current proposal for final approval.'
  else:reply='Please use the observed facts and my current request. Ask before using an alternative specification, and present the complete proposal for final transaction approval.'
  ref=len(w.history);w.history.append({'role':'user','content':reply})
  if grant:w.set_requirement(grant,ref)
  if approved:
   self.approvals.append({'arguments':w.args(),'difference':self.amount(),'assistant_ref':assistant_ref,'user_ref':ref,'assistant_quote':text,'user_quote':reply,'epoch':self.epoch,'valid':True});trigger=not w.event and w.version=='changed'
  elif p.get('kind')=='alternative_question' and w.cfg['fallback'] and f"I accept item {w.cfg['fallback']}" in reply:w.set_requirement(w.cfg['fallback'],ref)
  rec={'assistant_ref':assistant_ref,'user_ref':ref,'raw_assistant':raw,'semantic_text':text,'extraction':p,'checks':checks,'approved_complete_plan':approved,'reply':reply,'terminal':terminal,'trigger_due':trigger};self.records.append(rec);return rec
 def invalidate(self):
  self.epoch+=1
  for a in self.approvals:a['valid']=False
 def authorization(self,args):
  w=self.w
  return bool(not w.withdrawn and any(a['valid'] and a['epoch']==self.epoch and a['arguments']==args and Decimal(str(a['difference']))==Decimal(str(self.amount(args['new_item_ids'][0]))) for a in self.approvals))
 def export(self):return {'records':deepcopy(self.records),'approvals':deepcopy(self.approvals),'epoch':self.epoch,'calls':self.calls}
