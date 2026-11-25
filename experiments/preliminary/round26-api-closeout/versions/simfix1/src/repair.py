"""Simulator-only original-refund proof correction; frozen agent/runtime unchanged."""
import sys
from pathlib import Path
V=Path(__file__).resolve().parents[1];E=V.parents[1]
sys.path.insert(0,str(E/'src'))
import core26 as c
import run26 as r
from core26 import read,save,sha,deepcopy
original=c.adjudicate
def repaired(w,text,ar,p):
 if w.business!='return':return original(w,text,ar,p)
 old=w.legal_methods
 def legal():
  values=list(old());o=w.observed.get('get_order_details')
  if o:
   method=o['payment_history'][0]['payment_method_id']
   if method not in values:values.insert(0,method)
  return values
 w.legal_methods=legal
 try:return original(w,text,ar,p)
 finally:w.legal_methods=old
c.adjudicate=repaired

def offline():
 t=__import__('offline26').Fixture();checks=[]
 for mid in ('R_30','R_31'):
  cfg=read(E/f'configs/tasks/{mid}/case.json');w=r.snapshot(cfg,t,'official');order=c.dump(w.tools.get_order_details(order_id=cfg['order_id']));w.observe('get_order_details',{'order_id':cfg['order_id']},order)
  amount=w.amount();method=order['payment_history'][0]['payment_method_id'];text=f"Return {c.packed(cfg['scope'])}, refund {amount} to original payment {method}. Do you approve?";p={'kind':'proposal','asks':True,'question_quote':'Do you approve?','item_ids':cfg['scope'],'payment_method_id':method,'payment_quote':method,'amount':float(amount),'amount_quote':str(amount)}
  assert repaired(w,text,len(w.history),p)['approved'];assert 'get_user_details' not in w.observed;checks.append(mid+' original method known from actual order, not private profile')
  z=r.snapshot(cfg,t,'official');assert not repaired(z,text,len(z.history),p)['approved'];checks.append(mid+' no observed order still cannot obtain final approval')
 save(V/'results/OFFLINE.json',{'passed':True,'checks':checks});print(checks)
def freeze():
 assert read(V/'results/OFFLINE.json')['passed'];r.verify();f=V/'FREEZE.json';assert not f.exists();save(f,{'original_freeze_sha256':sha(E/'configs/FREEZE.json'),'files':{str(Path(__file__).relative_to(c.R)):sha(Path(__file__))},'affected':['A_R_30_r1_official','A_R_30_r1_framework','A_R_31_r1_official','A_R_31_r1_framework'],'rule':'same native original payment proven by get_order_details, no need profile query; no model/policy/task/runtime changes'})
def run():
 r.verify();f=read(V/'FREEZE.json');assert all(sha(c.R/k)==v for k,v in f['files'].items());out=V/'results/recheck01';out.mkdir(parents=True,exist_ok=False);t=c.Transport(out);t.install();rows=[]
 for mid in ('R_30','R_31'):
  for g in ('official','framework'):
   cfg=read(E/f'configs/tasks/{mid}/case.json');n=f'A_{mid}_r1_{g}';rows.append(r.rollout(out,n,cfg,t,g));save(out/'OUTCOMES.json',rows)
 t.close()
if __name__=='__main__':{'offline':offline,'freeze':freeze,'run':run}[sys.argv[1]]()
