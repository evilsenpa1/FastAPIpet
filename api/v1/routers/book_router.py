from fastapi import APIRouter, Depends, File, UploadFile
from services import book_service
from schemas.book_schema import BookAddSchema, BookDeleteSchema, BookUpdateSchema
from db.session import SessionDep
from dependencies import auth_dep, book_dep
from repository.book_repo import BookRepository
from core.auth_security import security


router = APIRouter()


@router.get("/get_books")
async def get_book_route(session: SessionDep):
    return await book_service.get_books(session)


@router.get("/book_by_id/{book_id}")
async def book_by_id_route(
    book_id: int, repo: BookRepository = Depends(BookRepository)
):
    return await repo.get_book_by_id(book_id)


@router.post("/update_books")
async def update_book_route(data: BookUpdateSchema, session: SessionDep):
    return await book_service.update_book(data, session)


@router.delete("/delete_books", dependencies=[Depends(security.access_token_required)])
async def delete_book_route(data: BookDeleteSchema, session: SessionDep):
    return await book_service.delete_book(data, session)


@router.post("/upload_book", dependencies=[Depends(security.access_token_required)])
async def upload_book_route(
    data: BookAddSchema = Depends(book_dep.parse_book_data),
    file: UploadFile | None = File(default=None),
    user_id: int = Depends(auth_dep.get_current_user_id),
    repo: BookRepository = Depends(BookRepository),
):
    return await book_service.upload_book(user_id, file, data, repo)
