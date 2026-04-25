from fastapi import APIRouter, Response, Depends, status
from schemas.auth_schema import RegisterRequest, LoginRequest, UserResponse
from services.auth_service import AuthService
from dependencies.auth_dep import get_auth_service, get_current_user_id
from core.auth_security import security

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_route(
    data: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
):
    user = await service.create_user(data)
    return {"user_id": user.id}


@router.post("/login")
async def login_route(
    data: LoginRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    user = await service.authenticate_user(data.email, data.password)
    access_token = security.create_access_token(uid=str(user.id))

    refresh_token = security.create_refresh_token(uid=str(user.id))

    security.set_access_cookies(access_token, response)
    security.set_refresh_cookies(refresh_token, response)

    return {"message": "Logged in"}


@router.post("/refresh")
async def refresh_route(
    response: Response,
    payload = Depends(security.refresh_token_required),
):
    
    new_access_token = security.create_access_token(uid=payload.sub)
    security.set_access_cookies(new_access_token, response)
    return {"message": "Token refreshed"}

@router.get("/staff_check")
async def staff_check_route(id: int = Depends(get_current_user_id), service: AuthService = Depends(get_auth_service)):
    return await service.is_staff(id)


