from fastapi import APIRouter, Response, Depends
from schemas.auth_schema import RegisterRequest, LoginRequest, UserResponse
from services.auth_service import AuthService
from dependencies.auth_dep import get_auth_service, get_current_user_id
from core.auth_security import security

router = APIRouter()


# @router.get("/protected", dependencies=[Depends(security.access_token_required)])
# def protected_route():
#     return {"data": "Supersecret"}


@router.post("/register")
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
    token = security.create_access_token(uid=str(user.id))
    security.set_access_cookies(token, response)
    return {"message": "Logged in"}

@router.get("/staff_check")
async def staff_check_route(id: int = Depends(get_current_user_id), service: AuthService = Depends(get_auth_service)):
    return service.is_staff(id)


