from aiogram import  Router
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import CommandStart
from aiogram import F

from common import config
from database.database import add_new_member
from keyboards import inline

user_private_router = Router()
user_private_router.message.filter(F.chat.func(lambda chat: chat.type == "private"))

@user_private_router.message(CommandStart())
async def start_command(message: Message) -> None:
    await message.delete()
    pic = FSInputFile("images/italian-american-mafia.jpg")
    await message.answer_photo(pic, config.START_MESSAGE, reply_markup=inline.start_menu)
    await add_new_member(message)

@user_private_router.callback_query(F.data == "roles_cb")
async def roles_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.edit_caption(caption=config.ROLES_MESSAGE, reply_markup=inline.start_menu)

@user_private_router.callback_query(F.data == "rules_cb")
async def roles_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.edit_caption(caption=config.RULES_MESSAGE, reply_markup=inline.start_menu)

@user_private_router.callback_query(F.data == "about_cb")
async def roles_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.edit_caption(caption=config.ABOUT_MESSAGE, reply_markup=inline.start_menu)

@user_private_router.message()
async def unknown_message(message: Message) -> None:
    await message.delete()
