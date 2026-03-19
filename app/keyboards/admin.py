from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_status_keyboard(registration_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Contacted", callback_data=f"admin_status:{registration_id}:contacted")
    builder.button(text="Payment Pending", callback_data=f"admin_status:{registration_id}:payment_pending")
    builder.button(text="Paid", callback_data=f"admin_status:{registration_id}:paid")
    builder.button(text="Joined", callback_data=f"admin_status:{registration_id}:joined")
    builder.button(text="Cancelled", callback_data=f"admin_status:{registration_id}:cancelled")

    builder.adjust(2, 2, 1)
    return builder.as_markup()