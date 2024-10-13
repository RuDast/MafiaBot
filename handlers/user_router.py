from aiogram import types, Router
from aiogram.types import Message, PollAnswer
from aiogram.filters import Command, CommandStart, StateFilter



user_router = Router()

@user_router.message(CommandStart())
async def startCommand(message: Message):
    await message.delete()
    await message.answer('Привет, это была команда для старта бота')
