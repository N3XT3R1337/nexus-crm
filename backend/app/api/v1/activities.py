from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime
from app.database import get_db
from app.models.activity import Activity
from app.models.user import User
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityResponse, ActivityListResponse
from app.api.deps import get_current_user, require_perm

router = APIRouter(prefix="/activities", tags=["Activities"])


@router.get("", response_model=ActivityListResponse)
async def list_activities(
    page: int = Query(1, ge=1),
    per_page: int = Query(25, ge=1, le=100),
    type_filter: str = Query(None, alias="type"),
    completed: bool = Query(None),
    contact_id: str = Query(None),
    deal_id: str = Query(None),
    user_id: str = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    current_user: User = Depends(require_perm("activities:read")),
    db: AsyncSession = Depends(get_db),
):
    query = select(Activity)
    count_query = select(func.count(Activity.id))

    if current_user.organization_id:
        query = query.where(Activity.organization_id == current_user.organization_id)
        count_query = count_query.where(Activity.organization_id == current_user.organization_id)

    if type_filter:
        query = query.where(Activity.type == type_filter)
        count_query = count_query.where(Activity.type == type_filter)

    if completed is not None:
        query = query.where(Activity.completed == completed)
        count_query = count_query.where(Activity.completed == completed)

    if contact_id:
        query = query.where(Activity.contact_id == contact_id)
        count_query = count_query.where(Activity.contact_id == contact_id)

    if deal_id:
        query = query.where(Activity.deal_id == deal_id)
        count_query = count_query.where(Activity.deal_id == deal_id)

    if user_id:
        query = query.where(Activity.user_id == user_id)
        count_query = count_query.where(Activity.user_id == user_id)

    total = await db.scalar(count_query) or 0
    sort_col = getattr(Activity, sort_by, Activity.created_at)
    if sort_order == "asc":
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())

    offset = (page - 1) * per_page
    result = await db.execute(query.offset(offset).limit(per_page))
    activities = result.scalars().all()

    return ActivityListResponse(
        items=[ActivityResponse.model_validate(a) for a in activities],
        total=total, page=page, per_page=per_page,
        pages=(total + per_page - 1) // per_page if per_page else 0,
    )


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(
    activity_id: str,
    current_user: User = Depends(require_perm("activities:read")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalar_one_or_none()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return ActivityResponse.model_validate(activity)


@router.post("", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_activity(
    data: ActivityCreate,
    current_user: User = Depends(require_perm("activities:write")),
    db: AsyncSession = Depends(get_db),
):
    activity = Activity(
        **data.model_dump(),
        user_id=current_user.id,
        organization_id=current_user.organization_id,
    )
    db.add(activity)
    await db.flush()
    await db.refresh(activity)
    return ActivityResponse.model_validate(activity)


@router.put("/{activity_id}", response_model=ActivityResponse)
async def update_activity(
    activity_id: str,
    data: ActivityUpdate,
    current_user: User = Depends(require_perm("activities:write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalar_one_or_none()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    update_data = data.model_dump(exclude_unset=True)
    if "completed" in update_data and update_data["completed"] and not activity.completed:
        activity.completed_at = datetime.utcnow()
    for key, value in update_data.items():
        setattr(activity, key, value)

    await db.flush()
    await db.refresh(activity)
    return ActivityResponse.model_validate(activity)


@router.delete("/{activity_id}")
async def delete_activity(
    activity_id: str,
    current_user: User = Depends(require_perm("activities:delete")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalar_one_or_none()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    await db.delete(activity)
    await db.flush()
    return {"message": "Activity deleted", "success": True}


@router.post("/{activity_id}/complete", response_model=ActivityResponse)
async def complete_activity(
    activity_id: str,
    current_user: User = Depends(require_perm("activities:write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalar_one_or_none()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity.completed = True
    activity.completed_at = datetime.utcnow()
    await db.flush()
    await db.refresh(activity)
    return ActivityResponse.model_validate(activity)
