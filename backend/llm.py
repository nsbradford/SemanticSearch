import logging
import os
from typing import Dict, List

import litellm
from litellm import acompletion
from backend.models import LLMChatCompletionMessage
from backend.utils import getEnvironment

# https://docs.litellm.ai/docs/observability/promptlayer_integration
litellm.success_callback = ["promptlayer"]

# https://docs.helicone.ai/getting-started/integration-method/litellm
litellm.api_base = "https://oai.hconeai.com/v1"
litellm.headers = {
    "Helicone-Auth": f"Bearer {os.getenv('HELICONE_API_KEY')}",
    "Helicone-Cache-Enabled": "true",
}


async def llm_get(model: str, messages: List[LLMChatCompletionMessage]) -> str:
    print(f"Calling LLM {model}")
    response = await acompletion(
        model=model,
        messages=[m.dict() for m in messages],
        temperature=0,
        metadata={"environment": getEnvironment()},
    )
    text = response.choices[0].message.content
    print(f"LLM response: {response.choices[0].message.content}")
    return text
