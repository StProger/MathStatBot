from bot.filters.admin_filter import IsAdmin

from bot.routers import cancel, menu
from bot.routers.admin import highlight, main_calculate
from bot.routers.admin.calculate_actions import minus, minus_wait, percent, plus_wait, plus



def register_filters():

    cancel.router.callback_query.filter(IsAdmin())

    menu.router.callback_query.filter(IsAdmin())

    highlight.router.callback_query.filter(IsAdmin())

    main_calculate.router.callback_query.filter(IsAdmin())

    minus.router.callback_query.filter(IsAdmin())
    minus.router.message.filter(IsAdmin())

    minus_wait.router.message.filter(IsAdmin())
    minus_wait.router.callback_query.filter(IsAdmin())

    percent.router.callback_query.filter(IsAdmin())
    percent.router.message.filter(IsAdmin())

    plus_wait.router.message.filter(IsAdmin())
    plus_wait.router.callback_query.filter(IsAdmin())

    plus.router.message.filter(IsAdmin())
    plus.router.callback_query.filter(IsAdmin())