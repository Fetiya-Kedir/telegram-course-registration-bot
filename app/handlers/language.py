from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.language import language_keyboard
from app.keyboards.menu import main_menu_keyboard
from app.services.user_language import set_user_language
from app.utils.i18n import t

router = Router()


def main_menu_text(lang: str) -> str:
    return (
        f"<b>{t(lang, 'MAIN_MENU_TITLE')}</b>\n\n"
        f"{t(lang, 'MAIN_MENU_PROMPT')}"
    )


def language_menu_text(lang: str = "en") -> str:
    return (
        f"<b>{t(lang, 'WELCOME_TITLE')}</b>\n\n"
        f"{t(lang, 'WELCOME_DESC')}\n\n"
        f"{t(lang, 'CHOOSE_LANGUAGE')}"
    )


@router.callback_query(F.data.startswith("lang:"))
async def language_callback_handler(callback: CallbackQuery) -> None:
    lang = callback.data.split(":")[1]
    user_id = callback.from_user.id

    set_user_language(user_id, lang)

    await callback.message.edit_text(
        text=main_menu_text(lang),
        reply_markup=main_menu_keyboard(lang),
    )
    await callback.answer()


@router.callback_query(F.data == "menu:change_language")
async def change_language_handler(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text=language_menu_text("en"),
        reply_markup=language_keyboard(),
    )
    await callback.answer()