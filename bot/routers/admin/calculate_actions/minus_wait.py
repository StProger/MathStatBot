from datetime import date

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.service.redis_serv import user
from bot.database.models.groups import Groups
from bot.database.models.payments import Payments
from bot.database.api import plus_amount
from bot.keyboard import main_key
from bot.service.misc.get_list_pay import get_list_pay
from bot.service.redis_serv.user import set_users_text

router = Router()


@router.callback_query(F.data == "calculate_minus_wait")
async def get_amount(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state(f"minus_wait:get_amount")

    mes_ = await callback.message.answer(
        text="Введите сумму.",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Отмена", callback_data="cancel"
                    )
                ]
            ]
        )
    )

    await user.set_msg_to_delete(
        user_id=callback.from_user.id,
        message_id=mes_.message_id,
        chat_id=callback.message.chat.id
    )

    await callback.answer()


@router.message(StateFilter("minus_wait:get_amount"))
async def update_common_pay(message: types.Message, state: FSMContext):

    try:
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=(await user.get_msg_to_delete(
                user_id=message.from_user.id,
                chat_id=message.chat.id
            ))
        )

        await message.delete()
    except:
        pass

    amount = message.text

    if not (amount.isdigit()):
        mes_ = await message.answer("Введите сумму.")

        await user.set_msg_to_delete(
            user_id=message.from_user.id,
            message_id=mes_.message_id,
            chat_id=message.chat.id
        )
        return

    # await plus_amount(
    #     amount=int(amount),
    #     username=username,
    #     group_id=message.chat.id
    # )

    # Payments.insert(
    #     username=username,
    #     amount=int(amount),
    #     created_at=date.today(),
    #     group_id=message.chat.id
    # ).execute()

    query = Groups.update(
        waiting_pay=Groups.waiting_pay - int(amount)
    ).where(Groups.group_id == message.chat.id)

    query.execute()

    group = Groups.get(Groups.group_id == message.chat.id)

    users_text = await user.get_users_text(chat_id=message.chat.id)

    currency = float(await user.get_currency())

    if users_text:

        new_users_text = await get_list_pay(chat_id=message.chat.id)

        await set_users_text(chat_id=message.chat.id, text=new_users_text)

        history_payments = group.payment_history

        if history_payments:

            history_payments = history_payments.split(",")

            if history_payments[-1] == '':
                history_payments = history_payments[:-1]

            text_history = ""

            for payment in history_payments[:-1]:
                text_history += f"{payment}р ({round(float(payment) / currency)})\n"

            text = f"""🌠<b>{date.today().strftime('%Y-%m-%d')} Начало работы

Курс доллара: {currency:.2f}р

🆔 Айди чата: <code>{message.chat.id}</code>
🧮 Процент чата: <code>{group.percent_group}%</code>

⚜️ Статистика:

История выплат:
{text_history}

⏳ Ожидаем: {group.waiting_pay}р
💳 К выплате: {group.about_pay}р ({round(group.about_pay / currency)}$)
💴 Общая сумма: {group.common_pay}р

{new_users_text}

💸 Выплачено: {group.paid}р ({round((float(group.paid) * currency))}$)</b>"""

            await message.bot.edit_message_text(
                text=text,
                reply_markup=main_key(),
                chat_id=message.chat.id,
                message_id=group.message_id
            )
        else:

            text = f"""🌠<b>{date.today().strftime('%Y-%m-%d')} Начало работы

Курс доллара: {currency:.2f}р

🆔 Айди чата: <code>{message.chat.id}</code>
🧮 Процент чата: <code>{group.percent_group}%</code>

⚜️ Статистика:

⏳ Ожидаем: {group.waiting_pay}р
💳 К выплате: {group.about_pay}р ({round(group.about_pay / currency)}$)
💴 Общая сумма: {group.common_pay}р

{new_users_text}

💸 Выплачено: {group.paid}р ({round((float(group.paid) * currency))}$)</b>"""

            await message.bot.edit_message_text(
                text=text,
                reply_markup=main_key(),
                chat_id=message.chat.id,
                message_id=group.message_id
            )

    else:

        history_payments = group.payment_history

        if history_payments:

            history_payments = history_payments.split(",")

            if history_payments[-1] == '':
                history_payments = history_payments[:-1]

            text_history = ""

            for payment in history_payments:
                text_history += f"{payment}р ({round(float(payment) / currency)}$)\n"

            text = f"""🌠<b>{date.today().strftime('%Y-%m-%d')} Начало работы

Курс доллара: {currency:.2f}р

🆔 Айди чата: <code>{message.chat.id}</code>
🧮 Процент чата: <code>{group.percent_group}%</code>

⚜️ Статистика:

История выплат:
{text_history}

⏳ Ожидаем: {group.waiting_pay}р
💳 К выплате: {group.about_pay}р ({round(group.about_pay / currency)}$)
💴 Общая сумма: {group.common_pay}р

💸 Выплачено: {group.paid}р ({round((float(group.paid) * currency))}$)</b>"""

            await message.bot.edit_message_text(
                text=text,
                reply_markup=main_key(),
                chat_id=message.chat.id,
                message_id=group.message_id
            )
        else:

            text = f"""🌠<b>{date.today().strftime('%Y-%m-%d')} Начало работы

Курс доллара: {currency:.2f}р

🆔 Айди чата: <code>{message.chat.id}</code>
🧮 Процент чата: <code>{group.percent_group}%</code>

⚜️ Статистика:

⏳ Ожидаем: {group.waiting_pay}р
💳 К выплате: {group.about_pay}р ({round(group.about_pay / currency)}$)
💴 Общая сумма: {group.common_pay}р

💸 Выплачено: {group.paid}р ({round((float(group.paid) * currency))}$)</b>"""

            await message.bot.edit_message_text(
                text=text,
                reply_markup=main_key(),
                chat_id=message.chat.id,
                message_id=group.message_id
            )

    await state.clear()



