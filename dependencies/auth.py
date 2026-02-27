# auth/dependencies.py
from fastapi import Depends
from db.session import SessionDep 
from repository.auth import UserRepository
from services.auth_service import AuthService


def get_user_repo(db: SessionDep) -> UserRepository:
    return UserRepository(db)


def get_auth_service(
    repo: UserRepository = Depends(get_user_repo),
) -> AuthService:
    return AuthService(repo)