from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_status_keyboard(registration_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Contacted", callback_data=f"admin_status:{registration_id}:contacted")
    builder.button(text="Payment Pending", callback_data=f"admin_status:{registration_id}:payment_pending")
    builder.button(text="Joined", callback_data=f"admin_status:{registration_id}:joined")
    builder.button(text="Cancelled", callback_data=f"admin_status:{registration_id}:cancelled")

    builder.adjust(2, 2)
    return builder.as_markup()


def admin_duration_keyboard(registration_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Set 2 Months", callback_data=f"admin_duration:{registration_id}:2")
    builder.button(text="Set 3 Months", callback_data=f"admin_duration:{registration_id}:3")
    builder.button(text="Set 4 Months", callback_data=f"admin_duration:{registration_id}:4")

    builder.adjust(1, 1, 1)
    return builder.as_markup()


def admin_payment_keyboard(registration_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="+1 Payment", callback_data=f"admin_payment:{registration_id}:increment")

    builder.adjust(1)
    return builder.as_markup()