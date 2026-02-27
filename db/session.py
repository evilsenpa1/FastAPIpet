from fastapi import Depends
from .base import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

SessionDep = Annotated[AsyncSession, Depends(get_session)]