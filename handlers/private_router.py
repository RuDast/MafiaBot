from aiogram import Router
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart
from aiogram import F

from classes.game import Game
from classes.player import Player
from classes.vote import NightVote
from database.database import add_new_user
from keyboards import inline
from data.config import messages
from data.roles import roles_index_list

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
    player = Player.get(int(data[1]), int(data[0]))

    vote: NightVote = game.get_last_vote()
    vote.mafia_vote(player)

    # TODO если равны кол-во голосов и макс кол-во голосов, не ждать таймер
    # vote.get_votes_count() == vote.get_max_votes_count():
    # skip_waiting()

    await callback.answer("🆗")
    await callback.message.answer(f"Ваш голос в {player.name} успешно отдан.")

# и так далее

@user_private_router.message()
async def unknown_message(message: Message) -> None:
    await message.delete()


