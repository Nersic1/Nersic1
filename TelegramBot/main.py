import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

from services.promo import promo_check
from services.user_service import get_inactive_users
from data_base.db import database, create_tables
from handlers.user_handlers import user_router
from handlers.admin_handlers import admin_router
from handlers.order_handlers import order_router


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
main_admin_id = int(os.getenv("MAIN_ADMIN_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(user_router)
dp.include_router(admin_router)
dp.include_router(order_router)

async def periodic_check():
    while True:
        print('я запустился и считаю 60 секунд')
        await promo_check(bot)
        await asyncio.sleep(60)

async def on_startup():
    create_tables()
    await database.connect()
    asyncio.create_task(periodic_check())
    print("Бот запущен, база подключена ✅")

async def on_shutdown():
    await database.disconnect()
    print("Бот выключен, база отключена❌")
print("🟢 main() запустился")
async def main():

    await on_startup()
# register_all_handlers(dp)  # добавим позже
# Запускаем проверку промо (в будущем можно вынести в планировщик)

    print("🚀 Бот начинает polling...")

    await dp.start_polling(bot, skip_updates=True)
    await on_shutdown()
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Пизда он вырублен')
