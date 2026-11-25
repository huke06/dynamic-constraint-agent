"""Read-only verification of execution freezes and preserved prior source tree."""
from post26 import *
import sys,subprocess

def run():
 sys.path.insert(0,str(E/'src'));import run26
 run26.verify();checked=[]
 for p in [R/'experiments/preliminary/round25-on-demand-v2/configs/FREEZE.json',E/'configs/FREEZE.json',*sorted((E/'versions').glob('*/FREEZE.json'))]:
  x=read(p);fs=x.get('files',{})
  for name,expected in fs.items():assert sha(R/name)==expected,(p,name)
  checked.append({'freeze':str(p.relative_to(R)),'checked_files':len(fs),'passed':True})
 for p in (E/'versions').glob('*/EXTRA_*_FREEZE.json'):
  x=read(p);source=p.parent/('extra_R55.py' if 'R55' in p.name else 'extra_RDB02.py');assert sha(source)==x['source_sha256'];checked.append({'freeze':str(p.relative_to(R)),'extra_runner_checked':True,'passed':True})
 old=['experiments/preliminary/round23-framework-loop','experiments/preliminary/round24-official-and-trajectory','src/dynamic_constraint_agent_v2']
 changes=subprocess.check_output(['git','diff','--name-only','HEAD','--',*old],cwd=R).decode().splitlines();assert not changes,changes
 report={'passed':True,'freezes':checked,'prior_23_24_tracked_byte_changes':changes,'sample_validation':read(E/'samples/VALIDATION_REPORT.json')['passed'],'formal_counts':{'round25':16,'A01':len(read(E/'results/A01/OUTCOMES.json')),'B01':len(read(E/'results/B01/OUTCOMES.json')),'targeted_rechecks':sum(len(read(p)) for p in (E/'versions').glob('*/results/*/OUTCOMES.json'))},'native_tau2_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd='D:/experimentn/tau2-official').decode().strip(),'native_agent_source_sha256':sha(Path('D:/experimentn/tau2-official/src/tau2/agent/llm_agent.py')),'native_tools_source_sha256':sha(Path('D:/experimentn/tau2-official/src/tau2/domains/retail/tools.py'))};save(E/'results/DELIVERY_CHECKS.json',report);print(report)
if __name__=='__main__':run()
