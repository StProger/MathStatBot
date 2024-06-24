from datetime import date

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.service.redis_serv import user
from bot.database.models.groups import Groups
from bot.database.models.payments import Payments
from bot.keyboard import main_key


router = Router()


@router.callback_query(F.data == "calculate_minus_wait")
async def get_amount(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state(f"minus_wait:get_amount")

    mes_ = await callback.message.answer(
        text="Введите сумму и ник пользователя.",
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

    if len(message.text.split()) != 2:

        mes_ = await message.answer("Введите сумму и ник пользователя")

        await user.set_msg_to_delete(
            user_id=message.from_user.id,
            message_id=mes_.message_id,
            chat_id=message.chat.id
        )
        return

    data = message.text.split()

    if not (data[0].isdigit()):

        mes_ = await message.answer("Введите сначала сумму, потом ник пользователя\n(пример: <code>сумма ник</code>")

        await user.set_msg_to_delete(
            user_id=message.from_user.id,
            message_id=mes_.message_id,
            chat_id=message.chat.id
        )
        return

    amount = data[0]

    username = data[1]

    Payments.insert(
        username=username,
        amount=int(amount),
        created_at=date.today(),
        group_id=message.chat.id
    ).execute()

    query = Groups.update(
        common_pay=Groups.common_pay + int(amount),
        waiting_pay=Groups.waiting_pay - int(amount)
    ).where(Groups.group_id == message.chat.id)

    query.execute()

    group = Groups.get(Groups.group_id == message.chat.id)

    users_text = await user.get_users_text(chat_id=message.chat.id)

    if users_text:

        history_payments = group.payment_history

        if history_payments:

            history_payments = history_payments.split(",")

            text_history = ""

            for payment in history_payments[:-1]:
                text_history += f"{payment}<b>р</b>\n"

            text = f"""🌠<b>{date.today().strftime('%Y-%m-%d')} Начало работы

🆔 Айди чата: <code>{message.chat.id}</code>
🧮 Процент чата: <code>{group.percent_group}%</code>

⚜️ Статистика:

История выплат:
{text_history}

⏳ Ожидаем: {group.waiting_pay}р
💳 К выплате: {group.about_pay}р
💴 Общая сумма: {group.common_pay}р

{users_text}

💸 Выплачено: {group.paid} $</b>"""

            await message.bot.edit_message_text(
                text=text,
                reply_markup=main_key(),
                chat_id=message.chat.id,
                message_id=group.message_id
            )
        else:

            text = f"""🌠<b>{date.today().strftime('%Y-%m-%d')} Начало работы

🆔 Айди чата: <code>{message.chat.id}</code>
🧮 Процент чата: <code>{group.percent_group}%</code>

⚜️ Статистика:

⏳ Ожидаем: {group.waiting_pay}р
💳 К выплате: {group.about_pay}р
💴 Общая сумма: {group.common_pay}р

{users_text}

💸 Выплачено: {group.paid} $</b>"""

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

            text_history = ""

            for payment in history_payments:
                text_history += f"{payment}<b>р</b>\n"

            text = f"""🌠<b>{date.today().strftime('%Y-%m-%d')} Начало работы

🆔 Айди чата: <code>{message.chat.id}</code>
🧮 Процент чата: <code>{group.percent_group}%</code>

⚜️ Статистика:

История выплат:
{text_history}

⏳ Ожидаем: {group.waiting_pay}р
💳 К выплате: {group.about_pay}р
💴 Общая сумма: {group.common_pay}р

💸 Выплачено: {group.paid} $</b>"""

            await message.bot.edit_message_text(
                text=text,
                reply_markup=main_key(),
                chat_id=message.chat.id,
                message_id=group.message_id
            )
        else:

            text = f"""🌠<b>{date.today().strftime('%Y-%m-%d')} Начало работы

🆔 Айди чата: <code>{message.chat.id}</code>
🧮 Процент чата: <code>{group.percent_group}%</code>

⚜️ Статистика:

⏳ Ожидаем: {group.waiting_pay}р
💳 К выплате: {group.about_pay}р
💴 Общая сумма: {group.common_pay}р

💸 Выплачено: {group.paid} $</b>"""

            await message.bot.edit_message_text(
                text=text,
                reply_markup=main_key(),
                chat_id=message.chat.id,
                message_id=group.message_id
            )

    await state.clear()


