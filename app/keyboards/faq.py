from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.i18n import t


def faq_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=t(lang, "FAQ_Q1"), callback_data="faq:q1")
    builder.button(text=t(lang, "FAQ_Q2"), callback_data="faq:q2")
    builder.button(text=t(lang, "FAQ_Q3"), callback_data="faq:q3")
    builder.button(text=t(lang, "FAQ_Q4"), callback_data="faq:q4")
    builder.button(text=t(lang, "NAV_BACK_MAIN"), callback_data="menu:main")

    builder.adjust(1)
    return builder.as_markup()