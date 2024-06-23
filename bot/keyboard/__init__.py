from aiogram import types


def main_key():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="🔼 Выделить", callback_data="highlight"
                ),
                types.InlineKeyboardButton(
                    text="➡️ Посчитать", callback_data="calculate_actions"
                )
            ]
        ]
    )


def calculate_key():

    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Добавить", callback_data="calculate_plus"
                ),
                types.InlineKeyboardButton(
                    text="Вычесть", callback_data="calculate_minus"
                ),
                types.InlineKeyboardButton(
                    text="Процент", callback_data="calculate_percent"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Добавить ожидание", callback_data="calculate_plus_wait"
                ),
                types.InlineKeyboardButton(
                    text="Вычесть ожидание", callback_data="calculate_minus_wait"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Назад", callback_data="back_main"
                )
            ]
        ]
    )