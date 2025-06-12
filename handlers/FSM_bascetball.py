import asyncio
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import  StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from commands.text_answers import bascet_greeting
from keyboard.reply_kb import basketball_begin, bascet_event_bascet_stop, start_rb
from database.requests import *

basketball_router = Router()

class ThrowBall(StatesGroup):
    start = State()
    throwing = State()
    stop = State()

@basketball_router.callback_query(F.data == 'bascetball')
async def bascet_greeting_start(callback: CallbackQuery):
    await callback.answer('Начинаем матч!')
    await callback.message.answer(bascet_greeting, reply_markup=basketball_begin)

@basketball_router.message(F.text == 'Начать матч  🏀')
async def bascet_start(message: Message, state: FSMContext):
    await state.set_state(ThrowBall.start)
    await message.answer("Бросай мяч первым", reply_markup=bascet_event_bascet_stop)
    await state.set_state(ThrowBall.throwing)

@basketball_router.message(F.dice, F.dice.emoji == '🏀', StateFilter(ThrowBall.throwing))
async def throwing_ball(message: Message, state: FSMContext):
    
    data = await state.get_data()
    user_scores = data.get("user_scores", 0)
    bot_scores = data.get("bot_scores", 0)
    user_attempts = data.get("user_attempts", 0)
    bot_attempts = data.get("bot_attempts", 0)

    user_score: int = message.dice.value
    user_throwing = await message.answer("Ждем попадания...", reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(5)
    await user_throwing.delete()
    if user_score in [4, 5, 6]:
        await message.reply('Попадание! +3 очка')
        user_scores+=3
    else:
        await message.reply('Промах')
    user_attempts+=1

    await asyncio.sleep(1)
    bot_throwing = await message.answer_dice(emoji='🏀', reply_markup=ReplyKeyboardRemove())
    bot_score: int = bot_throwing.dice.value

    await asyncio.sleep(5)
    if bot_throwing.dice.value in [4, 5, 6]:
        await bot_throwing.reply("Попадание! +3 очка противнику", reply_markup=bascet_event_bascet_stop)
        bot_scores+=3
    else:
        await bot_throwing.reply("Противник промахнулся!",reply_markup=bascet_event_bascet_stop)
    bot_attempts+=1

    await state.update_data(user_scores=user_scores, bot_scores=bot_scores, user_attempts=user_attempts, bot_attempts=bot_attempts)

    if bot_attempts == 6 and user_attempts == 6:
        await state.set_state(ThrowBall.stop)
        data = await state.get_data()
        user_scores = data.get('user_scores', 0)
        bot_scores = data.get('bot_scores', 0)
        user_attempts = data.get("user_attempts", 0)
        bot_attempts = data.get("bot_attempts", 0)

        user_like_winner_score = user_scores - bot_scores
        status = "Победитель" if user_scores > bot_scores else "Проигравший"
        await set_bascetball_scores(message.from_user.id,f'@{message.from_user.username}', status, user_like_winner_score)
        await message.answer(f"<b>ИГРА ЗАВЕРШЕНА!</b>\n\n Вы - {status},\nСумма ваших очков : {user_scores}\nОчки бота:{bot_scores}\n\n <b>Ваш итоговый результат: {user_like_winner_score}</b>", reply_markup=ReplyKeyboardRemove())
        await message.answer('Вы вышли в главное меню', reply_markup=start_rb)
        await state.clear()


@basketball_router.message(F.text == 'Завершить баскетбольный\n матч')
async def throw_stop(message: Message, state: FSMContext):
    await state.set_state(ThrowBall.stop)

    data = await state.get_data()
    user_scores = data.get('user_scores', 0)
    bot_scores = data.get('bot_scores', 0)
    user_attempts = data.get("user_attempts", 0)
    bot_attempts = data.get("bot_attempts", 0)

    await message.answer('Вы завершили игру, матч не окончен. Ваш результат не сохранен', reply_markup=ReplyKeyboardRemove())
    await message.answer('Вы вышли в главную меню', reply_markup=start_rb)
    await state.clear()
