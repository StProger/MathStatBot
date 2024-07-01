from aiogram.enums import ChatMemberStatus
from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
from aiogram import Bot


class IsAdmin(Filter):
    """
    Check if user is an admin
    """

    async def __call__(self, update: Message | CallbackQuery, bot: Bot) -> bool:
        try:
            group_id = None
            if isinstance(update, CallbackQuery):
                group_id = update.message.chat.id
            elif isinstance(update, Message):

                group_id = update.chat.id
            if group_id:
                user_status = (await bot.get_chat_member(
                    chat_id=group_id,
                    user_id=update.from_user.id
                )).status

                return user_status in {ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR}
        except Exception as e:

            print(e)
