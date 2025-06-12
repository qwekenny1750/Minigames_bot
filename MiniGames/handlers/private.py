from aiogram import Router, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

from commands.text_answers import *
from keyboard.inline import *
from keyboard.reply_kb import *


from database.requests import *

router = Router()

@router.message(CommandStart())
@router.message(Command('menu'))
async def start_menu(message: Message):
    await set_user(message.from_user.id, f'@{message.from_user.username}')
    await message.answer(f'Превет, {message.from_user.first_name}!\n Давай сыграем в игру:', reply_markup=start_rb)

@router.message(F.text == '弔A Language')
async def choosing_language(message: Message):
    await message.answer('Выберите доступный язык:', reply_markup=inline_language)

@router.message(F.text == 'Перейти к играм 🎮')
async def choosing_game(message: Message):
    await message.answer(f"Выберите игру, в которую хотите сыграть", reply_markup=inline_games)

@router.callback_query(F.data == 'mini_games')
async def choosing_mini_game(callback: CallbackQuery):
    await callback.answer('Выберите мини-игру:')
    await callback.message.edit_text('Выберите мини-игру, в которую хотите сыграть:', reply_markup=inline_mini_game)

@router.message(Command('help'))
@router.message(F.text=='Все комманды')
async def help(message: Message):
    await message.answer(help_text)

@router.message(F.text == 'Техподдержка ⚙️')
async def sending_contact(message: Message):
    await message.answer('Отправьте свой контакт для связи с техподдержкой!\n Отправить контакт 👇', reply_markup=sending_phone)

@router.message(F.contact)
async def registr_contact(message: Message):
    await set_phone(message.from_user.id, message.contact.phone_number)
    await message.answer(technosupport_text, reply_markup=start_rb)

@router.callback_query(F.data == 'rus')
async def lang(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Поддерживаемый язык бота: Russan')


@router.message(Command('score'))
async def show_score(message: Message):
    roll_db_max_score = await stat_roll(message.from_user.id)
    bascet_db_max_score = await stat_bascet(message.from_user.id)
    football_db_max_score = await stat_football(message.from_user.id)
    city_max_db_score = await stat_city(message.from_user.id)
    score_text = f"""
    Твои максимальные очки в играх:

    <b>Игра в города:</b>  {city_max_db_score}
    <b>Игра в кубик:</b>   {roll_db_max_score}
    <b>Игра в баскетбол:</b>  {bascet_db_max_score}
    <b>Игра в бутбол:</b>   {football_db_max_score}
    """
    await message.answer(score_text)

@router.message(Command('leaderbord'))
async def leaderboard(message: Message):
    leaders_city = await set_leaderboard_city()
    leaders_roll = await set_leaderboard_roll()
    leaders_bascet = await set_leaderboard_bascetball()
    leaders_football = await set_leaderboard_football()

    text_c = "🏆 ЛИДЕРЫ ИГРЫ В ГОРОДА:\n\n"
    text_r =  "\n🏆 ЛИДЕРЫ ИГРЫ В КУБИК:\n\n"
    text_b =  "\n🏆 ЛИДЕРЫ ИГРЫ В БАСКЕТБОЛ:\n\n"
    text_f =   "\n🏆 ЛИДЕРЫ ИГРЫ В ФУТБОЛ:\n\n"
    text = text_c+text_r+text_b+text_f
    for usernamec, max_scorec in leaders_city:
        text_c += f"username: {usernamec} | наибольшие очки: {max_scorec}\n"
    for usernamer, max_scorer in leaders_roll:
        text_r += f"username: {usernamer} | наибольшие очки: {max_scorer}\n"
    for usernameb, max_scoreb in leaders_bascet:
        text_b += f"username: {usernameb} | наибольшие очки: {max_scoreb}\n"
    for usernamef, max_scoref in leaders_football:
        text_f += f"username: {usernamef} | наибольшие очки: {max_scoref}\n"
    text = text_c+text_r+text_b+text_f
    await message.answer(text=text)
