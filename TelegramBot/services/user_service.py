from datetime import date, timedelta
from sqlalchemy import select
from data_base.db import database, users

async def add_user(telegram_id: str, username: str):
    query = select(users).where(users.c.telegram_id == telegram_id)
    existing_user = await database.fetch_one(query)
#1.select(users) — выбрать всех из таблицы users 2.where(...) — но только тех, у кого telegram_id совпадает
    if existing_user:
        return

    await database.execute(
        users.insert().values(
            telegram_id=telegram_id,
            last_purchase_date=None,
            last_item=None,
            promo_sent=0
        #await database.execute если мы не нашли пользователя то создаем его в базе данных
        )
    )

async def update_purchase(telegram_id: str, item_name: str):
    await database.execute( #Выполняем SQL-запрос к базе. Так как мы используем асинхронную библиотеку databases, всё делается через await.
        users.update() #Обновляем таблицу users
        .where(users.c.telegram_id == telegram_id) #выбираем строку по Telegram ID
        .values( #задаём новые значения:
            last_purchase_date=date.today(), #сегодняшняя дата
            last_item=item_name, #какой товар
            promo_sent = 0 #обнуляем, чтобы бонус мог быть снова выслан через 2 месяца.
        )
    )

async def get_inactive_users():
    cutoff = date.today() - timedelta(days=60) # Отсечка по времени
    #cutoff = datetime.now() - timedelta(minutes=5) для проверки работоспособности бота кусок кода меняющий 60 дней на 5 минут
    query = select(users).where(
        users.c.last_purchase_date != None,  # покупка вообще была
        users.c.last_purchase_date < cutoff,  # была больше 60 дней назад
        users.c.promo_sent == 0 # промо ещё не отправлялось
    )
    return await database.fetch_all(query) # Вернёт список таких пользователей

async def mark_promo_sent(telegram_id: str):
    await database.execute( #Выполняем SQL-команду. Мы не извлекаем данные, а обновляем
        users.update() #users.update(): начинаем команду UPDATE для таблицы users.
        .where(users.c.telegram_id == telegram_id) #указываем, какую строку обновлять — по telegram_id.
        .values(promo_sent=1) # выставляем поле promo_sent в 1, что означает «отправлено».
    )

async def mark_welcome_bonus_sent(telegram_id: str):
    query = users.update().where(users.c.telegram_id == telegram_id).values(welcome_promo_sent=1)
    await database.execute(query)

async def has_received_welcome_promo(telegram_id: str) -> bool:
    query = select(users.c.welcome_promo_sent).where(users.c.telegram_id == telegram_id)
    result = await database.fetch_one(query)
    return result is not None and result["welcome_promo_sent"] == 1