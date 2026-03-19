import asyncio
import re

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from app.config.settings import get_settings
from app.database.session import AsyncSessionLocal
from app.keyboards.contact import registration_handoff_keyboard
from app.keyboards.form_navigation import form_navigation_keyboard
from app.keyboards.menu import main_menu_keyboard
from app.keyboards.registration import registration_confirm_keyboard
from app.services.google_sheets_service import append_registration_to_google_sheets
from app.services.notification_service import notify_admins_new_registration
from app.services.registration_service import create_registration
from app.services.user_language import get_user_language
from app.states.registration import RegistrationForm
from app.utils.i18n import t

router = Router()


def registration_summary_text(lang: str, data: dict) -> str:
    return (
        f"<b>{t(lang, 'REG_SUMMARY_TITLE')}</b>\n\n"
        f"{t(lang, 'REG_NAME_LABEL')}: <b>{data['full_name']}</b>\n"
        f"{t(lang, 'REG_DEPARTMENT_LABEL')}: <b>{data['department']}</b>\n"
        f"{t(lang, 'REG_PHONE_LABEL')}: <b>{data['phone']}</b>\n"
        f"{t(lang, 'REG_CLASS_LABEL')}: <b>{data['class_name']}</b>\n\n"
        f"{t(lang, 'REG_CONFIRM_PROMPT')}"
    )


def is_valid_phone(phone: str) -> bool:
    cleaned = phone.strip().replace(" ", "")

    patterns = [
        r"^09\d{8}$",
        r"^07\d{8}$",
        r"^\+2519\d{8}$",
        r"^\+2517\d{8}$",
        r"^2519\d{8}$",
        r"^2517\d{8}$",
    ]

    return any(re.fullmatch(pattern, cleaned) for pattern in patterns)


def normalize_phone(phone: str) -> str:
    cleaned = phone.strip().replace(" ", "")

    if cleaned.startswith("09") or cleaned.startswith("07"):
        return "+251" + cleaned[1:]

    if cleaned.startswith("251"):
        return "+" + cleaned

    return cleaned


def is_back_command(text: str, lang: str) -> bool:
    return text == t(lang, "FORM_BACK")


def is_cancel_command(text: str, lang: str) -> bool:
    return text == t(lang, "FORM_CANCEL")


@router.callback_query(F.data.startswith("class:"))
async def start_registration_from_class(callback: CallbackQuery, state: FSMContext) -> None:
    lang = get_user_language(callback.from_user.id)
    class_id = callback.data.split(":")[1]
    class_name = t(lang, f"CLASS_{class_id}")

    await state.update_data(class_id=class_id, class_name=class_name, lang=lang)
    await state.set_state(RegistrationForm.full_name)

    await callback.message.edit_text(
        text=f"<b>{class_name}</b>\n\n{t(lang, 'REG_ASK_NAME')}"
    )

    await callback.message.answer(
        t(lang, "REG_ASK_NAME"),
        reply_markup=form_navigation_keyboard(lang),
    )

    await callback.answer()


@router.message(RegistrationForm.full_name)
async def process_full_name(message: Message, state: FSMContext) -> None:
    lang = get_user_language(message.from_user.id)

    if not message.text:
        await message.answer(
            t(lang, "REG_INVALID_TEXT"),
            reply_markup=form_navigation_keyboard(lang),
        )
        return

    if is_cancel_command(message.text, lang):
        await state.clear()
        await message.answer(
            t(lang, "FORM_CANCELLED"),
            reply_markup=main_menu_keyboard(lang),
        )
        return

    if is_back_command(message.text, lang):
        await message.answer(
            t(lang, "REG_ASK_NAME"),
            reply_markup=form_navigation_keyboard(lang),
        )
        return

    await state.update_data(full_name=message.text.strip())
    await state.set_state(RegistrationForm.department)
    await message.answer(
        t(lang, "REG_ASK_DEPARTMENT"),
        reply_markup=form_navigation_keyboard(lang),
    )


