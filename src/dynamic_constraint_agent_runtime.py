"""On-demand scheduling for the frozen v2 business interface."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Dispatch:
    """The next module boundary and whether it requires a decision-model call."""

    route: str
    reason: str
    work: dict | None = None


def _program_work(kind, object_id, expected, reason):
    return Dispatch("program", reason, {
        "work_type": kind,
        "object": object_id,
        "parameters": {},
        "evidence_refs": [],
        "expected": expected,
        "reason": reason,
    })


def _confirmed_before(world):
    """Detect a prior request for approval of this exact plan."""
    fingerprint = world.plan["fingerprint"]
    return any(
        ask["kind"] == "confirm"
        and (ask.get("proposal") or {}).get("fingerprint") == fingerprint
        for ask in world.asks.values()
    )


def choose_dispatch(world, *, on_demand=True, program_retry_allowed=True):
    """Advance routine steps from visible evidence and leave open choices to the model."""
    if world.stopped or world.writes:
        return Dispatch("finished", "The task has already ended.")
    if world.pending:
        return Dispatch("state_semantics", "Actual user messages still need interpretation.")
    if not on_demand or not program_retry_allowed:
        return Dispatch("decision_model", "This step requires a model decision.")
    if world.needs_review or world.withdrawn or not world.core.authenticated:
        return Dispatch("decision_model", "The current request or evidence needs review.")

    scope = world.cfg["scope"]
    order_id = world.cfg["order_id"]
    if world.core.orders[order_id]["status"] != "delivered":
        return Dispatch("decision_model", "The order status needs a new decision.")

    # A known stock failure cannot be resolved by selecting the same offer automatically.
    if any(world.stock(item) is False for item in scope):
        return Dispatch("decision_model", "An observed stock conflict requires a choice.")

    missing_catalogues = {
        world.item(item)["product_id"] for item in scope if world.product(item) is None
    }
    if len(missing_catalogues) == 1:
        product_id = next(iter(missing_catalogues))
        return _program_work(
            "query", product_id, "record current inventory",
            "A unique required catalogue observation is missing and its product ID is known.",
        )
    if missing_catalogues or not world.feasible():
        return Dispatch("decision_model", "A constraint conflict or missing evidence requires a choice.")

    # Structured current targets must match the approved/specified options on every line.
    if any(
        item not in world.permission_sources
        or world.variant(item) is None
        or world.variant(item)["options"] != world.core.requirements.get(item)
        for item in scope
    ):
        return Dispatch("decision_model", "The effective specification needs resolution.")
    if not world.current_plan():
        return _program_work(
            "prepare", order_id, "store a feasible current whole-order plan",
            "Every current item is specified and in stock, and the whole amount is within the cap.",
        )
    if world.current_auth():
        return _program_work(
            "submit", order_id, "register the current authorized plan once",
            "The current feasible plan has effective whole-order authorization.",
        )
    if not _confirmed_before(world):
        return _program_work(
            "confirm", order_id, "request independent approval of the current plan",
            "The feasible current plan is complete and has not been presented for approval.",
        )
    return Dispatch("decision_model", "A prior confirmation of this plan needs follow-up.")
