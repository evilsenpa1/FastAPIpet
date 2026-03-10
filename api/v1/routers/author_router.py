from fastapi import APIRouter, Depends
from schemas.book_schema import AuthorAddSchema, AuthorDeleteSchema
from db.session import SessionDep
from services import book_service
from repository.author_repo import AuthorRepository

router = APIRouter()


@router.get("/get_authors")
async def get_author_route(session: SessionDep):
    return await book_service.get_authors(session)


@router.get("/author_by_id/{author_id}")
async def author_by_id_route(
    author_id: int, repo: AuthorRepository = Depends(AuthorRepository)
):
    return await repo.get_author_by_id(author_id)


@router.post("/add_authors")
async def add_author_route(data: AuthorAddSchema, session: SessionDep):
    return await book_service.add_author(data, session)


@router.post("/update_authors")
async def update_author_route(data: AuthorAddSchema, session: SessionDep):
    return await book_service.update_author(data, session)


@router.delete("/delete_authors")
async def delete_author_route(data: AuthorDeleteSchema, session: SessionDep):
    return await book_service.delete_author(data, session)
