from sqlalchemy import select
from db.session import SessionDep
from models.book_model import AuthorModel
from utils.crud import CrudBase


class AuthorRepository(CrudBase[AuthorModel]):
    def __init__(self, db: SessionDep):
        super().__init__(model=AuthorModel, db=db)

    async def get_list_by_ids(self, author_ids):
        result = await self.db.execute(select(self.model).where(self.model.id.in_(author_ids)))
        authors = result.scalars().all()

        return authors
