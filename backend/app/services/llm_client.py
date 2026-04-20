from __future__ import annotations

from typing import Any

import requests

from app.core.config import get_settings
from app.core.logging_config import get_logger


logger = get_logger(__name__)

# Example model endpoint:
# MODEL_SERVER_URL=http://your-qwen-server:8001/v1/completions


class LLMClient:
    def __init__(self, base_url: str, model_name: str, timeout_seconds: int) -> None:
        self.base_url = base_url
        self.model_name = model_name
        self.timeout_seconds = timeout_seconds

    def generate_completion(
        self,
        prompt: str,
        *,
        max_tokens: int = 64,
        temperature: float = 0.3,
    ) -> str:
        payload: dict[str, Any] = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        try:
            response = requests.post(
                self.base_url,
                json=payload,
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
            body = response.json()
            choices = body.get("choices", [])
            if not choices:
                logger.warning("Model server returned no completion choices")
                return ""
            return str(choices[0].get("text", "")).strip()
        except requests.RequestException as exc:
            logger.error("Model server request failed", exc_info=exc)
            return ""


def get_llm_client() -> LLMClient:
    settings = get_settings()
    return LLMClient(
        base_url=settings.model_server_url,
        model_name=settings.model_name,
        timeout_seconds=settings.model_timeout_seconds,
    )
