from __future__ import annotations

from functools import lru_cache

from app.models.request_models import SuggestRequest
from app.models.response_models import SuggestResponse
from app.services.autocomplete_service import (
    AutocompleteService,
    get_autocomplete_service,
)
from app.services.grammar_service import GrammarService, get_grammar_service
from app.services.spell_service import SpellService, get_spell_service


class SuggestionOrchestrator:
    def __init__(
        self,
        spell_service: SpellService,
        grammar_service: GrammarService,
        autocomplete_service: AutocompleteService,
    ) -> None:
        self.spell_service = spell_service
        self.grammar_service = grammar_service
        self.autocomplete_service = autocomplete_service

    def build_suggestions(self, payload: SuggestRequest) -> SuggestResponse:
        spell_result = self.spell_service.correct_text(payload.text)
        grammar_suggestions = self.grammar_service.analyze(spell_result.corrected_text)
        typing_context = spell_result.corrected_text[: payload.cursor_position]
        next_word_predictions = self.autocomplete_service.predict_next_words(
            typing_context
        )

        return SuggestResponse(
            corrected_text=spell_result.corrected_text,
            spelling_suggestions=spell_result.suggestions,
            grammar_suggestions=grammar_suggestions,
            next_word_predictions=next_word_predictions,
        )


@lru_cache
def get_suggestion_orchestrator() -> SuggestionOrchestrator:
    return SuggestionOrchestrator(
        spell_service=get_spell_service(),
        grammar_service=get_grammar_service(),
        autocomplete_service=get_autocomplete_service(),
    )
