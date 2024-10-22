import json

from aiogram.types import Message

from utils.logger import notify_new_user


async def add_new_user(message: Message):
    with open("database/users.json") as file:
        users = json.load(file)["users"]
    if message.from_user.id not in users:
        users.append(message.from_user.id)
        with open("database/users.json", encoding="utf-8", mode="w") as file:
            json.dump({"users": users}, file)
        await notify_new_user(message)


def check_users():
    with open("database/users.json") as file:
        users = json.load(file)["users"]
    return users


def is_user_in_db(user_id: int) -> bool:
    users = check_users()
    return user_id in users
