from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.webhook import Webhook
from app.models.user import User
from app.schemas.common import WebhookCreate, WebhookUpdate, WebhookResponse
from app.api.deps import require_perm

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.get("")
async def list_webhooks(
    current_user: User = Depends(require_perm("webhooks:read")),
    db: AsyncSession = Depends(get_db),
):
    query = select(Webhook)
    if current_user.organization_id:
        query = query.where(Webhook.organization_id == current_user.organization_id)
    result = await db.execute(query.order_by(Webhook.created_at.desc()))
    webhooks = result.scalars().all()
    return [WebhookResponse.model_validate(w) for w in webhooks]


@router.get("/{webhook_id}", response_model=WebhookResponse)
async def get_webhook(
    webhook_id: str,
    current_user: User = Depends(require_perm("webhooks:read")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Webhook).where(Webhook.id == webhook_id))
    webhook = result.scalar_one_or_none()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return WebhookResponse.model_validate(webhook)


@router.post("", response_model=WebhookResponse, status_code=status.HTTP_201_CREATED)
async def create_webhook(
    data: WebhookCreate,
    current_user: User = Depends(require_perm("webhooks:write")),
    db: AsyncSession = Depends(get_db),
):
    webhook = Webhook(**data.model_dump(), organization_id=current_user.organization_id)
    db.add(webhook)
    await db.flush()
    await db.refresh(webhook)
    return WebhookResponse.model_validate(webhook)


@router.put("/{webhook_id}", response_model=WebhookResponse)
async def update_webhook(
    webhook_id: str,
    data: WebhookUpdate,
    current_user: User = Depends(require_perm("webhooks:write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Webhook).where(Webhook.id == webhook_id))
    webhook = result.scalar_one_or_none()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(webhook, key, value)
    await db.flush()
    await db.refresh(webhook)
    return WebhookResponse.model_validate(webhook)


@router.delete("/{webhook_id}")
async def delete_webhook(
    webhook_id: str,
    current_user: User = Depends(require_perm("webhooks:write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Webhook).where(Webhook.id == webhook_id))
    webhook = result.scalar_one_or_none()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    await db.delete(webhook)
    await db.flush()
    return {"message": "Webhook deleted", "success": True}
