from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.i18n import t


def student_main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(lang, "NAV_BACK_MAIN"), callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()