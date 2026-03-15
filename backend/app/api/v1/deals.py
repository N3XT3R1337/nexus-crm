from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models.deal import Deal, DealStage
from app.models.tag import Tag
from app.models.user import User
from app.models.audit_log import AuditLog
from app.schemas.deal import (
    DealCreate, DealUpdate, DealResponse, DealListResponse,
    DealStageCreate, DealStageUpdate, DealStageResponse,
    DealStageTransition, DealWin, DealLose,
)
from app.api.deps import get_current_user, require_perm
from app.services.deal_pipeline import transition_deal_stage, win_deal, lose_deal, get_pipeline_summary
import json

router = APIRouter(prefix="/deals", tags=["Deals"])


@router.get("/stages", response_model=list[DealStageResponse])
async def list_stages(
    current_user: User = Depends(require_perm("deals:read")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(DealStage).order_by(DealStage.order))
    return [DealStageResponse.model_validate(s) for s in result.scalars().all()]


@router.post("/stages", response_model=DealStageResponse, status_code=status.HTTP_201_CREATED)
async def create_stage(
    data: DealStageCreate,
    current_user: User = Depends(require_perm("settings:write")),
    db: AsyncSession = Depends(get_db),
):
    stage = DealStage(**data.model_dump(), organization_id=current_user.organization_id)
    db.add(stage)
    await db.flush()
    await db.refresh(stage)
    return DealStageResponse.model_validate(stage)


@router.put("/stages/{stage_id}", response_model=DealStageResponse)
async def update_stage(
    stage_id: str,
    data: DealStageUpdate,
    current_user: User = Depends(require_perm("settings:write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(DealStage).where(DealStage.id == stage_id))
    stage = result.scalar_one_or_none()
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(stage, key, value)
    await db.flush()
    await db.refresh(stage)
    return DealStageResponse.model_validate(stage)


@router.delete("/stages/{stage_id}")
async def delete_stage(
    stage_id: str,
    current_user: User = Depends(require_perm("settings:write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(DealStage).where(DealStage.id == stage_id))
    stage = result.scalar_one_or_none()
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    await db.delete(stage)
    await db.flush()
    return {"message": "Stage deleted", "success": True}


@router.get("/pipeline")
async def get_pipeline(
    current_user: User = Depends(require_perm("deals:read")),
    db: AsyncSession = Depends(get_db),
):
    return await get_pipeline_summary(db, current_user.organization_id)


@router.get("", response_model=DealListResponse)
async def list_deals(
    page: int = Query(1, ge=1),
    per_page: int = Query(25, ge=1, le=100),
    search: str = Query(None),
    status_filter: str = Query(None, alias="status"),
    stage_id: str = Query(None),
    priority: str = Query(None),
    owner_id: str = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    current_user: User = Depends(require_perm("deals:read")),
    db: AsyncSession = Depends(get_db),
):
    query = select(Deal).options(selectinload(Deal.stage))
    count_query = select(func.count(Deal.id))

    if current_user.organization_id:
        query = query.where(Deal.organization_id == current_user.organization_id)
        count_query = count_query.where(Deal.organization_id == current_user.organization_id)

    if search:
        term = f"%{search}%"
        query = query.where(Deal.title.ilike(term))
        count_query = count_query.where(Deal.title.ilike(term))

    if status_filter:
        query = query.where(Deal.status == status_filter)
        count_query = count_query.where(Deal.status == status_filter)

    if stage_id:
        query = query.where(Deal.stage_id == stage_id)
        count_query = count_query.where(Deal.stage_id == stage_id)

    if priority:
        query = query.where(Deal.priority == priority)
        count_query = count_query.where(Deal.priority == priority)

    if owner_id:
        query = query.where(Deal.owner_id == owner_id)
        count_query = count_query.where(Deal.owner_id == owner_id)

    total = await db.scalar(count_query) or 0
    sort_col = getattr(Deal, sort_by, Deal.created_at)
    if sort_order == "asc":
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())

    offset = (page - 1) * per_page
    result = await db.execute(query.offset(offset).limit(per_page))
    deals = result.scalars().all()

    return DealListResponse(
        items=[DealResponse.model_validate(d) for d in deals],
        total=total, page=page, per_page=per_page,
        pages=(total + per_page - 1) // per_page if per_page else 0,
    )


@router.get("/{deal_id}", response_model=DealResponse)
async def get_deal(
    deal_id: str,
    current_user: User = Depends(require_perm("deals:read")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Deal).options(selectinload(Deal.stage)).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return DealResponse.model_validate(deal)


@router.post("", response_model=DealResponse, status_code=status.HTTP_201_CREATED)
async def create_deal(
    data: DealCreate,
    current_user: User = Depends(require_perm("deals:write")),
    db: AsyncSession = Depends(get_db),
):
    deal_data = data.model_dump(exclude={"tag_ids"})
    deal = Deal(
        **deal_data,
        owner_id=current_user.id,
        organization_id=current_user.organization_id,
    )
    if data.stage_id:
        stage_result = await db.execute(select(DealStage).where(DealStage.id == data.stage_id))
        stage = stage_result.scalar_one_or_none()
        if stage:
            deal.probability = stage.probability

    db.add(deal)
    await db.flush()

    if data.tag_ids:
        tag_result = await db.execute(select(Tag).where(Tag.id.in_(data.tag_ids)))
        deal.tags = list(tag_result.scalars().all())

    audit = AuditLog(
        action="create", entity_type="deal", entity_id=deal.id,
        changes=json.dumps(deal_data, default=str), user_id=current_user.id,
        organization_id=current_user.organization_id,
    )
    db.add(audit)
    await db.flush()
    await db.refresh(deal)
    return DealResponse.model_validate(deal)


@router.put("/{deal_id}", response_model=DealResponse)
async def update_deal(
    deal_id: str,
    data: DealUpdate,
    current_user: User = Depends(require_perm("deals:write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Deal).options(selectinload(Deal.stage)).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    update_data = data.model_dump(exclude_unset=True)
    tag_ids = update_data.pop("tag_ids", None)
    for key, value in update_data.items():
        setattr(deal, key, value)

    if tag_ids is not None:
        tag_result = await db.execute(select(Tag).where(Tag.id.in_(tag_ids)))
        deal.tags = list(tag_result.scalars().all())

    await db.flush()
    await db.refresh(deal)
    return DealResponse.model_validate(deal)


@router.delete("/{deal_id}")
async def delete_deal(
    deal_id: str,
    current_user: User = Depends(require_perm("deals:delete")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Deal).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    await db.delete(deal)
    await db.flush()
    return {"message": "Deal deleted", "success": True}


@router.post("/{deal_id}/transition", response_model=DealResponse)
async def transition_stage(
    deal_id: str,
    data: DealStageTransition,
    current_user: User = Depends(require_perm("deals:change_stage")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Deal).options(selectinload(Deal.stage)).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    updated = await transition_deal_stage(db, deal, data.stage_id, current_user.id)
    if not updated:
        raise HTTPException(status_code=400, detail="Invalid stage")
    return DealResponse.model_validate(updated)


@router.post("/{deal_id}/win", response_model=DealResponse)
async def mark_deal_won(
    deal_id: str,
    data: DealWin,
    current_user: User = Depends(require_perm("deals:write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Deal).options(selectinload(Deal.stage)).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    updated = await win_deal(db, deal, current_user.id, data.actual_close_date)
    return DealResponse.model_validate(updated)


@router.post("/{deal_id}/lose", response_model=DealResponse)
async def mark_deal_lost(
    deal_id: str,
    data: DealLose,
    current_user: User = Depends(require_perm("deals:write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Deal).options(selectinload(Deal.stage)).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    updated = await lose_deal(db, deal, current_user.id, data.lost_reason)
    return DealResponse.model_validate(updated)
