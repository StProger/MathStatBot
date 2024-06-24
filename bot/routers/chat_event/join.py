from aiogram import F, Router, Bot, types
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER, ADMINISTRATOR
from aiogram.types import ChatMemberUpdated

from bot.database.models.groups import Groups
from bot.keyboard import main_key

from datetime import date


router = Router()
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR
    )
)
async def bot_added_as_admin(event: ChatMemberUpdated, bot: Bot):

    chat_info = await bot.get_chat(event.chat.id)

    if chat_info.permissions.can_send_messages:

        text = f"""🌠<b>{date.today().strftime('%Y-%m-%d')} Начало работы

🆔 Айди чата: <code>{event.chat.id}</code>
🧮 Процент чата: <code>0.0%</code>

⚜️ Статистика:

⏳ Ожидаем: 0р
💳 К выплате: 0р
💴 Общая сумма: 0р


💸 Выплачено: 0 $</b>"""

        mes_ = await event.answer(
            text,
            reply_markup=main_key()
        )

        await bot.pin_chat_message(
            chat_id=event.chat.id,
            message_id=mes_.message_id
        )

        Groups.insert(
            group_id=event.chat.id,
            message_id=mes_.message_id
        ).execute()
        print("Добавили")