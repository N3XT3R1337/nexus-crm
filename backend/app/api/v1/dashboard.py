from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
from app.database import get_db
from app.models.user import User
from app.models.deal import Deal, DealStatus
from app.models.contact import Contact
from app.models.activity import Activity
from app.schemas.common import DashboardStats
from app.api.deps import require_perm
from app.services.analytics import get_dashboard_stats
from app.services.deal_pipeline import get_pipeline_summary

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
async def dashboard_stats(
    current_user: User = Depends(require_perm("dashboard:read")),
    db: AsyncSession = Depends(get_db),
):
    return await get_dashboard_stats(db, current_user.organization_id)


@router.get("/pipeline-summary")
async def pipeline_summary(
    current_user: User = Depends(require_perm("dashboard:read")),
    db: AsyncSession = Depends(get_db),
):
    return await get_pipeline_summary(db, current_user.organization_id)


@router.get("/recent-deals")
async def recent_deals(
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(require_perm("deals:read")),
    db: AsyncSession = Depends(get_db),
):
    query = select(Deal).order_by(Deal.created_at.desc()).limit(limit)
    if current_user.organization_id:
        query = query.where(Deal.organization_id == current_user.organization_id)
    result = await db.execute(query)
    deals = result.scalars().all()
    from app.schemas.deal import DealResponse
    return [DealResponse.model_validate(d) for d in deals]


@router.get("/recent-activities")
async def recent_activities(
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(require_perm("activities:read")),
    db: AsyncSession = Depends(get_db),
):
    query = select(Activity).order_by(Activity.created_at.desc()).limit(limit)
    if current_user.organization_id:
        query = query.where(Activity.organization_id == current_user.organization_id)
    result = await db.execute(query)
    activities = result.scalars().all()
    from app.schemas.activity import ActivityResponse
    return [ActivityResponse.model_validate(a) for a in activities]


@router.get("/upcoming-activities")
async def upcoming_activities(
    days: int = Query(7, ge=1, le=30),
    current_user: User = Depends(require_perm("activities:read")),
    db: AsyncSession = Depends(get_db),
):
    now = datetime.utcnow()
    future = now + timedelta(days=days)
    query = select(Activity).where(
        Activity.due_date >= now,
        Activity.due_date <= future,
        Activity.completed == False,
    ).order_by(Activity.due_date.asc())
    if current_user.organization_id:
        query = query.where(Activity.organization_id == current_user.organization_id)
    result = await db.execute(query)
    activities = result.scalars().all()
    from app.schemas.activity import ActivityResponse
    return [ActivityResponse.model_validate(a) for a in activities]


@router.get("/deal-value-by-month")
async def deal_value_by_month(
    months: int = Query(12, ge=1, le=24),
    current_user: User = Depends(require_perm("dashboard:read")),
    db: AsyncSession = Depends(get_db),
):
    data = []
    now = datetime.utcnow()
    for i in range(months - 1, -1, -1):
        target = now - timedelta(days=30 * i)
        month_start = target.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1)

        filters = [Deal.actual_close_date >= month_start, Deal.actual_close_date < month_end, Deal.status == DealStatus.WON]
        if current_user.organization_id:
            filters.append(Deal.organization_id == current_user.organization_id)

        total = await db.scalar(select(func.coalesce(func.sum(Deal.value), 0)).where(*filters)) or 0
        count = await db.scalar(select(func.count(Deal.id)).where(*filters)) or 0

        data.append({
            "month": month_start.strftime("%Y-%m"),
            "revenue": float(total),
            "deals_won": count,
        })

    return data


@router.get("/contacts-by-source")
async def contacts_by_source(
    current_user: User = Depends(require_perm("dashboard:read")),
    db: AsyncSession = Depends(get_db),
):
    query = select(Contact.source, func.count(Contact.id).label("count")).group_by(Contact.source)
    if current_user.organization_id:
        query = query.where(Contact.organization_id == current_user.organization_id)
    result = await db.execute(query)
    return [{"source": row.source, "count": row.count} for row in result.all()]


@router.get("/audit-log")
async def recent_audit_log(
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_perm("audit:read")),
    db: AsyncSession = Depends(get_db),
):
    from app.models.audit_log import AuditLog
    from app.schemas.common import AuditLogResponse
    query = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
    if current_user.organization_id:
        query = query.where(AuditLog.organization_id == current_user.organization_id)
    result = await db.execute(query)
    logs = result.scalars().all()
    return [AuditLogResponse.model_validate(l) for l in logs]
