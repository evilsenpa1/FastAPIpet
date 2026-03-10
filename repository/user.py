from fastapi import HTTPException
from sqlalchemy import select
from db.session import SessionDep
from models.auth import UserModel
from schemas.user_schema import UserPatchSchema


class UserRepository:
    def __init__(self, db: SessionDep):
        self.db = db

    async def get_by_email(self, email: str) -> UserModel | None:
        result = await self.db.execute(select(UserModel).where(UserModel.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> UserModel | None:
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_all_users(self) -> UserModel | None:
        query = select(UserModel)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(
        self,
        email: str,
        username: str,
        hashed_password: str,
    ) -> UserModel:
        user = UserModel(email=email, username=username, hashed_password=hashed_password)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def patch(self, user_id: int, patch: UserPatchSchema):
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        existing = result.scalar_one_or_none()

        if existing is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        update_data = patch.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(existing, field, value)

        await self.db.commit()
        await self.db.refresh(existing)

        return existing