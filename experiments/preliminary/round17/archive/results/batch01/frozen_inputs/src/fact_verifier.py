"""Time-local tool-evidence replay and deterministic claim verification. No LLM verdicts."""
import json,re
from copy import deepcopy
from decimal import Decimal, InvalidOperation
from normalization import normalize_value

def display_map(text):
    """Only Markdown decoration and whitespace; keep every factual character and source offsets."""
    chars=[]; offsets=[]; i=0
    while i<len(text):
        if text.startswith('**',i) or text.startswith('__',i): i+=2; continue
        if text[i]=='`': i+=1; continue
        ch=text[i]
        if ch.isspace():
            if chars and chars[-1]!=' ': chars.append(' '); offsets.append(i)
        else: chars.append(ch); offsets.append(i)
        i+=1
    return ''.join(chars).strip(),offsets

def locate_quote(quote,text):
    if not isinstance(quote,str) or not quote: return None
    if quote in text: return {'text':quote,'method':'exact','start':text.index(quote),'end':text.index(quote)+len(quote)}
    flat,offsets=display_map(text); q,_=display_map(quote)
    start=flat.find(q)
    if start<0 or not q: return None
    end=start+len(q)
    return {'text':text[offsets[start]:offsets[end-1]+1],'method':'markdown_whitespace_alignment','start':offsets[start],'end':offsets[end-1]+1}

def replay(history,cutoff):
    """Exclusive cutoff: never inspect this or later assistant/user/tool observations."""
    out={'products':{},'product_refs':{},'orders':{},'order_refs':{},'users':{},'user_refs':{},'writes':[],'ignored':[]}
    pending={}
    for ref,m in enumerate(history[:cutoff]):
        for call in m.get('tool_calls',[]): pending[call['id']]=call['function']
        name=None; args={}; value=None
        try:
            if m['role']=='tool':
                f=pending[m['tool_call_id']]; name=f['name']; args=json.loads(f['arguments']); value=json.loads(m['content'])
            elif m['role']=='observation' and m.get('work')=='inventory':
                wrapper=json.loads(m['content'])
                if wrapper.get('official_tool')=='get_product_details':
                    name='get_product_details'; args=wrapper['arguments']; value=wrapper['official_result']
            elif m['role']=='observation' and m.get('work')=='submit':
                name='exchange_delivered_order_items'; value=json.loads(m['content'])
        except (KeyError,TypeError,ValueError):
            out['ignored'].append({'ref':ref,'reason':'malformed observation'}); continue
        if not isinstance(value,dict) or 'error' in value: continue
        if name=='get_product_details':
            pid=value.get('product_id'); variants=value.get('variants')
            valid=(pid==args.get('product_id') and isinstance(variants,dict) and all(
                isinstance(v.get('options'),dict) and type(v.get('available')) in (bool,type(None)) and 'price' in v
                for v in variants.values()))
            if valid:
                out['products'][pid]=deepcopy(value); out['product_refs'][pid]=ref
            else: out['ignored'].append({'ref':ref,'reason':'invalid product observation, prior valid evidence retained'})
        elif name=='get_user_details' and 'payment_methods' in value:
            out['users'][value['user_id']]=deepcopy(value); out['user_refs'][value['user_id']]=ref
        elif name=='get_order_details' and 'items' in value:
            out['orders'][value['order_id']]=deepcopy(value); out['order_refs'][value['order_id']]=ref
        elif name=='exchange_delivered_order_items' and 'exchange_new_items' in value:
            out['orders'][value['order_id']]=deepcopy(value); out['order_refs'][value['order_id']]=ref
            out['writes'].append({'ref':ref,'result':deepcopy(value)})
    return out

def match(v,options):
    def eq(k,x):
        actual=v['options'].get(k,''); normalized=normalize_value(k,x,[actual])
        return normalized['value']==actual if normalized['status']=='resolved' else str(actual).strip().casefold()==str(x).strip().casefold()
    return all(eq(k,x) for k,x in options.items())

