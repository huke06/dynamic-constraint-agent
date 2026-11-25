"""Post-run evidence audit. Never imported by a runner; does not alter raw scores."""
from post26 import *

def run():
 review={};records=[]
 sources=[(E/'results/A01','A01'),(E/'results/B01','B01')]
 for name in ['simfix1','simfix2','simfix3','simfix4','statefix1','statefix2','statefix3']:
  for p in sorted((E/'versions'/name/'results').glob('*')):
   if (p/'OUTCOMES.json').exists():sources.append((p,name+'/'+p.name))
 for p,label in sources:
  for row in read(p/'OUTCOMES.json'):
   n=row['id'];tr=read(p/(n+'_trace.json'));issues=[];status='supported';claims=[]
   # Audit units are the current source state, literal model output, execution, and final DB.
   for ix,e in enumerate(tr):
    if e['module']=='native_speech':
     z=e['user_result'];claims.append({'event':ix,'kind':'speech','quote':e['text'],'literal_extraction':z.get('extraction'),'program_checks':z.get('checks'),'source_history_length':len(e['before']['history'])})
    elif e['module']=='work_selection' and e['source']=='decision_model':
     d=e['model_output'];fb=tr[ix+1];claims.append({'event':ix,'kind':'decision','decision':d,'cited_original_records':[{'ref':i,'record':fb['before']['history'][i]} for i in d['evidence_refs'] if isinstance(i,int) and 0<=i<len(fb['before']['history'])]})
     if d['work_type']=='stop' and 'withdrew' in d['reason'].lower():
      if not any('entire' in fb['before']['history'][i]['content'].lower() and 'withdraw' in fb['before']['history'][i]['content'].lower() for i in d['evidence_refs'] if isinstance(i,int) and 0<=i<len(fb['before']['history'])):issues.append('停止理由可由当前状态支持，但所引记录不是撤回原话；禁止作为准确引用示范')
   if label=='A01' and row['group']=='official' and any(t in n for t in ['R_30_','R_31_','R_51_','R_55_','E_EDB05_']):status='simulator_bias';issues.append('原始模拟器误判合法退款路径/具体选择追问/暂停后的继续询问；不得算框架优势')
   if label=='A01' and n=='A_E_EDB06_r1_official':status='simulator_bias';issues.append('首次多选替代问题被提取为information并给出无关cap提示；最终正确但过程投入被污染')
   if label=='simfix3/recheck01' and n=='A_E_EDB05_r2_official':status='simulator_bias';issues.append('含proceed的继续问题仍误记stop；simfix4另批复验')
   if label=='simfix2/recheck_R55' and n=='A_R_55_r1_official':status='mixed_model_simulator';issues.append('第一次把退款路线许可和完整确认合问；模拟未回答其中明确的路线选择而仅要求纠正。后续模型重复完整确认，未取得独立路线许可；还声称礼品卡立即入账，原生工具仅登记return requested，不支持此事实')
   if n=='A_E_EDB08_r1_official':status='contradicted';issues.append('事件0/1把整单差额+3.53/+4.09/+6.27/+9.18/+10.06标为满足<=1.10，最终写入虽正确，中间数值判断错误')
   if label=='A01' and n=='A_R_51_r1_framework':issues.append('模型把用户要求先解释/比较表述成Policy requires；操作合理但来源归因过强，不收SFT')
   if label=='B01' and 'E26_capacity' in n and n.endswith('_analyze'):
    status='contradicted';issues.append('容量优先原话已可见，模型仍称color/material为最高优先、capacity为lowest-impact；第二次更称1L改1.5L保留容量。两次中间理由错误，不能凭正确写入导出偏好')
   if not row['correct'] and row['group']=='framework':status='program_or_semantic_failure';issues.append('保留未办结：见实际semantic_update/拒绝反馈及pending原话，不导出正示范')
   if issues and status=='supported':status='pending'
   review[label+'/'+n]={'status':status,'issues':issues,'reviewer':'assistant evidence audit, not independent blind review','scope':'current tool amounts/stock/scope/payment/status; current intent and literal cited source; model reasons separate from end result'}
   records.append({'phase':label,'id':n,'verdict':review[label+'/'+n],'claims':claims,'source_trace':str(p/(n+'_trace.json')),'source_sha256':sha(p/(n+'_trace.json'))})
 save(E/'results/FACT_REVIEW.json',review);save(E/'results/FACT_AUDIT_RECORDS.json',records)
 print('reviewed trajectories',len(records),Counter(v['status'] for v in review.values()))

if __name__=='__main__':run()
