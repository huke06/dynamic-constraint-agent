EXTRACT='''Extract factual ASSERTIONS from this ONE assistant utterance. Do NOT judge truth or repair
it using the catalogue. The entity index is only for resolving IDs/options; no stock or prices supplied.
Return JSON {"claims":[{"kind":"exists|stock|enumeration|price|options|difference|payment|order_status|write|uncertain|nonassertion",
"quote":"EXACT substring from utterance","selector":{"variant_id":"id or omit","old_item_id":"id or omit","options":{}},
"scope":"all|available","time":"current|after_exchange","asserted":<typed value>,"reason":"only if ambiguous"}],
"unparsed":["exact factual span you could not represent"]}.
exists: asserted boolean; scope=all means catalogue existence, available means at least one in-stock
matching SKU. stock: asserted true/false/"unknown" for a named SKU or exact combination. Do not conflate
does-not-exist with stock=false. Unqualified not-in-stock for a combination absent from catalogue can
be uncertain; do not silently interpret it as existence. Preserve ambiguity as uncertain.
enumeration: asserted LIST of {"variant_id":"..."} or {"options":{...}} patterns claimed to be exhaustive;
selector.options specifies the filter (e.g. zoom=10x or black+M), scope all vs available as actually said.
Extract 'only', 'either/or', 'the variants are', and parenthetical catalogue claims, not just final plan.
When a paragraph explicitly concerns available variants, preserve that restriction; a later explicit
'does not exist in the catalog' still asserts existence=false. Do not omit contradictory clauses.
price: asserted number, identify original item with old_item_id vs proposed SKU with variant_id/options.
options: asserted option subset for an identified SKU. difference: asserted signed numeric charge positive,
refund negative; ground target variant if no prepared plan. payment: asserted subset of
{"payment_method_id":"...","source":"credit_card|paypal|gift_card","brand":"visa|mastercard", "last_four":"..."}.
Never reinterpret internal ID digits as actual last_four. order_status: asserted literal state, current
or after_exchange. write: asserted boolean for ALREADY submitted, not a promise to submit after yes.
Questions, hypothetical acceptance, intentions, polite requests and policy reminders without a checkable
state/amount are nonassertion; do not turn them into current facts. An uncertain meaning stays uncertain.
Extract ALL distinct existence/stock/options/price/amount/payment/status/write claims, including lists
and parentheticals. A quote may support several separate atomic facts. Copy original wording, do not
provide a corrected quote. Max 30 claims; put any excess/unsupported semantics in unparsed.
Do not output whether task succeeded, model scores, or preferred first action.'''

JUDGE_EXTRACT='''Extract ONLY explicit factual assertions this evaluator makes about tool observations.
Do not decide whether the evaluator is right. Return JSON {"claims":[{"quote":"exact substring from
one supplied issue reason or limitations", "ref":integer, "variant_id":"...", "field":"available",
"asserted":true|false|"unknown"}],"unparsed":[]}.
Example: 'ref 12 shows available=null for item X' means ref=12, variant_id=X, asserted=unknown.
Only extract explicitly attributable ref/variant pairs; do not invent refs from the actual history.
Other semantic criticisms can be left in unparsed. Do not use the final write as stock evidence.'''
