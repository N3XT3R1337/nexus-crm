from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, extract
from datetime import datetime, timedelta
from app.models.deal import Deal, DealStage, DealStatus
from app.models.contact import Contact
from app.models.company import Company
from app.models.activity import Activity


async def get_dashboard_stats(db: AsyncSession, organization_id: str = None):
    filters = []
    if organization_id:
        filters.append(Contact.organization_id == organization_id)

    total_contacts = await db.scalar(select(func.count(Contact.id)).where(*filters)) or 0

    company_filters = []
    if organization_id:
        company_filters.append(Company.organization_id == organization_id)
    total_companies = await db.scalar(select(func.count(Company.id)).where(*company_filters)) or 0

    deal_filters = []
    if organization_id:
        deal_filters.append(Deal.organization_id == organization_id)

    total_deals = await db.scalar(select(func.count(Deal.id)).where(*deal_filters)) or 0
    won_deals = await db.scalar(
        select(func.count(Deal.id)).where(Deal.status == DealStatus.WON, *deal_filters)
    ) or 0
    lost_deals = await db.scalar(
        select(func.count(Deal.id)).where(Deal.status == DealStatus.LOST, *deal_filters)
    ) or 0
    open_deals = await db.scalar(
        select(func.count(Deal.id)).where(Deal.status == DealStatus.OPEN, *deal_filters)
    ) or 0
    total_revenue = await db.scalar(
        select(func.coalesce(func.sum(Deal.value), 0)).where(Deal.status == DealStatus.WON, *deal_filters)
    ) or 0
    pipeline_value = await db.scalar(
        select(func.coalesce(func.sum(Deal.value), 0)).where(Deal.status == DealStatus.OPEN, *deal_filters)
    ) or 0

    closed_deals = won_deals + lost_deals
    conversion_rate = (won_deals / closed_deals * 100) if closed_deals > 0 else 0
    avg_deal_value = (total_revenue / won_deals) if won_deals > 0 else 0

    week_ago = datetime.utcnow() - timedelta(days=7)
    activity_filters = [Activity.created_at >= week_ago]
    if organization_id:
        activity_filters.append(Activity.organization_id == organization_id)
    activities_this_week = await db.scalar(
        select(func.count(Activity.id)).where(*activity_filters)
    ) or 0

    month_ago = datetime.utcnow() - timedelta(days=30)
    contact_month_filters = [Contact.created_at >= month_ago]
    if organization_id:
        contact_month_filters.append(Contact.organization_id == organization_id)
    new_contacts_this_month = await db.scalar(
        select(func.count(Contact.id)).where(*contact_month_filters)
    ) or 0

    return {
        "total_contacts": total_contacts,
        "total_companies": total_companies,
        "total_deals": total_deals,
        "total_revenue": float(total_revenue),
        "won_deals": won_deals,
        "lost_deals": lost_deals,
        "open_deals": open_deals,
        "conversion_rate": round(conversion_rate, 2),
        "avg_deal_value": round(float(avg_deal_value), 2),
        "pipeline_value": float(pipeline_value),
        "activities_this_week": activities_this_week,
        "new_contacts_this_month": new_contacts_this_month,
    }


async def get_revenue_forecast(db: AsyncSession, months: int = 6, organization_id: str = None):
    forecasts = []
    now = datetime.utcnow()

    for i in range(months):
        target_month = now + timedelta(days=30 * i)
        month_start = target_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1)

        filters = [Deal.expected_close_date >= month_start, Deal.expected_close_date < month_end]
        if organization_id:
            filters.append(Deal.organization_id == organization_id)

        predicted = await db.scalar(
            select(func.coalesce(func.sum(Deal.value), 0)).where(
                Deal.status == DealStatus.OPEN, *filters
            )
        ) or 0

        weighted = await db.scalar(
            select(func.coalesce(func.sum(Deal.value * Deal.probability / 100), 0)).where(
                Deal.status == DealStatus.OPEN, *filters
            )
        ) or 0

        actual_filters = [Deal.actual_close_date >= month_start, Deal.actual_close_date < month_end]
        if organization_id:
            actual_filters.append(Deal.organization_id == organization_id)
        actual = await db.scalar(
            select(func.coalesce(func.sum(Deal.value), 0)).where(
                Deal.status == DealStatus.WON, *actual_filters
            )
        ) or 0

        forecasts.append({
            "month": month_start.strftime("%Y-%m"),
            "predicted": float(predicted),
            "actual": float(actual),
            "weighted": float(weighted),
        })

    return forecasts


async def get_pipeline_velocity(db: AsyncSession, organization_id: str = None):
    stages_query = select(DealStage).order_by(DealStage.order)
    if organization_id:
        stages_query = stages_query.where(DealStage.organization_id == organization_id)
    result = await db.execute(stages_query)
    stages = result.scalars().all()

    velocities = []
    for stage in stages:
        filters = [Deal.stage_id == stage.id]
        if organization_id:
            filters.append(Deal.organization_id == organization_id)

        deal_count = await db.scalar(
            select(func.count(Deal.id)).where(*filters)
        ) or 0

        won_from_stage = await db.scalar(
            select(func.count(Deal.id)).where(Deal.status == DealStatus.WON, *filters)
        ) or 0

        total_from_stage = deal_count + won_from_stage
        stage_conversion = (won_from_stage / total_from_stage * 100) if total_from_stage > 0 else 0

        velocities.append({
            "stage_name": stage.name,
            "avg_days": round(stage.probability / 10, 1),
            "deal_count": deal_count,
            "conversion_rate": round(stage_conversion, 2),
        })

    return velocities


async def get_sales_by_owner(db: AsyncSession, organization_id: str = None):
    from app.models.user import User
    query = select(
        User.id,
        User.first_name,
        User.last_name,
        func.count(Deal.id).label("total_deals"),
        func.coalesce(func.sum(Deal.value), 0).label("total_value"),
        func.count(Deal.id).filter(Deal.status == DealStatus.WON).label("won_deals"),
    ).outerjoin(Deal, Deal.owner_id == User.id)

    if organization_id:
        query = query.where(User.organization_id == organization_id)

    query = query.group_by(User.id, User.first_name, User.last_name)
    result = await db.execute(query)
    rows = result.all()

    return [
        {
            "user_id": row.id,
            "name": f"{row.first_name} {row.last_name}",
            "total_deals": row.total_deals,
            "total_value": float(row.total_value),
            "won_deals": row.won_deals,
        }
        for row in rows
    ]
