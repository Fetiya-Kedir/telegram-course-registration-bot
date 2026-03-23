import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from app.config.settings import get_settings
from app.database.session import AsyncSessionLocal
from app.keyboards.admin import (
    admin_status_keyboard,
    admin_duration_keyboard,
    admin_payment_keyboard,
)
from app.services.google_sheets_service import (
    update_registration_status_in_google_sheets,
    update_course_duration_in_google_sheets,
    update_months_paid_in_google_sheets,
)
from app.services.notification_service import notify_student_status_update
from app.services.registration_service import (
    update_registration_status,
    update_course_duration,
    increment_months_paid,
    get_registration_by_id,
)
from app.utils.i18n import t

router = Router()


ALLOWED_STATUSES = {
    "contacted",
    "payment_pending",
    "joined",
    "cancelled",
}

ALLOWED_DURATIONS = {2, 3, 4}


def combined_admin_keyboard(registration_id: int) -> InlineKeyboardMarkup:
    status_markup = admin_status_keyboard(registration_id)
    duration_markup = admin_duration_keyboard(registration_id)
    payment_markup = admin_payment_keyboard(registration_id)

    combined_rows = (
        status_markup.inline_keyboard
        + duration_markup.inline_keyboard
        + payment_markup.inline_keyboard
    )
    return InlineKeyboardMarkup(inline_keyboard=combined_rows)


def format_admin_message(registration) -> str:
    lang_label = "English" if registration.language == "en" else "አማርኛ"

    if registration.course_duration_months <= 0:
        duration_text = t(registration.language, "ADMIN_DURATION_NOT_SET")
        progress_text = t(registration.language, "ADMIN_DURATION_NOT_SET")
    else:
        duration_text = f"{registration.course_duration_months} month(s)"
        progress_text = f"{registration.months_paid} / {registration.course_duration_months}"

    username_text = (
        f"@{registration.telegram_username}"
        if registration.telegram_username
        else t(registration.language, "ADMIN_USERNAME_MISSING")
    )

    return (
        f"<b>{t(registration.language, 'ADMIN_NEW_REG_TITLE')}</b>\n\n"
        f"{t(registration.language, 'ADMIN_REFERENCE_LABEL')}: <b>{registration.reference_code}</b>\n"
        f"{t(registration.language, 'ADMIN_NAME_LABEL')}: <b>{registration.full_name}</b>\n"
        f"{t(registration.language, 'ADMIN_DEPARTMENT_LABEL')}: <b>{registration.department}</b>\n"
        f"{t(registration.language, 'ADMIN_PHONE_LABEL')}: <b>{registration.phone}</b>\n"
        f"{t(registration.language, 'ADMIN_CLASS_LABEL')}: <b>{registration.class_name}</b>\n"
        f"{t(registration.language, 'ADMIN_LANGUAGE_LABEL')}: <b>{lang_label}</b>\n"
        f"{t(registration.language, 'ADMIN_DURATION_LABEL')}: <b>{duration_text}</b>\n"
        f"{t(registration.language, 'ADMIN_MONTHS_PAID_LABEL')}: <b>{registration.months_paid}</b>\n"
        f"{t(registration.language, 'ADMIN_PAYMENT_PROGRESS_LABEL')}: <b>{progress_text}</b>\n"
        f"{t(registration.language, 'ADMIN_STATUS_LABEL')}: <b>{registration.status}</b>\n"
        f"{t(registration.language, 'ADMIN_USERNAME_LABEL')}: <b>{username_text}</b>\n"
        f"{t(registration.language, 'ADMIN_USER_ID_LABEL')}: <code>{registration.telegram_user_id}</code>"
    )


