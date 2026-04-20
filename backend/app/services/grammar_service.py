import re

from app.models.response_models import GrammarSuggestion


class GrammarService:
    def analyze(self, text: str) -> list[GrammarSuggestion]:
        # Future improvement: promote these rules into a configurable rule engine
        # so grammar policies can evolve without changing service code.
        suggestions: list[GrammarSuggestion] = []
        stripped_text = text.strip()

        if not stripped_text:
            return suggestions

        if re.search(r"\s{2,}", text):
            suggestions.append(
                GrammarSuggestion(
                    message="Multiple consecutive spaces detected.",
                    suggestion="Replace repeated spaces with a single space.",
                )
            )

        first_char = stripped_text[0]
        if first_char.isalpha() and first_char.islower():
            suggestions.append(
                GrammarSuggestion(
                    message="Sentence should start with a capital letter.",
                    suggestion=f"Capitalize '{first_char}'.",
                )
            )

        if stripped_text[-1].isalnum():
            suggestions.append(
                GrammarSuggestion(
                    message="Sentence may be missing terminal punctuation.",
                    suggestion="Consider ending the sentence with '.', '!' or '?'.",
                )
            )

        lowered = stripped_text.lower()
        if " i " in f" {lowered} ":
            suggestions.append(
                GrammarSuggestion(
                    message="Standalone first-person pronoun should be capitalized.",
                    suggestion="Replace 'i' with 'I'.",
                )
            )

        return suggestions


def get_grammar_service() -> GrammarService:
    return GrammarService()
