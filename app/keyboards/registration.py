from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.i18n import t


def registration_confirm_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(lang, "REG_CONFIRM"), callback_data="reg:confirm")
    builder.button(text=t(lang, "REG_CANCEL"), callback_data="reg:cancel")
    builder.adjust(2)
    return builder.as_markup()