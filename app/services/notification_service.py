from aiogram import Bot

from app.config.settings import get_settings
from app.database.models import Registration
from app.keyboards.admin import admin_status_keyboard, admin_duration_keyboard
from app.keyboards.student import student_main_menu_keyboard
from app.utils.i18n import t


def format_payment_progress(registration: Registration) -> str:
    if registration.course_duration_months <= 0:
        return t(registration.language, "ADMIN_DURATION_NOT_SET")

    return f"{registration.months_paid} / {registration.course_duration_months}"


def format_duration_value(registration: Registration) -> str:
    if registration.course_duration_months <= 0:
        return t(registration.language, "ADMIN_DURATION_NOT_SET")

    return f"{registration.course_duration_months} month(s)"


def format_admin_registration_message(registration: Registration) -> str:
    lang_label = "English" if registration.language == "en" else "አማርኛ"
    username = (
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
        f"{t(registration.language, 'ADMIN_DURATION_LABEL')}: <b>{format_duration_value(registration)}</b>\n"
        f"{t(registration.language, 'ADMIN_MONTHS_PAID_LABEL')}: <b>{registration.months_paid}</b>\n"
        f"{t(registration.language, 'ADMIN_PAYMENT_PROGRESS_LABEL')}: <b>{format_payment_progress(registration)}</b>\n"
        f"{t(registration.language, 'ADMIN_STATUS_LABEL')}: <b>{registration.status}</b>\n"
        f"{t(registration.language, 'ADMIN_USERNAME_LABEL')}: <b>{username}</b>\n"
        f"{t(registration.language, 'ADMIN_USER_ID_LABEL')}: <code>{registration.telegram_user_id}</code>"
    )


async def notify_admins_new_registration(bot: Bot, registration: Registration) -> None:
    settings = get_settings()
    message_text = format_admin_registration_message(registration)

    for admin_id in settings.admin_ids:
        await bot.send_message(
            chat_id=admin_id,
            text=message_text,
            reply_markup=admin_combined_keyboard(registration.id),
        )


def build_student_status_message(registration: Registration) -> str:
    lang = registration.language

    status_key_map = {
        "contacted": "STUDENT_STATUS_CONTACTED",
        "payment_pending": "STUDENT_STATUS_PAYMENT_PENDING",
        "joined": "STUDENT_STATUS_JOINED",
        "cancelled": "STUDENT_STATUS_CANCELLED",
    }

    message_key = status_key_map.get(registration.status)
    if not message_key:
        return ""

    return (
        f"<b>{t(lang, 'STUDENT_STATUS_UPDATE_TITLE')}</b>\n\n"
        f"{t(lang, message_key)}\n\n"
        f"{t(lang, 'STUDENT_STATUS_REFERENCE_LABEL')}: <b>{registration.reference_code}</b>"
    )


async def notify_student_status_update(bot: Bot, registration: Registration) -> None:
    message_text = build_student_status_message(registration)

    if not message_text:
        return

    await bot.send_message(
        chat_id=registration.telegram_user_id,
        text=message_text,
        reply_markup=student_main_menu_keyboard(registration.language),
    )


def admin_combined_keyboard(registration_id: int):
    from aiogram.types import InlineKeyboardMarkup

    status_markup = admin_status_keyboard(registration_id)
    duration_markup = admin_duration_keyboard(registration_id)

    combined_rows = status_markup.inline_keyboard + duration_markup.inline_keyboard
    return InlineKeyboardMarkup(inline_keyboard=combined_rows)