from __future__ import annotations

from app.models.request_models import RewriteMode
from app.services.llm_client import LLMClient, get_llm_client


PROMPTS = {
    RewriteMode.REPHRASE: "Rephrase the following sentence without changing meaning: {text}",
    RewriteMode.FORMAL: "Convert the following text into a professional formal email tone: {text}",
    RewriteMode.INFORMAL: "Rewrite the following text in a friendly informal tone: {text}",
}


class RewriteService:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    def rewrite(self, text: str, mode: RewriteMode) -> str:
        prompt = PROMPTS[mode].format(text=text)

        # AI model integration: this sends the rewrite prompt to the configured Qwen-compatible model endpoint.
        rewritten = self.llm_client.generate_completion(
            prompt,
            max_tokens=256,
            temperature=0.45,
        )
        return rewritten.strip() or text


def get_rewrite_service() -> RewriteService:
    return RewriteService(get_llm_client())
