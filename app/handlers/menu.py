from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.menu import main_menu_keyboard
from app.keyboards.faq import faq_keyboard
from app.keyboards.classes import classes_keyboard
from app.keyboards.navigation import back_to_main_keyboard
from app.services.user_language import get_user_language
from app.config.settings import get_settings
from app.keyboards.contact import contact_admin_menu_keyboard
from app.utils.i18n import t

router = Router()


def main_menu_text(lang: str) -> str:
    return (
        f"<b>{t(lang, 'MAIN_MENU_TITLE')}</b>\n\n"
        f"{t(lang, 'MAIN_MENU_PROMPT')}"
    )


def faq_text(lang: str) -> str:
    return (
        f"<b>{t(lang, 'FAQ_TITLE')}</b>\n\n"
        f"{t(lang, 'FAQ_PROMPT')}"
    )


def class_text(lang: str) -> str:
    return (
        f"<b>{t(lang, 'CLASS_TITLE')}</b>\n\n"
        f"{t(lang, 'CLASS_PROMPT')}"
    )


@router.callback_query(F.data == "menu:main")
async def main_menu_handler(callback: CallbackQuery) -> None:
    lang = get_user_language(callback.from_user.id)

    await callback.message.edit_text(
        text=main_menu_text(lang),
        reply_markup=main_menu_keyboard(lang),
    )
    await callback.answer()


@router.callback_query(F.data == "menu:faq")
async def faq_menu_handler(callback: CallbackQuery) -> None:
    lang = get_user_language(callback.from_user.id)

    await callback.message.edit_text(
        text=faq_text(lang),
        reply_markup=faq_keyboard(lang),
    )
    await callback.answer()


@router.callback_query(F.data == "menu:register")
async def register_menu_handler(callback: CallbackQuery) -> None:
    lang = get_user_language(callback.from_user.id)

    await callback.message.edit_text(
        text=class_text(lang),
        reply_markup=classes_keyboard(lang),
    )
    await callback.answer()


@router.callback_query(F.data == "menu:contact")
async def contact_admin_handler(callback: CallbackQuery) -> None:
    lang = get_user_language(callback.from_user.id)
    settings = get_settings()

    text = (
        f"<b>{t(lang, 'CONTACT_TITLE')}</b>\n\n"
        f"{t(lang, 'CONTACT_DESC')}"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=contact_admin_menu_keyboard(lang, settings.admin_username),
    )
    await callback.answer()

@router.callback_query(F.data.startswith("faq:"))
async def faq_answer_handler(callback: CallbackQuery) -> None:
    lang = get_user_language(callback.from_user.id)
    faq_key = callback.data.split(":")[1]

    answer_map = {
        "q1": ("FAQ_Q1", "FAQ_A1"),
        "q2": ("FAQ_Q2", "FAQ_A2"),
        "q3": ("FAQ_Q3", "FAQ_A3"),
        "q4": ("FAQ_Q4", "FAQ_A4"),
    }

    q_key, a_key = answer_map[faq_key]

    text = (
        f"<b>{t(lang, q_key)}</b>\n\n"
        f"{t(lang, a_key)}"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=faq_keyboard(lang),
    )
    await callback.answer()

