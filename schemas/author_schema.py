from pydantic import BaseModel
from typing import List, Optional



class AuthorAddSchema(BaseModel):
    author: str


class AuthorSchema(AuthorAddSchema):
    id: int


class AuthorPatchSchema(BaseModel):
    author: Optional[str] = None


class AuthorDeleteSchema(AuthorSchema):
    pass
