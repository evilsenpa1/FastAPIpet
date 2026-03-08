from schemas.book import (
    BookAddSchema,
    AuthorAddSchema,
    BookDeleteSchema,
    BookUpdateSchema,
    AuthorUpdateSchema,
    AuthorDeleteSchema,
)
from db.session import SessionDep
from models.book import BookModel, AuthorModel
from repository.book import BookRepository
from sqlalchemy import select
from fastapi import HTTPException, File, UploadFile, Depends
import aiofiles
from pathlib import Path
import uuid
from utils import file_manager


async def get_books(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query)
    return result.scalars().all()


async def get_authors(session: SessionDep):
    query = select(AuthorModel)
    result = await session.execute(query)
    return result.scalars().all()





async def update_book(data: BookUpdateSchema, session: SessionDep):

    result = await session.execute(select(BookModel).filter(BookModel.id == data.id))
    book = result.scalars().first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.name = "New name"
    book.year = 6666

    await session.commit()
    return {"status": "success"}


async def delete_book(data: BookDeleteSchema, session: SessionDep):

    result = await session.execute(select(BookModel).filter(BookModel.id == data.id))
    book = result.scalars().first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    await session.delete(book)
    await session.commit()
    return {"status": "success"}


async def add_author(data: AuthorAddSchema, session: SessionDep):

    new_author = AuthorModel(
        author=data.author,
    )
    session.add(new_author)
    await session.commit()
    return {"status": "success"}


async def update_author(data: AuthorUpdateSchema, session: SessionDep):

    result = await session.execute(
        select(AuthorModel).filter(AuthorModel.id == data.id)
    )
    author = result.scalars().first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    author.name = "New author"

    await session.commit()
    return {"status": "success"}


async def delete_author(data: AuthorDeleteSchema, session: SessionDep):

    result = await session.execute(
        select(AuthorModel).filter(AuthorModel.id == data.id)
    )
    author = result.scalars().first()

    if not author:
        raise HTTPException(status_code=404, detail="Book not found")

    await session.delete(author)
    await session.commit()
    return {"status": "success"}


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {".doc", ".docx", ".pdf", ".txt"}


def get_file_path(user_id: int, filename: str) -> Path:
    file_ext = Path(filename).suffix.lower()
    unique_name = f"{uuid.uuid4()}{file_ext}"

    user_dir = UPLOAD_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)

    return user_dir / unique_name


async def upload_book(user_id: int, file: UploadFile, data: BookAddSchema, repo: BookRepository):
    if not file:
        return {"message": "No upload file sent"}

    file_ext = Path(file.filename).suffix.lower()

    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file_ext}' not allowed. Use: {ALLOWED_EXTENSIONS}",
        )

    file_path = get_file_path(user_id, file.filename)

    await file_manager.create_file(file_path, file)


    try:
        await repo.create_book(file_path, data)
    except HTTPException:
        file_manager.delete_file(file_path)
        raise
    except Exception as e:
        file_manager.delete_file(file_path)
        print(f"ERROR: {e}", flush=True)
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error")

    return {"filename": file.filename}
