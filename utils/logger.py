from aiogram import Bot
from aiogram.types import Message

from loguru import logger

from data.config import config


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


def notify_new_session_game(game_session, chat_id) -> None:
    logger.info(f"Создана новая игра в чате {chat_id}: "
                f"{str(game_session)}")
