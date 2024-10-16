from aiogram import types, Router
from aiogram.types import Message, PollAnswer
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram import F
from aiogram.enums import parse_mode

from common.config import rules_text

user_router = Router()
user_router.message.filter(F.chat.func(lambda chat: chat.type == "private"))

@user_router.message(CommandStart())
async def start_command(message: Message):
    await message.delete()
    await message.answer('Привет, это была команда для старта бота')

@user_router.message()
async def rules_print_command(message: Message):
    await message.delete()
    await message.answer(rules_text, parse_mode=parse_mode.ParseMode.HTML)

