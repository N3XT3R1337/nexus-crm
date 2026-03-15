import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_activity(client: AsyncClient, admin_headers, sample_contact):
    response = await client.post("/api/v1/activities", headers=admin_headers, json={
        "type": "call",
        "subject": "Follow-up call",
        "contact_id": sample_contact.id,
    })
    assert response.status_code == 201
    assert response.json()["subject"] == "Follow-up call"


@pytest.mark.asyncio
async def test_list_activities(client: AsyncClient, admin_headers):
    response = await client.get("/api/v1/activities", headers=admin_headers)
    assert response.status_code == 200
    assert "items" in response.json()


@pytest.mark.asyncio
async def test_complete_activity(client: AsyncClient, admin_headers, sample_contact):
    create_response = await client.post("/api/v1/activities", headers=admin_headers, json={
        "type": "task",
        "subject": "Send proposal",
        "contact_id": sample_contact.id,
    })
    activity_id = create_response.json()["id"]
    response = await client.post(f"/api/v1/activities/{activity_id}/complete", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["completed"] is True
