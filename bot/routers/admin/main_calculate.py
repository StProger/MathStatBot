from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup

from bot.keyboard import calculate_key

router = Router()


@router.callback_query(F.data == "calculate_actions")
async def calculate(callback: types.CallbackQuery):

    await callback.message.edit_reply_markup(
        reply_markup=calculate_key()
    )