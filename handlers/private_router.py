from aiogram import Router
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import CommandStart
from aiogram import F

import json

from database.database import add_new_member
from keyboards import inline

user_private_router = Router()
user_private_router.message.filter(F.chat.func(lambda chat: chat.type == "private"))
with open("handlers/config.json", encoding="utf-8") as file:
    config = json.load(file)


@user_private_router.message(CommandStart())
async def start_command(message: Message) -> None:
    await message.delete()
    pic = FSInputFile("images/italian-american-mafia.jpg")
    await message.answer_photo(pic, config["START_MESSAGE"], reply_markup=inline.start_kb)
    await add_new_member(message)


@user_private_router.callback_query(F.data == "roles_cb")
async def roles_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.edit_caption(caption=config["ROLES_MESSAGE"], reply_markup=inline.roles_pagination_kb(0))


@user_private_router.callback_query(F.data.startswith("role_"))
async def roles_pagination_callback(callback: CallbackQuery) -> None:
    index = int(callback.data.replace("roles_", ""))
    await callback.message.edit_caption(caption=str(index))


@user_private_router.callback_query(F.data == "rules_cb")
async def rules_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.message.caption != config["RULES_MESSAGE"]:
        await callback.message.edit_caption(caption=config["RULES_MESSAGE"], reply_markup=inline.start_kb)


@user_private_router.callback_query(F.data == "about_cb")
async def about_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.message.caption != config["ABOUT_MESSAGE"]:
        await callback.message.edit_caption(caption=config["ABOUT_MESSAGE"], reply_markup=inline.start_kb)


@user_private_router.message()
async def unknown_message(message: Message) -> None:
    await message.delete()
