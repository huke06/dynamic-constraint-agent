"""Actual explicit refund-choice question outranks a parser's rule-question label."""
import sys,importlib.util,re
from pathlib import Path
V=Path(__file__).resolve().parent;E=V.parents[1]
spec=importlib.util.spec_from_file_location('prior_simfix',E/'versions/simfix1/src/repair.py');prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
c=prior.c;r=prior.r;read=c.read;save=c.save;sha=c.sha
old=c.adjudicate
def repaired(w,text,ar,p):
 raw=c.deepcopy(p);q=p.get('question_quote')or''
 if w.business=='return' and p.get('kind')=='constraint_question' and p.get('active_offers') and c.contains(text,q) and re.search(r'accept|choose|select',q,re.I):
  p=c.deepcopy(p);p['kind']='refund_permission'
 rec=old(w,text,ar,p)
 if raw!=p:rec['raw_semantic_extraction']=raw;rec['program_question_binding']='actual explicit accept/choose question plus active concrete refund offer; not a generic policy inquiry'
 return rec
c.adjudicate=repaired
def offline():
 cfg=read(E/'configs/tasks/R_51/case.json');w=r.snapshot(cfg,None,'official');m=w.cfg['original_payment'];text=f'Legal route: refund to {m}. Which concrete route do you accept?';p={'kind':'constraint_question','asks':True,'question_quote':'Which concrete route do you accept?','active_offers':[{'payment_method_id':m,'quote':m,'status':'active'}]};z=repaired(w,text,len(w.history),p);assert z.get('accepted_offer')==m and not z['approved'];save(V/'OFFLINE.json',{'passed':True,'checks':['mixed explanation + explicit current choice binds permission','still no full transaction authorization']})
def freeze():
 assert read(V/'OFFLINE.json')['passed'];r.verify();save(V/'FREEZE.json',{'files':{str(Path(__file__).relative_to(c.R)):sha(Path(__file__)),str((E/'versions/simfix1/src/repair.py').relative_to(c.R)):sha(E/'versions/simfix1/src/repair.py')},'affected':['A_R_51_r1_official','A_R_51_r1_framework'],'scope':'simulator classification only; original explicit question was already a valid offered choice'})
def run():
 r.verify();assert all(sha(c.R/k)==v for k,v in read(V/'FREEZE.json')['files'].items());out=V/'results/recheck01';out.mkdir(parents=True,exist_ok=False);t=c.Transport(out);t.install();rows=[]
 for g in ('official','framework'):
  n='A_R_51_r1_'+g;rows.append(r.rollout(out,n,read(E/'configs/tasks/R_51/case.json'),t,g));save(out/'OUTCOMES.json',rows)
 t.close()
if __name__=='__main__':{'offline':offline,'freeze':freeze,'run':run}[sys.argv[1]]()
