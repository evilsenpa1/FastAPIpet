from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from services.book_service import BookService
from dependencies.book_dep import get_book_service
from schemas.book_schema import BookCreateRequest, BookPatchSchema, BookResponseSchema
from schemas.openapi_schemas import UPLOAD_BOOK_OPENAPI
from dependencies import auth_dep, book_dep, author_dep
from repository.author_repo import AuthorRepository
from core.auth_security import security
from dependencies.auth_dep import require_staff


router = APIRouter()


@router.get("/")
async def all_books_route(service: BookService = Depends(get_book_service)):
    return await service.get_all_books()


@router.get("/{book_id}")
async def book_by_id_route(
    book_id: int, service: BookService = Depends(get_book_service)
):
    book = await service.get_book_by_id(book_id)

    if not book:
        raise HTTPException(
            status_code=404, detail=f"Book with id '{book_id}' not found"
        )

    return book


@router.patch(
    "/{book_id}",
    dependencies=[Depends(security.access_token_required), Depends(require_staff)],
    response_model=BookResponseSchema,
)
async def patch_book_route(
    book_id: int,
    data: BookPatchSchema,
    service: BookService = Depends(get_book_service),
    author_repo: AuthorRepository = Depends(author_dep.get_author_repo),
):
    return await service.patch_book(book_id, data, author_repo)


@router.delete(
    "/{book_id}",
    dependencies=[Depends(security.access_token_required), Depends(require_staff)],
)
async def delete_book_route(
    book_id: int, service: BookService = Depends(get_book_service)
):
    return await service.delete_book(book_id)


@router.post(
    "/",
    dependencies=[Depends(security.access_token_required), Depends(require_staff)],
    openapi_extra=UPLOAD_BOOK_OPENAPI,
    response_model=BookResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def upload_book_route(
    service: BookService = Depends(get_book_service),
    user_id: int = Depends(auth_dep.get_current_user_id),
    file: UploadFile | None = File(default=None),
    data: BookCreateRequest = Depends(book_dep.parse_book_data),
    author_repo: AuthorRepository = Depends(author_dep.get_author_repo),
):
    return await service.create_book(user_id, file, data, author_repo)
