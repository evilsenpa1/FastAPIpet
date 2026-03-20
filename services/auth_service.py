# auth/service.py
import bcrypt
from fastapi import HTTPException, status
from models.auth_model import UserModel
from repository.user_repo import UserRepository
from core import auth_security
from jose import JWTError, jwt
from models.auth_model import UserModel, UserRole
from schemas.auth_schema import RegisterRequest


def hash_password(password: str) -> str:
    # bcrypt — синхронный по природе, async здесь не нужен
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, data: RegisterRequest) -> UserModel:
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "Email already registered",
            )
        user_data = data.model_dump()
        user_data["hashed_password"] = hash_password(user_data.pop("password"))
        return await self.repo.create(user_data)

    async def authenticate_user(self, email: str, password: str) -> UserModel:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Invalid credentials",
            )
        if not user.is_active:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Account is disabled",
            )
        return user

    async def get_user_by_id(self, user_id: int) -> UserModel:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        return user

    async def all_users(self) -> UserModel:
        query = await self.repo.get_all_users()
        return query

    async def is_staff(self, user_id: int) -> bool:
        STAFF_ROLES = {UserRole.MODERATOR, UserRole.ADMIN}

        user = await self.get_user_by_id(user_id)

        return user.role in STAFF_ROLES
