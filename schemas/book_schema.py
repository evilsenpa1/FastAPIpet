from pydantic import BaseModel, field_validator, Field, ConfigDict
from typing import List, Optional

class BookAddSchema(BaseModel):
    name: str
    authors_ids: List[int]
    description: str
    year: int = Field()
    month: int = Field()
    day: int = Field()
    file_path: str


    @field_validator("name")
    @classmethod 
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip() 


class BookSchema(BookAddSchema):
    id: int


class BookPatchSchema(BaseModel):
    name: Optional[str] = None
    authors_ids: Optional[List[int]] = None
    description: Optional[str] = None
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    file_path: Optional[str] = None




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
    year: int
    month: int
    day: int
    file_path: str
    authors: List[AuthorNestedSchema]  # ← ORM relationship, не authors_ids

    model_config = ConfigDict(from_attributes=True)


class BookDeleteSchema(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)

