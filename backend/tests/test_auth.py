import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    response = await client.post("/api/v1/auth/register", json={
        "email": "newuser@test.io",
        "password": "securepass123",
        "first_name": "New",
        "last_name": "User",
    })
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == "newuser@test.io"


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, admin_user):
    response = await client.post("/api/v1/auth/register", json={
        "email": "admin@test.io",
        "password": "securepass123",
        "first_name": "Dup",
        "last_name": "User",
    })
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, admin_user):
    response = await client.post("/api/v1/auth/login", json={
        "email": "admin@test.io",
        "password": "admin123",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["role"] == "super_admin"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, admin_user):
    response = await client.post("/api/v1/auth/login", json={
        "email": "admin@test.io",
        "password": "wrongpassword",
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, admin_headers):
    response = await client.get("/api/v1/auth/me", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "admin@test.io"


@pytest.mark.asyncio
async def test_update_me(client: AsyncClient, admin_headers):
    response = await client.put("/api/v1/auth/me", headers=admin_headers, json={
        "first_name": "Updated",
    })
    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated"


@pytest.mark.asyncio
async def test_change_password(client: AsyncClient, admin_headers):
    response = await client.post("/api/v1/auth/change-password", headers=admin_headers, json={
        "current_password": "admin123",
        "new_password": "newadmin123",
    })
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_change_password_wrong_current(client: AsyncClient, admin_headers):
    response = await client.post("/api/v1/auth/change-password", headers=admin_headers, json={
        "current_password": "wrongpass",
        "new_password": "newpass123",
    })
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient, admin_user):
    login_response = await client.post("/api/v1/auth/login", json={
        "email": "admin@test.io",
        "password": "admin123",
    })
    refresh_token = login_response.json()["refresh_token"]
    response = await client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token,
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_invalid_token(client: AsyncClient):
    response = await client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401
