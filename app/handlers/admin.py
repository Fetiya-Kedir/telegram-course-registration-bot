import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.config.settings import get_settings
from app.database.session import AsyncSessionLocal
from app.keyboards.admin import admin_status_keyboard
from app.services.google_sheets_service import update_registration_status_in_google_sheets
from app.services.registration_service import update_registration_status
from app.utils.i18n import t

router = Router()


ALLOWED_STATUSES = {
    "contacted",
    "payment_pending",
    "paid",
    "joined",
    "cancelled",
}


def format_status_label(status: str) -> str:
    return status.replace("_", " ").title()


@router.callback_query(F.data.startswith("admin_status:"))
async def admin_status_update_handler(callback: CallbackQuery) -> None:
    settings = get_settings()

    if callback.from_user.id not in settings.admin_ids:
        await callback.answer(t("en", "ADMIN_NOT_AUTHORIZED"), show_alert=True)
        return

    # Acknowledge the click immediately for smoother Telegram UX.
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

    updated_text = (
        f"<b>{t(registration.language, 'ADMIN_NEW_REG_TITLE')}</b>\n\n"
        f"{t(registration.language, 'ADMIN_REFERENCE_LABEL')}: <b>{registration.reference_code}</b>\n"
        f"{t(registration.language, 'ADMIN_NAME_LABEL')}: <b>{registration.full_name}</b>\n"
        f"{t(registration.language, 'ADMIN_DEPARTMENT_LABEL')}: <b>{registration.department}</b>\n"
        f"{t(registration.language, 'ADMIN_PHONE_LABEL')}: <b>{registration.phone}</b>\n"
        f"{t(registration.language, 'ADMIN_CLASS_LABEL')}: <b>{registration.class_name}</b>\n"
        f"{t(registration.language, 'ADMIN_LANGUAGE_LABEL')}: <b>{'English' if registration.language == 'en' else 'አማርኛ'}</b>\n"
        f"{t(registration.language, 'ADMIN_STATUS_LABEL')}: <b>{registration.status}</b>\n"
        f"{t(registration.language, 'ADMIN_USERNAME_LABEL')}: "
        f"<b>{'@' + registration.telegram_username if registration.telegram_username else t(registration.language, 'ADMIN_USERNAME_MISSING')}</b>\n"
        f"{t(registration.language, 'ADMIN_USER_ID_LABEL')}: <code>{registration.telegram_user_id}</code>"
    )

    # Update the admin message promptly.
    await callback.message.edit_text(
        text=updated_text,
        reply_markup=admin_status_keyboard(registration.id),
    )

    # Sync Sheets in a thread so it does not block the bot.
    try:
        await asyncio.to_thread(
            update_registration_status_in_google_sheets,
            registration.reference_code,
            registration.status,
        )
    except Exception as e:
        print(f"Google Sheets status update failed: {e}")