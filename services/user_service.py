from schemas.user import UserLoginSchema
from fastapi import HTTPException, Response
from core.security import security, config

def login(creds: UserLoginSchema, response: Response):
    if creds.username == "test" and creds.password == "test":
        token = security.create_access_token(uid="12345")
        response.set_cookie(
            key=config.JWT_ACCESS_COOKIE_NAME,
            value=token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60 * 60,
        )
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")