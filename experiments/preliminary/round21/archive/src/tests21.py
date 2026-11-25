"""Offline regression tests using frozen cases and real native-tool methods."""

from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

from construct20 import R, read, save
from official20 import native_roll, user
from simulator21 import clarified_offer, includes_quote
from tau2.data_model.message import AssistantMessage, ToolCall
from tests20 import check as prior_checks
from world20 import World, dump


def make_world(task_id):
    config = read(R / f"configs/stage2/{task_id}/case.json")
    world = World(config, "stable", None)
    item = config["scope"][0]
    product_id = world.item(item)["product_id"]
    args = {"product_id": product_id}
    world.observe("get_product_details", args, dump(world.tools.get_product_details(**args)))
    return world, item


def check():
    checks = prior_checks()["checks"]
    world, item = make_world("49")
    offers = [row["item_id"] for row in world.alternatives(item)[:2]]
    assert len(offers) == 2 and world.stock(item) is False
    message = f"Would you accept {offers[0]} or {offers[1]}?"
    world.history.append({"role": "assistant", "content": message})
    clarification = {
        "kind": "clarification", "question_quote": message, "clarify_item_id": item,
        "offered_variants": [{"variant_id": sku, "quote": sku} for sku in offers],
    }
    transport = SimpleNamespace(json=lambda *_args, **_kwargs: clarification)
    choice = user(world, transport, message, len(world.history) - 1)
    chosen = world.oracle[item]
    checks["49_offer_has_explicit_matching_permission"] = (
        chosen in offers and chosen in choice["reply"]
        and world.history[choice["user_ref"]]["content"] == world.env_records[-1]["reply"]
    )
    checks["49_specification_does_not_grant_final_authorization"] = not world.env_approvals
    replacement = next(sku for sku in offers if sku != chosen)
    reprompt = f"Would you accept {replacement}?"
    reply = clarified_offer(world, len(world.history) - 1, item, reprompt, {})
    checks["49_later_questions_preserve_agreed_specification"] = chosen in reply["reply"] and world.oracle[item] == chosen

    # Use a real, consistent proposal whose source evidence contains Markdown formatting.
    cfg = world.cfg
    delta = Decimal(str(world.variant(item, chosen)["price"])) - Decimal(str(world.item(item)["price"]))
    total = f"{delta:.2f}"
    proposal = f"Exchange {item} for {chosen}. Net difference: **{total}** USD. Pay by **{cfg['payment_method_id']}**. Do you approve?"
    world.history.append({"role": "assistant", "content": proposal})
    extraction = {
        "kind": "proposal", "asks": True, "question_quote": "Do you approve?",
        "pairs": [{"item_id": item, "new_item_id": chosen, "quote": f"Exchange {item} for {chosen}."}],
        "difference": float(delta), "amount_quote": f"Net difference: {total} USD.",
        "payment_method_id": cfg["payment_method_id"], "payment_quote": f"Pay by {cfg['payment_method_id']}.",
    }
    approval = user(world, SimpleNamespace(json=lambda *_a, **_k: extraction), proposal, len(world.history) - 1)
    checks["49_markdown_proposal_is_approved"] = approval["approved"] and world.env_valid(world.expected_args())
    checks["markup_normalization_preserves_money_and_quote_boundaries"] = (
        includes_quote("Net **-7.99** USD", "Net -7.99 USD")
        and not includes_quote("Net **-7.99** USD", "Net -8.00 USD")
        and not includes_quote("Net **-7.99** USD", "Net 7.99 USD")
    )

    # Check the real loop exits as soon as the native transfer tool succeeds.
    config = read(R / "configs/stage2/49/case.json")
    handoff = AssistantMessage(role="assistant", tool_calls=[
        ToolCall(id="transfer-1", name="transfer_to_human_agents", arguments={"summary": "Needs human assistance"})
    ])
    mock_agent = SimpleNamespace(
        get_init_state=lambda _history: SimpleNamespace(messages=[]),
        generate_next_message=lambda _incoming, state: (handoff, state),
    )
    with TemporaryDirectory(prefix="round21-handoff-") as directory, patch("official20.LLMAgent", return_value=mock_agent):
        out = Path(directory)
        result = native_roll(config, "stable", "handoff_check", SimpleNamespace(), out)
        trajectory = read(out / "handoff_check_trajectory.json")
    checks["native_handoff_is_terminal_without_exchange_or_simulator_call"] = (
        result["handoff"] and result["writes"] == 0 and result["error"] is None
        and [event["module"] for event in trajectory] == ["native_execution", "terminal_handoff"]
    )

    world, item = make_world("49")
    old_ref = len(world.history)
    world.history.append({"role": "user", "content": "Earlier completed remark."})
    new_ref = len(world.history)
    world.history.append({"role": "user", "content": "Now about this item: " + world.item(item)["name"]})
    world.last_change_ref = old_ref
    world.pending = [new_ref]
    world.feedback = [{"kind": "semantic_update", "processed_refs": [old_ref]}]
    local = world.local()
    checks["semantic_payload_omits_processed_user_reference"] = (
        local["pending_source_refs"] == [new_ref]
        and "Earlier completed remark." not in str(local)
        and "processed_refs" not in str(local)
    )
    try:
        world.apply({"updates": [{"source_ref": old_ref, "quote": "Earlier completed remark.", "kind": "stop"}], "processed_refs": [new_ref]})
    except ValueError:
        checks["processed_user_reference_cannot_change_business_state"] = not world.withdrawn and world.pending == [new_ref]
    else:
        checks["processed_user_reference_cannot_change_business_state"] = False

    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError(failed)
    return {"passed": True, "model_calls": 0, "check_count": len(checks), "checks": checks}


if __name__ == "__main__":
    report = check()
    save(R / "results/offline_regression.json", report)
    print(f'{report["check_count"]} checks passed; no online model calls.')

