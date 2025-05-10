import asyncio
from data_base.db import database, create_tables

async def main():
    create_tables()  # создаём таблицы (один раз)
    await database.connect()  # подключаемся
    print("База данных готова ✅")
    await database.disconnect()  # отключаемся

asyncio.run(main())