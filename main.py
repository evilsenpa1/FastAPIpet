from authx.exceptions import MissingTokenError
from db.base import Base, engine
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.v1.v1_router import v1_router
import uvicorn

app = FastAPI()

app.include_router(v1_router)


@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return {"status": "success"}


@app.exception_handler(MissingTokenError)
async def missing_token_handler(request: Request, exc: MissingTokenError):
    return JSONResponse(status_code=401, content={"detail": "Not authenticated"})


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
