"""Shared natural-language extraction. The frozen Round 26 program adjudicates permission."""

import json
import re
import time


MODEL = "qwen3.5-4b-q4-k-m"
INSTRUCTIONS = """
Set asks=true when question_quote is an actual request directly addressed to the user, even if explanatory paragraphs follow. Internal narration such as 'I need to ask the user' is not a question.
An actual final question asking which replacement or whether to accept a concrete substitute is spec_permission, with topic=none. Include the cited active options and their original purchased item ID. The unavailable replacement SKU is not the original purchased item ID. A final question naming one SKU offers only that SKU. For a question asking which of the listed options to choose, include the actual applicable list. Keep offer quotes short, literal and contiguous, and include the option ID in the quote.
A question asking whether to accept a specific refund route is refund_permission, with topic=none. A question asking what the refund policy or signed cap means is constraint_question. Only use cap_direction for an actual question about the sign or meaning of the cap. A reference to the cap in a description is not a question about it.
Use proposal only when the assistant is asking the user to approve the complete current transaction. Separate route/specification permission from transaction approval. Distinguish a declared stop from a temporary hold that asks the user to continue. Copy questions and facts from the actual utterance and use null/empty arrays for missing evidence. Return only the JSON object.
""".strip()
KINDS = {"proposal", "spec_permission", "refund_permission", "constraint_question", "stop", "other"}
TOPICS = {"cap_direction", "amount_basis", "refund_policy", "scope", "none"}


def literal_proposal(payload):
    text = payload["actual_assistant"]
    marker = re.search(r'\{\s*"arguments"\s*:', text)
    if marker is None:
        return None
    try:
        plan, end = json.JSONDecoder().raw_decode(text, marker.start())
        args = plan["arguments"]
        ids = args["item_ids"]
        method = args["payment_method_id"]
        exchange = payload["business"] == "exchange"
        amount_key = "difference" if exchange else "refund_amount"
        amount = float(plan[amount_key])
        replacements = args["new_item_ids"] if exchange else []
    except (KeyError, TypeError, ValueError):
        return None
    quote = re.search(r"\bDo you (?:approve|confirm)\b[^?]*\?", text[end:], re.I)
    literal = text[marker.start():end]
    amount_quote = re.search(rf'"{amount_key}"\s*:\s*"?-?\d+\.\d+"?', literal)
    if not (quote and amount_quote and isinstance(ids, list) and isinstance(method, str) and method in literal):
        return None
    if exchange and (not isinstance(replacements, list) or len(replacements) != len(ids)):
        return None
    return {"kind": "proposal", "asks": True, "question_quote": quote.group(), "proposal_quote": literal,
            "item_ids": ids, "pairs": [{"item_id": i, "new_item_id": v} for i, v in zip(ids, replacements)],
            "payment_method_id": method, "payment_quote": method, "amount": amount,
            "amount_quote": amount_quote.group(), "active_offers": [], "rejected_offer_ids": [], "topic": "none"}


