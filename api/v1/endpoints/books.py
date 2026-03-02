from fastapi import APIRouter
from services import book_service
from schemas.book import BookAddSchema, BookDeleteSchema, BookUpdateSchema
from db.session import SessionDep

router = APIRouter(prefix="/book")


@router.get("/get_books", tags=["Books"])
async def get_book_route(session: SessionDep):
    return await book_service.get_books(session)




@router.post("/add_books", tags=["Books"])
async def add_book_route(data: BookAddSchema, session: SessionDep):
    return await book_service.add_book(data, session)


@router.post("/update_books", tags=["Books"])
async def update_book_route(data: BookUpdateSchema, session: SessionDep):
    return await book_service.update_book(data, session)

@router.post("/delete_books", tags=["Books"])
async def delete_book_route(data: BookDeleteSchema, session: SessionDep):
    return await book_service.delete_book(data, session)

