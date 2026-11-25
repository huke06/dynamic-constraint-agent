"""Catalogue-supported enum aliases; no stock, price, ranking or fuzzy guesses."""
import unicodedata
from copy import deepcopy
ALIASES={'size':[['S','small'],['M','medium'],['L','large'],['XL','extra large']]}
def token(v): return ' '.join(unicodedata.normalize('NFKC',str(v)).strip().casefold().split())
def enums(product):
    result={}
    for v in product['variants'].values():
        for key,value in v['options'].items(): result.setdefault(key,set()).add(value)
    return {k:sorted(values) for k,values in sorted(result.items())}
def normalize_value(key,value,legal):
    candidates={v for v in legal if token(v)==token(value)}
    for alternatives in ALIASES.get(key,[]):
        if token(value) in {token(a) for a in alternatives}:
            candidates.update(v for v in legal if token(v) in {token(a) for a in alternatives})
    return {'raw':value,'candidates':sorted(candidates),'value':next(iter(candidates)) if len(candidates)==1 else None,
            'status':'resolved' if len(candidates)==1 else 'pending_verification'}
def normalize_options(options,legal):
    result={}; audit=[]
    for key,value in options.items():
        matches=[k for k in legal if token(k)==token(key)]
        rec=normalize_value(matches[0],value,legal[matches[0]]) if len(matches)==1 else {
            'raw':value,'candidates':[],'value':None,'status':'pending_verification'}
        rec.update(raw_key=key,key=matches[0] if len(matches)==1 else None); audit.append(rec)
        if rec['status']=='resolved': result[rec['key']]=rec['value']
    return result,audit
def normalize_semantics(raw,legal):
    result=deepcopy(raw); audit=[]
    for field in ('hard_options','preferred_options'):
        result[field],rows=normalize_options(raw[field],legal)
        audit.extend({**row,'field':field} for row in rows)
    return result,{'resolved':all(row['status']=='resolved' for row in audit),'fields':audit}
