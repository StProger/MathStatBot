from aiogram import Router, types, F
from aiogram.filters import Command, CommandObject

from bot.filters import IsAdmin
from bot.service.redis_serv.user import set_currency

router = Router()


@router.message(Command("set_dollar"), F.chat.type == "private")
async def set_dollar(message: types.Message, command: CommandObject):

    await message.delete()
    if command.args is None:

        await message.answer("Введите курс.")
    else:

        try:
            val = float(command.args.replace(",", "."))
        except ValueError:
            await message.answer("Проверьте корректность курса.")
            return

        await set_currency(val)

        await message.answer("Курс изменён.")