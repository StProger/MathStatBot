from datetime import date

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.service.redis_serv import user as user_redis
from bot.database.models.groups import Groups
from bot.keyboard import main_key


router = Router()


@router.callback_query(F.data == "calculate_percent")
async def get_amount(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state(f"percent:get_amount")

    mes_ = await callback.message.answer(
        text="Введите процент от 1 до 100.",
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

    await user_redis.set_msg_to_delete(
        user_id=callback.from_user.id,
        message_id=mes_.message_id,
        chat_id=callback.message.chat.id
    )

    await callback.answer()


@router.message(StateFilter("percent:get_amount"))
async def update_common_pay(message: types.Message, state: FSMContext):

    try:
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=(await user_redis.get_msg_to_delete(
                user_id=message.from_user.id,
                chat_id=message.chat.id
            ))
        )

        await message.delete()
    except:
        pass


    data = message.text

    if (not (data.isdigit())) or (not (1 <= int(data) <= 100)):

        mes_ = await message.answer("Введите число от 1 до 100.")

        await user_redis.set_msg_to_delete(
            user_id=message.from_user.id,
            message_id=mes_.message_id,
            chat_id=message.chat.id
        )
        return

    percent_admin = int(data)

    percent_users = 100 - percent_admin

    """Процент:
    Пишешь процент (число)
    Этот процент уходит в прибыль от общей суммы (то есть от 100к, 15к уйдёт админам при 15%)"""

    group: Groups = Groups.get(Groups.group_id == message.chat.id)

    if group.about_pay != 0:

        history_payments = group.payment_history

        if history_payments:
            history_payments = history_payments.split(",")
            if history_payments[-1] == '':
                history_payments = history_payments[:-1]
            history_payments.append(str(group.about_pay))
            history_payments = ",".join(history_payments)
        else:
            history_payments = f"{group.about_pay},"

        query = Groups.update(payment_history=history_payments,
                              paid=group.paid + group.about_pay).where(Groups.group_id == message.chat.id)
        query.execute()
    #print(group.common_pay)
    about_pay = int(group.common_pay * (percent_users / 100))
    #print(about_pay)
    query = Groups.update(
        about_pay=about_pay,
        percent_group=float(percent_admin)
    ).where(Groups.group_id == message.chat.id)
    query.execute()
    query = Groups.update(common_pay=0).where(Groups.group_id == message.chat.id)
    query.execute()

    group = Groups.get(Groups.group_id == message.chat.id)

    users_text = await user_redis.get_users_text(chat_id=message.chat.id)

    currency = float(await user_redis.get_currency())

    if users_text:

        history_payments = group.payment_history
        #print(history_payments)

        if history_payments:

            history_payments = history_payments.split(",")
            if history_payments[-1] == '':
                history_payments = history_payments[:-1]
            #print(f"Разделённый: {history_payments}")
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
    
{users_text}
    
💸 Выплачено: {group.paid}р ({round((float(group.paid) / currency))}$)</b>"""

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

{users_text}

💸 Выплачено: {group.paid}р ({round((float(group.paid) / currency))}$)</b>"""

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
    
💸 Выплачено: {group.paid}р ({round((float(group.paid) / currency))}$)</b>"""

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

💸 Выплачено: {group.paid}р ({round((float(group.paid) / currency))}$)</b>"""

            await message.bot.edit_message_text(
                text=text,
                reply_markup=main_key(),
                chat_id=message.chat.id,
                message_id=group.message_id
            )

    await state.clear()



