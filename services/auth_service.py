# auth/service.py
import bcrypt
from fastapi import HTTPException, status
from models.auth import User
from repository.auth import UserRepository


def hash_password(password: str) -> str:
    # bcrypt — синхронный по природе, async здесь не нужен
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(
        self,
        email: str,
        username: str,
        password: str,
    ) -> User:
        existing = await self.repo.get_by_email(email)
        if existing:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "Email already registered",
            )
        return await self.repo.create(
            email=email,
            username=username,
            hashed_password=hash_password(password),
        )

    async def authenticate_user(self, email: str, password: str) -> User:
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

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        return user