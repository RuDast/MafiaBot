from aiogram.types import BotCommand

private_commands = {
    BotCommand(command='start', description='Перезапустить бота в чате'),
}

group_commands = {
    BotCommand(command='start_game', description='Запустить игру в беседе'),
    BotCommand(command='end_game', description='Завершить игру досрочно'),
    BotCommand(command='leave_game', description='Выйти с игры')
}
