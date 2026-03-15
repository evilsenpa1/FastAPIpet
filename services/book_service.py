from schemas.book_schema import (
    BookAddSchema,
    BookDeleteSchema,
    BookPatchSchema,
)
from db.session import SessionDep
from models.book_model import BookModel, AuthorModel
from repository.book_repo import BookRepository
from repository.author_repo import AuthorRepository
from dependencies.author_dep import get_author_repo
from sqlalchemy import select
from fastapi import HTTPException, File, UploadFile, Depends
import aiofiles
from pathlib import Path
import uuid
from utils import file_manager


class BookService:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    async def get_all_books(self):
        return await self.repo.get_all()

    async def get_book_by_id(self, id: int):
        return await self.repo.get_by_id(id)

    async def create_book(self, user_id: int, file, data: BookAddSchema, author_repo):

        await self._validate_authors(data.authors_ids)

        file_path = await self._get_file_path(user_id, file)

        await file_manager.create_file(file_path, file)

        file_path = str(file_path)

        data.file_path = file_path

        try:
            authors_ids = data.authors_ids
            book_data = data.model_dump(exclude={"authors_ids"})
            new_book = await self.repo.create(book_data, authors_ids, author_repo)
        except HTTPException:
            file_manager.delete_file(file_path)
            raise
        except Exception as e:
            file_manager.delete_file(file_path)
            print(f"ERROR: {e}", flush=True)
            import traceback

            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Internal server error")

        return new_book

    async def patch_book(self, id: int, data: BookPatchSchema) -> BookModel:
        if data.authors_ids is not None:
            await self._validate_authors(data.authors_ids)

        return await self.repo.patch(id, data)

    async def delete_book(self, id: int):
        return await self.repo.delete(id)

    async def _validate_authors(
        self,
        author_ids: list[int],
    ) -> None:
        author_repo = get_author_repo(self.repo.db)
        authors = await author_repo.get_list_by_ids(author_ids)
        if len(authors) != len(author_ids):
            raise HTTPException(status_code=404, detail="One or more authors not found")

    async def _get_file_path(self, user_id: int, file: str) -> Path:

        if not file:
            return {"message": "No upload file sent"}

        UPLOAD_DIR = Path("uploads")
        UPLOAD_DIR.mkdir(exist_ok=True)
        ALLOWED_EXTENSIONS = {".doc", ".docx", ".pdf", ".txt"}

        file_ext = Path(file.filename).suffix.lower()

        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type '{file_ext}' not allowed. Use: {ALLOWED_EXTENSIONS}",
            )

        unique_name = f"{uuid.uuid4()}{file_ext}"

        user_dir = UPLOAD_DIR / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)

        return user_dir / unique_name


