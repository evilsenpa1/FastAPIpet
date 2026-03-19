from pydantic import BaseModel, EmailStr
from typing import Optional

class UserPatchSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

