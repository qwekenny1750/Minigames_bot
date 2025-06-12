from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import keyboard.reply as kb
import database.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Добро пожаловать в магазин кроссовок', reply_markup=kb.main)

@router.massage(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Добро пожаловать в каталог!', reply_markup=await kb.categories())

@router.callback_query(F.data.startwith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите товар по категории', reply_markup=await kb.items(callback.data.split('_')[1]))

