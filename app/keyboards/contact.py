from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.utils.i18n import t


def contact_admin_keyboard(lang: str, admin_username: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t(lang, "CONTACT_ADMIN_BUTTON"),
                    url=f"https://t.me/{admin_username}",
                )
            ]
        ]
    )