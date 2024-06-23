from aiogram import Dispatcher

from bot.routers.chat_event import join
from bot.routers.chat_event import left
from bot.routers import menu
from bot.routers.admin import main_calculate, highlight
from bot.routers.admin.calculate_actions import plus


def register_all_routers(dp: Dispatcher):

    dp.include_router(join.router)
    dp.include_router(left.router)
    dp.include_router(menu.router)
    dp.include_router(main_calculate.router)
    dp.include_router(highlight.router)
    dp.include_router(plus.router)
