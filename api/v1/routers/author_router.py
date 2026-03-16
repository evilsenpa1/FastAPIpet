from fastapi import APIRouter, Depends, HTTPException
from schemas.author_schema import AuthorAddSchema, AuthorSchema, AuthorPatchSchema
from db.session import SessionDep
from services import book_service
from services.author_service import AuthorService
from repository.author_repo import AuthorRepository
from repository.book_repo import BookRepository
from dependencies.book_dep import get_book_repo
from dependencies.author_dep import get_author_service
from core.auth_security import security
from dependencies.auth_dep import require_staff

router = APIRouter()


@router.get("/get_all_authors")
async def all_authors_route(service: AuthorService = Depends(get_author_service)):
    return await service.get_all_authors()


@router.get("/author_by_id/{author_id}")
async def author_by_id_route(
    author_id: int, service: AuthorService = Depends(get_author_service)
):
    author = await service.get_author_by_id(author_id)
    if not author:
        return HTTPException(status_code=404, detail="Author not found")

    return author


@router.post(
    "/add_author",
    dependencies=[Depends(security.access_token_required), Depends(require_staff)],
)
async def add_author_route(
    data: AuthorAddSchema, service: AuthorService = Depends(get_author_service)
):
    return await service.create_author(data)


@router.patch(
    "/update_author/{author_id}",
    dependencies=[Depends(security.access_token_required), Depends(require_staff)],
)
async def patch_author_route(
    author_id: int,
    data: AuthorPatchSchema,
    service: AuthorService = Depends(get_author_service),
):
    return await service.patch_author(author_id, data)


@router.delete(
    "/delete_author/{author_id}",
    dependencies=[Depends(security.access_token_required), Depends(require_staff)],
)
async def delete_author_route(
    author_id: int,
    service: AuthorService = Depends(get_author_service),
    book_repo: BookRepository = Depends(get_book_repo),
):
    return await service.delete_author(author_id, book_repo)
