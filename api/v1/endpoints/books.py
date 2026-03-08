from fastapi import APIRouter, Depends, File, UploadFile
from services import book_service
from schemas.book import BookAddSchema, BookDeleteSchema, BookUpdateSchema
from db.session import SessionDep
from dependencies import auth, books
from repository.book import BookRepository


router = APIRouter(prefix="/book")


@router.get("/get_books", tags=["Books"])
async def get_book_route(session: SessionDep):
    return await book_service.get_books(session)




@router.post("/update_books", tags=["Books"])
async def update_book_route(data: BookUpdateSchema, session: SessionDep):
    return await book_service.update_book(data, session)

@router.post("/delete_books", tags=["Books"])
async def delete_book_route(data: BookDeleteSchema, session: SessionDep):
    return await book_service.delete_book(data, session)


@router.post("/upload_book", tags=["Books"])
async def upload_book_route(
    data: BookAddSchema = Depends(books.parse_book_data),
    file: UploadFile | None = File(default=None),
    user_id: int = Depends(auth.get_current_user_id),
    repo: BookRepository = Depends(BookRepository),
):
    return await book_service.upload_book(user_id, file, data, repo)