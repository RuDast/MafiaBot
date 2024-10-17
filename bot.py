import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats
from dotenv import find_dotenv, load_dotenv

from handlers.private_router import user_private_router
from handlers.group_router import user_group_router
from common.bot_commands import private_commands, group_commands

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)
dp.include_router(user_private_router)
dp.include_router(user_group_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private_commands, scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=group_commands, scope=BotCommandScopeAllGroupChats())
    await dp.start_polling(bot, allowed_updates=['message'])


if __name__ == '__main__':
    asyncio.run(main())