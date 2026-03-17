from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def language_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="English", callback_data="lang:en")
    builder.button(text="አማርኛ", callback_data="lang:am")
    builder.adjust(2)
    return builder.as_markup()