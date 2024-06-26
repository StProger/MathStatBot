from bot.database.models.payments import Payments

from peewee import *

from datetime import date


async def get_list_pay(chat_id: int):

    text = ""
    sum_pay = fn.SUM(Payments.amount).alias("sum_pay")
    query = Payments.select(Payments, sum_pay).where((Payments.group_id == chat_id)
                                                     & (Payments.created_at == date.today())).group_by(Payments.username)

    for payment in query:

        text += f"{payment.username} {payment.sum_pay}<b>р</b>\n"

    return text
