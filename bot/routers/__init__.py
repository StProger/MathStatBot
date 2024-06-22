from aiogram import Dispatcher

from bot.routers.chat_event import join
from bot.routers.chat_event import left


def register_all_routers(dp: Dispatcher):

    dp.include_router(join.router)
    dp.include_router(left.router)
