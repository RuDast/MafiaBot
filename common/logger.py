from aiogram import Bot
from aiogram.types import Message

from loguru import logger
import json


with open("common/config.json") as file:
    config = json.load(file)


async def log_to_admins(bot: Bot, text: str, log=True) -> None:
    if log:
        logger.info(text)

    try:
        await bot.send_message(config["GROUP_TO_LOG"], text, message_thread_id=config["GROUP_TO_LOG_THREAD"])
    except Exception as e:
        logger.error(e)


async def notify_new_user(message: Message) -> None:
    logger.info("Зарегистрирован новый пользователь "
                f"({message.from_user.full_name} "
                f"(link: {message.from_user.username}) #{message.from_user.id})")
    await log_to_admins(message.bot, "👤 Зарегистрирован новый пользователь "
                                     f"(<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a> "
                                     f"(link: @{message.from_user.username}) #{message.from_user.id})", False)
