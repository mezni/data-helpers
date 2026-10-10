def get_order_status(order_id: str) -> dict:
    if not order_id.isdigit():
        raise ValueError(f"Invalid order ID: {order_id}")

    orders = {
        "4821": {"status": "shipped", "estimated_delivery": "2026-10-12"},
    }

    if order_id in orders:
        return orders[order_id]
    return {"status": "not_found"}