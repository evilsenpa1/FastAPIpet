from fastapi import APIRouter, Depends
from services.user_service import UserService
from dependencies.auth_dep import get_user_service, require_staff
from schemas.user_schema import UserPatchSchema, UserSelfPatchSchema
from core.auth_security import security
from dependencies.auth_dep import get_current_user_id

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(security.access_token_required), Depends(require_staff)],
)
async def all_users_route(service: UserService = Depends(get_user_service)):
    return await service.all_users()


@router.get(
    "/{user_id}",
    dependencies=[Depends(security.access_token_required), Depends(require_staff)],
)
async def user_by_id_route(
    user_id: int, service: UserService = Depends(get_user_service)
):
    return await service.get_user_by_id(user_id)


# /me must be before /{user_id} to avoid routing conflict
@router.patch("/me", dependencies=[Depends(security.access_token_required)])
async def patch_me_route(
    schema: UserSelfPatchSchema,
    user_id: int = Depends(get_current_user_id),
    service: UserService = Depends(get_user_service),
):
    return await service.patch_user(schema, user_id)


@router.patch(
    "/patch_user/{user_id}",
    dependencies=[Depends(security.access_token_required), Depends(require_staff)],
)
async def patch_user_route(
    schema: UserPatchSchema,
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    return await service.patch_user(schema, user_id)


@router.delete(
    "/delete_user/{user_id}",
    dependencies=[Depends(security.access_token_required), Depends(require_staff)],
)
async def delete_user_route(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    return await service.delete_user(user_id)
