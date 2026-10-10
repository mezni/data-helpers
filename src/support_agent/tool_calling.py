import json

from support_agent.llm_client import create_llm_client


class InvalidToolArgumentsError(Exception):
    pass


def get_order_status(order_id: str) -> dict:
    if not isinstance(order_id, str) or not order_id.isdigit():
        raise InvalidToolArgumentsError(f"Invalid order ID: {order_id}")

    orders = {
        "4821": {"status": "shipped", "estimated_delivery": "2026-10-12"},
    }

    if order_id in orders:
        return orders[order_id]
    return {"status": "not_found"}


def execute_tool(name: str, arguments_str: str) -> dict:
    try:
        args = json.loads(arguments_str)
    except (json.JSONDecodeError, ValueError):
        return {"error": "invalid_json_arguments"}

    if name == "get_order_status":
        try:
            return get_order_status(args["order_id"])
        except InvalidToolArgumentsError:
            return {"error": "invalid_tool_arguments"}
        except ValueError:
            return {"error": "tool_execution_failed"}
    return {"error": "unsupported_tool"}


def handle_ticket(ticket: str) -> dict:
    client = create_llm_client()
    max_rounds = 5

    for round_num in range(max_rounds):
        response = client.chat.completions.create(
            model="test-model",
            messages=[{"role": "user", "content": ticket}],
        )

        if not response.choices[0].message.tool_calls:
            raise RuntimeError("exceeded the limit")

        for tool_call in response.choices[0].message.tool_calls:
            if tool_call.function.name == "get_order_status":
                args = json.loads(tool_call.function.arguments)
                get_order_status(args["order_id"])
            else:
                pass

    raise RuntimeError("exceeded the limit")