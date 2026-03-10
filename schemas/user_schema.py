from pydantic import BaseModel, EmailStr
from typing import Optional

class UserPatchSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    is_active: Optional[bool] = None

