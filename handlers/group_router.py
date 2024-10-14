from aiogram import types, Router
from aiogram.types import Message, PollAnswer
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram import F



group_router = Router()
group_router.message.filter(F.chat.func(lambda chat: chat.type in ["group", "supergroup"]))


@group_router.message()
async def newCommand(message: Message):
    await message.delete()
    await message.answer('+')
