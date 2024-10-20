from aiogram import Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram import F

from common.config import get_roles_list
from database.database import check_members, add_game_session
from classes.game_class import Game
from classes.member_class import Member
from database.database import check_members, add_new_game
from keyboards import inline

user_group_router = Router()
user_group_router.message.filter(F.chat.func(lambda chat: chat.type in ["group", "supergroup"]))


@user_group_router.message(Command("start_game"))
async def start_game_command(message: Message) -> None:
    await message.delete()

    admin = Member((await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)).user)
    game = Game(admin)

    pic = FSInputFile("images/italian-american-mafia.jpg")
    await message.answer_photo(pic, start_game_message(admin, game), reply_markup=inline.game_start_menu(game.id))


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
                                        reply_markup=inline.game_start_menu(game.id))


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
                                        reply_markup=inline.game_start_menu(game.id))


@user_group_router.callback_query(F.data.startswith('game_start_cb'))
async def game_start_cb(callback: CallbackQuery) -> None:
    game_id = int(callback.data.replace('game_start_cb-', ''))
    game = Game.get_by_id(game_id)
    admin = game.admin
    if admin.id != callback.from_user.id:
        await callback.answer("Вы не создатель игры")
        return
    await callback.answer()
    await callback.message.edit_caption(caption=str(game))
    add_new_game(game)


def start_game_message(admin: Member, game: Game):
    return (f"{admin.name} открыл набор в мафию\n"
            f"\n"
            f"Играют:\n"
            f"{'\n'.join([f'<a href="tg://user?id={player.id}">{player.name}</a>' for player in game.players])}"
            f"\n"
            f"\n"
            f"Если вы хотите учавствовать, нажмите на кнопку ниже")


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

    roles_list = get_roles_list(max(5, len(players_id)))
    shuffle(roles_list)
    roles_user = dict()
    for i in range(len(players_id)):
        roles_user[players_id[i]] = roles_list[i]
        await message.bot.send_message(players_id[i], roles_list[i])
    add_game_session(message.chat.id, roles_user)
    await message.answer(f"В данной игре участвуют: {', '.join(players_name)}\n"
                         f"...")
    return players

# def get_roles_from_users(message: Message, players: list[Member]):
#     roles_list = get_roles_list(max(config.MIN_PLAYERS_COUNT, len(players)))
#     shuffle(roles_list)
#
#     for i in range(len(players)):
#         players[i].role = roles_list[i]
#
#     return players
