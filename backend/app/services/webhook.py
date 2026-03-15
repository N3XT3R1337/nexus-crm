from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.webhook import Webhook
from datetime import datetime
import json
import hashlib
import hmac


async def get_active_webhooks(db: AsyncSession, event: str, organization_id: str = None):
    query = select(Webhook).where(Webhook.is_active == True)
    if organization_id:
        query = query.where(Webhook.organization_id == organization_id)
    result = await db.execute(query)
    webhooks = result.scalars().all()
    return [w for w in webhooks if event in json.loads(w.events)]


def generate_webhook_signature(payload: str, secret: str) -> str:
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()


async def record_webhook_trigger(db: AsyncSession, webhook_id: str, success: bool):
    result = await db.execute(select(Webhook).where(Webhook.id == webhook_id))
    webhook = result.scalar_one_or_none()
    if webhook:
        webhook.last_triggered_at = datetime.utcnow()
        if not success:
            webhook.failure_count += 1
        else:
            webhook.failure_count = 0
        await db.flush()
