from fastapi import HTTPException
from sqlalchemy import select
from db.session import SessionDep
from pydantic import BaseModel
# from typing import Generic, TypeVar, Type

class CrudBase:
    def __init__(self, db: SessionDep):
        self.db = db

    async def get_by_id(self, id: int, model):
        result = await self.db.execute(select(model).where(model.id == id))
        return result.scalar_one_or_none()

    async def get_all(self, model, skip: int = 0, limit: int = 100):
        query = select(model)
        result = await self.db.execute(select(model).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, model, data: BaseModel):
        obj = model(**data.model_dump())
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def patch(self, id: int, model, data: BaseModel):
        result = await self.db.execute(select(model).where(model.id == id))
        existing = result.scalar_one_or_none()

        if existing is None:
            raise HTTPException(status_code=404, detail="Content not found")

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(existing, field, value)

        await self.db.commit()
        await self.db.refresh(existing)

        return existing

    async def delete(self, id: int, model):
        result = await self.get_by_id(id, model)

        if not result:
            raise HTTPException(status_code=404, detail="Content not found")

        await self.db.delete(result)
        await self.db.commit()
        return {"status": "Success deleted"}
