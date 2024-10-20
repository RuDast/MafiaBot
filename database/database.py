import json

from aiogram.types import Message

from utils.logger import notify_new_user


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

def is_member_in_db(user_id: int) -> bool:
    users = check_members()
    return user_id in users


def add_game_session(game):
    with open(f"database/sessions/session_{game.id}.json", encoding="utf-8", mode="w") as file:
        json.dump(game.__dict__(), file)