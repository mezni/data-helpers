import re
from typing import TypedDict


class TicketResult(TypedDict):
    category: str
    order_id: str | None
    needs_order_lookup: bool


def classify_ticket(ticket: str) -> TicketResult:
    text = ticket.strip().lower()

    if not text:
        raise ValueError("Ticket cannot be empty")

    order_match = re.search(
        r"\border\s*#?\s*(\d+)\b",
        text,
    )

    if any(word in text for word in ("arrived", "delivery", "shipped")):
        category = "order_status"
    elif any(word in text for word in ("refund", "money back")):
        category = "refund"
    else:
        category = "general"

    return {
        "category": category,
        "order_id": order_match.group(1) if order_match else None,
        "needs_order_lookup": (category == "order_status" and order_match is not None),
    }
