from aiogram import Router, F, types
from aiogram.exceptions import TelegramBadRequest

from bot.database.models.payments import Payments
from bot.database.models.groups import Groups

from datetime import date


router = Router()


@router.callback_query(F.data == "highlight")
async def highlight(callback: types.CallbackQuery):

    users = Payments.select().where((Payments.group_id == callback.message.chat.id) &
                                    (Payments.created_at == date.today()))

    group: Groups = Groups.get(Groups.group_id == callback.message.chat.id)

    users_text = ""

    for user in users:

        user: Payments
        users_text += f"[{user.user_id}] {user.username} | {user.amount}р\n"

    text = f"""🌠<b>[{callback.from_user.first_name}] {date.today().strftime('%Y-%m-%d')}
Начало работы

🆔 Айди чата: {callback.message.chat.id}
🧮 Процент чата: {group.percent_group}%

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
    except TelegramBadRequest:
        await callback.answer()
        return
