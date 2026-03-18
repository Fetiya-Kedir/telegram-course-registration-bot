from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Registration


def generate_reference_code(registration_id: int) -> str:
    return f"DSN-{registration_id:04d}"


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

    registration.reference_code = generate_reference_code(registration.id)
    await session.commit()
    await session.refresh(registration)

    return registration