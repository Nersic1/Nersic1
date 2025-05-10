from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup

user_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔍 Мой ID"),
        KeyboardButton(text="🎁Получить приветственный бонус")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
