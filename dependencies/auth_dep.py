# auth/dependencies.py
from fastapi import Depends, HTTPException, status
from db.session import SessionDep
from repository.user_repo import UserRepository
from services.auth_service import AuthService
from services.user_service import UserService
from schemas.user_schema import UserPatchSchema
from core.auth_security import security


def get_user_repo(db: SessionDep) -> UserRepository:
    return UserRepository(db)


def get_auth_service(
    repo: UserRepository = Depends(get_user_repo),
) -> AuthService:
    return AuthService(repo)


def get_user_service(
    repo: UserRepository = Depends(get_user_repo),
) -> UserService:
    return UserService(repo)


def get_current_user_id(payload=Depends(security.access_token_required)) -> int:
    return int(payload.sub)


async def require_staff(
    user_id: int = Depends(get_current_user_id),
    auth_service: AuthService = Depends(get_auth_service),
) -> int:
    if not await auth_service.is_staff(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return user_id
