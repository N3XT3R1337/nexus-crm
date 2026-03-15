import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_tag(client: AsyncClient, admin_headers):
    response = await client.post("/api/v1/tags", headers=admin_headers, json={
        "name": "Enterprise",
        "color": "#8B5CF6",
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Enterprise"


@pytest.mark.asyncio
async def test_list_tags(client: AsyncClient, admin_headers, sample_tag):
    response = await client.get("/api/v1/tags", headers=admin_headers)
    assert response.status_code == 200
    assert "items" in response.json()


@pytest.mark.asyncio
async def test_duplicate_tag(client: AsyncClient, admin_headers, sample_tag):
    response = await client.post("/api/v1/tags", headers=admin_headers, json={
        "name": "VIP",
        "color": "#EF4444",
    })
    assert response.status_code == 400
