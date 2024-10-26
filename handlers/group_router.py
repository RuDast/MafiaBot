from random import shuffle

from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram import F

from classes.game import Game, GameState
from classes.player import Player
from keyboards import inline
from data.roles import roles_list, mafia, lawyer, don
from data.config import config
from keyboards.inline import choose_mafia_victim_kb, choose_don_check, choose_sheriff_check, choose_lawyer_def, \
    choose_doctor_heal, choose_prostitute_sleep, choose_maniac_victim, day_vote_kb

user_group_router = Router()
user_group_router.message.filter(F.chat.func(lambda chat: chat.type in ["group", "supergroup"]))


@user_group_router.message(Command("start_game"))
async def start_game_command(message: Message, bot: Bot) -> None:
    await message.delete()

    game = Game(bot, message.chat.id)
    admin = Player((await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)).user,
                   game.id)
    await game.appoint_admin(admin)

    pic = FSInputFile("images/italian-american-mafia.jpg")
    await message.answer_photo(pic, start_game_message(admin, game), reply_markup=inline.game_start_kb(game.id))


@user_group_router.callback_query(F.data.startswith('invite_cb'))
async def invite_cb(callback: CallbackQuery) -> None:
    game_id = int(callback.data.replace('invite_cb-', ''))
    try:
        game = Game.find_by_id(game_id)
        if game.state != GameState.waiting:
            await callback.answer("Игра уже началась!")
            return
        cur_user = Player((await callback.bot.get_chat_member(chat_id=callback.message.chat.id,
                                                              user_id=callback.from_user.id)).user, game_id)
    except IndexError:
        await callback.answer("Ошибка")
        return

    if not await game.add_player(cur_user, callback):
        await callback.answer("Ошибка")
        return


    admin = game.admin
    await callback.answer()
    await callback.message.edit_caption(caption=start_game_message(admin, game),
                                        reply_markup=inline.game_start_kb(game.id))


@user_group_router.callback_query(F.data.startswith('leave_cb'))
async def leave_cb(callback: CallbackQuery) -> None:
    game_id = int(callback.data.replace('leave_cb-', ''))
    try:
        game = Game.find_by_id(game_id)
        cur_user = Player((await callback.bot.get_chat_member(chat_id=callback.message.chat.id,
                                                              user_id=callback.from_user.id)).user, game_id)
    except IndexError:
        await callback.answer("Ошибка")
        return

    if not game.remove_player(cur_user):
        await callback.answer("Ошибка")
        return

    admin = game.admin
    await callback.answer()
    await callback.message.edit_caption(caption=start_game_message(admin, game),
                                        reply_markup=inline.game_start_kb(game.id))


@user_group_router.callback_query(F.data.startswith('game_start_cb'))
async def game_start_cb(callback: CallbackQuery) -> None:
    game_id = int(callback.data.replace('game_start_cb-', ''))
    game = Game.find_by_id(game_id)
    admin = game.admin
    if admin.id != callback.from_user.id:
        await callback.answer("Вы не создатель игры")
        return
    if len(game.players) < config['MIN_PLAYERS']:
        await callback.answer(
            f"Минимальное количество игроков - {config['MIN_PLAYERS']}. Вам не хватает {config['MIN_PLAYERS'] - len(game.players)} игроков")
        return

    session_roles = roles_list[:len(game.players)]
    shuffle(session_roles)

    for i in range(len(game.players)):
        game.players[i].role = session_roles[i]
        await callback.bot.send_photo(chat_id=game.players[i].id,
                                      photo=game.players[i].role.photo,
                                      caption=f"Твоя роль в игре - {game.players[i].role.format_message()}")

    await game.start()

    await callback.answer()
    await callback.message.edit_caption(caption=game_started_message(game))

    await night(callback, game)