def bind_direct_question(payload, value):
    """Bind unmistakable requests to literal offers; authorization remains downstream."""
    text = payload["actual_assistant"]
    questions = list(re.finditer(r"(?:[^\n.!?]|(?<=\d)\.(?=\d))*\?", text))
    for match in reversed(questions):
        question = match.group().strip(" \t*#")
        if re.search(r"\b(?:cap|limit|negative)\b", question, re.I) and (re.search(r"\b(?:means?|meaning|interpret|sign)\b", question, re.I) or re.search(r"\bminimum\b.*\bmaximum\b|\bmaximum\b.*\bminimum\b", question, re.I)):
            value.update(kind="constraint_question", asks=True, question_quote=question,
                         topic="cap_direction", active_offers=[])
            return value
        if re.search(r"\b(?:do you|can you|would you|please)\b.{0,35}\b(?:approve|confirm|authorize)\b", question, re.I):
            complete = re.search(r"\b(?:complete|exact|entire|whole|all|final)\b.{0,35}\b(?:plan|proposal|return|exchange|transaction|scope)\b", question, re.I)
            transaction = re.search(r"\b(?:return(?:ing)?|exchang(?:e|ing))\b", question, re.I)
            method = re.search(r"\b(?:gift_card|credit_card|paypal)_[A-Za-z0-9]+\b", question)
            amounts = list(re.finditer(r"\$\s*(-?\d[\d,]*\.\d{2})\b", question))
            ids = re.findall(r"\b\d{10}\b", question)
            if complete or (transaction and method and amounts and ids):
                value.update(kind="proposal", asks=True, question_quote=question, topic="none", active_offers=[])
                if payload["business"] == "return" and transaction and method and len(amounts) == 1 and ids:
                    value.update(item_ids=list(dict.fromkeys(ids)), payment_method_id=method.group(),
                                 payment_quote=method.group(), amount=float(amounts[0].group(1).replace(",", "")),
                                 amount_quote=amounts[0].group())
                return value
        if payload["business"] == "exchange":
            direct = re.search(r"\b(?:do you (?:accept|prefer|want)|which (?:alternative|replacement|variant|sku))\b", question, re.I)
            if not direct or not re.search(r"\b(?:sku|variant|specification|replacement)\b", question, re.I):
                continue
            in_question = re.findall(r"\b(?:sku|variant)\s*[:#]?\s*(\d{10})\b", question, re.I)
            options = []
            if in_question:
                options = [(key, question) for key in dict.fromkeys(in_question)]
            else:
                # Only the immediately preceding actual option list, with no rejected options.
                prefix = text[:match.start()]
                lists = list(re.finditer(r"(?im)^\s*[-*]\s*(?:sku\s+|variant\s+)?(\d{10})\s*[:—-][^\r\n]*", prefix))
                if lists:
                    block = [lists[-1]]
                    for item in reversed(lists[:-1]):
                        if prefix[item.end():block[0].start()].strip():
                            break
                        block.insert(0, item)
                    options = [(item.group(1), item.group().strip()) for item in block
                               if not re.search(r"not available|unavailable|rejected|prohibited|out of stock", item.group(), re.I)]
            if not options:
                continue
            original = re.search(r"\boriginal (?:purchased )?item\s+(\d{10})\b", question, re.I)
            value.update(kind="spec_permission", asks=True, question_quote=question, topic="none", active_offers=[
                {"item_id": original.group(1) if original else None, "variant_id": key,
                 "payment_method_id": None, "quote": quote, "status": "active"} for key, quote in options
            ])
            return value
        if re.search(r"\bdo you (?:accept|choose|want)\b.*\brefund\b", question, re.I):
            methods = re.findall(r"\b(?:gift_card|credit_card|paypal)_[A-Za-z0-9]+\b", question)
            if len(set(methods)) == 1:
                value.update(kind="refund_permission", asks=True, question_quote=question, topic="none", active_offers=[
                    {"item_id": None, "variant_id": None, "payment_method_id": methods[0], "quote": question, "status": "active"}
                ])
                return value
    if not questions:
        stop = re.search(r"(?im)(?:^|[.!]\s+)(I (?:will|won't|will not) (?:not )?(?:submit|register|process|stop|cancel)[^.!\n]*|(?:your|the) order will remain unchanged[^.!\n]*)", text)
        if stop and re.search(r"\b(?:not|won't|stop|cancel|unchanged)\b", stop.group(1), re.I) and not re.search(r"\b(?:until|unless|before approval|not yet)\b", text, re.I):
            value.update(kind="stop", asks=False, question_quote="", topic="none", active_offers=[], stop_quote=stop.group(1))
        elif re.search(r"\bI (?:need to|must|should|will|have to) ask (?:the user|them)\b", text, re.I):
            value.update(kind="other", asks=False, question_quote="", topic="none", active_offers=[])
    return value


