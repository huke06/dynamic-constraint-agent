"""No-model scorer regression tests; facts never depend on legacy judge booleans."""
import json
from pathlib import Path
from fact_verifier import replay,verify
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'09_固定起点续行复验/results/20261122T132951508463Z'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def check():
    camera=read(OLD/'t52_r2_unknown_clarify_final_state.json'); history=camera['F']['dialogue']
    ctx={'product_id':'8940227892','order_id':'#W4689314','item_id':'5996159312','payment_method_id':'paypal_8194385','plan':None}
    def claim(kind,asserted,selector,quote='literal test quote',**extra):
        return {'kind':kind,'asserted':asserted,'selector':selector,'quote':quote,**extra}
    before=replay(history,12)
    c=claim('exists',False,{'options':{'resolution':'30MP','storage':'CF card','zoom':'10x'}})
    assert verify(c,c['quote'],before,ctx)['status']=='contradicted'
    c=claim('stock',False,{'variant_id':'3892645120'})
    assert verify(c,c['quote'],before,ctx)['status']=='supported'
    c=claim('stock',True,{'variant_id':'6384525445'})
    assert verify(c,c['quote'],before,ctx)['status']=='pending'
    after=replay(history,16)
    assert verify(c,c['quote'],after,ctx)['status']=='supported'
    assert before['products']['8940227892']['variants']['6384525445']['available'] is None
    helmet=read(OLD/'t70_r2_unknown_inventory_final_state.json'); h=helmet['F']['dialogue']
    ctxh={'product_id':'7765186836','order_id':'#W3947049','item_id':'3358616356','payment_method_id':'credit_card_7901829','plan':None}
    c=claim('stock',True,{'variant_id':'1665571435'})
    assert verify(c,c['quote'],replay(h,12),ctxh)['status']=='pending'
    assert verify(c,c['quote'],replay(h,13),ctxh)['status']=='supported'
    assert replay(h,13)['product_refs']['7765186836']==12
    c=claim('payment',{'last_four':'7901829'},{})
    assert verify(c,c['quote'],replay(h,13),ctxh)['status']=='contradicted'
    c=claim('difference',-0.44,{'variant_id':'1665571435'})
    assert verify(c,c['quote'],replay(h,13),ctxh)['status']=='supported'
    c=claim('order_status','pending (items modified)',{},time='after_exchange')
    assert verify(c,c['quote'],before,ctx)['status']=='contradicted'
    c=claim('write',True,{})
    assert verify(c,c['quote'],before,ctx)['status']=='contradicted'
    # Newer unknown supersedes old true; failed observations do not overwrite valid stock.
    prod=replay(h,13)['products']['7765186836']
    import copy
    changed=copy.deepcopy(prod); changed['variants']['1665571435']['available']=None
    extra={'role':'observation','work':'inventory','content':json.dumps({'official_tool':'get_product_details','arguments':{'product_id':'7765186836'},'official_result':changed})}
    extended=h[:13]+[extra]
    assert replay(extended,len(extended))['products']['7765186836']['variants']['1665571435']['available'] is None
    failed={'role':'observation','work':'inventory','content':json.dumps({'official_tool':'get_product_details','arguments':{'product_id':'7765186836'},'official_result':{'error':'failed'}})}
    assert replay(h[:13]+[failed],14)['products']['7765186836']['variants']['1665571435']['available'] is True
    c=claim('maximum','5x',{'options':{'resolution':'30MP','storage':'CF card'}},field='zoom',scope='available')
    checked=verify(c,c['quote'],after,ctx); assert checked['status']=='supported'; json.dumps(checked)
    c=claim('exchange_scope',['5996159312'],{})
    assert verify(c,c['quote'],after,{**ctx,'scope':['5996159312']})['status']=='supported'
    c=claim('order_id','#W4689314',{})
    assert verify(c,c['quote'],after,ctx)['status']=='supported'
    from fact_verifier import locate_quote
    location=locate_quote('Price difference: $34.07','**Price difference:** $34.07')
    assert location and location['text']=='Price difference:** $34.07'
    report={'passed':True,'tests':['camera exists but unavailable distinguished','no later evidence before cutoff',
        'helmet official ref12 true overrides masked ref8 null','payment ID not last_four','exact signed Decimal difference',
        'exchange state differs from modify-pending state','already-write assertion checked at time',
        'latest valid unknown retained and failed observation ignored','maximum/scope/order-ID distinct types and JSON numeric serialization',
        'Markdown-only quote alignment preserves exact factual characters'],'model_calls':0}
    (HERE/'fact_selfcheck.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report
if __name__=='__main__': print(json.dumps(check(),ensure_ascii=False,indent=2))
