import uuid
import logging
from pathlib import Path

from fastapi import HTTPException, UploadFile

from schemas.book_schema import BookAddSchema, BookCreateRequest, BookPatchSchema
from models.book_model import BookModel, AuthorModel
from repository.book_repo import BookRepository
from repository.author_repo import AuthorRepository
from utils import file_manager

logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("uploads")
ALLOWED_EXTENSIONS = {".doc", ".docx", ".pdf", ".txt"}

class BookService:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    async def get_all_books(self) -> list[BookModel]:
        return await self.repo.get_all()

    async def get_book_by_id(self, id: int) -> BookModel | None:
        return await self.repo.get_by_id(id)

    async def create_book(
        self,
        user_id: int,
        file: UploadFile | None,
        data: BookCreateRequest,
        author_repo: AuthorRepository,
    ) -> BookModel:
        # Validate authors and reuse the fetched list — avoids a second DB query in repo.create()
        authors = await self._validate_authors(data.authors_ids, author_repo)

        file_path = await self._get_file_path(user_id, file)
        await file_manager.create_file(file_path, file)

        internal_data = BookAddSchema(**data.model_dump(), file_path=str(file_path))
        book_dict = internal_data.model_dump(exclude={"authors_ids"})

        try:
            new_book = await self.repo.create(book_dict, authors)
        except HTTPException:
            await file_manager.delete_file(file_path)
            raise
        except Exception as e:
            await file_manager.delete_file(file_path)
            logger.error("ERROR: %s", e)
            raise HTTPException(status_code=500, detail="Internal server error")

        return new_book

    async def patch_book(
        self, id: int, data: BookPatchSchema, author_repo: AuthorRepository
    ) -> BookModel:
        authors = None
        if data.authors_ids is not None:
            authors = await self._validate_authors(data.authors_ids, author_repo)

        return await self.repo.patch(id, data, authors)

    async def delete_book(self, id: int) -> dict:
        book = await self.repo.get_by_id(id)
        if not book:
            raise HTTPException(status_code=404, detail=f"Book {id} not found")

        if book.file_path:
            await file_manager.delete_file(book.file_path)

        return await self.repo.delete(id)

    async def _validate_authors(
        self, author_ids: list[int], author_repo: AuthorRepository
    ) -> list[AuthorModel]:
        """Checks all IDs exist and returns the ORM objects for immediate reuse."""
        authors = await author_repo.get_list_by_ids(author_ids)
        if len(authors) != len(author_ids):
            raise HTTPException(status_code=404, detail="One or more authors not found")
        return authors

    async def _get_file_path(self, user_id: int, file: UploadFile | None) -> Path:
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")

        file_ext = Path(file.filename).suffix.lower()

        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type '{file_ext}' not allowed. Use: {ALLOWED_EXTENSIONS}",
            )

        UPLOAD_DIR.mkdir(exist_ok=True)
        user_dir = UPLOAD_DIR / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)

        return user_dir / f"{uuid.uuid4()}{file_ext}"
