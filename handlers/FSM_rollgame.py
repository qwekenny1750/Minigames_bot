import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from keyboard.reply_kb import roll_begin, roll_event_roll_stop, start_rb
from commands.text_answers import roll_greeteng
from database.requests import *

roll_router = Router()

class Rolling(StatesGroup):
    start = State()
    rolling = State()
    stop = State()


@roll_router.callback_query(F.data == 'roll')
async def roll_greeting(callback: CallbackQuery):
    await callback.answer('Начинаем игру')
    await callback.message.answer(roll_greeteng, reply_markup=roll_begin)


@roll_router.message(F.text == 'Начать игру\n в кости 🎲!')
async def roll_start(message: Message, state: FSMContext):
    await state.set_state(Rolling.start)
    await message.answer("Кидай кубик", reply_markup=roll_event_roll_stop)
    await state.set_state(Rolling.rolling)


@roll_router.message(F.dice, F.dice.emoji == '🎲',  StateFilter(Rolling.rolling))
async def main_rolling_with_score(message: Message, state: FSMContext):

    data = await state.get_data()
    user_scores = data.get('user_scores', 0)
    bot_scores = data.get('bot_scores', 0)

    user_score: int = message.dice.value
    rolling = await message.reply(f"Ждем результатов...", reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(4)
    await rolling.delete()
    await message.answer(f"Твое очко: {user_score}")
    user_scores += user_score

    bot_dice = await message.answer_dice(emoji="🎲", reply_markup=ReplyKeyboardRemove())
    bot_score: int = bot_dice.dice.value
    await asyncio.sleep(4)
    await bot_dice.reply(f"Очко бота: {bot_score}", reply_markup=roll_event_roll_stop)
    bot_scores+=bot_score

    await state.update_data(user_scores=user_scores, bot_scores=bot_scores)

@roll_router.message(F.text == 'Завершить игру\nв кубик')
async def roll_stop(message: Message, state: FSMContext):
    await state.set_state(Rolling.stop)

    data = await state.get_data()
    user_scores = data.get('user_scores', 0)
    bot_scores = data.get('bot_scores', 0)
    user_like_winner_score = user_scores - bot_scores
    await set_roll_scores(message.from_user.id,f'@{message.from_user.username}', user_like_winner_score)
    await message.answer("Игра завершена", reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await message.answer(f'Вы вышли в главное меню, ваши очки: {user_like_winner_score}', reply_markup=start_rb)
    
    await state.clear()

