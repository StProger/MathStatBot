from aiogram import Router, F, types
from aiogram.exceptions import TelegramBadRequest

from bot.database.models.payments import Payments
from bot.database.models.groups import Groups
from bot.keyboard import main_key
from bot.service.redis_serv import user as user_redis
from bot.service.misc.get_list_pay import get_list_pay

from datetime import date


router = Router()


@router.callback_query(F.data == "highlight")
async def highlight(callback: types.CallbackQuery):

    group: Groups = Groups.get(Groups.group_id == callback.message.chat.id)

    users_text = await get_list_pay(chat_id=callback.message.chat.id)

    if users_text == "":

        await callback.answer()
        return

    await user_redis.set_users_text(chat_id=callback.message.chat.id, text=users_text)

    text = f"""🌠<b>{date.today().strftime('%Y-%m-%d')} Начало работы

🆔 Айди чата: <code>{callback.message.chat.id}</code>
🧮 Процент чата: <code>{group.percent_group}%</code>

⚜️ Статистика:

⏳ Ожидаем: {group.waiting_pay}р
💳 К выплате: {group.about_pay}р
💴 Общая сумма: {group.common_pay}р

{users_text}

💸 Выплачено: {group.paid} $</b>"""

    try:

        await callback.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=group.message_id,
            text=text,
            reply_markup=main_key()
        )
    except TelegramBadRequest:
        await callback.answer()
        return
