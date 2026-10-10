
from unittest.mock import MagicMock, patch

from support_agent.llm_classifier import classify_ticket


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

    message = MagicMock()
    message.content = (
        '{"category":"order_status",'
        '"order_id":"4821",'
        '"needs_order_lookup":true}'
    )

    client.chat.completions.create.return_value.choices = [
        MagicMock(message=message)
    ]

    result = classify_ticket("Where is order #4821?")

    assert result.category == "order_status"
    assert result.order_id == "4821"
    assert result.needs_order_lookup is True

    client.chat.completions.create.assert_called_once()
