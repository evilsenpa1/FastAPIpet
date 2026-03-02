
from fastapi import APIRouter
from schemas.book import AuthorAddSchema, AuthorDeleteSchema
from db.session import SessionDep
from services import book_service

router = APIRouter(prefix="/author")

@router.get("/get_authors", tags=["Authors"])
async def get_author_route(session: SessionDep):
    return await book_service.get_authors(session)

@router.post("/add_authors", tags=["Authors"])
async def add_author_route(data: AuthorAddSchema, session: SessionDep):
    return await book_service.add_author(data, session)


@router.post("/update_authors", tags=["Authors"])
async def update_author_route(data: AuthorAddSchema, session: SessionDep):
    return await book_service.update_author(data, session)


@router.post("/delete_authors", tags=["Authors"])
async def delete_author_route(data: AuthorDeleteSchema, session: SessionDep):
    return await book_service.delete_author(data, session)

