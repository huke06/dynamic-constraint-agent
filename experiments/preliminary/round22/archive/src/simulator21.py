"""Deterministic adapter between native Agent speech and the controlled user."""

import re


_FORMATTING = re.compile(r"(\*\*|__|\x60)(?=\S)(.+?)(?<=\S)\1")


def includes_quote(message, quote):
    """Accept only exact evidence, apart from matched Markdown emphasis."""
    return isinstance(quote, str) and bool(quote.strip()) and (
        quote in message or quote in _FORMATTING.sub(r"\2", message)
    )


def clarified_offer(world, assistant_ref, item_id, message, extracted):
    """Respond only to actual offers and record new permission with its reply."""
    product = world.product(item_id)
    if not product:
        return None
    current = world.oracle[item_id]
    available = {
        variant_id for variant_id, variant in product["variants"].items()
        if variant["available"] is True and variant_id != item_id
    }
    offered = {
        variant["variant_id"] for variant in (extracted.get("offered_variants") or [])
        if isinstance(variant, dict)
        and variant.get("variant_id") in available
        and includes_quote(message, variant.get("quote"))
    }
    if not offered:
        offered = {
            variant_id for variant_id in available
            if re.search(rf"(?<!\d){re.escape(variant_id)}(?!\d)", message)
        }
    if not offered:
        return None

    if current in available:
        # Confirm the user's prior preference without granting transaction approval.
        ref = len(world.history)
        reply = f"Keep item {current}, the specification I already agreed to. Please show the complete proposal for final approval."
        world.history.append({"role": "user", "content": reply})
        world.env_records.append({
            "ask_kind": "clarify", "assistant_ref": assistant_ref, "user_ref": ref,
            "reply": reply, "approved": False,
        })
        return {"reply": reply, "user_ref": ref}

    # The controlled user's choice is deterministic even when several offers are valid.
    def offer_position(variant_id):
        position = message.find(variant_id)
        return position if position >= 0 else len(message), variant_id

    chosen = min(offered, key=offer_position)
    ref = world.reply("clarify", assistant_ref, {
        "object": item_id, "offered_variant_id": chosen, "text": message,
        "explicit_variant": len(offered) > 1 or chosen not in message,
    })
    return {"reply": world.history[ref]["content"], "user_ref": ref}


def record_handoff(world, tool_name, is_error):
    """Record a successful transfer as a terminal outcome distinct from a write."""
    if tool_name != "transfer_to_human_agents" or is_error:
        return False
    world.stopped = True
    return True

