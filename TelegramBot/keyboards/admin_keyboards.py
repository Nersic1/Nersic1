from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import os
from dotenv import load_dotenv
load_dotenv()

ADMIN_ID = os.getenv("MAIN_ADMIN_ID")
# Главное меню главного админа
def get_main_admin_panel():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить нового админа", callback_data="add_admin")],
        [InlineKeyboardButton(text="📋 Список админов", callback_data="list_admins")],
        [InlineKeyboardButton(text="❌ Удалить админа", callback_data="delete_admin")],
        [InlineKeyboardButton(text="🔙 Выход", callback_data="exit_main_admin")]
    ])
def generate_admin_delete_keyboard(admins):
    buttons = [
        [InlineKeyboardButton(text=f"Удалить ID {row['telegram_id']}", callback_data=f"confirm_delete:{row['telegram_id']}")]
        for row in admins if str(row['telegram_id']) != str(ADMIN_ID)
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons + [
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_admin_panel")]
    ])

def get_admin_panel():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📦 Создать первый заказ пользователя")],
                                        [KeyboardButton(text="🔙 Выход")],
],
            resize_keyboard=True,
            input_field_placeholder="Выберите действие"
)