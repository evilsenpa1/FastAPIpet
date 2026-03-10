from fastapi import APIRouter, Depends
from services.user_service import UserService
from dependencies.auth_dep import get_user_service
from schemas.user_schema import UserPatchSchema
from core.auth_security import security
from dependencies.auth_dep import get_current_user_id

router = APIRouter()


@router.get("/all_users", dependencies=[Depends(security.access_token_required)])
async def all_users_route(service: UserService = Depends(get_user_service)):
    return await service.all_users()


@router.get(
    "/user_by_id/{user_id}", dependencies=[Depends(security.access_token_required)]
)
async def user_by_id_route(
    user_id: int, service: UserService = Depends(get_user_service)
):
    return await service.get_user_by_id(user_id)


@router.patch("/patch_user/me", dependencies=[Depends(security.access_token_required)])
async def user_patch_route(
    schema: UserPatchSchema,
    user_id: int = Depends(get_current_user_id),
    service: UserService = Depends(get_user_service),
):
    return await service.patch_user(schema, user_id)
