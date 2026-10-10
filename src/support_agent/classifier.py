import re

from pydantic import ValidationError

from support_agent.schemas import TicketInput, TicketOutput


def classify_ticket(ticket: str) -> TicketOutput:
    try:
        validated = TicketInput(message=ticket)
    except ValidationError as exc:
        raise ValueError("Ticket cannot be empty") from exc

    text = validated.message.lower()

    match = re.search(r"\border\s*#?\s*(\d+)\b", text)

    if any(word in text for word in ("arrived", "delivery", "shipped")):
        category = "order_status"
    elif any(word in text for word in ("refund", "money back")):
        category = "refund"
    else:
        category = "general"

    order_id = match.group(1) if match else None

    return TicketOutput(
        category=category,
        order_id=order_id,
        needs_order_lookup=(category == "order_status" and order_id is not None),
    )