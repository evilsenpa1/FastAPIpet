from authx.exceptions import MissingTokenError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.v1.v1_router import v1_router
import uvicorn
from contextlib import asynccontextmanager
from core.startup import create_initial_superuser


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_initial_superuser()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(v1_router)


@app.exception_handler(MissingTokenError)
async def missing_token_handler(request: Request, exc: MissingTokenError):
    return JSONResponse(status_code=401, content={"detail": "Not authenticated"})




if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
