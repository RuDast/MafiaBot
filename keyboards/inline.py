from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json


with open("config.json") as file:
    config = json.load(file)

start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🫂 Роли", callback_data='roles_cb'),
    ],
    [
        InlineKeyboardButton(text="📄 Правила", callback_data="rules_cb"),
        InlineKeyboardButton(text="🔞 О нас", callback_data="about_cb"),
    ]
])


def game_start_kb(game_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Присоединиться", callback_data=f"invite_cb-{game_id}"),
            InlineKeyboardButton(text="Отключиться", callback_data=f"leave_cb-{game_id}"),
        ],
        [
            InlineKeyboardButton(text="Начать игру", callback_data=f"game_start_cb-{game_id}")
        ]
    ])

def roles_pagination_kb(index: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️Назад", callback_data=f"role_{(index - 1) % config["MAX_ROLES_COUNT"]}"),
            InlineKeyboardButton(text="🏠", callback_data=f"home_cb"),
            InlineKeyboardButton(text="Далее▶️", callback_data=f"role_{(index + 1) % config["MAX_ROLES_COUNT"]}")
        ]
    ])
