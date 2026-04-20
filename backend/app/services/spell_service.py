from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import get_close_matches

from app.models.response_models import SpellingSuggestion


WORD_PATTERN = re.compile(r"\b[a-zA-Z']+\b")


@dataclass(frozen=True)
class SpellCheckResult:
    corrected_text: str
    suggestions: list[SpellingSuggestion]


class SpellService:
    def __init__(self) -> None:
        # Future improvement: replace this seed dictionary with a domain-specific lexicon
        # loaded from configuration or persisted storage.
        self.dictionary = {
            "a",
            "about",
            "after",
            "an",
            "and",
            "are",
            "assistant",
            "be",
            "business",
            "can",
            "client",
            "company",
            "complete",
            "could",
            "customer",
            "data",
            "deadline",
            "document",
            "draft",
            "email",
            "enterprise",
            "for",
            "formal",
            "grammar",
            "have",
            "hello",
            "improve",
            "informal",
            "is",
            "it",
            "meeting",
            "message",
            "need",
            "next",
            "of",
            "on",
            "please",
            "project",
            "proposal",
            "provide",
            "rephrase",
            "report",
            "review",
            "schedule",
            "sentence",
            "soon",
            "spelling",
            "status",
            "team",
            "text",
            "that",
            "the",
            "their",
            "there",
            "this",
            "to",
            "tomorrow",
            "update",
            "we",
            "will",
            "with",
            "work",
            "writing",
            "you",
            "your",
        }

    def correct_text(self, text: str) -> SpellCheckResult:
        suggestions: list[SpellingSuggestion] = []
        corrected_parts: list[str] = []
        last_index = 0

        for match in WORD_PATTERN.finditer(text):
            word = match.group(0)
            normalized = word.lower()
            corrected_word = word

            if normalized not in self.dictionary and len(normalized) > 2:
                candidates = get_close_matches(
                    normalized, self.dictionary, n=1, cutoff=0.8
                )
                if candidates:
                    suggestion = self._match_case(candidates[0], word)
                    corrected_word = suggestion
                    suggestions.append(
                        SpellingSuggestion(
                            original=word,
                            suggestion=suggestion,
                            start_index=match.start(),
                            end_index=match.end(),
                        )
                    )

            corrected_parts.append(text[last_index : match.start()])
            corrected_parts.append(corrected_word)
            last_index = match.end()

        corrected_parts.append(text[last_index:])
        return SpellCheckResult(
            corrected_text="".join(corrected_parts), suggestions=suggestions
        )

    @staticmethod
    def _match_case(suggestion: str, original: str) -> str:
        if original.isupper():
            return suggestion.upper()
        if original.istitle():
            return suggestion.title()
        return suggestion


def get_spell_service() -> SpellService:
    return SpellService()
