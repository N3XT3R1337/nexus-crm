from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime
from app.models.deal import Deal, DealStage, DealStatus
from app.models.notification import Notification, NotificationType
from app.models.audit_log import AuditLog
import json


DEFAULT_STAGES = [
    {"name": "Lead", "order": 1, "probability": 10.0, "color": "#8B5CF6"},
    {"name": "Qualified", "order": 2, "probability": 25.0, "color": "#3B82F6"},
    {"name": "Proposal", "order": 3, "probability": 50.0, "color": "#F59E0B"},
    {"name": "Negotiation", "order": 4, "probability": 75.0, "color": "#F97316"},
    {"name": "Closed Won", "order": 5, "probability": 100.0, "color": "#10B981"},
    {"name": "Closed Lost", "order": 6, "probability": 0.0, "color": "#EF4444"},
]


async def create_default_stages(db: AsyncSession, organization_id: str = None):
    stages = []
    for stage_data in DEFAULT_STAGES:
        stage = DealStage(
            name=stage_data["name"],
            order=stage_data["order"],
            probability=stage_data["probability"],
            color=stage_data["color"],
            organization_id=organization_id,
        )
        db.add(stage)
        stages.append(stage)
    await db.flush()
    for s in stages:
        await db.refresh(s)
    return stages


async def transition_deal_stage(
    db: AsyncSession, deal: Deal, new_stage_id: str, user_id: str
):
    old_stage_id = deal.stage_id
    result = await db.execute(select(DealStage).where(DealStage.id == new_stage_id))
    new_stage = result.scalar_one_or_none()
    if not new_stage:
        return None

    deal.stage_id = new_stage_id
    deal.probability = new_stage.probability
    deal.updated_at = datetime.utcnow()

    if new_stage.name == "Closed Won":
        deal.status = DealStatus.WON
        deal.actual_close_date = datetime.utcnow()
        deal.probability = 100.0
    elif new_stage.name == "Closed Lost":
        deal.status = DealStatus.LOST
        deal.actual_close_date = datetime.utcnow()
        deal.probability = 0.0
    else:
        deal.status = DealStatus.OPEN

    audit = AuditLog(
        action="stage_transition",
        entity_type="deal",
        entity_id=deal.id,
        changes=json.dumps({"old_stage_id": old_stage_id, "new_stage_id": new_stage_id}),
        user_id=user_id,
        organization_id=deal.organization_id,
    )
    db.add(audit)

    if deal.owner_id and deal.owner_id != user_id:
        notification = Notification(
            type=NotificationType.STAGE_CHANGE,
            title=f"Deal '{deal.title}' moved to {new_stage.name}",
            message=f"The deal has been moved to {new_stage.name} stage",
            link=f"/deals/{deal.id}",
            user_id=deal.owner_id,
            organization_id=deal.organization_id,
        )
        db.add(notification)

    await db.flush()
    await db.refresh(deal)
    return deal


async def win_deal(db: AsyncSession, deal: Deal, user_id: str, actual_close_date=None):
    result = await db.execute(
        select(DealStage).where(DealStage.name == "Closed Won").limit(1)
    )
    won_stage = result.scalar_one_or_none()
    deal.status = DealStatus.WON
    deal.actual_close_date = actual_close_date or datetime.utcnow()
    deal.probability = 100.0
    if won_stage:
        deal.stage_id = won_stage.id

    if deal.owner_id:
        notification = Notification(
            type=NotificationType.DEAL_WON,
            title=f"Deal Won: {deal.title}",
            message=f"Congratulations! Deal worth ${deal.value:,.2f} has been won!",
            link=f"/deals/{deal.id}",
            user_id=deal.owner_id,
            organization_id=deal.organization_id,
        )
        db.add(notification)

    audit = AuditLog(
        action="deal_won",
        entity_type="deal",
        entity_id=deal.id,
        changes=json.dumps({"value": deal.value}),
        user_id=user_id,
        organization_id=deal.organization_id,
    )
    db.add(audit)
    await db.flush()
    await db.refresh(deal)
    return deal


async def lose_deal(db: AsyncSession, deal: Deal, user_id: str, lost_reason: str):
    result = await db.execute(
        select(DealStage).where(DealStage.name == "Closed Lost").limit(1)
    )
    lost_stage = result.scalar_one_or_none()
    deal.status = DealStatus.LOST
    deal.actual_close_date = datetime.utcnow()
    deal.probability = 0.0
    deal.lost_reason = lost_reason
    if lost_stage:
        deal.stage_id = lost_stage.id

    if deal.owner_id:
        notification = Notification(
            type=NotificationType.DEAL_LOST,
            title=f"Deal Lost: {deal.title}",
            message=f"Deal worth ${deal.value:,.2f} has been lost. Reason: {lost_reason}",
            link=f"/deals/{deal.id}",
            user_id=deal.owner_id,
            organization_id=deal.organization_id,
        )
        db.add(notification)

    audit = AuditLog(
        action="deal_lost",
        entity_type="deal",
        entity_id=deal.id,
        changes=json.dumps({"lost_reason": lost_reason}),
        user_id=user_id,
        organization_id=deal.organization_id,
    )
    db.add(audit)
    await db.flush()
    await db.refresh(deal)
    return deal


async def get_pipeline_summary(db: AsyncSession, organization_id: str = None):
    query = select(
        DealStage.id,
        DealStage.name,
        DealStage.order,
        DealStage.color,
        DealStage.probability,
        func.count(Deal.id).label("deal_count"),
        func.coalesce(func.sum(Deal.value), 0).label("total_value"),
    ).outerjoin(Deal, (Deal.stage_id == DealStage.id) & (Deal.status == DealStatus.OPEN))

    if organization_id:
        query = query.where(DealStage.organization_id == organization_id)

    query = query.group_by(DealStage.id).order_by(DealStage.order)
    result = await db.execute(query)
    rows = result.all()

    return [
        {
            "id": row.id,
            "name": row.name,
            "order": row.order,
            "color": row.color,
            "probability": row.probability,
            "deal_count": row.deal_count,
            "total_value": float(row.total_value),
        }
        for row in rows
    ]
