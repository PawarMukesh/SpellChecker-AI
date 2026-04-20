from enum import Enum

from pydantic import BaseModel, Field, field_validator


class RewriteMode(str, Enum):
    REPHRASE = "rephrase"
    FORMAL = "formal"
    INFORMAL = "informal"


class SuggestRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    cursor_position: int = Field(..., ge=0)

    @field_validator("cursor_position")
    @classmethod
    def validate_cursor_position(cls, value: int, info):
        text = info.data.get("text", "")
        if value > len(text):
            raise ValueError("cursor_position cannot exceed text length")
        return value


class RewriteRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    mode: RewriteMode
