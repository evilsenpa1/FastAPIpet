from fastapi import APIRouter, Response, Depends
from schemas.auth import RegisterRequest, LoginRequest
from services.auth_service import AuthService
from dependencies.auth import get_auth_service
from core.auth_security import security

router = APIRouter(prefix="/auth")


@router.get("/protected", dependencies=[Depends(security.access_token_required)], tags=["Users"])
def protected_route():
    return {"data": "Supersecret"}


@router.post("/register",  tags=["Users"])
async def register_route(
    data: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
):
    user = await service.create_user(data.email, data.username, data.password)
    return {"user_id": user.id}


@router.post("/login", tags=["Users"])
async def login_route(
    data: LoginRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    user = await service.authenticate_user(data.email, data.password)
    token = security.create_access_token(uid=str(user.id))
    security.set_access_cookies(token, response)
    return {"message": "Logged in"}


@router.get("/all_users", dependencies=[Depends(security.access_token_required)], tags=["Users"])
async def all_users_route( service: AuthService = Depends(get_auth_service)):
    return await service.all_users()