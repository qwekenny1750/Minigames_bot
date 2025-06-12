from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



inline_games  = InlineKeyboardMarkup(
    inline_keyboard =[
        [InlineKeyboardButton(text='Игра в города', callback_data='city_game')],
        [InlineKeyboardButton(text='Мини-игры 🎲', callback_data='mini_games')]
    ])

inline_language = InlineKeyboardMarkup(
    inline_keyboard= [
        [
            InlineKeyboardButton(text='Руский', callback_data='rus')
        ]
    ]
)

inline_mini_game = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Игра в кубик 🎲', callback_data='roll')],
        [InlineKeyboardButton(text='Игра в баскетбол 🏀', callback_data='bascetball')],
        [InlineKeyboardButton(text='Игра в Футбол ⚽️', callback_data='football')]
    ]
)

inline_city_game = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='НАЧАТЬ ИГРУ', callback_data='start_city_game')]
    ]
)