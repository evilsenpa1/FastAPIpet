from core import settings
from db.base import get_session_ctx
from repository.user_repo import UserRepository
from models.auth_model import UserRole
import bcrypt


async def create_initial_superuser():
    if not settings.SUPERUSER_EMAIL:
        return  # не задано — пропускаем

    async with get_session_ctx() as session:
        repo = UserRepository(session)
        existing = await repo.get_by_email(settings.SUPERUSER_EMAIL)
        if existing:
            return  # уже есть — ничего не делаем

        hashed = bcrypt.hashpw(
            settings.SUPERUSER_PASSWORD.encode(), bcrypt.gensalt()
        ).decode()

        await repo.create(
            {
                "username": settings.SUPERUSER_USERNAME,
                "email": settings.SUPERUSER_EMAIL,
                "hashed_password": hashed,
                "role": UserRole.ADMIN,
                "is_active": True,
            }
        )
        print(f"✅ Superuser {settings.SUPERUSER_EMAIL} created.")
