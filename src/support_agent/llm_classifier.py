
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from support_agent.schemas import TicketInput, TicketOutput

load_dotenv()

SYSTEM_PROMPT = """
You classify customer support tickets.

Choose exactly one category:
- order_status: questions about delivery, shipping, tracking, or order status
- refund: requests about refunds or getting money back
- general: everything else

Extract an order ID only when it is explicitly present.
Do not invent an order ID.
Set needs_order_lookup to true only when:
- category is order_status
- an order ID is present

Return only a JSON object with:
category, order_id, needs_order_lookup.
""".strip()


def classify_ticket(ticket: str) -> TicketOutput:
    validated = TicketInput(message=ticket)

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")

    if not api_key or not model:
        raise RuntimeError(
            "Set OPENAI_API_KEY and OPENAI_MODEL in your environment."
        )

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": validated.message},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("The model returned an empty response.")

    result = json.loads(content)

    # Validate the model's output against our application contract.
    return TicketOutput.model_validate(result)
