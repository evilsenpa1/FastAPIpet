from fastapi import APIRouter
from api.v1.routers.auth_router import router as auth_router
from api.v1.routers.book_router import router as book_router
from api.v1.routers.author_router import router as author_router
from api.v1.routers.user_router import router as user_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(book_router, prefix="/book", tags=["Books"])
v1_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
v1_router.include_router(author_router, prefix="/author", tags=["Authors"])
v1_router.include_router(user_router, prefix="/user", tags=["Users"])
