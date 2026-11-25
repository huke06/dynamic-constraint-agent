"""Create-only full local copy; all original paths remain unchanged."""
from post26 import *
import shutil

if __name__=='__main__':
 target=Path('D:/experimentn/实验原始归档/round26-api-closeout-20261126');assert not target.exists(),'choose a new archive name; never overwrite'
 target.mkdir(parents=True);files=[]
 for root in [R/'experiments/preliminary/round25-on-demand-v2',E]:
  files.extend(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='RAW_ARCHIVES.json')
 files += [R/'src/dynamic_constraint_agent_runtime.py',R/'tests/test_on_demand_runtime.py',R/'docs/research_log.md',R/'experiments/preliminary/README.md']
 entries=[]
 for p in sorted(set(files)):
  rel=p.relative_to(R);q=target/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);h=sha(p);assert sha(q)==h;entries.append({'relative_path':str(rel),'bytes':p.stat().st_size,'sha256':h})
 manifest=target/'MANIFEST.json';save(manifest,{'source_root':str(R),'archive_root':str(target),'files':entries})
 save(E/'RAW_ARCHIVES.json',{'original_root':str(R),'archive_root':str(target),'manifest':str(manifest),'manifest_sha256':sha(manifest),'copied_files':len(entries),'copied_bytes':sum(e['bytes'] for e in entries),'verified_all_copied_bytes':True,'originals_preserved':True,'raw_patterns_not_in_git':['model_calls.jsonl','request_events.jsonl','*_start.json','*_visible_start.json','*_final.json','*_trace.json'],'prior_round24_sources':str(R/'experiments/preliminary/round24-official-and-trajectory/RAW_ARCHIVES.json'),'replay_requires':'original relative paths (or restored files), prior frozen repository versions, and local tau2-official environment; no credentials stored'})
 print('archived',len(entries),'files',sum(e['bytes'] for e in entries),'bytes')
