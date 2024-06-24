from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

router = Router()


@router.callback_query(StateFilter("*"), F.data == "cancel")
async def cancel(callback: types.CallbackQuery, state: FSMContext):

    await state.clear()
    await callback.message.delete()
