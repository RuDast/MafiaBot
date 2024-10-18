from aiogram import types, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F

from database.database import check_members

user_group_router = Router()
user_group_router.message.filter(F.chat.func(lambda chat: chat.type in ["group", "supergroup"]))


@user_group_router.message(Command("start_game"))
async def start_game_command(message: Message) -> None:
    await message.delete()
    members = check_members()
    players_id = []
    players_name = []
    for member_id in members:
        try:
            user = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=member_id)
            players_id.append(member_id)
            players_name.append(dict(dict(user)["user"])["first_name"])
        except Exception as error:
            print(f"Error:\n{error}")

    await message.answer(f"В данной игре участвуют: {', '.join(players_name)}\n"
                         f"...")
