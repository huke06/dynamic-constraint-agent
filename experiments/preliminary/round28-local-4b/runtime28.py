"""Round 28 changes to shared extraction and source-bound return termination."""

from contextlib import contextmanager
import json
from pathlib import Path
import re
import sys
from unittest.mock import patch

ROUND = Path(__file__).resolve().parent
PREVIOUS = ROUND.parent / "round27-local-4b"
sys.path.insert(0, str(PREVIOUS))

import prepare27 as prep
import recheck27 as shared
import recheck_amount27 as signed
import run27 as backends
import simulator27 as sim


# Detect questions seeking group-level, present authorization, then let the
# business adjudicator check full scope, amount, stock, method and epoch.
APPROVAL = re.compile(r"\b(?:approve|authori[sz]e|proceed|go ahead|confirm|submit|register|process)\b", re.I)
AMOUNT_ONLY = re.compile(r"\b(?:confirm|verify|check|approve)\s+(?:(?:that|whether|the|this|only|just|my|current|total|stated)\s+){0,6}(?:amount|total|calculation|difference|refund amount|price)\b", re.I)
MONEY_INQUIRY = re.compile(r"\b(?:what|how much|which)\b[^?]*\b(?:amount|total|difference|refund|fee|price|cost)\b", re.I)
CHOICE_NOUN = re.compile(r"\b(?:route|method|option|sku|variant)\b", re.I)
PARTIAL = re.compile(r"\b(?:only|just)\s+(?:the\s+)?(?:first|second|one|that|this|item|sku|refund method|payment method|amount|price)\b|\b(?:partial approval|for now|instead of the full)\b", re.I)
CONDITIONAL = re.compile(r"\b(?:if|unless|provided that|as long as|subject to|on condition that)\b", re.I)
WITHDRAW_BUSINESS = re.compile(r"\b(?:withdraw|cancel)\s+(?:(?:my|the|this)\s+)?(?:entire|whole)\s+return\s+(?:request|transaction)\b", re.I)
EXPLICIT_HOLD = re.compile(r"\b(?:do not|don't|please don't)\s+(?:submit|register|process|proceed)\b", re.I)


def authorize_question(text, extraction, contains):
    if extraction.get("kind") != "proposal":
        return None
    quote = extraction.get("question_quote") or ""
    if not extraction.get("asks") or not contains(text, quote) or not APPROVAL.search(quote):
        return "no_current_authorization_question"
    # Evaluate the full current question even if an extraction drops its qualifier.
    for question in re.findall(r"(?:[^\n.!?]|(?<=\d)\.(?=\d))*\?", text):
        if contains(question, quote):
            quote = question
            break
    if AMOUNT_ONLY.search(quote) or MONEY_INQUIRY.search(quote):
        return "amount_inquiry_only"
    if PARTIAL.search(quote):
        return "partial_confirmation"
    if CONDITIONAL.search(quote) or EXPLICIT_HOLD.search(quote):
        return "conditional_or_withheld_confirmation"
    return None


def normalized(core, payload, extraction):
    text = payload["actual_assistant"]
    quote = extraction.get("question_quote") or ""
    if core.contains(text, quote) and "?" in quote and extraction.get("topic") != "cap_direction":
        if AMOUNT_ONLY.search(quote) or (MONEY_INQUIRY.search(quote) and not APPROVAL.search(quote) and not CHOICE_NOUN.search(quote)):
            return dict(extraction, kind="constraint_question", asks=True, topic="amount_basis", active_offers=[])
    reason = authorize_question(text, extraction, core.contains)
    if not reason:
        return extraction
    result = dict(extraction, kind="other", asks=False, question_quote="", topic="none", active_offers=[])
    result["proposal_guard_reason"] = reason
    return result


def withdrawal_evidence(world):
    """Read the latest accepted semantic result and its actual user record."""
    if not world.withdrawn or world.pending:
        return None
    for update in reversed(world.parsed_history):
        if update.get("kind") != "withdrawal":
            continue
        ref, quote = update.get("source_ref"), update.get("quote") or ""
        if type(ref) is not int or not 0 <= ref < len(world.history):
            return None
        source = world.history[ref]
        if (source.get("role") == "user" and quote in (source.get("content") or "")
                and WITHDRAW_BUSINESS.search(quote) and not CONDITIONAL.search(quote)
                and not any(m.get("role") == "user" for m in world.history[ref + 1:])):
            return ref
        return None
    return None


@contextmanager
def installed(repair):
    core, runner = repair.c, repair.r
    original_dispatch = runner.return_dispatch
    with shared.repairs(core):
        previous_bind = sim.bind_direct_question
        previous_adjudicate = core.adjudicate
        previous_simulator = backends.Simulator

        def bind(payload, value):
            value = previous_bind(payload, value)
            return normalized(core, payload, signed.bind_signed_amount(payload, value))

        def adjudicate(world, text, ref, extraction):
            # Covers the typed visible-plan path, which bypasses model binding.
            safe = normalized(core, {"actual_assistant": text}, extraction)
            return previous_adjudicate(world, text, ref, safe)

        def dispatch(world, program_retry_allowed=True):
            ref = withdrawal_evidence(world)
            if ref is not None:
                return core.Dispatch("program", "accepted explicit whole-return withdrawal; no discretion or write", {
                    "work_type": "stop", "object": world.cfg["order_id"], "parameters": {},
                    "evidence_refs": [ref], "expected": "acknowledge stopping with unchanged database",
                    "reason": "latest source-bound whole-return withdrawal closes active work",
                })
            return original_dispatch(world, program_retry_allowed)

        class Simulator(previous_simulator):
            def extract(self, messages, branch, trigger, limit=2100):
                payload = json.loads(messages[1]["content"])
                result = super().extract(messages, branch, trigger, limit)
                return normalized(core, payload, result)

        with (patch.object(sim, "bind_direct_question", bind), patch.object(core, "adjudicate", adjudicate),
              patch.object(backends, "Simulator", Simulator), patch.object(runner, "return_dispatch", dispatch)):
            yield
