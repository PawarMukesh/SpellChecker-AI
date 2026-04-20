from pydantic import BaseModel, Field


class SpellingSuggestion(BaseModel):
    original: str
    suggestion: str
    start_index: int
    end_index: int


class GrammarSuggestion(BaseModel):
    message: str
    suggestion: str


class SuggestResponse(BaseModel):
    corrected_text: str
    spelling_suggestions: list[SpellingSuggestion] = Field(default_factory=list)
    grammar_suggestions: list[GrammarSuggestion] = Field(default_factory=list)
    next_word_predictions: list[str] = Field(default_factory=list)


class RewriteResponse(BaseModel):
    rewritten_text: str
