import asyncio
import os
import logging

from dotenv import find_dotenv, load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from commands.cmd import commands
from handlers.private import router
from handlers.FSM_rollgame import roll_router
from handlers.FSM_bascetball import basketball_router
from handlers.FSM_football import football_router
from handlers.FSM_city_game import city_router
from database.models import create_db

ALLOWED_UPDATES = ['message', 'edited_message', 'business_connection', 'business_message', 'edited_business_message', 'callback_query']

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(router)
dp.include_router(roll_router)
dp.include_router(basketball_router)
dp.include_router(football_router)
dp.include_router(city_router)


async def main():
    await create_db()
    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('aiologs_mini.log', encoding='utf-8')
    ]
    )       
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands = commands, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

if __name__ == '__main__':
    asyncio.run(main())