@router.message(RegistrationForm.department)
async def process_department(message: Message, state: FSMContext) -> None:
    lang = get_user_language(message.from_user.id)

    if not message.text:
        await message.answer(
            t(lang, "REG_INVALID_TEXT"),
            reply_markup=form_navigation_keyboard(lang),
        )
        return

    if is_cancel_command(message.text, lang):
        await state.clear()
        await message.answer(
            t(lang, "FORM_CANCELLED"),
            reply_markup=main_menu_keyboard(lang),
        )
        return

    if is_back_command(message.text, lang):
        await state.set_state(RegistrationForm.full_name)
        await message.answer(
            t(lang, "REG_ASK_NAME"),
            reply_markup=form_navigation_keyboard(lang),
        )
        return

    await state.update_data(department=message.text.strip())
    await state.set_state(RegistrationForm.phone)
    await message.answer(
        t(lang, "REG_ASK_PHONE"),
        reply_markup=form_navigation_keyboard(lang),
    )


@router.message(RegistrationForm.phone)
async def process_phone(message: Message, state: FSMContext) -> None:
    lang = get_user_language(message.from_user.id)

    if not message.text:
        await message.answer(
            t(lang, "REG_INVALID_TEXT"),
            reply_markup=form_navigation_keyboard(lang),
        )
        return

    if is_cancel_command(message.text, lang):
        await state.clear()
        await message.answer(
            t(lang, "FORM_CANCELLED"),
            reply_markup=main_menu_keyboard(lang),
        )
        return

    if is_back_command(message.text, lang):
        await state.set_state(RegistrationForm.department)
        await message.answer(
            t(lang, "REG_ASK_DEPARTMENT"),
            reply_markup=form_navigation_keyboard(lang),
        )
        return

    phone = message.text.strip()
    if not is_valid_phone(phone):
        await message.answer(
            t(lang, "REG_INVALID_PHONE"),
            reply_markup=form_navigation_keyboard(lang),
        )
        return

    normalized_phone = normalize_phone(phone)

    await state.update_data(phone=normalized_phone)
    data = await state.get_data()
    await state.set_state(RegistrationForm.confirm)

    await message.answer(
        registration_summary_text(lang, data),
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(
        t(lang, "REG_CONFIRM_ACTION"),
        reply_markup=registration_confirm_keyboard(lang),
    )


@router.callback_query(RegistrationForm.confirm, F.data == "reg:confirm")
async def confirm_registration(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()

    lang = get_user_language(callback.from_user.id)
    data = await state.get_data()
    settings = get_settings()

    async with AsyncSessionLocal() as session:
        registration = await create_registration(
            session=session,
            telegram_user_id=callback.from_user.id,
            telegram_username=callback.from_user.username,
            full_name=data["full_name"],
            department=data["department"],
            phone=data["phone"],
            language=data["lang"],
            class_id=data["class_id"],
            class_name=data["class_name"],
        )

    handoff_text = (
        f"<b>{t(lang, 'REG_HANDOFF_TITLE')}</b>\n\n"
        f"{t(lang, 'REG_HANDOFF_DESC')}\n\n"
        f"{t(lang, 'REG_REFERENCE_LABEL')}: <b>{registration.reference_code}</b>\n\n"
        f"{t(lang, 'REG_CONTACT_ADMIN')} "
        f"<b>@{settings.admin_username}</b>"
    )

    await callback.message.edit_text(
        text=handoff_text,
        reply_markup=registration_handoff_keyboard(lang, settings.admin_username),
    )

    await state.clear()

    try:
        await asyncio.to_thread(append_registration_to_google_sheets, registration)
    except Exception as e:
        print(f"Google Sheets append failed: {e}")

    await notify_admins_new_registration(callback.bot, registration)


@router.callback_query(F.data == "reg:cancel")
async def cancel_registration(callback: CallbackQuery, state: FSMContext) -> None:
    lang = get_user_language(callback.from_user.id)

    await state.clear()

    await callback.message.edit_text(
        text=f"{t(lang, 'REG_CANCELLED')}\n\n{t(lang, 'MAIN_MENU_PROMPT')}",
        reply_markup=main_menu_keyboard(lang),
    )
    await callback.answer()