async def night(callback: CallbackQuery, game: Game) -> None:
    game.create_night_vote()
    await callback.message.answer(text="Город засыпает.....")

    for player in game.players:
        if player.role.id in [0, 3]:  # MAFIA
            message = ""
            mafia_players = [i for i in game.players if i.role.id == 0 and i.is_alive]
            if len(mafia_players) > 1:
                other_mafia = ', '.join(
                    [f'<a href="tg://user?id={i.id}">'
                     f'{"🐺" if i.role.id == 3 else "⚖️" if i.role.id == 5 else ""}{i.name}'
                     f'</a>'
                     for i in game.players if i.role.id == 0 and i.is_alive and i != player])
                message += f"Ваши союзники: {other_mafia}\n"
            message += "Выберите жертву:"
            await callback.bot.send_message(player.id, message, reply_markup=choose_mafia_victim_kb(game, player))

        if player.role.id == 2:  # PROSTITUTE
            message = "Выберите игрока, с которым хотите переспать:"
            await callback.bot.send_message(player.id, message, reply_markup=choose_prostitute_sleep(game))

        if player.role.id == 3:  # DON
            message = "Выберите игрока, которого вы хотите проверить:"
            await callback.bot.send_message(player.id, message, reply_markup=choose_don_check(game))

        if player.role.id == 4:  # SHERIFF
            message = "Выберите игрока, которого вы хотите проверить:"
            await callback.bot.send_message(player.id, message, reply_markup=choose_sheriff_check(game))

        if player.role.id == 5:  # LAWYER
            message = "Выберите игрока, которого вы хотите защитить:"
            await callback.bot.send_message(player.id, message, reply_markup=choose_lawyer_def(game))

        if player.role.id == 6:  # DOCTOR
            message = "Выберите игрока, которого вы хотите спасти:"
            await callback.bot.send_message(player.id, message, reply_markup=choose_doctor_heal(game))

        if player.role.id == 7:  # MANIAC
            message = "Выберите игрока, вы хотите убить:"
            await callback.bot.send_message(player.id, message, reply_markup=choose_maniac_victim(game))

        if player.role.id == 8:  # SERGEANT
            sheriffs = [i for i in game.players if i.role.id == 4 and i.is_alive]
            if len(sheriffs) == 0:
                message = "Выберите игрока, которого вы хотите защитить:"
                await callback.bot.send_message(player.id, message, reply_markup=choose_sheriff_check(game))

    await game.goto_morning(callback)

    if game.mafia_team_count() >= game.civilian_team_count():
        game.state = GameState.ended
        await callback.message.answer(f"Мафия победила!\n\nУчастники команды мафии:"
                                      f"{', '.join([f'{player.name}' for player in game.players if player.role in [mafia, don, lawyer]])}")
        game.instances.remove(game)
    else:
        await day(callback=callback, game=game)


async def day(callback: CallbackQuery, game: Game) -> None:
    game.create_day_vote()

    for player in game.players:
        if not player.is_alive:
            continue
        await callback.bot.send_message(chat_id=player.id,
                                        text="Дневное голосование\nВыберите игрока, которого хотите исключить",
                                        reply_markup=day_vote_kb(game, player))

    await game.goto_night(callback=callback)

    if game.mafia_team_count() == 0:
        game.state = GameState.ended
        await callback.message.answer(f"Мирные жители выиграли!\n\nУчастники команды мафии: {', '.join([f'{player.name}' for player in game.players if player.role in [mafia, don, lawyer]])}")
        game.instances.remove(game)
    elif game.mafia_team_count() == game.civilian_team_count():
        game.state = GameState.ended
        await callback.message.answer(f"Мафия победила!\n\nУчастники команды мафии: {', '.join([f'{player.name}' for player in game.players if player.role in [mafia, don, lawyer]])}")
        game.instances.remove(game)

    else:
        await night(callback, game)




def start_game_message(admin: Player, game: Game) -> str:
    return "{} открыл набор в мафию\n\nИграют:\n{}\n\nЕсли вы хотите учавствовать, нажмите на кнопку ниже".format(
        admin.name,
        "\n".join([f'<a href="tg://user?id={player.id}">{player.name}</a>' for player in game.players]))


def game_started_message(game: Game) -> str:
    return "Игра №{} начинается\n\nИгроки:\n{}\n\nРоли были распределены.".format(
        game.id,
        '\n'.join(['<a href="tg://user?id={}">{}</a>'.format(
            player.id,
            player.name
        ) for player in game.players])
    )
