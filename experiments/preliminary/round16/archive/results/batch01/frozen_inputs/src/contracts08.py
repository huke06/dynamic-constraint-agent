SEMANTICS='''Interpret ONLY the current user reply; preserve previous evidence separately. Return JSON:
{"permission_update":{"kind":"none|grant|reuse|revoke","variant_id":null|"observed id",
"source_ref":null|integer,"source_quote":"exact original user substring"},
"change":{"present":false,"ambiguous":false,"source_ref":null|integer,"source_quote":"",
"hard_options":{},"preferred_options":{},"variant_id":null,"payment_method_id":null},
"authorization":{"approved":false,"source_ref":null|integer,"source_quote":"",
"arguments":null|{"order_id":"...","item_ids":["..."],"new_item_ids":["..."],"payment_method_id":"..."},
"stated_difference":null|number},"reason":"supported interpretation"}.
permission_update=none preserves an existing rule. For reuse, copy its ORIGINAL source/quote/variant
exactly; never relabel older words as current. New grants/revokes quote the CURRENT reply and use
current_user_ref. Willingness IF in stock grants a rule, not stock or transaction approval.
authorization concerns ONLY the current complete plan and CURRENT reply: approved=true only for
current_work=confirm and actual explicit approval of disclosed exact items, amount and payment.
Use current_user_ref and current words here, never an old permission quote. Refund negative, charge
positive; extract disclosed amount, never calculate missing money. An unchanged final yes need not
grant permission again; preserve existing permission. Old permission never substitutes for approval.
If the CURRENT reply changes requirements, variant or payment, set change.present=true and quote it.
Such changes invalidate the proposal; do not approve the changed plan in the same reply. Unchanged
final approval is NOT a change. Leave ambiguity unresolved. Do not invent facts or another work.'''
