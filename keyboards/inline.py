from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🫂 Роли", callback_data='roles_cb'),
    ],
    [
        InlineKeyboardButton(text="📄 Правила", callback_data="rules_cb"),
        InlineKeyboardButton(text="🔞 О нас", callback_data="about_cb"),
    ]
])


def game_start_menu(game_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Присоединиться", callback_data=f"invite_cb-{game_id}"),
            InlineKeyboardButton(text="Отключиться", callback_data=f"leave_cb-{game_id}"),
        ],
        [
            InlineKeyboardButton(text="Начать игру", callback_data=f"game_start_cb-{game_id}")
        ]
    ])
