from sqlalchemy import select
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
        course_duration_months=0,
        months_paid=0,
        status="new",
    )

    session.add(registration)

    await session.flush()

    registration.reference_code = generate_reference_code(registration.id)

    await session.commit()
    await session.refresh(registration)

    return registration


async def get_registration_by_id(
    session: AsyncSession,
    registration_id: int,
) -> Registration | None:
    result = await session.execute(
        select(Registration).where(Registration.id == registration_id)
    )
    return result.scalar_one_or_none()


async def update_registration_status(
    session: AsyncSession,
    registration_id: int,
    new_status: str,
) -> Registration | None:
    registration = await get_registration_by_id(session, registration_id)
    if registration is None:
        return None

    registration.status = new_status
    await session.commit()
    await session.refresh(registration)
    return registration


async def update_course_duration(
    session: AsyncSession,
    registration_id: int,
    duration_months: int,
) -> Registration | None:
    registration = await get_registration_by_id(session, registration_id)
    if registration is None:
        return None

    registration.course_duration_months = duration_months
    await session.commit()
    await session.refresh(registration)
    return registration


async def increment_months_paid(
    session: AsyncSession,
    registration_id: int,
) -> Registration | None:
    registration = await get_registration_by_id(session, registration_id)
    if registration is None:
        return None

    registration.months_paid += 1
    await session.commit()
    await session.refresh(registration)
    return registration