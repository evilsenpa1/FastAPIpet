from fastapi import HTTPException
from sqlalchemy import select
from db.session import SessionDep
from models.auth_model import UserModel
from schemas.user_schema import UserPatchSchema
from utils.crud import CrudBase


class UserRepository(CrudBase[UserModel]):
    def __init__(self, db: SessionDep):
        super().__init__(model=UserModel, db=db)
    
    async def get_by_email(self, email):
        result = await self.db.execute(select(self.model).where(self.model.email == email))
        return result.scalar_one_or_none()
