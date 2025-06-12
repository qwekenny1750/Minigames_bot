import asyncio
import os
import logging

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from handlers.handlers import router
from database.models import async_main

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
dp.include_router(router=router)

async def main():
    await async_main()
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    
asyncio.run(main())