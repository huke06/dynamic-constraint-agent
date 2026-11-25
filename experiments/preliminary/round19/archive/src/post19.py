"""Post-run evidence packet, independent speech arithmetic, and report tables."""
import json,re,hashlib,sys
from decimal import Decimal
from pathlib import Path
from collections import Counter
from construct18 import R,read,save,sha
from score19 import linefile
def packet():
 items=[];auto=[]
 for folder in ('main','context','pilot01','pilot02','pilot03'):
  out=R/'results'/folder
  if not(out/'results.json').exists():continue
  for n in read(out/'results.json'):
   final=read(out/(n+'_final.json'));seen=set()
   for idx,e in enumerate(read(out/(n+'_trajectory.json'))):
    ar=e.get('assistant_ref');rec=e.get('user_record') or (e.get('result') if isinstance(e.get('result'),dict) and 'extraction'in e['result'] else None)
    if ar is not None and ar not in seen:
     seen.add(ar);text=rec['semantic_text'] if rec else e.get('assistant_message',{}).get('content') or e.get('after',{}).get('history',[{}])[ar].get('content','');b=e.get('before');findings=[]
     if rec and rec.get('extraction',{}).get('kind')=='full_proposal':
      p=rec['extraction'];vid=p.get('replacement_variant_id');v=b['ledger']['products'][b['cfg']['product_id']]['variants'].get(vid);q=p.get('amount_quote','');amount=p.get('amount');old=next(i for i in b['cfg']['environment']['orders'][b['cfg']['order_id']]['items'] if i['item_id']==b['cfg']['item_id'])
      if v and isinstance(amount,(int,float)) and q and q in text:
       expected=Decimal(str(v['price']))-Decimal(str(old['price']));nums=[Decimal(s) for s in re.findall(r'-?\d+\.\d{1,2}',q)];literal=any(abs(x)==abs(Decimal(str(amount))) for x in nums)
       if not literal:findings.append({'type':'simulator_amount_extraction_unverified','status':'pending','quote':q,'extracted_amount':amount,'expected_amount':str(expected)})
       elif Decimal(str(amount))!=expected:
        sign_error=abs(Decimal(str(amount)))==abs(expected) and (('refund'in q.lower() and amount>0) or ('charge'in q.lower() and amount<0))
        findings.append({'type':'simulator_sign_error' if sign_error else 'incorrect_stated_difference','status':'pending' if sign_error else 'contradicted','quote':q,'extracted_amount':amount,'expected_amount':str(expected),'prices':{'new':v['price'],'original':old['price']}})
     record={'folder':folder,'id':n,'entry':idx,'assistant_ref':ar,'text':text,'current_goal':{'variant':b['desired'],'withdrawn':b['withdrawn'],'user_quote':b['history'][b['permission_source']]['content']},'latest_visible_catalog':b['ledger']['products'],'latest_visible_order':b['ledger']['orders'],'user_interpretation':rec,'auto_findings':findings};items.append(record)
     auto.extend([{'id':n,'entry':idx,**x} for x in findings])
    if e.get('closing_text'):items.append({'folder':folder,'id':n,'entry':idx,'assistant_ref':None,'text':e['closing_text'],'current_goal':{'variant':e['after']['desired'],'withdrawn':e['after']['withdrawn']},'latest_visible_catalog':e['after']['ledger']['products'],'latest_visible_order':e['after']['ledger']['orders'],'user_interpretation':None,'auto_findings':[]})
   # A simulator request can fail AFTER the Agent has spoken. Preserve that speech
   # even though no successful user_record or normal entry was created.
   initial_count=len(read(out/(n+'_start.json'))['history']);h=final['world']['history'];known={x['text'] for x in items if x['id']==n}
   for ref,m in enumerate(h):
    text=m.get('content')
    if ref>=initial_count and m['role']=='assistant' and text and ref not in seen and text not in known:
     items.append({'folder':folder,'id':n,'entry':None,'assistant_ref':ref,'text':text,'current_goal':{'variant':final['world']['desired'],'withdrawn':final['world']['withdrawn']},'latest_visible_catalog':final['world']['ledger']['products'],'latest_visible_order':final['world']['ledger']['orders'],'user_interpretation':None,'auto_findings':[],'note':'speech retained despite interrupted user response'})
 save(R/'results/SPEECH_PACKET.json',{'method':'All actually spoken baseline and framework utterances, contemporaneous records. Framework internal reason is separate from spoken text. Not blinded independent gold.','items':items});save(R/'results/AUTO_FACTS.json',auto);print({'speech_items':len(items),'auto_findings':len(auto)})
