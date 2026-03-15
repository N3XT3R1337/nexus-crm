from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.tag import Tag
from app.models.user import User
from app.schemas.tag import TagCreate, TagUpdate, TagResponse, TagListResponse
from app.api.deps import get_current_user, require_perm

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("", response_model=TagListResponse)
async def list_tags(
    search: str = Query(None),
    current_user: User = Depends(require_perm("tags:read")),
    db: AsyncSession = Depends(get_db),
):
    query = select(Tag)
    count_query = select(func.count(Tag.id))

    if current_user.organization_id:
        query = query.where(Tag.organization_id == current_user.organization_id)
        count_query = count_query.where(Tag.organization_id == current_user.organization_id)

    if search:
        query = query.where(Tag.name.ilike(f"%{search}%"))
        count_query = count_query.where(Tag.name.ilike(f"%{search}%"))

    total = await db.scalar(count_query) or 0
    result = await db.execute(query.order_by(Tag.name))
    tags = result.scalars().all()

    return TagListResponse(items=[TagResponse.model_validate(t) for t in tags], total=total)


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(
    tag_id: str,
    current_user: User = Depends(require_perm("tags:read")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = result.scalar_one_or_none()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return TagResponse.model_validate(tag)


@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    data: TagCreate,
    current_user: User = Depends(require_perm("tags:write")),
    db: AsyncSession = Depends(get_db),
):
    existing = await db.execute(select(Tag).where(Tag.name == data.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Tag already exists")
    tag = Tag(**data.model_dump(), organization_id=current_user.organization_id)
    db.add(tag)
    await db.flush()
    await db.refresh(tag)
    return TagResponse.model_validate(tag)


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: str,
    data: TagUpdate,
    current_user: User = Depends(require_perm("tags:write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = result.scalar_one_or_none()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(tag, key, value)
    await db.flush()
    await db.refresh(tag)
    return TagResponse.model_validate(tag)


@router.delete("/{tag_id}")
async def delete_tag(
    tag_id: str,
    current_user: User = Depends(require_perm("tags:delete")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = result.scalar_one_or_none()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    await db.delete(tag)
    await db.flush()
    return {"message": "Tag deleted", "success": True}