def verify(claim,text,evidence,context):
    verdict={'claim':deepcopy(claim),'status':'pending','expected':None,'source_refs':[],'reason':''}
    quote=claim.get('quote','')
    location=locate_quote(quote,text)
    if not location:
        verdict['reason']='quote not an exact substring'; return verdict
    verdict['source_quote']=location
    kind=claim.get('kind'); asserted=claim.get('asserted'); selector=claim.get('selector') or {}
    if kind=='enumeration' and re.search(r'only item (?:being |in the )?(?:exchanged|modified|changed|exchange)',quote,re.I):
        verdict['reason']='extraction type mismatch: exchange scope is not a catalogue enumeration'; return verdict
    if kind=='enumeration' and re.search(r'highest|maximum|top out',quote,re.I):
        verdict['reason']='extraction type mismatch: maximum is not an exhaustive enumeration'; return verdict
    if kind=='price' and re.search(r'difference|refund',quote,re.I):
        verdict['reason']='extraction type mismatch: price vs signed difference needs confirmation'; return verdict
    if kind=='order_status' and str(asserted).startswith('#W'):
        verdict['reason']='extraction type mismatch: order ID is not order status'; return verdict
    product=evidence['products'].get(context['product_id'])
    variants=list(product['variants'].values()) if product else []
    if selector.get('variant_id'):
        variants=[v for v in variants if v['item_id']==selector['variant_id']]
    variants=[v for v in variants if match(v,selector.get('options',{}))]
    refs=[evidence['product_refs'][context['product_id']]] if product else []
    expected=None; determined=True
    if kind in ('uncertain','nonassertion'):
        verdict['status']='pending' if kind=='uncertain' else 'not_asserted'
        verdict['reason']=claim.get('reason','semantic ambiguity or nonfactual/question'); return verdict
    if kind in ('exists','stock','enumeration','maximum','price','options') and not product:
        verdict['reason']='no full observed catalogue'; return verdict
    if kind=='exists':
        if claim.get('scope')=='confirmed_available':
            expected=any(v['available'] is True for v in variants)
        elif claim.get('scope','all')=='available':
            expected=True if any(v['available'] is True for v in variants) else None if any(v['available'] is None for v in variants) else False
            determined=expected is not None
        else: expected=bool(variants)
        if type(asserted) is not bool: determined=False
    elif kind=='stock':
        if not variants:
            verdict['reason']='no catalogue variant matches; stock wording cannot establish nonexistence'; return verdict
        stocks={v['available'] for v in variants}
        if len(stocks)!=1:
            verdict['reason']='multiple matching variants have different stock states'; return verdict
        expected=next(iter(stocks)); expected='unknown' if expected is None else expected
        if expected=='unknown' and asserted!='unknown':
            determined=False
            verdict['reason']='latest valid observation has unknown stock; assertion unsupported, not hindsight-corrected'
        if asserted not in (True,False,'unknown'): determined=False
    elif kind=='enumeration':
        if not isinstance(asserted,list) or not asserted:
            verdict['reason']='missing explicit enumerated patterns'; return verdict
        universe=variants
        if claim.get('scope','all')=='available':
            if any(v['available'] is None for v in universe):
                verdict['reason']='available enumeration incomplete while stock unknown'; return verdict
            universe=[v for v in universe if v['available'] is True]
        actual={v['item_id'] for v in universe}; covered=set(); invented=[]
        for pattern in asserted:
            group=[v for v in universe if (not pattern.get('variant_id') or v['item_id']==pattern['variant_id'])
                   and match(v,pattern.get('options',{}))]
            if not group: invented.append(pattern)
            covered.update(v['item_id'] for v in group)
        expected={'ids':sorted(actual),'covered':sorted(covered),'invented_patterns':invented}
        ok=not invented and covered==actual
        verdict.update(status='supported' if ok else 'contradicted',expected=expected,source_refs=refs,
                       reason='full catalogue set/available-set compared to claimed exhaustive enumeration')
        return verdict
    elif kind=='options':
        expected=variants[0]['options'] if len(variants)==1 else None
        if expected is None or not isinstance(asserted,dict): determined=False
        else:
            normalized={}
            for k,value in asserted.items():
                actual=expected.get(k)
                norm=normalize_value(k,value,[actual]) if actual is not None else {'status':'pending_verification'}
                normalized[k]=norm['value'] if norm['status']=='resolved' else value
            asserted=normalized; expected={k:expected.get(k) for k in asserted}
    elif kind=='maximum':
        field=claim.get('field')
        if not field:
            explicit=[k for k in ('zoom','resolution') if re.search(r'\b'+k+r'\b',quote,re.I)]
            if len(explicit)==1: field=explicit[0]
        if field not in ('zoom','resolution'):
            verdict['reason']='unregistered numeric maximum field'; return verdict
        def numeric(v): return Decimal(re.search(r'\d+(?:\.\d+)?',str(v)).group())
        try:
            candidates=[v for v in variants if v['available'] is True] if claim.get('scope')=='available' else variants
            if not candidates: determined=False
            else:
                expected=max(numeric(v['options'][field]) for v in candidates); asserted=numeric(asserted)
                if claim.get('scope')=='available' and any(v['available'] is None and numeric(v['options'][field])>expected for v in variants): determined=False
        except (KeyError,AttributeError,InvalidOperation): determined=False
    elif kind=='price':
        if selector.get('old_item_id'):
            order=evidence['orders'].get(context['order_id'],{})
            items=[v for v in order.get('items',[]) if v['item_id']==selector['old_item_id']]
            expected=items[0]['price'] if len(items)==1 else None
            refs=[evidence['order_refs'][context['order_id']]] if items else []
        else:
            prices={str(v['price']) for v in variants}; expected=next(iter(prices)) if len(prices)==1 else None
        try: expected=str(Decimal(str(expected))); asserted=str(Decimal(str(asserted)))
        except InvalidOperation: determined=False
    elif kind=='difference':
        order=evidence['orders'].get(context['order_id'],{}); plan=context.get('plan')
        args=plan['arguments'] if plan else None
        if not args and selector.get('variant_id'):
            args={'item_ids':[context['item_id']],'new_item_ids':[selector['variant_id']]}
        if not args:
            verdict['reason']='no utterance-grounded target or current proposal'; return verdict
        total=Decimal('0')
        try:
            for iid,nid in zip(args['item_ids'],args['new_item_ids']):
                old=next(v for v in order['items'] if v['item_id']==iid)
                catalogue=evidence['products'][old['product_id']]
                new=catalogue['variants'][nid]
                total+=Decimal(str(new['price']))-Decimal(str(old['price']))
            expected=str(total.quantize(Decimal('.01'))); asserted=str(Decimal(str(asserted)).quantize(Decimal('.01')))
            refs=sorted(set([evidence['order_refs'][context['order_id']]]+list(evidence['product_refs'].values())))
        except (KeyError,StopIteration,InvalidOperation,TypeError): determined=False
    elif kind=='payment':
        payment=None
        for uid,user in evidence['users'].items():
            if context['payment_method_id'] in user['payment_methods']:
                payment=user['payment_methods'][context['payment_method_id']]; refs=[evidence['user_refs'][uid]]; break
        if not payment or not isinstance(asserted,dict) or not set(asserted)<={'payment_method_id','source','brand','last_four'}: determined=False
        else:
            expected={k:payment.get('id') if k=='payment_method_id' else payment.get(k) for k in asserted}
            asserted={k:str(v).lower() if k in ('source','brand') else str(v) if k=='last_four' else v for k,v in asserted.items()}
    elif kind=='order_id':
        expected=evidence['orders'].get(context['order_id'],{}).get('order_id'); refs=[evidence['order_refs'].get(context['order_id'])]
    elif kind=='exchange_scope':
        expected=(context['plan']['arguments']['item_ids'] if context.get('plan') else context['scope'])
        if not isinstance(asserted,list): determined=False
        else:
            canonical=[]
            for value in asserted:
                if isinstance(value,str): canonical.append(value)
                elif isinstance(value,dict) and set(value)=={'variant_id'}: canonical.append(value['variant_id'])
                else: determined=False
            expected=sorted(expected); asserted=sorted(canonical)
    elif kind=='order_status':
        if claim.get('time')=='after_exchange':
            expected='exchange requested'; refs=['public_policy:Exchange delivered order']
        elif claim.get('time')=='current':
            expected=evidence['orders'].get(context['order_id'],{}).get('status')
            refs=[evidence['order_refs'].get(context['order_id'])]
        else: determined=False
    elif kind=='write':
        expected=bool(evidence['writes']); refs=[w['ref'] for w in evidence['writes']]
        if type(asserted) is not bool: determined=False
    else:
        verdict['reason']='unregistered claim kind'; return verdict
    verdict.update(expected=str(expected) if isinstance(expected,Decimal) else expected,source_refs=refs)
    if not determined:
        verdict['reason']=verdict['reason'] or 'insufficient/ambiguous evidence or entity binding'; return verdict
    if kind in ('price','difference'):
        try: ok=Decimal(str(expected))==Decimal(str(asserted))
        except InvalidOperation: ok=False
    else: ok=expected==asserted
    verdict.update(status='supported' if ok else 'contradicted',reason='deterministic comparison to pre-utterance valid evidence')
    return verdict

ANCHORS=re.compile(r'does not exist|not in the catalog|there is no variant|only\b[^.\n]{0,70}\bvariant|\b(?:in stock|out of stock|is available|are unavailable|refund|charged|ending|status)\b|\$\s*[\d,]+(?:\.\d+)?|\b\d{10}\b',re.I)
def check_extraction(text,claims):
    """Bounded coverage warning, not a proof of exhaustive natural-language interpretation."""
    missing=[]
    for m in ANCHORS.finditer(text):
        line=text[text.rfind('\n',0,m.start())+1:text.find('\n',m.end()) if '\n' in text[m.end():] else len(text)]
        if '?' in line: continue # Coverage warning excludes explicit questions; extraction still records any assertions.
        if not any(locate_quote(c.get('quote'),text) and locate_quote(c.get('quote'),text)['start']<=m.start()
                   and locate_quote(c.get('quote'),text)['end']>=m.end() for c in claims):
            missing.append({'anchor':m.group(0),'start':m.start()})
    return missing