def tables():
 s=read(R/'results/SUMMARY.json');main=s.get('main',[]);context=s.get('context',[]);lines=['# 官方LLMAgent与精简框架：主配对表','','O官方，F框架。写入次数是实际原生DB写入；错误尝试单列，未触发和未办结不删除。操作粒度不同，不直接用helper数与native工具数排效率。','', '|基础题|版本/重复|O/F最终正确|O/F实际写入|O/F变化已触发|O/F变化后首个操作/对象|O/F无效提交尝试|O/F共同质量|O/F未完成原因|','|---|---|---|---|---|---|---|---|---|']
 def first(r):
  p=r['first_after_event']
  if not p:return '—'
  if p['operation']=='speech':
   e=read(R/f"results/main/{r['id']}_trajectory.json")[p['entry']];ex=e.get('user_record',{}).get('extraction',{});obj=ex.get('replacement_variant_id') or ('多款备选，见原文' if ex.get('kind')=='alternative_question' else e.get('before',{}).get('cfg',{}).get('order_id'));return ex.get('kind','speech')+':'+str(obj)
  if p['operation']=='stop':return 'stop:'+r['task_id']+'原订单'
  return p['operation']+':'+str(p['object'])
 pairs=[]
 for tid in read(R/'configs/tasks.json'):
  for ver in ('stable','changed'):
   for rep in (1,2):
    nn=[f't{tid}_{ver}_r{rep}_{g}' for g in ('official','framework')]
    if not all(any(r['id']==n for r in main) for n in nn):continue
    a,b=[next(r for r in main if r['id']==n) for n in nn];eligible=a['quality'] and b['quality'] and not(a['missing_usage'] or b['missing_usage'] or a['stop_reason'] or b['stop_reason']);pairs.append({'task_id':tid,'version':ver,'repeat':rep,'eligible_for_resource_comparison':eligible,'agent_calls_O_minus_F':a['agent_calls']-b['agent_calls'] if eligible else None,'agent_input_tokens_O_minus_F':a['agent_input_tokens']-b['agent_input_tokens'] if eligible else None,'agent_output_tokens_O_minus_F':a['agent_output_tokens']-b['agent_output_tokens'] if eligible else None});lines.append('|'+ '|'.join(map(str,[tid,ver+'/'+str(rep),str(a['final_correct'])+'/'+str(b['final_correct']),str(a['actual_write_count'])+'/'+str(b['actual_write_count']),str(a['event_triggered'])+'/'+str(b['event_triggered']),first(a)+' / '+first(b),str(len(a['unsafe_attempts']))+'/'+str(len(b['unsafe_attempts'])),str(a['quality'])+'/'+str(b['quality']),str(a['stop_reason']or'—')+' / '+str(b['stop_reason']or'—')]))+'|')
 (R/'results/MAIN_PAIRED_RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');save(R/'results/MAIN_RESOURCE_PAIRS.json',pairs)
 ct=['# 同状态上下文成本诊断','','O原上下文，C精简。仅两侧质量达标、用量完整、无提前停止时计算节省；调用和词元均只计本次Agent续行，用户语义开销另表。','', '|状态|O/C质量|O/C输入词元|O/C输出词元|O/C Agent调用|O/C缓存命中词元|输入降低|','|---|---|---|---|---|---|---:|'];cp=[]
 for tid in ('27','75'):
  a,b=[next(r for r in context if r['id']==f'cost_t{tid}_{mode}') for mode in ('original','compact')];ok=a['quality'] and b['quality'] and not(a['missing_usage'] or b['missing_usage'] or a['stop_reason'] or b['stop_reason']);saving=1-b['agent_input_tokens']/a['agent_input_tokens'] if ok and a['agent_input_tokens'] else None;cp.append({'task_id':tid,'quality_comparable':ok,'input_saving_fraction':saving,'original':a,'compact':b});ct.append('|'+ '|'.join(map(str,[tid,str(a['quality'])+'/'+str(b['quality']),str(a['agent_input_tokens'])+'/'+str(b['agent_input_tokens']),str(a['agent_output_tokens'])+'/'+str(b['agent_output_tokens']),str(a['agent_calls'])+'/'+str(b['agent_calls']),str(a['agent_cache_tokens'])+'/'+str(b['agent_cache_tokens']),f'{saving:.1%}' if saving is not None else '—']))+'|')
 (R/'results/CONTEXT_PAIRED_RESULTS.md').write_text('\n'.join(ct)+'\n',encoding='utf-8');save(R/'results/CONTEXT_PAIRS.json',cp)
 fieldrows=[]
 for folder in ('main','context'):
  for a in linefile(R/f'results/{folder}/model_calls.jsonl'):
   if a['category']!='agent':continue
   raw=a['messages'][1]['content'] if len(a['messages'])>1 else None
   try:obj=json.loads(raw);keys=list(obj) if isinstance(obj,dict) else None
   except (ValueError,TypeError):keys=None
   fieldrows.append({'folder':folder,'id':a['branch'],'payload_keys':keys,'input_characters':sum(len(str(m.get('content')or'')) for m in a['messages']),'tools_characters':len(json.dumps(a.get('tools'),ensure_ascii=False)),'usage':a.get('usage'),'actual_fields_in':'model_calls.jsonl messages/tools raw'})
 save(R/'results/CONTEXT_FIELDS.json',fieldrows)
 print({'main_pairs':len(pairs),'eligible':sum(p['eligible_for_resource_comparison'] for p in pairs),'context_pairs':len(cp)})
if __name__=='__main__':{'packet':packet,'tables':tables}[sys.argv[1]]()
