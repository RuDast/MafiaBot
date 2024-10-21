from random import shuffle

from aiogram import Router
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram import F

from database.database import check_members, add_game_session
from classes.game_class import Game, GameState
from classes.member_class import Member
from keyboards import inline
from data.roles import roles_list

user_group_router = Router()
user_group_router.message.filter(F.chat.func(lambda chat: chat.type in ["group", "supergroup"]))


@user_group_router.message(Command("start_game"))
async def start_game_command(message: Message) -> None:
    await message.delete()

    admin = Member((await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)).user)
    game = Game(admin)

    pic = FSInputFile("images/italian-american-mafia.jpg")
    await message.answer_photo(pic, start_game_message(admin, game), reply_markup=inline.game_start_kb(game.id))


@user_group_router.callback_query(F.data.startswith('invite_cb'))
async def invite_cb(callback: CallbackQuery) -> None:
    game_id = int(callback.data.replace('invite_cb-', ''))
    game = Game.get_by_id(game_id)
    cur_user = Member((await callback.bot.get_chat_member(chat_id=callback.message.chat.id,
                                                          user_id=callback.from_user.id)).user)
    if not game.add_member(cur_user):
        await callback.answer("Ошибка")
        return

    admin = game.admin
    await callback.answer()
    await callback.message.edit_caption(caption=start_game_message(admin, game),
                                        reply_markup=inline.game_start_kb(game.id))


@user_group_router.callback_query(F.data.startswith('leave_cb'))
async def leave_cb(callback: CallbackQuery) -> None:
    game_id = int(callback.data.replace('leave_cb-', ''))
    game = Game.get_by_id(game_id)
    cur_user = Member((await callback.bot.get_chat_member(chat_id=callback.message.chat.id,
                                                          user_id=callback.from_user.id)).user)

    if not game.delete_member(cur_user):
        await callback.answer("Ошибка")
        return

    admin = game.admin
    await callback.answer()
    await callback.message.edit_caption(caption=start_game_message(admin, game),
                                        reply_markup=inline.game_start_kb(game.id))


@user_group_router.callback_query(F.data.startswith('game_start_cb'))
async def game_start_cb(callback: CallbackQuery) -> None:
    game_id = int(callback.data.replace('game_start_cb-', ''))
    game = Game.get_by_id(game_id)
    admin = game.admin
    if admin.id != callback.from_user.id:
        await callback.answer("Вы не создатель игры")
        return
    if game.players_count < 2:
        await callback.answer(f"Минимальное количество игроков должно составлять 5. Вам не хватает {5-game.players_count} игроков")
        return

    await callback.answer()

    session_roles = roles_list[:game.players_count]
    shuffle(session_roles)
    for number in range(game.players_count):
        game.players[number].role = session_roles[number]
        await callback.bot.send_message(chat_id=game.players[number].id, text=game.players[number].role.name)

    game.state = GameState.started
    add_game_session(game)
    await callback.message.edit_caption(caption=game_started_message(game))



def start_game_message(admin: Member, game: Game):
    return (f"{admin.name} открыл набор в мафию\n"
            f"\n"
            f"Играют:\n"
            f"{'\n'.join([f'<a href="tg://user?id={player.id}">{player.name}</a>' for player in game.players])}"
            f"\n"
            f"\n"
            f"Если вы хотите учавствовать, нажмите на кнопку ниже")


def game_started_message(game: Game):
    return (f"Игра №{game.id} начинается\n\n"
            f"Игроки:\n"
            f"{'\n'.join([f'<a href="tg://user?id={player.id}">{player.name}</a>' for player in game.players])}"
            f"\n\n"
            f"Город засыпает...")


async def get_game_members(message: Message) -> list[Member]:
    members = check_members()
    players = []
    for member_id in members:
        try:
            user = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=member_id)
            if user.status in ['left', 'restricted', 'kicked']:
                continue
            if user not in players:
                players.append(Member(user.user))
        except Exception as error:
            print(f"Error:\n{error}")




