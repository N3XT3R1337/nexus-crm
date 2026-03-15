from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.report import Report
from app.models.user import User
from app.schemas.common import ReportCreate, ReportResponse
from app.api.deps import require_perm
from app.services.analytics import get_revenue_forecast, get_pipeline_velocity, get_sales_by_owner
import json

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("")
async def list_reports(
    page: int = Query(1, ge=1),
    per_page: int = Query(25, ge=1, le=100),
    report_type: str = Query(None, alias="type"),
    current_user: User = Depends(require_perm("reports:read")),
    db: AsyncSession = Depends(get_db),
):
    query = select(Report)
    count_query = select(func.count(Report.id))

    if current_user.organization_id:
        query = query.where(Report.organization_id == current_user.organization_id)
        count_query = count_query.where(Report.organization_id == current_user.organization_id)

    if report_type:
        query = query.where(Report.type == report_type)
        count_query = count_query.where(Report.type == report_type)

    total = await db.scalar(count_query) or 0
    offset = (page - 1) * per_page
    result = await db.execute(query.order_by(Report.created_at.desc()).offset(offset).limit(per_page))
    reports = result.scalars().all()

    return {
        "items": [ReportResponse.model_validate(r) for r in reports],
        "total": total, "page": page, "per_page": per_page,
    }


@router.get("/revenue-forecast")
async def revenue_forecast(
    months: int = Query(6, ge=1, le=24),
    current_user: User = Depends(require_perm("reports:read")),
    db: AsyncSession = Depends(get_db),
):
    return await get_revenue_forecast(db, months, current_user.organization_id)


@router.get("/pipeline-velocity")
async def pipeline_velocity(
    current_user: User = Depends(require_perm("reports:read")),
    db: AsyncSession = Depends(get_db),
):
    return await get_pipeline_velocity(db, current_user.organization_id)


@router.get("/sales-by-owner")
async def sales_by_owner(
    current_user: User = Depends(require_perm("reports:read")),
    db: AsyncSession = Depends(get_db),
):
    return await get_sales_by_owner(db, current_user.organization_id)


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: str,
    current_user: User = Depends(require_perm("reports:read")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return ReportResponse.model_validate(report)


@router.post("", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    data: ReportCreate,
    current_user: User = Depends(require_perm("reports:write")),
    db: AsyncSession = Depends(get_db),
):
    report = Report(
        **data.model_dump(),
        user_id=current_user.id,
        organization_id=current_user.organization_id,
    )
    db.add(report)
    await db.flush()
    await db.refresh(report)
    return ReportResponse.model_validate(report)


@router.delete("/{report_id}")
async def delete_report(
    report_id: str,
    current_user: User = Depends(require_perm("reports:delete")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    await db.delete(report)
    await db.flush()
    return {"message": "Report deleted", "success": True}
