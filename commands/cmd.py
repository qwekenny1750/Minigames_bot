from aiogram.types import BotCommand

commands = [
    BotCommand(command='start', description='Перезапустить бота'),
    BotCommand(command='menu', description='Выйти в главное меню'),
    BotCommand(command='help', description='Показать все команды'),
    BotCommand(command='score', description='Твои лучшие результаты'),
    BotCommand(command='leaderbord', description='Показать таблицу лидеров игр')
]