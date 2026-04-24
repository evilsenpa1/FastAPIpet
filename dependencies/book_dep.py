from db.session import SessionDep
from repository.book_repo import BookRepository
from services.book_service import BookService
from fastapi import HTTPException, Form, Depends
from schemas.book_schema import BookCreateRequest
import json



def get_book_repo(db: SessionDep) -> BookRepository:
    return BookRepository(db=db)


def get_book_service(
    repo: BookRepository = Depends(get_book_repo),
) -> BookService:
    return BookService(repo)


def parse_book_data(data: str = Form(...)) -> BookCreateRequest:
    try:
        return BookCreateRequest(**json.loads(data))
    except (json.JSONDecodeError, ValueError) as e:
        raise HTTPException(status_code=422, detail=f"Invalid book data: {e}")
