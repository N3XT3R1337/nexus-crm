import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_contacts(client: AsyncClient, admin_headers, sample_contact):
    response = await client.get("/api/v1/contacts", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_create_contact(client: AsyncClient, admin_headers, sample_company):
    response = await client.post("/api/v1/contacts", headers=admin_headers, json={
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com",
        "phone": "+1987654321",
        "status": "lead",
        "source": "website",
        "company_id": sample_company.id,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Jane"
    assert data["last_name"] == "Smith"


@pytest.mark.asyncio
async def test_get_contact(client: AsyncClient, admin_headers, sample_contact):
    response = await client.get(f"/api/v1/contacts/{sample_contact.id}", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"


@pytest.mark.asyncio
async def test_update_contact(client: AsyncClient, admin_headers, sample_contact):
    response = await client.put(f"/api/v1/contacts/{sample_contact.id}", headers=admin_headers, json={
        "first_name": "Jonathan",
        "job_title": "CEO",
    })
    assert response.status_code == 200
    assert response.json()["first_name"] == "Jonathan"


@pytest.mark.asyncio
async def test_delete_contact(client: AsyncClient, admin_headers, sample_contact):
    response = await client.delete(f"/api/v1/contacts/{sample_contact.id}", headers=admin_headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_contact_not_found(client: AsyncClient, admin_headers):
    response = await client.get("/api/v1/contacts/nonexistent-id", headers=admin_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_viewer_cannot_create_contact(client: AsyncClient, viewer_headers):
    response = await client.post("/api/v1/contacts", headers=viewer_headers, json={
        "first_name": "Test",
        "last_name": "Viewer",
    })
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_filter_contacts_by_status(client: AsyncClient, admin_headers, sample_contact):
    response = await client.get("/api/v1/contacts?status=lead", headers=admin_headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_search_contacts(client: AsyncClient, admin_headers, sample_contact):
    response = await client.get("/api/v1/contacts?search=John", headers=admin_headers)
    assert response.status_code == 200
