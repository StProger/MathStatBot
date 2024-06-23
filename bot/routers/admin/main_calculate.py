from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup

router = Router()


@router.callback_query(F.data == "calculate")
async def calculate(callback: types.CallbackQuery):

    await callback.message.edit_reply_markup(
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Добавить", callback_data="calculate_plus"
                    ),
                    types.InlineKeyboardButton(
                        text="Вычесть", callback_data="calculate_minus"
                    ),
                    types.InlineKeyboardButton(
                        text="Процент", callback_data="calculate_percent"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="Добавить ожидание", callback_data="calculate_plus_wait"
                    ),
                    types.InlineKeyboardButton(
                        text="Вычесть ожидание", callback_data="calculate_minus_wait"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="Назад", callback_data="back_main"
                    )
                ]
            ]
        )
    )