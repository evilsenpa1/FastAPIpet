from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from services.book_service import BookService
from dependencies.book_dep import get_book_service
from schemas.book_schema import BookAddSchema, BookDeleteSchema, BookPatchSchema, BookResponseSchema
from schemas.openapi_schemas import UPLOAD_BOOK_OPENAPI
from db.session import SessionDep
from dependencies import auth_dep, book_dep, author_dep
from repository.author_repo import AuthorRepository
from core.auth_security import security
from dependencies.auth_dep import require_staff


router = APIRouter()


@router.get("/get_all_books")
async def all_books_route(service: BookService = Depends(get_book_service)):
    return await service.get_all_books()


@router.get("/book_by_id/{book_id}")
async def book_by_id_route(
    book_id: int, service: BookService = Depends(get_book_service)
):
    book = await service.get_book_by_id(book_id)

    if not book:
        raise HTTPException(
            status_code=404, detail=f"Book with id '{book_id}' not found"
        )

    return book


# @router.post("/update_books")
# async def update_book_route(data: BookPatchSchema, session: SessionDep):
#     return await book_service.update_book(data, session)


@router.delete(
    "/delete_books/{book_id}", dependencies=[Depends(security.access_token_required), Depends(require_staff)]
)
async def delete_book_route(
    book_id: int, service: BookService = Depends(get_book_service)
):
    return await service.delete_book(book_id)


@router.post("/upload_book", dependencies=[Depends(security.access_token_required), Depends(require_staff)], openapi_extra=UPLOAD_BOOK_OPENAPI, response_model=BookResponseSchema)
async def upload_book_route(
    service: BookService = Depends(get_book_service),
    user_id: int = Depends(auth_dep.get_current_user_id),
    file: UploadFile | None = File(default=None),
    data: BookAddSchema = Depends(book_dep.parse_book_data),
    author_repo: AuthorRepository = Depends(author_dep.get_author_repo),

):
    return await service.create_book(user_id, file, data, author_repo)


