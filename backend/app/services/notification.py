from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from app.models.notification import Notification


async def get_user_notifications(db: AsyncSession, user_id: str, page: int = 1, per_page: int = 20):
    offset = (page - 1) * per_page
    query = select(Notification).where(Notification.user_id == user_id).order_by(Notification.created_at.desc())
    total = await db.scalar(select(func.count(Notification.id)).where(Notification.user_id == user_id)) or 0
    unread = await db.scalar(
        select(func.count(Notification.id)).where(Notification.user_id == user_id, Notification.read == False)
    ) or 0
    result = await db.execute(query.offset(offset).limit(per_page))
    items = result.scalars().all()
    return items, total, unread


async def mark_notification_read(db: AsyncSession, notification_id: str, user_id: str):
    result = await db.execute(
        select(Notification).where(Notification.id == notification_id, Notification.user_id == user_id)
    )
    notification = result.scalar_one_or_none()
    if notification:
        notification.read = True
        await db.flush()
    return notification


async def mark_all_read(db: AsyncSession, user_id: str):
    await db.execute(
        update(Notification).where(Notification.user_id == user_id, Notification.read == False).values(read=True)
    )
    await db.flush()


async def create_notification(db: AsyncSession, user_id: str, type_: str, title: str, message: str = None, link: str = None, organization_id: str = None):
    notification = Notification(
        type=type_,
        title=title,
        message=message,
        link=link,
        user_id=user_id,
        organization_id=organization_id,
    )
    db.add(notification)
    await db.flush()
    await db.refresh(notification)
    return notification
