from aiogram import Router, types, F


router = Router()


@router.callback_query(F.data == "back_main")
async def menu(callback: types.CallbackQuery):

    await callback.message.edit_reply_markup(
        reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(
                            text="🔼 Выделить", callback_data="highlight"
                        ),
                        types.InlineKeyboardButton(
                            text="➡️ Посчитать", callback_data="calculate"
                        )
                    ]
                ]
            )
    )