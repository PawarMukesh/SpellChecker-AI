from fastapi import APIRouter, Depends

from app.models.request_models import RewriteRequest
from app.models.response_models import RewriteResponse
from app.services.rewrite_service import RewriteService, get_rewrite_service


router = APIRouter()


@router.post("/rewrite", response_model=RewriteResponse)
async def rewrite_text(
    payload: RewriteRequest,
    rewrite_service: RewriteService = Depends(get_rewrite_service),
):
    rewritten_text = rewrite_service.rewrite(payload.text, payload.mode)
    return RewriteResponse(rewritten_text=rewritten_text)
