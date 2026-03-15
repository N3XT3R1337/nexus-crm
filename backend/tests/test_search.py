import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_search_contacts(client: AsyncClient, admin_headers, sample_contact):
    response = await client.get("/api/v1/search?q=John", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert data["query"] == "John"


@pytest.mark.asyncio
async def test_search_companies(client: AsyncClient, admin_headers, sample_company):
    response = await client.get("/api/v1/search?q=Acme", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 0


@pytest.mark.asyncio
async def test_search_with_entity_filter(client: AsyncClient, admin_headers, sample_contact):
    response = await client.get("/api/v1/search?q=John&entity_types=contact", headers=admin_headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_search_empty_query(client: AsyncClient, admin_headers):
    response = await client.get("/api/v1/search?q=xyznonexistent123", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["total"] == 0
