from sqlalchemy import select
from sqlalchemy.orm import selectinload
from db.session import SessionDep
from models.book_model import AuthorModel, BookModel
from utils.crud import CrudBase

class AuthorRepository(CrudBase[AuthorModel]):
    def __init__(self, db: SessionDep):
        super().__init__(model=AuthorModel, db=db)

    async def get_list_by_ids(self, author_ids):
        result = await self.db.execute(select(self.model).where(self.model.id.in_(author_ids)))
        authors = result.scalars().all()

        return authors
    
    async def get_by_id(self, id: int) -> AuthorModel | None:
        result = await self.db.execute(
            select(self.model)
            .options(
                selectinload(self.model.books).selectinload(BookModel.authors)
            )
            .where(AuthorModel.id == id)
        )
        return result.scalar_one_or_none()

