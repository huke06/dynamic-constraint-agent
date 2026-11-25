"""Post-freeze analysis only: serialize the assistant's 54 semantic judgments.
Not an automated semantic classifier and not independent gold annotation.
"""
import json
from pathlib import Path
R=Path(__file__).resolve().parent.parent
packet=json.loads((R/'results/REVIEW_PACKET.json').read_text('utf-8'))
items=[]
for p in packet['items']:
 code=p['code'];stock=p['current_target_stock'];issues=[];status='supported'
 evidence={'latest_target_availability':stock,'current_conditions':p['current_conditions'],'permission':p['user_permission_and_preferences'],'acceptance':p['acceptance_status'],'contract_policy':p['current_contract_gate_policy']}
 if code in ('R008','R036'):
  status='contradicted';issues=[{'type':'observed_false_treated_as_missing_evidence','quote':p['statements'][0]['reason'],'finding':'已经有最新有效工具观察 available=false、来源12；条件明确不成立，而非缺少库存观察。以许可必须有货为由推导必须补查，把许可生效条件误当成当前证据缺口。已知状态的inventory不适用；拒绝记录另见原轨迹。不是把false说成unknown的逐字错误，也不是不允许一般性的刷新策略。'}]
 elif code=='R050':
  status='pending';issues=[{'type':'expected_refund_timing_not_proven','quote':p['statements'][0]['expected'],'finding':'exchange requested及差额-0.44有依据；refund is issued未区分申请登记与退款到账。工具仅写换货申请及差额，不返回实际退款交易。它是内部预期而非已对用户发出的到账承诺，故单列待核实，不判定确定事实错误。'}]
 items.append({'code':code,'status':status,'quoted_statements':p['statements'],'evidence':evidence,'issues':issues,'dimensions':{'unknown_vs_out_of_stock':'covered','not_yet_vs_refusal':'covered; no refusal inferred','historical_vs_current_gate':'covered; no historical compatibility gate asserted','variant_vs_transaction_authorization':'covered; fresh confirmation still required'},'review_method':'assistant read original and synonymous statements against contemporaneous state and contract policy, with masked IDs; not string-match scoring'})
(R/'results/REASON_REVIEW.json').write_text(json.dumps({'limits':packet['limits'],'mapping_opened_after_semantic_pass':True,'items':items},ensure_ascii=False,indent=2),encoding='utf-8')
