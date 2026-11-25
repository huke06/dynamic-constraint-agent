"""Whitelist agent request shapes; restricted simulation/evaluation data never supplied."""
import json
BANNED={'private_user_policy','user_private','acceptable_variant','evaluation_criteria','expected_answer',
        'canonical_semantics','database','R_write','R_goal','strict_pass','T_claims'}
SHAPES={'controller':{'state','W','remaining_budget'},'worker':{'u','context'},
        'user_semantics':{'goal','plan','assistant','customer','current_work','assistant_ref','current_user_ref'},
        'executor_parameters':{'u','goal','filtered_candidates','order_id','payment_method_id'}}
def validate(category,stage,messages):
    if category!='agent': return
    assert stage in SHAPES, 'No initial semantics or unregistered agent stage in fixed-start replication'
    payload=json.loads(messages[1]['content'])
    assert set(payload)==SHAPES[stage], 'Unregistered agent payload shape'
    def walk(v):
        if isinstance(v,dict):
            assert not (set(v)&BANNED), 'Restricted fields in agent payload'
            for x in v.values(): walk(x)
        elif isinstance(v,list):
            for x in v: walk(x)
    walk(payload)
