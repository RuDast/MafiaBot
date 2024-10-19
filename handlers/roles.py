from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto
import os
from dotenv import find_dotenv, load_dotenv


"""Это реализация функции roles в виде отдельного бота, позже его функции будут использованы в основным боте"""

TOKEN = "8101848418:AAEb1eJ7TGBKyvthzCNROSdGTs8OhEsErxg"
bot = Bot(TOKEN)
dp = Dispatcher(bot)

# Фото я брал с пк, а не из интернета, так что нужно будет изменить путь на путь на пк который будет использоваться для запуска
# Потом как появяться фото всех ролей, программа будет дополнена

roles = [
    {"name": "Мирный житель", 
    "description": "Вы - мирный житель, ночью не просыпаетесь. Днём участвуете в голосовании.",
    "photo": "./images/roles/Mirny.png"},
    {"name": "Мафия",
     "description": "Мафия. Вы - часть группировки под началом дона. Ночью просыпаетесь и сообща выбираете игрока, которого хотите 'устранить'. Если дон в игре - он выносит решение, иначе вы принимаете решение единолично.",
     "photo": "./images/roles/Mafia.png"},
    {"name": "Дон",
     "description": "Дон. Вы - глава мафиозной группировки и именно вы по итогам обсуждения выносите решение, даже если сошки против.",
     "photo": "./images/roles/Don.png"},
    {"name": "Шериф",
     "description": "Шериф. Вы - надежда этого города. Ночью вы просыпаетесь и решаете, кого проверить на причастность к банде. Удачи в поимке мафии!",
     "photo": "./images/roles/Sheriff.png"},
    {"name": "Доктор",
     "description": "Доктор. Ночью вы просыпаетесь и выбираете, кого будете лечить. Выбранный вами игрок не может быть убитым мафией.",
     "photo": "./images/roles/Doctor.png"},
    {"name": "Любовница",
     "description": "Любовница. Вы, благодаря связям, можете дать выбранному вами игроку алиби, благодаря чему он не может быть арестован шерифом. Кроме того, счастливчик не сможет участвовать в обсуждении следующим утром.",
     "photo": "./images/roles/Putana.png"},
    {"name": "Ведущий",
     "description": "Ведущим в данной игре является AYSSAY. Наслаждайтесь игрой!",
     "photo": "./images/roles/Anchor.png"}
]

def roles_keyboard(index = 0):
    kb = InlineKeyboardMarkup(row_width = 2)
    if index > 0:
        kb.insert(InlineKeyboardButton("Назад", callback_data = f"role_{index - 1}"))
    if index < len(roles) - 1:
        kb.insert(InlineKeyboardButton("Далее", callback_data = f"role_{index + 1}"))
    return kb

@dp.message_handler(commands=["roles"])
async def send_role(message: types.Message):
    await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)

    role_name = roles[0]['name']
    role_description = roles[0]['description']
    role_photo = roles[0]['photo']

    with open(role_photo, 'rb') as role_photo_file:
        await bot.send_photo(
            chat_id = message.from_user.id,
            photo = role_photo_file,
            caption = f"<b>{role_name}</b>\n\n{role_description}",
            parse_mode = 'HTML',
            reply_markup = roles_keyboard()
        )

    await message.answer(f"Я отправил информацию по ролям в личные сообщения игроку {message.from_user.full_name}.")
     
@dp.callback_query_handler(lambda c: c.data.startswith('role_'))
async def process_callback(callback_query: CallbackQuery):
    index = int(callback_query.data[-1])
    role_name = roles[index]['name']
    role_description = roles[index]['description']
    role_photo_path = roles[index]['photo']

    with open(role_photo_path, 'rb') as photo_file:
        media = InputMediaPhoto(
            media=photo_file,
            caption=f"<b>{role_name}</b>\n\n{role_description}",
            parse_mode='HTML'
        )

        await bot.edit_message_media(
            chat_id = callback_query.from_user.id,
            message_id = callback_query.message.message_id,
            media = media,
            reply_markup = roles_keyboard(index)
        )

    await callback_query.answer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)