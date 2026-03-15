from fastapi import Depends
from db.session import SessionDep
from repository.author_repo import AuthorRepository
from services.author_service import AuthorService
from core.auth_security import security


def get_author_repo(db: SessionDep) -> AuthorRepository:
    return AuthorRepository(db=db)


def get_author_service(
    repo: AuthorRepository = Depends(get_author_repo),
) -> AuthorService:
    return AuthorService(repo)
