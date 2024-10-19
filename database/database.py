import json

from aiogram.types import Message

from common.config import roles
from common.logger import notify_new_user, notify_new_session_game


async def add_new_member(message: Message):
    with open("database/users.json") as file:
        users = json.load(file)["users"]
    if message.from_user.id not in users:
        users.append(message.from_user.id)
        with open("database/users.json", encoding="utf-8", mode="w") as file:
            json.dump({"users": users}, file)
        await notify_new_user(message)


def check_members():
    with open("database/users.json") as file:
        users = json.load(file)["users"]
    return users

def add_game_session(chat_id, roles_users):
    chat_id = str(chat_id)
    with open("database/game_sessions.json",encoding="utf-8", mode="r") as file:
        game_sessions = json.load(file)
        game_sessions[chat_id] = {}
        for key, val in roles_users.items():
            roles_users[key] = {
                'role':val,
                'is_alive': True
            }
        game_sessions[chat_id]['users'] = roles_users
        game_sessions[chat_id]['is_finished'] = False
        game_sessions[chat_id]['winner'] = 'in_process'

        with open("database/game_sessions.json", encoding="utf-8", mode="w") as file:
            json.dump(game_sessions, file)
        notify_new_session_game(game_sessions[chat_id], chat_id)
