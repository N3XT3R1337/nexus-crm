import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_deal_stage_transition(client: AsyncClient, admin_headers, sample_deal, sample_stages):
    qualified_stage = sample_stages[1]
    response = await client.post(
        f"/api/v1/deals/{sample_deal.id}/transition",
        headers=admin_headers,
        json={"stage_id": qualified_stage.id},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["stage_id"] == qualified_stage.id
    assert data["probability"] == 25.0


@pytest.mark.asyncio
async def test_deal_win_flow(client: AsyncClient, admin_headers, sample_deal):
    response = await client.post(
        f"/api/v1/deals/{sample_deal.id}/win",
        headers=admin_headers,
        json={},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "won"
    assert data["probability"] == 100.0


@pytest.mark.asyncio
async def test_deal_lose_flow(client: AsyncClient, admin_headers, sample_deal):
    response = await client.post(
        f"/api/v1/deals/{sample_deal.id}/lose",
        headers=admin_headers,
        json={"lost_reason": "Price too high"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "lost"
    assert data["lost_reason"] == "Price too high"


@pytest.mark.asyncio
async def test_invalid_stage_transition(client: AsyncClient, admin_headers, sample_deal):
    response = await client.post(
        f"/api/v1/deals/{sample_deal.id}/transition",
        headers=admin_headers,
        json={"stage_id": "nonexistent-stage"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_stage(client: AsyncClient, admin_headers):
    response = await client.post("/api/v1/deals/stages", headers=admin_headers, json={
        "name": "Custom Stage",
        "order": 10,
        "probability": 60.0,
        "color": "#FF5733",
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Custom Stage"


@pytest.mark.asyncio
async def test_sales_can_transition(client: AsyncClient, sales_headers, sample_deal, sample_stages):
    response = await client.post(
        f"/api/v1/deals/{sample_deal.id}/transition",
        headers=sales_headers,
        json={"stage_id": sample_stages[2].id},
    )
    assert response.status_code == 200
