from sqlalchemy import select
from db.session import SessionDep
from models.book_model import BookModel, AuthorModel
from schemas.book_schema import BookAddSchema, BookPatchSchema
from fastapi import HTTPException, Depends
from db.session import get_session, SessionDep
from utils.crud import CrudBase
from repository.author_repo import AuthorRepository


class BookRepository(CrudBase[BookModel]):
    def __init__(self, db: SessionDep):
        super().__init__(model=BookModel, db=db)

    async def create(self, book_data, authors_ids, author_repo):
        new_book = await super().create(book_data)


        authors = await author_repo.get_list_by_ids(authors_ids)
        new_book.authors = authors
        await self.db.commit()
        await self.db.refresh(new_book)

        return new_book
