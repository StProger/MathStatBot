from bot.service.redis_serv.base import redis_pool


async def set_msg_to_delete(user_id: int, message_id: int, chat_id: int) -> None:
    """ Установка сообщения на удаление (пользователю) """
    await redis_pool.set(f"{chat_id}_{user_id}:msg:id", message_id)


async def get_msg_to_delete(user_id: int, chat_id: int) -> int:
    """ Получение сообщения, которое надо удалить у пользователя """
    return await redis_pool.get(f"{chat_id}_{user_id}:msg:id")


async def set_currency(value):

    await redis_pool.set(f"currency_amount", value)


async def get_currency():

    return float(await redis_pool.get(f"currency_amount"))


async def get_users_text(chat_id: int):

    users_text = await redis_pool.get(f"{chat_id}:users_text")
    if users_text == "":
        return None
    return users_text


async def set_users_text(chat_id: int, text):

    await redis_pool.set(f"{chat_id}:users_text", text)
