from sqlalchemy import select
from db.session import SessionDep
from models.book_model import AuthorModel
from db.session import SessionDep


class AuthorRepository:
    def __init__(self, db: SessionDep):
        self.db = db

    async def get_author_by_id(self, author_id: int) -> AuthorModel:
        result = await self.db.execute(select(AuthorModel).where(AuthorModel.id == author_id))
        return result.scalar_one_or_none()