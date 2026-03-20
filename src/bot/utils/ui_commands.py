from aiogram import Bot
from aiogram.types import BotCommandScopeDefault, BotCommand


async def set_ui_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="🤖 Запуск бота"),
        BotCommand(command="horoscope", description="🌙 Гороскоп на сегодня"),
        BotCommand(command="compatibility", description="💞 Совместимость знаков"),
        BotCommand(command="subscribe", description="📅 Подписка на гороскоп"),
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
