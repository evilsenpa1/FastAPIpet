import os
from dotenv import load_dotenv

from datetime import timedelta
from authx import AuthX, AuthXConfig

load_dotenv()

PROD = os.getenv("PROD")

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in environment variables!")

config = AuthXConfig(
    JWT_SECRET_KEY=SECRET_KEY,
    JWT_ALGORITHM="HS256",
    JWT_ACCESS_COOKIE_NAME="my_access_token",
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30),
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=7),
    JWT_TOKEN_LOCATION=["cookies"],
    JWT_COOKIE_SECURE=PROD,
    JWT_COOKIE_SAMESITE="lax",
    JWT_COOKIE_CSRF_PROTECT=True,

)

security = AuthX(config=config)