

from db.base import Base, engine
from fastapi import FastAPI
from api.v1.endpoints.users import router as auth_router
from api.v1.endpoints.books import router as book_router
import uvicorn

app = FastAPI()

app.include_router(auth_router)
app.include_router(book_router)

@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return {"status": "success"}








if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