def problems(payload, value, contains):
    text = payload["actual_assistant"]
    issues = []
    kind = value.get("kind")
    if kind not in KINDS or value.get("topic") not in TOPICS or type(value.get("asks")) is not bool:
        issues.append("classification_schema")
    quote = value.get("question_quote")
    if value.get("asks") and not contains(text, quote):
        issues.append("question_quote")
    # A literal direct question and an asserted absence of a question disagree.
    if not value.get("asks") and isinstance(quote, str) and "?" in quote and contains(text, quote):
        issues.append("question_boolean")
    if kind in {"spec_permission", "refund_permission"} and not value.get("asks"):
        issues.append("permission_without_question")
    offers = value.get("active_offers")
    if kind not in {"spec_permission", "refund_permission"}:
        return sorted(set(issues))
    if not isinstance(offers, list):
        issues.append("offers_schema")
    else:
        for offer in offers:
            if not isinstance(offer, dict):
                issues.append("offer_schema")
                continue
            option = offer.get("variant_id") or offer.get("payment_method_id")
            evidence = offer.get("quote")
            if offer.get("status") != "active" or not isinstance(option, str) or not isinstance(evidence, str) or option not in evidence or not contains(text, evidence):
                issues.append("offer_quote")
    return sorted(set(issues))


class Simulator:
    def __init__(self, log, contains, base_url):
        import httpx
        from openai import OpenAI

        self.client = OpenAI(base_url=base_url, api_key="local", timeout=60, max_retries=0,
                             http_client=httpx.Client(trust_env=False, timeout=60))
        self.log = log
        self.contains = contains

    def close(self):
        self.client.close()

    def extract(self, messages, branch, trigger, limit=2100):
        payload = json.loads(messages[1]["content"])
        literal = literal_proposal(payload)
        system = messages[0]["content"] + "\n\n" + INSTRUCTIONS
        for attempt in (1, 2):
            request = [{"role": "system", "content": system}, messages[1]]
            row = {"branch": branch, "role": "simulator", "backend": MODEL, "trigger_reason": trigger,
                   "attempt": attempt, "messages": request, "temperature": 0, "thinking": False,
                   "response_format": "json_object", "max_tokens": limit, "usage": None, "status": "failed"}
            start = time.perf_counter()
            retry = False
            try:
                reply = self.client.chat.completions.create(
                    model=MODEL, messages=request, temperature=0, max_tokens=limit,
                    response_format={"type": "json_object"},
                )
                row["response"] = reply.model_dump(exclude_none=True)
                row["usage"] = row["response"].get("usage")
                row["provider_request_id"] = reply._request_id
                text = (reply.choices[0].message.content or "").strip()
                if text.startswith("```") and text.endswith("```") and "\n" in text:
                    text = text.split("\n", 1)[1][:-3].strip()
                    row["format_normalization"] = "removed_complete_markdown_fence"
                if literal is not None:
                    result = literal
                    row["evidence_binding"] = result
                    row["binding_source"] = "literal_visible_proposal"
                else:
                    raw = json.loads(text)
                    result = bind_direct_question(payload, raw.copy()) if isinstance(raw, dict) else raw
                    if result != raw:
                        row["evidence_binding"] = result
                        row["binding_source"] = "literal_current_question"
                issues = problems(payload, result, self.contains) if isinstance(result, dict) else ["non_object"]
                if reply.choices[0].finish_reason != "stop":
                    issues.append("unfinished_extraction")
                if issues:
                    row["validation_issues"] = issues
                    system += "\nRe-read the last actual customer-facing question and the literal options. Correct these evidence errors: " + ", ".join(issues)
                    retry = True
                else:
                    row["status"] = "success"
                    return result
            except (ValueError, IndexError):
                row["validation_issues"] = ["invalid_json_response"]
                retry = True
            except Exception as error:
                status = getattr(error, "status_code", None)
                name = type(error).__name__
                row["error"] = {"type": name, "http_status": status, "request_id": getattr(error, "request_id", None)}
                retry = status in (408, 429, 500, 502, 503, 504) or "Connection" in name or "Timeout" in name
            finally:
                row["seconds"] = time.perf_counter() - start
                self.log.write(json.dumps(row, ensure_ascii=False) + "\n")
                self.log.flush()
            if not retry:
                break
            if "error" in row:
                time.sleep(1)
        raise RuntimeError("simulator_extraction_unverified")
