from fastapi import APIRouter
from services import book_service
from schemas.book import BookAddSchema, AuthorAddSchema, BookDeleteSchema, BookUpdateSchema, AuthorDeleteSchema
from db.session import SessionDep

router = APIRouter(prefix="/book")


@router.get("/get_books")
async def get_book_route(session: SessionDep):
    return await book_service.get_books(session)


@router.get("/get_authors")
async def get_author_route(session: SessionDep):
    return await book_service.get_authors(session)

@router.post("/add_books")
async def add_book_route(data: BookAddSchema, session: SessionDep):
    return await book_service.add_book(data, session)


@router.post("/update_books")
async def update_book_route(data: BookUpdateSchema, session: SessionDep):
    return await book_service.update_book(data, session)

@router.post("/delete_books")
async def delete_book_route(data: BookDeleteSchema, session: SessionDep):
    return await book_service.delete_book(data, session)


@router.post("/add_authors")
async def add_author_route(data: AuthorAddSchema, session: SessionDep):
    return await book_service.add_author(data, session)


@router.post("/update_authors")
async def update_author_route(data: AuthorAddSchema, session: SessionDep):
    return await book_service.update_author(data, session)


@router.post("/delete_authors")
async def delete_author_route(data: AuthorDeleteSchema, session: SessionDep):
    return await book_service.delete_author(data, session)