from fastapi import APIRouter, Depends

from app.models.request_models import SuggestRequest
from app.models.response_models import SuggestResponse
from app.services.orchestrator import (
    SuggestionOrchestrator,
    get_suggestion_orchestrator,
)


router = APIRouter()


@router.post("/suggest", response_model=SuggestResponse)
async def suggest_text(
    payload: SuggestRequest,
    orchestrator: SuggestionOrchestrator = Depends(get_suggestion_orchestrator),
):
    return orchestrator.build_suggestions(payload)
