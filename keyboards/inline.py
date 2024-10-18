from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🫂 Роли", callback_data='roles_cb'),
    ],
    [
        InlineKeyboardButton(text="📄 Правила", callback_data="rules_cb"),
        InlineKeyboardButton(text="🔞 О нас", callback_data="about_cb"),
    ]
])