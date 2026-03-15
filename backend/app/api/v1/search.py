from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.database import get_db
from app.models.user import User
from app.schemas.common import SearchResponse
from app.api.deps import get_current_user
from app.services.search import full_text_search

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("", response_model=SearchResponse)
async def search(
    q: str = Query(..., min_length=1),
    entity_types: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(25, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    types = entity_types.split(",") if entity_types else None
    results, total = await full_text_search(
        db, q, types, page, per_page, current_user.organization_id
    )
    return SearchResponse(results=results, total=total, query=q)
