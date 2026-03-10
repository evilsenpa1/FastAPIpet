from sqlalchemy import select
from db.session import SessionDep
from models.book import BookModel, AuthorModel
from schemas.book_schema import BookAddSchema
from fastapi import HTTPException, Depends
from db.session import get_session, SessionDep


class BookRepository:
    def __init__(self, db: SessionDep):
        self.db = db

    async def create_book(self, file_path, data: BookAddSchema) -> BookModel | None:
        author_objects = []
        for author_name in data.authors:
            result = await self.db.execute(select(AuthorModel).filter(AuthorModel.author == author_name))

            author = result.scalars().first()

            if author is None:
                raise HTTPException(status_code=404, detail=f"Author '{author_name}' not found")

            author_objects.append(author)

        if not author_objects:
            raise HTTPException(status_code=400, detail="List of authors is empty. Need to add at least 1 author")
        
        new_book= BookModel(
        name = data.name,
        authors = author_objects,
        description = data.description,
        year = data.year,
        month = data.month,
        day = data.day,
        file_path = str(file_path)
        )
        self.db.add(new_book)
        await self.db.commit()
        return {"status": "success"}
    
    async def get_book_by_id(self, book_id: int) -> BookModel | None:
        result = await self.db.execute(select(BookModel).where(BookModel.id == book_id))
        return result.scalar_one_or_none()