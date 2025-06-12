import asyncio
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database.requests import *
from keyboard.reply_kb import football_begin, football_stop_event, start_rb
from commands.text_answers import football_greeting

football_router = Router()

class Penalti(StatesGroup):
    start = State()
    kikking = State()
    stop = State()

@football_router.callback_query(F.data == 'football')
async def football_greeting_start(callback: CallbackQuery):
    await callback.answer('Начинаем соревновательное пенальти!')
    await callback.message.answer(football_greeting, reply_markup=football_begin)

@football_router.message(F.text == 'Начать матч ⚽️')
async def football_start(message: Message, state: FSMContext):
    await state.set_state(Penalti.start)
    await message.answer("Бейте мяч", reply_markup=football_stop_event)
    await state.set_state(Penalti.kikking)

@football_router.message(F.dice, StateFilter(Penalti.kikking))
async def kikking_ball(message: Message, state: FSMContext):

    data = await state.get_data()
    user_scores = data.get("user_scores", 0)
    bot_scores = data.get("bot_scores", 0)
    user_attempts = data.get("user_attempts", 0)
    bot_attempts = data.get("bot_attempts", 0)

    user_score: int = message.dice.value
    user_kikking = await message.reply("Ждем гол...", reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(4)
    await user_kikking.delete()
    if user_score in [3,4,5]:
        await message.reply('<b>ГОЛ!!</b> +1')
        user_scores+=1
    else:
        await message.reply('Промах')
    user_attempts+=1

    await asyncio.sleep(1)
    bot_kikking = await message.answer_dice(emoji='⚽️', reply_markup=ReplyKeyboardRemove())
    bot_score: int = bot_kikking.dice.value

    await asyncio.sleep(4)
    if bot_kikking.dice.value in [3,4,5]:
        await bot_kikking.reply('<b>Гол</b> противника! +1 очко противнику', reply_markup=football_stop_event)
        bot_scores+=1
    else:
        await bot_kikking.reply('Противник промахнулся', reply_markup=football_stop_event)
    bot_attempts+=1

    await state.update_data(user_scores=user_scores, bot_scores=bot_scores, user_attempts=user_attempts, bot_attempts=bot_attempts)

    if user_scores == 3 or bot_scores == 3:
        await state.set_state(Penalti.stop)
        data = await state.get_data()
        user_scores = data.get('user_scores', 0)
        bot_scores = data.get('bot_scores', 0)
        user_attempts = data.get("user_attempts", 0)
        bot_attempts = data.get("bot_attempts", 0)

        user_like_winner_scores = user_attempts
        status = "Победитель" if user_scores==3 else "Проигравший"
        await set_football_scores(message.from_user.id, f'@{message.from_user.username}', status, user_like_winner_scores)
        await message.answer(f"<b>ФУТБОЛЬНЫЙ МАТЧ ЗАВЕРШЕН</b>\n\nВы - {status},\n\n Ваши забитые пенальти за игру: {user_scores}\nЗабитые голы бота: {bot_scores}\n\n <b>Ваш итоговый результат: {user_attempts}</b>", reply_markup=ReplyKeyboardRemove())
        await message.answer("Вы вышли в главное меню", reply_markup=start_rb)
        await state.clear()

@football_router.message(F.text == 'Завершить футбольный\n матч')
async def kikking_stop(message: Message, state: FSMContext):
    await state.set_state(Penalti.stop)

    data = await state.get_data()
    user_scores = data.get('user_scores', 0)
    bot_scores = data.get('bot_scores', 0)
    user_attempts = data.get("user_attempts", 0)
    bot_attempts = data.get("bot_attempts", 0)

    await message.answer('Вы завершили игру, матч не окончен. Ваш результат не сохранен', reply_markup=ReplyKeyboardRemove())
    await message.answer('Вы вышли в главную меню', reply_markup=start_rb)
    await state.clear()
        