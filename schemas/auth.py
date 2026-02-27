from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(LoginRequest):
    username: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    role: str