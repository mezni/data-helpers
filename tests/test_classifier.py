import pytest

from support_agent.classifier import classify_ticket


def test_order_status_ticket():
    result = classify_ticket("My order #4821 has not arrived.")

    assert result.category == "order_status"
    assert result.order_id == "4821"
    assert result.needs_order_lookup is True


def test_empty_ticket_is_rejected():
    with pytest.raises(ValueError):
        classify_ticket("   ")


def test_general_ticket():
    result = classify_ticket("How do I change my email?")

    assert result.category == "general"
    assert result.needs_order_lookup is False
