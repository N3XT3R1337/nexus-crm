import pytest
from httpx import AsyncClient
from app.core.rbac import check_permission, get_role_level
from app.models.user import UserRole


def test_super_admin_has_all_permissions():
    assert check_permission(UserRole.SUPER_ADMIN, "contacts:read")
    assert check_permission(UserRole.SUPER_ADMIN, "contacts:write")
    assert check_permission(UserRole.SUPER_ADMIN, "contacts:delete")
    assert check_permission(UserRole.SUPER_ADMIN, "users:delete")
    assert check_permission(UserRole.SUPER_ADMIN, "settings:write")


def test_viewer_limited_permissions():
    assert check_permission(UserRole.VIEWER, "contacts:read")
    assert not check_permission(UserRole.VIEWER, "contacts:write")
    assert not check_permission(UserRole.VIEWER, "contacts:delete")
    assert not check_permission(UserRole.VIEWER, "users:read")


def test_sales_rep_permissions():
    assert check_permission(UserRole.SALES_REP, "contacts:read")
    assert check_permission(UserRole.SALES_REP, "contacts:write")
    assert not check_permission(UserRole.SALES_REP, "contacts:delete")
    assert check_permission(UserRole.SALES_REP, "deals:write")
    assert not check_permission(UserRole.SALES_REP, "users:read")


def test_manager_permissions():
    assert check_permission(UserRole.MANAGER, "contacts:delete")
    assert check_permission(UserRole.MANAGER, "users:read")
    assert not check_permission(UserRole.MANAGER, "users:write")


def test_admin_permissions():
    assert check_permission(UserRole.ADMIN, "users:write")
    assert check_permission(UserRole.ADMIN, "settings:write")
    assert not check_permission(UserRole.ADMIN, "users:delete")


def test_role_hierarchy():
    assert get_role_level(UserRole.SUPER_ADMIN) > get_role_level(UserRole.ADMIN)
    assert get_role_level(UserRole.ADMIN) > get_role_level(UserRole.MANAGER)
    assert get_role_level(UserRole.MANAGER) > get_role_level(UserRole.SALES_REP)
    assert get_role_level(UserRole.SALES_REP) > get_role_level(UserRole.VIEWER)


@pytest.mark.asyncio
async def test_viewer_cannot_write(client: AsyncClient, viewer_headers):
    response = await client.post("/api/v1/contacts", headers=viewer_headers, json={
        "first_name": "Test",
        "last_name": "Blocked",
    })
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_viewer_cannot_delete(client: AsyncClient, viewer_headers, sample_contact):
    response = await client.delete(f"/api/v1/contacts/{sample_contact.id}", headers=viewer_headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_sales_cannot_manage_users(client: AsyncClient, sales_headers):
    response = await client.get("/api/v1/users", headers=sales_headers)
    assert response.status_code == 403
