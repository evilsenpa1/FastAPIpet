from datetime import timedelta
from authx import AuthX, AuthXConfig
from core.settings import settings

config = AuthXConfig(
    JWT_SECRET_KEY=settings.SECRET_KEY,
    JWT_ALGORITHM="HS256",
    JWT_ACCESS_COOKIE_NAME="my_access_token",
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30),
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=7),
    JWT_TOKEN_LOCATION=["cookies"],
    JWT_COOKIE_SECURE=settings.PROD,
    JWT_COOKIE_SAMESITE="lax",
    JWT_COOKIE_CSRF_PROTECT=settings.PROD,
)

security = AuthX(config=config)
