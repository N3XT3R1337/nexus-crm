import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_deals(client: AsyncClient, admin_headers, sample_deal):
    response = await client.get("/api/v1/deals", headers=admin_headers)
    assert response.status_code == 200
    assert "items" in response.json()


@pytest.mark.asyncio
async def test_create_deal(client: AsyncClient, admin_headers, sample_stages, sample_contact):
    response = await client.post("/api/v1/deals", headers=admin_headers, json={
        "title": "New Deal",
        "value": 25000,
        "stage_id": sample_stages[0].id,
        "contact_id": sample_contact.id,
    })
    assert response.status_code == 201
    assert response.json()["title"] == "New Deal"


@pytest.mark.asyncio
async def test_get_deal(client: AsyncClient, admin_headers, sample_deal):
    response = await client.get(f"/api/v1/deals/{sample_deal.id}", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Big Enterprise Deal"


@pytest.mark.asyncio
async def test_update_deal(client: AsyncClient, admin_headers, sample_deal):
    response = await client.put(f"/api/v1/deals/{sample_deal.id}", headers=admin_headers, json={
        "value": 75000,
        "priority": "critical",
    })
    assert response.status_code == 200
    assert response.json()["value"] == 75000


@pytest.mark.asyncio
async def test_stage_transition(client: AsyncClient, admin_headers, sample_deal, sample_stages):
    response = await client.post(f"/api/v1/deals/{sample_deal.id}/transition", headers=admin_headers, json={
        "stage_id": sample_stages[1].id,
    })
    assert response.status_code == 200
    assert response.json()["stage_id"] == sample_stages[1].id


@pytest.mark.asyncio
async def test_win_deal(client: AsyncClient, admin_headers, sample_deal):
    response = await client.post(f"/api/v1/deals/{sample_deal.id}/win", headers=admin_headers, json={})
    assert response.status_code == 200
    assert response.json()["status"] == "won"


@pytest.mark.asyncio
async def test_lose_deal(client: AsyncClient, admin_headers, sample_deal):
    response = await client.post(f"/api/v1/deals/{sample_deal.id}/lose", headers=admin_headers, json={
        "lost_reason": "Budget constraints",
    })
    assert response.status_code == 200
    assert response.json()["status"] == "lost"


@pytest.mark.asyncio
async def test_list_stages(client: AsyncClient, admin_headers, sample_stages):
    response = await client.get("/api/v1/deals/stages", headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 6


@pytest.mark.asyncio
async def test_pipeline(client: AsyncClient, admin_headers, sample_deal):
    response = await client.get("/api/v1/deals/pipeline", headers=admin_headers)
    assert response.status_code == 200
