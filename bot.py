import asyncio
import os
from dotenv import find_dotenv, load_dotenv
from loguru import logger

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats
from aiogram.utils.token import TokenValidationError

from handlers.private_router import user_private_router
from handlers.group_router import user_group_router
from utils.bot_commands import private_commands, group_commands
from middlewares.antiflood import AntiFloodMiddleware
from data.config import config


async def on_startup(bot: Bot) -> None:
    print('starting bot...')
    # await log_to_admins(bot, "bot start by floppa")


async def on_shutdown(bot: Bot) -> None:
    print('ending bot...')
    # await log_to_admins(bot, "bot end by floppa")


async def main() -> None:
    load_dotenv(find_dotenv())
    try:
        bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    except TokenValidationError:
        logger.error('Cannot find API_TOKEN. Shutting down...')
        return
    dp = Dispatcher(bot=bot)

    dp.message.middleware(AntiFloodMiddleware(config["ANTIFLOOD_DELAY"]))

    dp.include_router(user_private_router)
    dp.include_router(user_group_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private_commands, scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=group_commands, scope=BotCommandScopeAllGroupChats())
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logger.add('logs.log', rotation='00:00', compression='zip', retention=7)
    asyncio.run(main())
