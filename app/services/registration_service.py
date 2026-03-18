from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Registration


async def create_registration(
    session: AsyncSession,
    telegram_user_id: int,
    telegram_username: str | None,
    full_name: str,
    department: str,
    phone: str,
    language: str,
    class_id: str,
    class_name: str,
) -> Registration:
    registration = Registration(
        telegram_user_id=telegram_user_id,
        telegram_username=telegram_username,
        full_name=full_name,
        department=department,
        phone=phone,
        language=language,
        class_id=class_id,
        class_name=class_name,
        status="new",
    )

    session.add(registration)
    await session.commit()
    await session.refresh(registration)

    return registration