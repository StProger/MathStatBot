import sys

from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher, Bot

from bot.settings import settings, BOT_SCHEDULER
from bot.routers import register_all_routers
from bot import logging
from bot.database.engine import db
from bot.database.models.groups import Groups
from bot.database.models.payments import Payments
from bot.service.misc.update_mes import update_mes
from bot.filters.admin_filter import IsAdmin
from bot.filters import register_filter

import asyncio


async def main():

    storage = RedisStorage.from_url(settings.fsm_redis_url)

    dp = Dispatcher(storage=storage)

    # dp.message.filter(IsAdmin())
    # dp.callback_query.filter(IsAdmin())

    bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML", link_preview_is_disabled=True))

    register_filters()
    register_all_routers(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await logging.setup()

    BOT_SCHEDULER.add_job(update_mes, trigger="cron", hour="0", args=(bot,))
    BOT_SCHEDULER.start()

    try:

        await dp.start_polling(bot)

    except KeyboardInterrupt:
        sys.exit(1)
    finally:
        await bot.session.close()


if __name__ == '__main__':

    db.create_tables([Groups, Payments])
    asyncio.run(main())
