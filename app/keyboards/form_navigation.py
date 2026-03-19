from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.utils.i18n import t


def form_navigation_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t(lang, "FORM_BACK")),
                KeyboardButton(text=t(lang, "FORM_CANCEL")),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )