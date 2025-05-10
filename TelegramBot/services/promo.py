from aiogram import Bot
from random import choices
from datetime import date
from collections import Counter

from services.user_service import get_inactive_users, mark_promo_sent

PROMO_REWARDS = [
    ('Скидка 500 рублей на следующий заказ', 0.75),
    ('Скидка 750 рублей на следующий заказ', 0.5),
    ('Скидка 10%', 0.35),
    ('Скидка 20%', 0.15),
    ('Скидка 30%', 0.005),
]

def get_random_reward():
    rewards = [r[0]for r in PROMO_REWARDS] # ["Скидка 10%", "Скидка 20%", ...] вообщем данные в массиве
    weights = [r[1]for r in PROMO_REWARDS] # [0.5, 0.3, 0.15, 0.05] проценты в массиве
    return choices(rewards,weights=weights)[0] # Выбирает случайную плюшку с заданными шансами

async def promo_check(bot: Bot):
    users = await get_inactive_users()# Получаем список пользователей, не покупавших 60+ дней
    for user in users:
        print(f"{type(user)} -> {user}")
        telegram_id = user["telegram_id"]

        reward = get_random_reward()

        try:
            await  bot.send_message(
                telegram_id,
                f'Привет! Мы заметили, что давно не было покупок и решили порадовать тебя 🎁\n'
                f'Наш небольшой подарок тебе: {reward}\n'
                f'Чтобы получить её — просто нажми кнопку ниже 👇',
                reply_markup=None  # позже добавим кнопку, сейчас просто заглушка
            )

            await  mark_promo_sent(telegram_id)

        except Exception as e:
            print(f"❌ Не удалось отправить сообщение {telegram_id}: {e}")

def test_random_rewards_distribution(trials: int = 100):
    counter = Counter()
    for _ in range(trials):
        reward = get_random_reward()
        counter[reward] += 1

    print(f"\n🎲 Результаты симуляции {trials} попыток:\n")
    for reward, count in counter.items():
        percent = round(count / trials * 100, 2)
        print(f"{reward}: {count} раз ({percent}%)")

test_random_rewards_distribution(10000)