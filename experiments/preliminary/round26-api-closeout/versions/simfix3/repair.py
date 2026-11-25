"""An actual question about continuation is not final termination."""
import sys,importlib.util,re
from pathlib import Path
V=Path(__file__).resolve().parent;E=V.parents[1]
spec=importlib.util.spec_from_file_location('refund_simfix',E/'versions/simfix2/repair.py');prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
c=prior.c;r=prior.r;read=c.read;save=c.save;sha=c.sha;old=c.adjudicate
def repaired(w,text,ar,p):
 q=p.get('question_quote')or''
 if p.get('kind')=='stop' and p.get('asks') and c.contains(text,q) and re.search(r'list|show|pick|choose|alternative|different.*option|continue',q,re.I) and not getattr(w,'oracle_withdrawn',False):
  rec=c.add_reply(w,ar,'Yes, please show or compare currently available compliant alternatives for the affected item. Keep every other agreed item and payment unchanged. This is permission to discuss options, not acceptance of any new SKU and not transaction approval.','information');return {**rec,'extraction':p,'program_question_binding':'conditional pause plus actual request to discuss alternatives is not task termination'}
 return old(w,text,ar,p)
c.adjudicate=repaired
def offline():
 cfg=read(c.a2.E/'configs/A/23/case.json');cfg.update(business='exchange',scenario='resource');w=r.snapshot(cfg,None,'official');text='I need to stop before processing. Would you like me to list the available alternatives?';p={'kind':'stop','asks':True,'question_quote':'Would you like me to list the available alternatives?','stop_quote':'I need to stop before processing.'};z=repaired(w,text,len(w.history),p);assert not w.stopped and not z['approved'] and not w.env_approvals;save(V/'OFFLINE.json',{'passed':True,'checks':['continuation question answered, not ended','no SKU permission or transaction approval invented']})
def freeze():
 assert read(V/'OFFLINE.json')['passed'];r.verify();files=[Path(__file__),E/'versions/simfix1/src/repair.py',E/'versions/simfix2/repair.py'];save(V/'FREEZE.json',{'files':{str(p.relative_to(c.R)):sha(p) for p in files},'affected_tasks':{'E_EDB05':[1,2]},'scope':'simulator termination/continuation binding only; no Agent policy/runtime change'})
def run():
 r.verify();assert all(sha(c.R/k)==v for k,v in read(V/'FREEZE.json')['files'].items());out=V/'results/recheck01';out.mkdir(parents=True,exist_ok=False);t=c.Transport(out);t.install();rows=[]
 for rep in (1,2):
  for g in ('official','framework'):
   n=f'A_E_EDB05_r{rep}_{g}';rows.append(r.rollout(out,n,read(E/'configs/tasks/E_EDB05/case.json'),t,g));save(out/'OUTCOMES.json',rows)
 t.close()
if __name__=='__main__':{'offline':offline,'freeze':freeze,'run':run}[sys.argv[1]]()
