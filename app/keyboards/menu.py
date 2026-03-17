from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.i18n import t


def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(lang, "MENU_REGISTER"), callback_data="menu:register")
    builder.button(text=t(lang, "MENU_FAQ"), callback_data="menu:faq")
    builder.button(text=t(lang, "MENU_CONTACT_ADMIN"), callback_data="menu:contact")
    builder.button(text=t(lang, "MENU_CHANGE_LANGUAGE"), callback_data="menu:change_language")
    builder.adjust(1)
    return builder.as_markup()