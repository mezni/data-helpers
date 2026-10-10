import os

from dotenv import load_dotenv
from openai import OpenAI

from support_agent.schemas import TicketInput, TicketOutput

load_dotenv()


SYSTEM_PROMPT = """
You classify customer support tickets.

Choose exactly one category:
- order_status: delivery, shipping, tracking, or order status
- refund: refunds, returns for reimbursement, or money back
- general: everything else

Decision rules:
1. If the customer requests a refund, choose refund,
   even when an order ID is included.
2. Extract an order ID only when explicitly present.
3. Never invent an order ID.
4. needs_order_lookup is true only when the category is
   order_status AND an order ID is present.
5. If the message asks about an order but gives no ID,
   classify it as order_status and set the lookup flag false.

Return data matching the supplied output schema.
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
