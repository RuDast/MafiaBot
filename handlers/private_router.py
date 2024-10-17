from aiogram import  Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram import F
from aiogram.enums import parse_mode

from common.config import rules
from database.database import add_new_member

user_private_router = Router()
user_private_router.message.filter(F.chat.func(lambda chat: chat.type == "private"))

@user_private_router.message(CommandStart())
async def start_command(message: Message):
    await message.delete()
    await message.answer('Меню навигации')
    add_new_member(message.chat.id)


@user_private_router.message(Command("rules"))
async def rules_print_command(message: Message):
    await message.delete()
    await message.answer(rules, parse_mode=parse_mode.ParseMode.HTML)

