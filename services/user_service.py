# auth/service.py
from fastapi import HTTPException, status
from models.auth_model import UserModel
from repository.user_repo import UserRepository
from schemas.user_schema import UserSelfPatchSchema


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_user_by_id(self, user_id: int) -> UserModel:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        return user

    async def all_users(self) -> list[UserModel]:
        return await self.repo.get_all()

    async def patch_user(self, schema: UserSelfPatchSchema, user_id: int):
        user = await self.repo.patch(user_id, schema)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        return user

    async def delete_user(self, user_id: int):
        return await self.repo.delete(user_id)
