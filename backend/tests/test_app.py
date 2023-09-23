from fastapi.testclient import TestClient
import pytest
from ..main import app

client = TestClient(app)

@pytest.mark.skip
@pytest.mark.parametrize(
    "payload, expected_status, expected_response",
    [
        (
            {
                "model": "gpt-3.5-turbo-0613",
                "messages": [
                    {
                        "role": "user",
                        "content": "What is the capital of France? Answer in 1 word.",
                    }
                ],
            },
            200,
            { "text": "Paris" },
        ),
        # Add more test cases here
    ],
)
def test_llm(payload, expected_status, expected_response):
    response = client.post("/llm/", json=payload)
    assert response.status_code == expected_status
    assert response.json() == expected_response
