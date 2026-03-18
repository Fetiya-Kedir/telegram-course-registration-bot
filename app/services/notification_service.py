from aiogram import Bot

from app.config.settings import get_settings
from app.database.models import Registration
from app.utils.i18n import t


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
        f"{t(registration.language, 'ADMIN_USERNAME_LABEL')}: <b>{username}</b>\n"
        f"{t(registration.language, 'ADMIN_USER_ID_LABEL')}: <code>{registration.telegram_user_id}</code>"
    )


async def notify_admins_new_registration(bot: Bot, registration: Registration) -> None:
    settings = get_settings()
    message_text = format_admin_registration_message(registration)

    for admin_id in settings.admin_ids:
        await bot.send_message(chat_id=admin_id, text=message_text)