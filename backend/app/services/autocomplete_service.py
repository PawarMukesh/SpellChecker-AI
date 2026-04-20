from __future__ import annotations

from app.core.logging_config import get_logger
from app.services.llm_client import LLMClient, get_llm_client


logger = get_logger(__name__)


class AutocompleteService:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    def predict_next_words(self, text: str) -> list[str]:
        if not text.strip():
            return []

        prompt = (
            "Predict the next three likely words for the text below. "
            "Return only a comma-separated list of three short predictions.\n\n"
            f"Text: {text}"
        )

        # AI model integration: this calls the configured Qwen-compatible model endpoint.
        completion = self.llm_client.generate_completion(
            prompt,
            max_tokens=24,
            temperature=0.2,
        )
        predictions = [
            item.strip(" -\n\t.,") for item in completion.replace("\n", ",").split(",")
        ]
        unique_predictions: list[str] = []

        for prediction in predictions:
            if prediction and prediction not in unique_predictions:
                unique_predictions.append(prediction)
            if len(unique_predictions) == 3:
                break

        logger.debug(
            "Generated autocomplete predictions",
            extra={"predictions": unique_predictions},
        )
        return unique_predictions


def get_autocomplete_service() -> AutocompleteService:
    return AutocompleteService(get_llm_client())
