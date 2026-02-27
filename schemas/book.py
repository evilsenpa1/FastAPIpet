from pydantic import BaseModel, field_validator, Field
from typing import List

class BookAddSchema(BaseModel):
    name: str
    authors: List[str]
    description: str
    year: int = Field()
    month: int = Field()
    day: int = Field()


    @field_validator("name")
    @classmethod 
    def not_empty(cls, v):
        if not v.strip():  # защита и от "   " (пробелы)
            raise ValueError("Field cannot be empty")
        return v.strip()   # можно сразу обрезать пробелы


class BookSchema(BookAddSchema):
    id: int


class BookUpdateSchema(BookSchema):
    pass


class BookDeleteSchema(BookSchema):
    pass


class AuthorAddSchema(BaseModel):
    author: str


class AuthorSchema(AuthorAddSchema):
    id: int


class AuthorUpdateSchema(AuthorSchema):
    pass


class AuthorDeleteSchema(AuthorSchema):
    pass
