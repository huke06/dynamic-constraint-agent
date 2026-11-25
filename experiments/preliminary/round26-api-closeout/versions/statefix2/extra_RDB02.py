from repair import *
if __name__=='__main__':
 r.verify();assert all(sha(c.R/k)==v for k,v in read(V/'FREEZE.json')['files'].items())
 plan=V/'EXTRA_RDB02_FREEZE.json';assert not plan.exists();save(plan,{'source_sha256':sha(Path(__file__)),'statefix2_freeze_sha256':sha(V/'FREEZE.json'),'affected':['A_R_RDB02_r1_official','A_R_RDB02_r1_framework'],'reason':'same anaphoric same-items rejection observed in statefix1 RDB02; no other tasks'})
 out=V/'results/recheck_RDB02';out.mkdir(parents=True,exist_ok=False);t=c.Transport(out);t.install();rows=[]
 for g in ('official','framework'):
  n='A_R_RDB02_r1_'+g;rows.append(r.rollout(out,n,read(E/'configs/tasks/R_RDB02/case.json'),t,g));save(out/'OUTCOMES.json',rows)
 t.close()
