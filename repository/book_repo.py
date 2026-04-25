from fastapi import HTTPException
from sqlalchemy import select

from db.session import SessionDep
from models.book_model import BookModel, AuthorModel
from schemas.book_schema import BookPatchSchema
from utils.crud import CrudBase


class BookRepository(CrudBase[BookModel]):
    def __init__(self, db: SessionDep):
        super().__init__(model=BookModel, db=db)

    async def create(self, book_data: dict, authors: list[AuthorModel]) -> BookModel:
        new_book = await super().create(book_data)
        new_book.authors = authors
        await self.db.commit()
        await self.db.refresh(new_book)
        return new_book

    async def patch(
        self, id: int, data: BookPatchSchema, authors: list[AuthorModel] | None = None
    ) -> BookModel:
        result = await self.db.execute(select(self.model).where(self.model.id == id))
        existing = result.scalar_one_or_none()

        if existing is None:
            raise HTTPException(status_code=404, detail="Book not found")

        # Exclude authors_ids — it's not a column, handled separately via relationship
        update_data = data.model_dump(exclude_unset=True, exclude={"authors_ids"})
        for field, value in update_data.items():
            setattr(existing, field, value)

        if authors is not None:
            existing.authors = authors

        await self.db.commit()
        await self.db.refresh(existing)
        return existing
