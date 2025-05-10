from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from services.user_service import add_user, has_received_welcome_promo,mark_welcome_bonus_sent  # Импорт из правильного модуля
from services.promo import get_random_reward
from keyboards.user_kb import user_keyboard

user_router = Router()

@user_router.message(CommandStart())
async def start_handler(message: Message):
    telegram_id = str(message.from_user.id)
    username = message.from_user.username or "Без имени"

    # Добавляем пользователя (или обновляем, если он уже есть)
    await add_user(telegram_id, username)

    # Проверка: получал ли пользователь приветственный бонус
    bonus_received = await has_received_welcome_promo(telegram_id)

    if not bonus_received:
        await message.answer(
            f"Привет, {username} 👋 Добро пожаловать!\n"
            f"Нажми на кнопку ниже, чтобы получить приветственный бонус 🎁",
            reply_markup=user_keyboard  # Реплай клавиатура
        )
    else:
        await message.answer(
            f"Привет, {username} 👋, это бот нашего магазина. ⬇️",
            reply_markup=user_keyboard
        )

@user_router.message(F.text == "🎁Получить приветственный бонус")
async def send_welcome_bonus(message: Message):
    telegram_id = str(message.from_user.id)

    # Проверяем, получал ли бонус
    bonus_received = await has_received_welcome_promo(telegram_id)

    if not bonus_received:
        reward = get_random_reward()
        await message.answer(
            f"Поздравляем! Вот твой приветственный бонус 🎁: {reward}"
        )
        # Обновляем статус бонуса в базе
        await mark_welcome_bonus_sent(telegram_id)
    else:
        await message.answer(
            "Ты уже получил приветственный бонус! 🎉"
        )

@user_router.message(F.text == "🔍 Мой ID")
async def send_my_id(message: Message):
    await message.answer(f"Ваш Telegram ID: {message.from_user.id}")