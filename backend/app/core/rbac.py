from functools import wraps
from fastapi import HTTPException, status
from app.models.user import UserRole

ROLE_HIERARCHY = {
    UserRole.SUPER_ADMIN: 5,
    UserRole.ADMIN: 4,
    UserRole.MANAGER: 3,
    UserRole.SALES_REP: 2,
    UserRole.VIEWER: 1,
}

PERMISSIONS = {
    "contacts:read": [UserRole.VIEWER, UserRole.SALES_REP, UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "contacts:write": [UserRole.SALES_REP, UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "contacts:delete": [UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "contacts:bulk_delete": [UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "companies:read": [UserRole.VIEWER, UserRole.SALES_REP, UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "companies:write": [UserRole.SALES_REP, UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "companies:delete": [UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "deals:read": [UserRole.VIEWER, UserRole.SALES_REP, UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "deals:write": [UserRole.SALES_REP, UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "deals:delete": [UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "deals:change_stage": [UserRole.SALES_REP, UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "activities:read": [UserRole.VIEWER, UserRole.SALES_REP, UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "activities:write": [UserRole.SALES_REP, UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "activities:delete": [UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "notes:read": [UserRole.VIEWER, UserRole.SALES_REP, UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "notes:write": [UserRole.SALES_REP, UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "notes:delete": [UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "reports:read": [UserRole.VIEWER, UserRole.SALES_REP, UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "reports:write": [UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "reports:delete": [UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "users:read": [UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "users:write": [UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "users:delete": [UserRole.SUPER_ADMIN],
    "settings:read": [UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "settings:write": [UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "webhooks:read": [UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "webhooks:write": [UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "api_keys:read": [UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "api_keys:write": [UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "audit:read": [UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "email_templates:read": [UserRole.SALES_REP, UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "email_templates:write": [UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "tags:read": [UserRole.VIEWER, UserRole.SALES_REP, UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "tags:write": [UserRole.SALES_REP, UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "tags:delete": [UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
    "dashboard:read": [UserRole.VIEWER, UserRole.SALES_REP, UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN],
}


def check_permission(user_role: str, permission: str) -> bool:
    allowed_roles = PERMISSIONS.get(permission, [])
    return UserRole(user_role) in allowed_roles


def require_permission(permission: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")
            if current_user is None:
                for arg in args:
                    if hasattr(arg, "role"):
                        current_user = arg
                        break
            if current_user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
            if not check_permission(current_user.role, permission):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def get_role_level(role: str) -> int:
    return ROLE_HIERARCHY.get(UserRole(role), 0)
