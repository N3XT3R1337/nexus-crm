from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from app.models.user import User
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from app.schemas.user import UserCreate, TokenResponse, UserResponse


async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


async def create_user(db: AsyncSession, user_data: UserCreate, organization_id: str = None):
    hashed = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
        phone=user_data.phone,
        organization_id=organization_id,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


def generate_tokens(user: User) -> TokenResponse:
    role_val = user.role.value if hasattr(user.role, "value") else user.role
    access = create_access_token({"sub": user.id, "email": user.email, "role": role_val})
    refresh = create_refresh_token({"sub": user.id})
    user_resp = UserResponse.model_validate(user)
    return TokenResponse(access_token=access, refresh_token=refresh, user=user_resp)


async def refresh_access_token(db: AsyncSession, refresh_token: str):
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        return None
    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        return None
    return generate_tokens(user)


async def update_last_login(db: AsyncSession, user: User):
    user.last_login = datetime.utcnow()
    await db.flush()