@router.callback_query(F.data.startswith("admin_status:"))
async def admin_status_update_handler(callback: CallbackQuery) -> None:
    settings = get_settings()

    if callback.from_user.id not in settings.admin_ids:
        await callback.answer(t("en", "ADMIN_NOT_AUTHORIZED"), show_alert=True)
        return

    await callback.answer()

    try:
        _, registration_id_str, new_status = callback.data.split(":")
        registration_id = int(registration_id_str)
    except ValueError:
        await callback.answer("Invalid callback data.", show_alert=True)
        return

    if new_status not in ALLOWED_STATUSES:
        await callback.answer("Invalid status.", show_alert=True)
        return

    async with AsyncSessionLocal() as session:
        registration = await update_registration_status(
            session=session,
            registration_id=registration_id,
            new_status=new_status,
        )

    if registration is None:
        await callback.answer(t("en", "ADMIN_REG_NOT_FOUND"), show_alert=True)
        return

    await callback.message.edit_text(
        text=format_admin_message(registration),
        reply_markup=combined_admin_keyboard(registration.id),
    )

    try:
        await asyncio.to_thread(
            update_registration_status_in_google_sheets,
            registration.reference_code,
            registration.status,
        )
    except Exception as e:
        print(f"Google Sheets status update failed: {e}")

    try:
        await notify_student_status_update(callback.bot, registration)
    except Exception as e:
        print(f"Student status notification failed: {e}")


@router.callback_query(F.data.startswith("admin_duration:"))
async def admin_duration_update_handler(callback: CallbackQuery) -> None:
    settings = get_settings()

    if callback.from_user.id not in settings.admin_ids:
        await callback.answer(t("en", "ADMIN_NOT_AUTHORIZED"), show_alert=True)
        return

    await callback.answer()

    try:
        _, registration_id_str, duration_str = callback.data.split(":")
        registration_id = int(registration_id_str)
        duration_months = int(duration_str)
    except ValueError:
        await callback.answer("Invalid callback data.", show_alert=True)
        return

    if duration_months not in ALLOWED_DURATIONS:
        await callback.answer("Invalid duration.", show_alert=True)
        return

    async with AsyncSessionLocal() as session:
        registration = await update_course_duration(
            session=session,
            registration_id=registration_id,
            duration_months=duration_months,
        )

    if registration is None:
        await callback.answer(t("en", "ADMIN_REG_NOT_FOUND"), show_alert=True)
        return

    await callback.message.edit_text(
        text=format_admin_message(registration),
        reply_markup=combined_admin_keyboard(registration.id),
    )

    try:
        await asyncio.to_thread(
            update_course_duration_in_google_sheets,
            registration.reference_code,
            registration.course_duration_months,
        )
    except Exception as e:
        print(f"Google Sheets duration update failed: {e}")


@router.callback_query(F.data.startswith("admin_payment:"))
async def admin_payment_increment_handler(callback: CallbackQuery) -> None:
    settings = get_settings()

    if callback.from_user.id not in settings.admin_ids:
        await callback.answer(t("en", "ADMIN_NOT_AUTHORIZED"), show_alert=True)
        return

    try:
        _, registration_id_str, action = callback.data.split(":")
        registration_id = int(registration_id_str)
    except ValueError:
        await callback.answer("Invalid callback data.", show_alert=True)
        return

    if action != "increment":
        await callback.answer("Invalid payment action.", show_alert=True)
        return

    async with AsyncSessionLocal() as session:
        registration = await get_registration_by_id(session, registration_id)

        if registration is None:
            await callback.answer(t("en", "ADMIN_REG_NOT_FOUND"), show_alert=True)
            return

        if registration.course_duration_months <= 0:
            await callback.answer(t("en", "ADMIN_SET_DURATION_FIRST"), show_alert=True)
            return

        if registration.months_paid >= registration.course_duration_months:
            await callback.answer(t("en", "ADMIN_FULLY_PAID"), show_alert=True)
            return

        registration = await increment_months_paid(session, registration_id)

    await callback.answer(t("en", "ADMIN_PAYMENT_RECORDED"))

    await callback.message.edit_text(
        text=format_admin_message(registration),
        reply_markup=combined_admin_keyboard(registration.id),
    )

    try:
        await asyncio.to_thread(
            update_months_paid_in_google_sheets,
            registration.reference_code,
            registration.months_paid,
        )
    except Exception as e:
        print(f"Google Sheets months_paid update failed: {e}")