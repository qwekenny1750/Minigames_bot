import asyncio
import os

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types

bot = Bot(token=os.getenv('TOKONGUARD'), parse_mode=ParseMode.HTML)
dp = Dispatcher()

async def main():
   await bot.delete_webhook(drop_pending_updates=True)
   await dp.start_polling()
   await bot.set_my_commands()

if __name__ == '__main__':
   asyncio.run(main())