from fastapi import HTTPException
from sqlalchemy import select
from db.session import SessionDep
from pydantic import BaseModel
from typing import Generic, TypeVar, Type
from sqlalchemy.orm import DeclarativeBase


ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class CrudBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: SessionDep = None):
        self.model = model
        self.db = db

    async def get_by_id(self, id: int) -> ModelType | None:
        result = await self.db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100):
        result = await self.db.execute(select(self.model).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, data: BaseModel):
        obj = self.model(**(data if isinstance(data, dict) else data.model_dump()))
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def patch(self, id: int, data: BaseModel):
        result = await self.db.execute(select(self.model).where(self.model.id == id))
        existing = result.scalar_one_or_none()

        if existing is None:
            raise HTTPException(status_code=404, detail="Content not found")

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(existing, field, value)

        await self.db.commit()
        await self.db.refresh(existing)

        return existing

    async def delete(self, id: int):
        result = await self.get_by_id(id)

        if not result:
            raise HTTPException(status_code=404, detail="Content not found")

        await self.db.delete(result)
        await self.db.commit()
        return {"status": "Success deleted"}
