from aiogram import Dispatcher

from bot.routers.chat_event import join
from bot.routers.chat_event import left
from bot.routers import menu, cancel
from bot.routers.admin import main_calculate, highlight
from bot.routers.admin.calculate_actions import plus
from bot.routers.admin.calculate_actions import minus
from bot.routers.admin.calculate_actions import minus_wait
from bot.routers.admin.calculate_actions import plus_wait


def register_all_routers(dp: Dispatcher):

    dp.include_router(join.router)
    dp.include_router(left.router)
    dp.include_router(menu.router)
    dp.include_router(main_calculate.router)
    dp.include_router(highlight.router)
    dp.include_router(plus.router)
    dp.include_router(minus.router)
    dp.include_router(minus_wait.router)
    dp.include_router(plus_wait.router)
    dp.include_router(cancel.router)
