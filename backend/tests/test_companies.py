import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_companies(client: AsyncClient, admin_headers, sample_company):
    response = await client.get("/api/v1/companies", headers=admin_headers)
    assert response.status_code == 200
    assert "items" in response.json()


@pytest.mark.asyncio
async def test_create_company(client: AsyncClient, admin_headers):
    response = await client.post("/api/v1/companies", headers=admin_headers, json={
        "name": "New Corp",
        "domain": "newcorp.com",
        "industry": "Technology",
        "size": "51-200",
    })
    assert response.status_code == 201
    assert response.json()["name"] == "New Corp"


@pytest.mark.asyncio
async def test_get_company(client: AsyncClient, admin_headers, sample_company):
    response = await client.get(f"/api/v1/companies/{sample_company.id}", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Acme Corp"


@pytest.mark.asyncio
async def test_update_company(client: AsyncClient, admin_headers, sample_company):
    response = await client.put(f"/api/v1/companies/{sample_company.id}", headers=admin_headers, json={
        "name": "Acme Corp Updated",
        "employee_count": 500,
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Acme Corp Updated"


@pytest.mark.asyncio
async def test_delete_company(client: AsyncClient, admin_headers, sample_company):
    response = await client.delete(f"/api/v1/companies/{sample_company.id}", headers=admin_headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_viewer_cannot_delete_company(client: AsyncClient, viewer_headers, sample_company):
    response = await client.delete(f"/api/v1/companies/{sample_company.id}", headers=viewer_headers)
    assert response.status_code == 403
