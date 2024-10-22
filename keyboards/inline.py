from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from classes.game import Game
from data.config import config

start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🫂 Роли", callback_data='role_0'),
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


def choose_mafia_victim_kb(game: Game):
    kb = []
    for player in game.players:
        if player.role.id != 0 and player.role.id != 3 and player.role.id != 5:
            kb.append(InlineKeyboardButton(text=f"{player.name}", callback_data=f"mafia_victim-{game.id}-{player.id}"))
    return InlineKeyboardMarkup(inline_keyboard=[kb])


def choose_don_check(game: Game):
    kb = []
    for player in game.players:
        if player.role.id not in [0, 3, 5]:
            kb.append(InlineKeyboardButton(text=f"{player.name}", callback_data=f"don_check-{game.id}-{player.id}"))
    return InlineKeyboardMarkup(inline_keyboard=[kb])


def choose_sheriff_check(game: Game):
    kb = []
    for player in game.players:
        kb.append(InlineKeyboardButton(text=f"{player.name}", callback_data=f"sheriff_check-{game.id}-{player.id}"))
    return InlineKeyboardMarkup(inline_keyboard=[kb])

def choose_lawyer_def(game: Game):
    kb = []
    for player in game.players:
        if player.role.id in [0, 3, 5]:
            kb.append(InlineKeyboardButton(text=f"{player.name}", callback_data=f"lawyer_def-{game.id}-{player.id}"))
    return InlineKeyboardMarkup(inline_keyboard=[kb])

def choose_doctor_def(game: Game):
    kb = []
    for player in game.players:
        kb.append(InlineKeyboardButton(text=f"{player.name}", callback_data=f"doctor_def-{game.id}-{player.id}"))
    return InlineKeyboardMarkup(inline_keyboard=[kb])

def choose_prostitute_sleep(game: Game):
    kb = []
    for player in game.players:
        kb.append(InlineKeyboardButton(text=f"{player.name}", callback_data=f"prostitute_sleep-{game.id}-{player.id}"))
    return InlineKeyboardMarkup(inline_keyboard=[kb])

def choose_maniac_victim(game: Game):
    kb = []
    for player in game.players:
        kb.append(InlineKeyboardButton(text=f"{player.name}", callback_data=f"maniac_victim-{game.id}-{player.id}"))
    return InlineKeyboardMarkup(inline_keyboard=[kb])
