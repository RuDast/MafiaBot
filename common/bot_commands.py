from aiogram.types import BotCommand

private_commands = {
    BotCommand(command='start', description='Перезапустить бота в чате'),
    BotCommand(command='rules', description='Получить правила игры'),

}

group_commands = {
    BotCommand(command='start_game', description='Запустить игру в беседе')
}