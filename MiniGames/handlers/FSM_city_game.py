import asyncio
from random import choice
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from keyboard.inline import inline_city_game
from commands.text_answers import city_greeting
from keyboard.reply_kb import city_stop, start_rb
from CITY_GAME_PACK.back_handling import *
from database.requests import stat_city, set_city_score

city_router = Router()

class CityGame(StatesGroup):
    start = State()
    first_city = State()
    sharing_city = State()
    stop = State()

random_photos = ['CITY_GAME_PACK/CITY1.jpg', 'CITY_GAME_PACK/CITY2.jpg', 'CITY_GAME_PACK/CITY3.jpg']
random_photo = choice(random_photos)

phrase = ['Отлично!', 'Очень неплохо.', 'Молодец!', 'Интересный город!', 'Окей.', '', 'Хм..', 'Я долго думал, но решил взять именно этот город.', 'Замечательно!', 'Хороший ход.']


@city_router.callback_query(F.data == 'city_game')
async def city_greeting_start(callback: CallbackQuery, state: FSMContext):
    random_photo = choice(random_photos)
    await callback.answer('Начинаем игру!')
    photo = FSInputFile(random_photo)
    await callback.message.answer_photo(photo=photo, caption=city_greeting, reply_markup=inline_city_game)
    await state.set_state(CityGame.start)

@city_router.callback_query(F.data=='start_city_game')
async def start_city_event(callback: CallbackQuery, state: FSMContext):
    global first_city
    first_city = choice_city()
    await callback.answer('Игра началсь!')
    await callback.message.answer('Я начинаю игру!\nОтветь городом, начинающимся на последнюю букву моего:')
    await callback.message.answer(f'<b>{first_city}</b>', reply_markup=city_stop)
    await state.set_state(CityGame.first_city)
    await state.update_data(used_city=[])

@city_router.message(CityGame.first_city)
async def game_event(message: Message, state: FSMContext):
    random_phrase = choice(phrase)


    updated_f1w = cut_filter_word(first_city)
    input_word = CheckIsTown(message.text)
    
    if input_word() == True:
        if message.text[0].lower() == updated_f1w[-1]:
            await message.answer('Отлично!')
            
            await state.set_state(CityGame.sharing_city)
            users_word = cut_filter_word(message.text)
            output_word = WordHandlerAnswerOutput(users_word[-1])
            an_city = output_word()
            bot_city = an_city[1]
            
            await state.update_data(bot_city=bot_city)
            await message.answer(f'{random_phrase} Мой город: <b>{an_city[1].upper()}</b>\n из страны {an_city[0]}')
        else:
            await message.answer('Город начинается не с этой буквы!')
    else:
        await message.answer('Такаого города не существует. Попробуй еще раз!')

@city_router.message(CityGame.sharing_city)
async def playing(message: Message, state: FSMContext):
    random_phrase = choice(phrase)

    data = await state.get_data()
    bot_city = data.get('bot_city')
    used_city = data.get("used_city", [])
    user_score = data.get("user_score", 0)

    users_word = cut_filter_word(message.text)
    check_is_town = CheckIsTown(message.text)
    if message.text == 'Сдаться':
        await state.set_state(CityGame.stop)
        await stop_city(message, state)
    else:
        if check_is_town() == True:
            bot_city_filtered = cut_filter_word(bot_city)
            if message.text[0].lower() == bot_city_filtered[-1].lower():
                if message.text.lower() in (city.lower() for city in used_city):
                    await message.answer('Город уже использован!')
                else:
                    used_city.append(message.text)
                    output_word = WordHandlerAnswerOutput(users_word[-1])
                    while True:
                        an_city = output_word()
                        if an_city == 'GAMEOVER':
                            await message.answer("ТЫ ПОБЕДИЛ БОТА!СДЕЛАНО НЕВОЗМОЖНОЕ. ИГРА ОКНОЧЕНА\nТЕБЕ ПРИСВАЕВАЕТСЯ ЭКСКЛЮЗИВНЫЙ СТАТУС 'ПОБЕДИТЕЛЬ'")
                            user_score+=10000
                            await state.clear()
                            break
                        else:
                            if an_city[1] not in used_city:
                                bot_city = an_city[1]
                                bot_city_filtered = cut_filter_word(bot_city)
                                user_score+=1
                                await state.update_data(used_city=used_city, user_score=user_score)
                                await state.update_data(bot_city=bot_city_filtered)
                                used_city.append(bot_city)
                                await message.answer(f'{random_phrase} Мой ГОРОД: <b>{an_city[1].upper()}</b>\n из страны {an_city[0]}')
                                break
            else:
                await message.answer('Город начинается не с этой буквы!')
        else:
            await message.answer('Города не существует. Попробуй ещё раз!')

        await state.update_data(used_city=used_city, bot_city=bot_city)


async def stop_city(message: Message, state: FSMContext):

    data = await state.get_data()
    used_city = data.get('used_city', [])
    user_score = data.get('user_score', 0)
    bot_city = data.get('bot_city', 0)

    await set_city_score(message.from_user.id, f'@{message.from_user.username}', user_score)
    await message.answer("Игра завершена", reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(2)
    await state.clear()
    await message.answer(f'ВАШИ ОЧКИ: {user_score}')
    await asyncio.sleep(1)
    await message.answer("Вы вышли в главное меню",reply_markup=start_rb)


