from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from classes.game import Game
from classes.player import Player
from data.config import config
from data.roles import sheriff, prostitute, maniac

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
            InlineKeyboardButton(text="◀️Назад", callback_data=f"role_{(index - 1) % config['MAX_ROLES_COUNT']}"),
            InlineKeyboardButton(text="🏠", callback_data=f"home_cb"),
            InlineKeyboardButton(text="Далее▶️", callback_data=f"role_{(index + 1) % config['MAX_ROLES_COUNT']}")
        ]
    ])


def choose_mafia_victim_kb(game: Game, mafia: Player):
    kb = []
    for victim in game.players:
        if victim.role.id in [0, 3, 5] or not victim.is_alive:
            continue
        kb.append(InlineKeyboardButton(text=f"{victim.name}", callback_data=f"mafia_victim-{game.id}-{victim.id}-{mafia.id}"))
    return InlineKeyboardMarkup(inline_keyboard=[kb])


def choose_don_check(game: Game):
    kb = []
    for player in game.players:
        if player.role.id in [0, 3, 5] or not player.is_alive:
            continue
        kb.append(InlineKeyboardButton(text=f"{player.name}", callback_data=f"don_check-{game.id}-{player.id}"))
    return InlineKeyboardMarkup(inline_keyboard=[kb])


def choose_sheriff_check(game: Game):
    kb = []
    for player in game.players:
        if player.role == sheriff or not player.is_alive:
            continue
        kb.append(InlineKeyboardButton(text=f"{player.name}", callback_data=f"sheriff_check-{game.id}-{player.id}"))
    return InlineKeyboardMarkup(inline_keyboard=[kb])

def choose_lawyer_def(game: Game):
    kb = []
    for player in game.players:
        if player.role.id in [0, 3, 5] or not player.is_alive:
            kb.append(InlineKeyboardButton(text=f"{player.name}", callback_data=f"lawyer_def-{game.id}-{player.id}"))
    return InlineKeyboardMarkup(inline_keyboard=[kb])

def choose_doctor_heal(game: Game):
    kb = []
    prev_night_vote = game.get_prev_night_vote(2)
    for player in game.players:
        if prev_night_vote is not None or not player.is_alive:
            if prev_night_vote.doctor_heal == player and player.role != prostitute:
                continue
        kb.append(InlineKeyboardButton(text=f"{player.name}", callback_data=f"doctor_heal-{game.id}-{player.id}"))
    return InlineKeyboardMarkup(inline_keyboard=[kb])

def choose_prostitute_sleep(game: Game):
    kb = []
    prev_night_vote = game.get_prev_night_vote(2)
    for player in game.players:
        if player.role == prostitute or not player.is_alive:
            continue
        if prev_night_vote is not None:
            if prev_night_vote.prostitute_sleep == player:
                continue
        kb.append(InlineKeyboardButton(text=f"{player.name}", callback_data=f"prostitute_sleep-{game.id}-{player.id}"))
    return InlineKeyboardMarkup(inline_keyboard=[kb])

def choose_maniac_victim(game: Game):
    kb = []
    for player in game.players:
        if player.role == maniac or not player.is_alive:
            continue
        kb.append(InlineKeyboardButton(text=f"{player.name}", callback_data=f"maniac_victim-{game.id}-{player.id}"))
    return InlineKeyboardMarkup(inline_keyboard=[kb])

def day_vote_kb(game: Game, vote_player: Player):
    kb = []
    for player in game.players:
        if vote_player.id == player.id or not player.is_alive:
            continue
        kb.append(InlineKeyboardButton(text=f"{player.name}", callback_data=f"player-{game.id}-{player.id}-{vote_player.id}"))
    return InlineKeyboardMarkup(inline_keyboard=[kb])
