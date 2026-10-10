from support_agent.llm_classifier import classify_ticket
from support_agent.schemas import TicketOutput


def handle_ticket(ticket: str) -> TicketOutput:
    return classify_ticket(ticket)