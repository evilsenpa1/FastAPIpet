from fastapi import APIRouter, Response, Depends
from schemas.auth import RegisterRequest, LoginRequest
from services.auth_service import AuthService
from dependencies.auth import get_auth_service
from core.auth_security import security

router = APIRouter(prefix="/auth")


@router.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():
    return {"data": "Supersecret"}


@router.post("/register")
async def register(
    data: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
):
    user = await service.create_user(data.email, data.username, data.password)
    return {"user_id": user.id}


@router.post("/login")
async def login(
    data: LoginRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    user = await service.authenticate_user(data.email, data.password)
    token = security.create_access_token(uid=str(user.id))
    security.set_access_cookies(token, response)
    return {"message": "Logged in"}