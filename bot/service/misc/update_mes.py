from datetime import date

from aiogram import Bot

from bot.database.models.groups import Groups
from bot.database.models.payments import Payments
from bot.keyboard import main_key
from bot.service.redis_serv.user import get_currency


async def update_mes(bot: Bot):

    groups: list[Groups] = Groups.select()
    query_delete_payments = Payments.delete()
    query_delete_payments.execute()

    currency = await get_currency()

    for group in groups:

        query = Groups.update(
            waiting_pay=0,
            about_pay=0,
            common_pay=0,
            percent_group=0.0,
            payment_history=None
        ).where(Groups.group_id == group.group_id)

        query.execute()

        text = f"""🌠<b>{date.today().strftime('%Y-%m-%d')} Начало работы

Курс доллара: {currency:.2f}

🆔 Айди чата: <code>{group.group_id}</code>
🧮 Процент чата: <code>0.0%</code>

⚜️ Статистика:

⏳ Ожидаем: 0р
💳 К выплате: 0р (0$)
💴 Общая сумма: 0р


💸 Выплачено: {group.paid}р ({round((float(group.paid) * currency))}$)</b>"""

        await bot.edit_message_text(
            text=text,
            reply_markup=main_key(),
            chat_id=group.group_id,
            message_id=group.message_id
        )