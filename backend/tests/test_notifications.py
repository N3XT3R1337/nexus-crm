import pytest
from httpx import AsyncClient
from app.services.notification import create_notification
from app.models.notification import NotificationType


@pytest.mark.asyncio
async def test_list_notifications(client: AsyncClient, admin_headers, db_session, admin_user):
    await create_notification(
        db_session, admin_user.id, NotificationType.SYSTEM,
        "Test notification", "Test message",
    )
    response = await client.get("/api/v1/notifications", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "unread_count" in data


@pytest.mark.asyncio
async def test_mark_notification_read(client: AsyncClient, admin_headers, db_session, admin_user):
    notification = await create_notification(
        db_session, admin_user.id, NotificationType.DEAL_WON,
        "Deal Won!", "Congrats",
    )
    response = await client.put(f"/api/v1/notifications/{notification.id}/read", headers=admin_headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_mark_all_read(client: AsyncClient, admin_headers, db_session, admin_user):
    await create_notification(db_session, admin_user.id, NotificationType.SYSTEM, "N1")
    await create_notification(db_session, admin_user.id, NotificationType.SYSTEM, "N2")
    response = await client.put("/api/v1/notifications/read-all", headers=admin_headers)
    assert response.status_code == 200
