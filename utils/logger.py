from aiogram import Bot
from aiogram.types import Message, CallbackQuery

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


async def notify_new_game(message: Message, game) -> None:
    logger.info("Пользователь {} #{} создал игру №{}".format(
        game.admin.name,
        game.admin.id,
        game.id))
    await log_to_admins(message.bot,
                        text="🎮Пользователь <b>{}</b> создал игру №{}.".format(
                            '<a href="tg://user?id={}">{}</a>'.format(game.admin.id, game.admin.name),
                            game.id), log=False)


async def notify_start_game(callback: CallbackQuery, game) -> None:
    logger.info(
        "Пользователь {} #{} начал игру №{}. Игроки: {}.".format(
            game.admin.name,
            game.admin.id,
            game.id,
            ', '.join(['{} #{}'.format(
                player.name,
                player.id) for player in game.players])))

    await log_to_admins(callback.bot,
                        text="🎮Пользователь <b>{}</b> начал игру №{}.\n\nИгроки:\n{}".format(
                            '<a href="tg://user?id={}">{}</a>'.format(game.admin.id, game.admin.name),
                            game.id,
                            '\n'.join(['<a href="tg://user?id={}">{}</a> - {}'.format(
                                player.id,
                                player.name,
                                player.role.name) for player in game.players])), log=False)


async def notify_end_game(callback: CallbackQuery, game) -> None:
    logger.info(
        "Игра №{} завершилась. Игроки: {}. Победа: {}".format(
            game.id,
            ', '.join(['{} #{}'.format(
                player.name,
                player.id) for player in game.original_players]),
            game.win))

    await log_to_admins(callback.bot,
                        text="🎮Игра №{} завершилась. Игроки: {}. Победа: {}".format(
                            game.id,
                            '\n'.join(['<a href="tg://user?id={}">{}</a> - {}'.format(
                                player.id,
                                player.name,
                                player.role.name) for player in game.original_players]),
                            game.win), log=False)


async def notify_delete_game(callback: CallbackQuery, game) -> None:
    logger.info(
        "Пользователь {} #{} удалил игру №{}. Игроки: {}.".format(
            game.admin.name,
            game.admin.id,
            game.id,
            ', '.join(['{} #{}'.format(
                player.name,
                player.id) for player in game.players])))

    await log_to_admins(callback.bot,
                        text="🎮Пользователь <b>{}</b> удалил игру №{}.\n\nИгроки:\n{}".format(
                            '<a href="tg://user?id={}">{}</a>'.format(game.admin.id, game.admin.name),
                            game.id,
                            '\n'.join(['<a href="tg://user?id={}">{}</a> - {}'.format(
                                player.id,
                                player.name,
                                player.role.name) for player in game.players])), log=False)
