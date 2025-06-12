from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_rb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Перейти к играм 🎮')
        ],
        [
            KeyboardButton(text='弔A Language'),
            KeyboardButton(text='Все комманды')
        ],
        [
            KeyboardButton(text='Техподдержка ⚙️')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие'
)

sending_phone = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отправить контакт', request_contact=True)]
    ],
    input_field_placeholder='Отправьте контакт',
    one_time_keyboard=True
)

roll_begin = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Начать игру\n в кости 🎲!")]
    ],
    one_time_keyboard=True
)

roll_event_roll_stop = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text='🎲'),
            KeyboardButton(text='Завершить игру\nв кубик')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Бросьте кубик!"
)

basketball_begin = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Начать матч  🏀")]
    ],
    one_time_keyboard=True
)

bascet_event_bascet_stop = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🏀'),
            KeyboardButton(text='Завершить баскетбольный\n матч')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Бросьте мяч в кольцо"
)

football_begin = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Начать матч ⚽️")]
    ],
    one_time_keyboard=True
)


football_stop_event = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='⚽️'),
            KeyboardButton(text='Завершить футбольный\n матч')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Бей пенальти"
)

city_stop = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Сдаться')]
    ],
    input_field_placeholder='Введите название города:',
    resize_keyboard=True
)