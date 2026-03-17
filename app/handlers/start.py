from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards.language import language_keyboard
from app.utils.i18n import t

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    lang = "en"

    text = (
        f"<b>{t(lang, 'WELCOME_TITLE')}</b>\n\n"
        f"{t(lang, 'WELCOME_DESC')}\n\n"
        f"{t(lang, 'CHOOSE_LANGUAGE')}"
    )

    await message.answer(text, reply_markup=language_keyboard())