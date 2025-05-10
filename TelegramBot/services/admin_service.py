from data_base.db import database, admins
from sqlalchemy import insert, select, delete
import os
from dotenv import load_dotenv
load_dotenv()

MAIN_ADMIN_ID = int(os.getenv("MAIN_ADMIN_ID"))  # замени на свой ID

async def is_main_admin(telegram_id: int) -> bool:
    return telegram_id == MAIN_ADMIN_ID

async def add_admin(telegram_id: int):
    query = insert(admins).values(telegram_id=str(telegram_id))
    await database.execute(query)

async def get_all_admins():
    query = select(admins)
    return await database.fetch_all(query)

async def remove_admin(telegram_id: str):
    query = delete(admins).where(admins.c.telegram_id == telegram_id)
    await database.execute(query)

async def is_admin(telegram_id: int) -> bool:
    query = select(admins).where(admins.c.telegram_id == str(telegram_id))
    return await database.fetch_one(query) is not None