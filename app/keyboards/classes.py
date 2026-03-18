from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.i18n import t


def classes_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=t(lang, "CLASS_1"), callback_data="class:1")
    builder.button(text=t(lang, "CLASS_2"), callback_data="class:2")
    builder.button(text=t(lang, "CLASS_3"), callback_data="class:3")
    builder.button(text=t(lang, "CLASS_4"), callback_data="class:4")
    builder.button(text=t(lang, "CLASS_5"), callback_data="class:5")
    builder.button(text=t(lang, "CLASS_6"), callback_data="class:6")
    builder.button(text=t(lang, "NAV_BACK_MAIN"), callback_data="menu:main")

    builder.adjust(1)
    return builder.as_markup()