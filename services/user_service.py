# auth/service.py
from fastapi import HTTPException, status
from models.auth import UserModel
from repository.user import UserRepository
from schemas.user_schema import UserPatchSchema



class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo


    async def get_user_by_id(self, user_id: int) -> UserModel:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        return user

    async def all_users(self) -> UserModel:
        query = await self.repo.get_all_users()
        return query
    
    async def patch_user(self, schema: UserPatchSchema, user_id: int):
        user = await self.repo.patch(user_id, schema)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        return user