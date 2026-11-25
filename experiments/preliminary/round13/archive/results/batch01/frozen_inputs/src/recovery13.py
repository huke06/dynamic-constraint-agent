"""Current-turn clarification completion, independent from historical permission existence."""
import json
from copy import deepcopy
from engine import Case
import repairs12
from exchange_core import packed
PRE_CANDIDATES=Case.candidates;PRE_COMPLETED=Case.completed;PRE_APPLY=Case.apply_user;PRE_STATE=Case.state;PRE_COMPACT=Case.compact
RESOLUTION='''Additionally return clarification_resolution:{"kind":"new_permission"|"explicit_rejection"|"information_unclear","source_ref":current_user_ref,"source_quote":"exact substring from THIS reply","reason":"..."}. Judge only the current reply. A historic permission is not a new answer. Explicit rejection means the customer refuses exchange/available alternatives, not merely rejects the out-of-stock original. If accepting another named variant, return permission_update grant with this reply's exact source too. Permission to a variant is distinct from approval of a complete transaction. Do not mark authorization approved merely because a variant is acceptable.'''
def begin(c):
 c.clarification_context={'assistant_ref_expected':len(c.history),'prior_permission_source':(getattr(c,'conditional_permission',None) or {}).get('source'),'prior_variant':(getattr(c,'conditional_permission',None) or {}).get('variant_id')}
 c.last_clarification_outcome=None
def apply(c,parsed,ar,ur):
 PRE_APPLY(c,parsed,ar,ur)
 ctx=getattr(c,'clarification_context',None)
 if not ctx or ar!=ctx['assistant_ref_expected']:return
 resolution=parsed.get('clarification_resolution',{});quote=resolution.get('source_quote','');source_ok=resolution.get('source_ref')==ur and bool(quote) and quote in c.history[ur]['content']
 kind=resolution.get('kind');rule=getattr(c,'conditional_permission',None)
 fresh=bool(source_ok and kind=='new_permission' and rule and rule['source']==ur and rule['source_quote'] in c.history[ur]['content'] and rule['variant_id']!=ctx['prior_variant'])
 rejection=source_ok and kind=='explicit_rejection'
 outcome='new_permission' if fresh else 'explicit_rejection' if rejection else 'information_unclear'
 event={'outcome':outcome,'assistant_ref':ar,'user_ref':ur,'source_quote':quote,'source_valid':source_ok,'new_permission_received':fresh,'new_permission_effective':bool(fresh and rule['sat']=='满足'),'completion_satisfied':bool(fresh or rejection),'semantic_resolution':deepcopy(resolution)}
 c.last_clarification_outcome=event;c.clarification_outcomes=getattr(c,'clarification_outcomes',[])+[deepcopy(event)]
 if rejection:c.user_declined=True
def candidates(c):
 if getattr(c,'user_declined',False):return []
 ws=PRE_CANDIDATES(c)
 for w in ws:
  if w['work_id']=='clarify':w['completion_test']='current_reply_clarification_resolved';w['expected_output']='This round: a new alternative permission, explicit refusal, or unresolved information; historical rule alone cannot complete this work.'
 return ws
def completed(c,test):
 if test=='current_reply_clarification_resolved':
  outcome=getattr(c,'last_clarification_outcome',None);ctx=getattr(c,'clarification_context',None)
  return bool(outcome and ctx and outcome['assistant_ref']==ctx['assistant_ref_expected'] and outcome['user_ref']>ctx['assistant_ref_expected'] and outcome['completion_satisfied'])
 return PRE_COMPLETED(c,test)
def state(c):
 d=PRE_STATE(c);d['P']['clarification_outcomes']=deepcopy(getattr(c,'clarification_outcomes',[]));d['H']['current_clarification']=deepcopy(getattr(c,'last_clarification_outcome',None));return d
def compact(c):
 d=PRE_COMPACT(c);d['current_clarification']=deepcopy(getattr(c,'last_clarification_outcome',None));return d
class Client(repairs12.Client):
 def ask(self,branch,category,stage,messages,max_tokens=1400,case=None):
  if stage=='user_semantics' and json.loads(messages[1]['content']).get('current_work')=='clarify':messages=[{'role':'system','content':messages[0]['content']+'\n'+RESOLUTION},messages[1]]
  return super().ask(branch,category,stage,messages,max_tokens,case)
def install():
 Case.candidates=candidates;Case.completed=completed;Case.apply_user=apply;Case.state=state;Case.compact=compact
