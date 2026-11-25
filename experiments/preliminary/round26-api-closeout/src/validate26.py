"""Independent local process validates exported training records and provenance."""
from post26 import *
from export26 import read_jsonl,decode,hashed_messages
def validate():
 out=E/'samples';manifest=read(out/'SFT_MANIFEST.json');seen={};counts=Counter();errors=[];raw_cache={}
 forbidden={'environment_only','oracle','env_approvals','changed_target','change_type','future_event','evaluation_answer','private_user_preferences'}
 def no_private(x):
  if isinstance(x,dict):return not forbidden.intersection(x) and all(no_private(v) for v in x.values())
  if isinstance(x,list):return all(no_private(v) for v in x)
  return True
 for m in manifest:
  try:
   row=read_jsonl(out/m['file'])[m['line']-1];msgs=row['messages'];assert len(msgs)>=3 and msgs[0]['role']=='system' and msgs[-1]['role']=='assistant';d=decode(msgs[-1]['content']);assert all(k in d for k in ('work_type','object','parameters','evidence_refs','expected','reason'));assert hashed_messages(msgs)==m['messages_sha256'];assert no_private(json.loads(msgs[1]['content']))
   p=Path(m['source']['request_file']);assert sha(p)==m['source']['request_sha256'];cs=raw_cache.setdefault(str(p),calls(p.parent));c=cs[m['source']['request_row']];assert c['response']['id']==m['source']['response_id'];assert c['messages']==msgs[:-1];assert decode(c['response']['choices'][0]['message']['content'])==d;assert m['source']['generation']=='model_autonomous';assert all(m['checks'].values());seen.setdefault(m['base_task'],m['partition']);assert seen[m['base_task']]==m['partition'];counts[d['work_type']]+=1
  except Exception as ex:errors.append({'sample':m['sample_id'],'error':type(ex).__name__+': '+str(ex)})
 dm=read(out/'DPO_MANIFEST.json');dpo=read_jsonl(out/'dpo_all.jsonl')
 for m in dm:
  try:
   x=dpo[m['line']-1];prompt=x['prompt'];assert len(prompt)==2 and prompt[0]['role']=='system' and prompt[1]['role']=='user';assert hashed_messages(prompt)==m['prompt_sha256'];state=json.loads(prompt[1]['content']);assert no_private(state);p=Path(m['visible_snapshot']);assert sha(p)==m['snapshot_sha256'] and state==read(p);assert x['chosen']!=x['rejected'];assert len(x['chosen'])==len(x['rejected'])==1
   for field,path in [('chosen','chosen_source'),('rejected','rejected_source')]:
    d=decode(x[field][0]['content']);assert all(k in d for k in ('work_type','object','parameters','evidence_refs','expected','reason'));tr=read(Path(m[path]));assert d==tr[0]['model_original_choice'] and tr[0]['allowed'];assert m['candidate_generation'].startswith('predeclared_')
    assert all(isinstance(i,int) and 0<=i<len(tr[0]['before']['history']) for i in d['evidence_refs'])
    stem=Path(m[path]).name.removesuffix('_trace.json');assert read(Path(m[path]).parent/(stem+'_visible_start.json'))==state
   repeats=m['supporting_repeats'];assert len(repeats)==2 and repeats[0]['direction']==repeats[1]['direction'] and repeats[0]['direction'] not in ('tie','pending');assert all(p['same_input'] for p in repeats);seen.setdefault(m['base_task'],m['partition']);assert seen[m['base_task']]==m['partition']
  except Exception as ex:errors.append({'DPO':m['id'],'error':type(ex).__name__+': '+str(ex)})
 report={'passed':not errors,'SFT_records':len(manifest),'SFT_work_types':dict(counts),'DPO_records':len(dm),'grouped_partitions':seen,'errors':errors,'checks':['required messages/decision fields','actual serialized request and response ID/output','source file SHA256','no future/private dictionary fields','DPO single shared prompt + exact visible snapshot','DPO actual allowed first work, 2 repeats stable','same base task across SFT/DPO stays in one split','automatic/forced steps are not autonomous SFT'],'limits':['human factual review is assistant audit, not independent blind review','DPO candidate actions are preregistered, not autonomous teacher responses','no training or training-effect claim']};save(out/'VALIDATION_REPORT.json',report);print(report);assert report['passed']
if __name__=='__main__':validate()
