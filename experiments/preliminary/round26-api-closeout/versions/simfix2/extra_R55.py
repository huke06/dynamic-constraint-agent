"""Separately preregistered replication of the same mixed-choice simulator defect."""
from repair import *
if __name__=='__main__':
 r.verify();assert all(sha(c.R/k)==v for k,v in read(V/'FREEZE.json')['files'].items())
 plan=V/'EXTRA_R55_FREEZE.json';assert not plan.exists();save(plan,{'source_sha256':sha(Path(__file__)),'simfix2_freeze_sha256':sha(V/'FREEZE.json'),'affected':['A_R_55_r1_official','A_R_55_r1_framework'],'reason':'same explicit refund-choice question misclassified as constraint question in original R55; both sides rerun, old failure retained'})
 out=V/'results/recheck_R55';out.mkdir(parents=True,exist_ok=False);t=c.Transport(out);t.install();rows=[]
 for g in ('official','framework'):
  n='A_R_55_r1_'+g;rows.append(r.rollout(out,n,read(E/'configs/tasks/R_55/case.json'),t,g));save(out/'OUTCOMES.json',rows)
 t.close()
