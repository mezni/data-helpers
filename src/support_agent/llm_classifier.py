import os

from dotenv import load_dotenv
from openai import OpenAI

from support_agent.schemas import TicketInput, TicketOutput

load_dotenv()

SYSTEM_PROMPT = """
Classify the customer support ticket.

Categories:
- order_status: delivery, shipping, tracking, or order status
- refund: refunds or requests for money back
- general: everything else

Rules:
- Extract an order ID only if explicitly present.
- Never invent an order ID.
- Set needs_order_lookup to true only when the category is
  order_status and an order ID is present.
- Return data matching the provided schema.
""".strip()


def classify_ticket(ticket: str) -> TicketOutput:
    validated = TicketInput(message=ticket)

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")

    if not api_key or not model:
        raise RuntimeError("Set OPENAI_API_KEY and OPENAI_MODEL.")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": validated.message},
        ],
        response_format=TicketOutput,
        temperature=0,
    )

    message = response.choices[0].message

    if message.refusal:
        raise ValueError("The model refused to classify this ticket.")

    if message.parsed is None:
        raise ValueError("The model returned no parsed result.")

    return message.parsed
