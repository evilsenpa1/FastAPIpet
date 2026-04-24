from contextlib import asynccontextmanager

from core.settings import DATABASE_URL

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(DATABASE_URL)

SessionLocal = async_sessionmaker(autocommit = False, autoflush=False, expire_on_commit=False, bind=engine)

class Base(DeclarativeBase):
    pass

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

@asynccontextmanager
async def get_session_ctx() -> AsyncSession:
    async with SessionLocal() as session:
        yield session