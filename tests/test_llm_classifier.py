from unittest.mock import MagicMock, patch

from support_agent.llm_classifier import classify_ticket
from support_agent.schemas import TicketOutput


@patch("support_agent.llm_classifier.OpenAI")
@patch.dict(
    "os.environ",
    {
        "OPENAI_API_KEY": "test-key",
        "OPENAI_MODEL": "test-model",
    },
)
def test_classifies_order_status(mock_openai):
    client = MagicMock()
    mock_openai.return_value = client

    expected = TicketOutput(
        category="order_status",
        order_id="4821",
        needs_order_lookup=True,
    )

    message = MagicMock()
    message.parsed = expected
    message.refusal = None

    client.chat.completions.parse.return_value.choices = [MagicMock(message=message)]

    result = classify_ticket("Where is order #4821?")

    assert result == expected
    client.chat.completions.parse.assert_called_once()


@patch("support_agent.llm_classifier.OpenAI")
@patch.dict(
    "os.environ",
    {
        "OPENAI_API_KEY": "test-key",
        "OPENAI_MODEL": "test-model",
    },
)
def test_handles_model_refusal(mock_openai):
    client = MagicMock()
    mock_openai.return_value = client

    message = MagicMock()
    message.parsed = None
    message.refusal = "Unable to process this request."

    client.chat.completions.parse.return_value.choices = [MagicMock(message=message)]

    import pytest

    with pytest.raises(ValueError, match="refused"):
        classify_ticket("Where is order #4821?")
