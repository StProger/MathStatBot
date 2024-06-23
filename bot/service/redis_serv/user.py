from bot.service.redis_serv.base import redis_pool


async def set_msg_to_delete(user_id: int, message_id: int, chat_id: int) -> None:
    """ Установка сообщения на удаление (пользователю) """
    await redis_pool.set(f"{chat_id}_{user_id}:msg:id", message_id)


async def get_msg_to_delete(user_id: int, chat_id: int) -> int:
    """ Получение сообщения, которое надо удалить у пользователя """
    return await redis_pool.get(f"{chat_id}_{user_id}:msg:id")


async def get_users_text(chat_id: int):

    return await redis_pool.get(f"{chat_id}:users_text")


async def set_users_text(chat_id: int, text):

    await redis_pool.set(f"{chat_id}:users_text", text)
