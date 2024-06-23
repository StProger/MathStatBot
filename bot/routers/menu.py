from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from bot.keyboard import main_key

router = Router()


@router.callback_query(F.data == "back_main")
async def menu(callback: types.CallbackQuery, state: FSMContext):

    await state.clear()
    await callback.message.edit_reply_markup(
        reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=main_key()
            )
    )