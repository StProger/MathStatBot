from datetime import date

from bot.database.models.payments import Payments


async def plus_amount(amount: int, username: str, group_id: int):

    user_payment = Payments.get_or_none(username=username, group_id=group_id)

    if user_payment:

        user_payment.amount += amount
        user_payment.save()

    else:

        Payments.insert(
            username=username,
            group_id=group_id,
            amount=amount,
            created_at=date.today()
        ).execute()


async def minus_amount(amount: int, username: str, group_id: int):

    user_payment = Payments.get_or_none(username=username, group_id=group_id)

    if user_payment:

        if user_payment.amount < amount:
            return "NOT MONEY"
        user_payment.amount -= amount
        user_payment.save()
    else:

        return "NOT EXIST"
