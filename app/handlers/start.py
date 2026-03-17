from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        "Welcome to DS Nursing Online Class!\n\n"
        "Please choose your preferred language."
    )
    