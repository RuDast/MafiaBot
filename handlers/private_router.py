from aiogram import Router
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart
from aiogram import F

from classes.game import Game
from classes.player import Player
from classes.vote import NightVote, DayVote
from database.database import add_new_user
from keyboards import inline
from data.config import messages
from data.roles import roles_index_list, roles_data, sheriff, mafia, lawyer, don

user_private_router = Router()
user_private_router.message.filter(F.chat.func(lambda chat: chat.type == "private"))


@user_private_router.message(CommandStart())
async def start_command(message: Message) -> None:
    await message.delete()
    pic = FSInputFile("images/italian-american-mafia.jpg")
    await message.answer_photo(pic, messages["START_MESSAGE"], reply_markup=inline.start_kb)
    await add_new_user(message)


@user_private_router.callback_query(F.data.startswith("role_"))
async def roles_pagination_callback(callback: CallbackQuery) -> None:
    index = int(callback.data.replace("role_", ""))
    await callback.message.edit_media(media=InputMediaPhoto(media=roles_index_list[index].photo,
                                                            caption=roles_index_list[index].format_message()),
                                      reply_markup=inline.roles_pagination_kb(index))


@user_private_router.callback_query(F.data == "rules_cb")
async def rules_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.message.caption != messages["RULES_MESSAGE"]:
        await callback.message.edit_caption(caption=messages["RULES_MESSAGE"], reply_markup=inline.start_kb)


@user_private_router.callback_query(F.data == "about_cb")
async def about_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.message.caption != messages["ABOUT_MESSAGE"]:
        await callback.message.edit_caption(caption=messages["ABOUT_MESSAGE"], reply_markup=inline.start_kb)


@user_private_router.callback_query(F.data == "home_cb")
async def start_callback(callback: CallbackQuery):
    await callback.answer()
    pic = FSInputFile("images/italian-american-mafia.jpg")
    await callback.message.edit_media(media=InputMediaPhoto(media=pic,
                                                            caption=messages["START_MESSAGE"]),
                                      reply_markup=inline.start_kb)

# VOTES BELOW
@user_private_router.callback_query(F.data.startswith("mafia_victim-"))
async def mafia_vote_callback(callback: CallbackQuery):
    data = callback.data.replace("mafia_victim-", "").split('-')
    game = Game.find_by_id(int(data[0]))
    victim = Player.get(int(data[1]), int(data[0]))
    mafia = Player.get(int(data[2]), int(data[0]))

    vote: NightVote = game.get_prev_night_vote(1)
    vote.mafia_vote(mafia, victim)


    # TODO если равны кол-во голосов и макс кол-во голосов, не ждать таймер
    # vote.get_votes_count() == vote.get_max_votes_count():
    # skip_waiting()

    await callback.answer(f"Ваш голос за {victim.name} успешно отдан.")
    await callback.message.delete()


@user_private_router.callback_query(F.data.startswith("don_check-"))
async def don_check_callback(callback: CallbackQuery):
    data = callback.data.replace("don_check-", "").split('-')
    game = Game.find_by_id(int(data[0]))
    player = Player.get(player_id=int(data[1]), game_id=int(game.id))

    vote: NightVote = game.get_prev_night_vote(1)
    vote.don_check = player

    if player.role == sheriff:
        await callback.answer(f"{player.name} оказался шерифом.")
    else:
        await callback.answer(f"{player.name} не является шерифом.")

    await callback.message.delete()


@user_private_router.callback_query(F.data.startswith("sheriff_check-"))
async def shreriff_check_callback(callback: CallbackQuery) -> None:
    data = callback.data.replace("sheriff_check-", "").split('-')
    game = Game.find_by_id(int(data[0]))
    player = Player.get(player_id=int(data[1]), game_id=int(game.id))

    vote: NightVote = game.get_prev_night_vote(1)
    vote.sheriff_check = player

    if player.role in [mafia, don, lawyer]:
        await callback.answer(f"{player.name} оказался мафией.")
    else:
        await callback.answer(f"{player.name} не мафия.")
    await callback.message.delete()


@user_private_router.callback_query(F.data.startswith("doctor_heal-"))
async def doctor_heal_callback(callback: CallbackQuery) -> None:
    data = callback.data.replace("doctor_heal-", "").split('-')
    game = Game.find_by_id(int(data[0]))
    player = Player.get(player_id=int(data[1]), game_id=int(game.id))

    vote: NightVote = game.get_prev_night_vote(1)
    vote.doctor_heal = player
    await callback.answer(f"Вы лечите {player.name}.")
    await callback.message.delete()


@user_private_router.callback_query(F.data.startswith("prostitute_sleep-"))
async def prostitute_sleep_callback(callback: CallbackQuery) -> None:
    data = callback.data.replace("prostitute_sleep-", "").split('-')
    game = Game.find_by_id(int(data[0]))
    player = Player.get(player_id=int(data[1]), game_id=int(game.id))

    vote: NightVote = game.get_prev_night_vote(1)
    vote.prostitute_sleep = player
    await callback.answer(f"Вы провели ночь с {player.name}")
    await callback.message.delete()


@user_private_router.callback_query(F.data.startswith("player-"))
async def player_day_vote_callback(callback: CallbackQuery) -> None:
    data = callback.data.replace("player-", "").split('-')
    game = Game.find_by_id(int(data[0]))
    selected_player = Player.get(player_id=int(data[1]), game_id=int(game.id))
    voted_player = Player.get(player_id=int(data[2]), game_id=int(game.id))

    vote: DayVote = game.get_prev_day_vote(1)
    vote.add_new_vote(voted_player, selected_player)

    await callback.answer(f"Голос за {selected_player.name} успешно отдан")
    await callback.message.delete()


@user_private_router.message()
async def unknown_message(message: Message) -> None:
    await message.delete()
