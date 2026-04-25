from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserResponseSchema(BaseModel):
    id: int
    email: str
    username: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserSelfPatchSchema(BaseModel):
    """Fields a user is allowed to change about themselves."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserPatchSchema(UserSelfPatchSchema):
    """Extended schema for staff: also allows changing role and active status."""
    role: Optional[str] = None
    is_active: Optional[bool] = None

