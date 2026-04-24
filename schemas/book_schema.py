from datetime import date

from pydantic import BaseModel, field_validator, ConfigDict
from typing import List, Optional

class BookCreateRequest(BaseModel):
    """Client-facing schema: what the API consumer sends when creating a book."""
    name: str
    authors_ids: List[int]
    description: str
    pub_date: date

    @field_validator("name")
    @classmethod
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()


class BookAddSchema(BookCreateRequest):
    """Internal schema: BookCreateRequest + server-generated file_path."""
    file_path: Optional[str] = None


class BookSchema(BookAddSchema):
    id: int


class BookPatchSchema(BaseModel):
    name: Optional[str] = None
    authors_ids: Optional[List[int]] = None
    description: Optional[str] = None
    pub_date: Optional[date] = None




# Вложенная схема автора — БЕЗ обратной ссылки на books
class AuthorNestedSchema(BaseModel):
    id: int
    author: str

    model_config = ConfigDict(from_attributes=True)


# Response-схема — то что возвращает API
class BookResponseSchema(BaseModel):
    id: int
    name: str
    description: str
    pub_date: date
    file_path: str
    authors: List[AuthorNestedSchema]  # ← ORM relationship, не authors_ids

    model_config = ConfigDict(from_attributes=True)


class BookDeleteSchema(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)

