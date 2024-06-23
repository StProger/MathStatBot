from aiogram import Dispatcher

from bot.routers.chat_event import join
from bot.routers.chat_event import left
from bot.routers import menu
from bot.routers.admin import main_calculate, highlight



def register_all_routers(dp: Dispatcher):

    dp.include_router(join.router)
    dp.include_router(left.router)
    dp.include_router(menu.router)
    dp.include_router(main_calculate.router)
    dp.include_router(highlight.router)
