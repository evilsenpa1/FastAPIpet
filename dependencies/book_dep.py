from fastapi import HTTPException, Form
from schemas.book_schema import BookAddSchema
import json


def parse_book_data(data: str = Form(...)) -> BookAddSchema:
    try:
        return BookAddSchema(**json.loads(data))
    except (json.JSONDecodeError, ValueError) as e:
        raise HTTPException(status_code=422, detail=f"Invalid book data: {e}")
