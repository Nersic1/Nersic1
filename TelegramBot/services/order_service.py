from data_base.db import database, orders, users
from sqlalchemy import select
from datetime import date

async def create_order(telegram_id: str, username: str, item_name: str, price: int, date_value: date, admin_id: str):
    # 1. Вставляем заказ в таблицу orders
    query = orders.insert().values(
        telegram_id=telegram_id,
        username=username,
        item_name=item_name,
        price=price,
        order_date=date_value,
        created_by_admin_id=admin_id
    )
    await database.execute(query)

    # 2. Обновляем дату последней покупки в таблице users
    query_check_user = select(users).where(users.c.telegram_id == telegram_id)
    user = await database.fetch_one(query_check_user)

    if user:
        update_query = (
            users.update()
            .where(users.c.telegram_id == telegram_id)
            .values(
                last_purchase_date=date_value,
                last_item=item_name,
                promo_sent=0  # сбрасываем флаг — можно снова получать бонус через 2 месяца
            )
        )
        update_query = users.update().where(users.c.telegram_id == telegram_id).values(
            last_purchase_date=date_value,
            last_item=item_name
        )
        await database.execute(update_query)

async def get_orders_for_user(telegram_id: str):
    query = select(orders).where(orders.c.telegram_id == telegram_id)
    return await database.fetch_all(query)

async def get_orders_for_admin(admin_id: str):
    query = select(orders).where(orders.c.created_by_admin_id == admin_id)
    return await database.fetch_all(query)