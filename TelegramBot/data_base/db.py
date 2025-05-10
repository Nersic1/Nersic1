from sqlalchemy import Table, Column, Integer, String, Date, MetaData, create_engine, select
from databases import Database

DATABASE_URL = "sqlite:///users.db"
database = Database(DATABASE_URL)  # Для асинхронных запросов
engine = create_engine(DATABASE_URL)  # Для создания таблиц (однократно, sync)
# 1. Создаём объект metadata — это как чертёж, в котором будут таблицы
metadata = MetaData()


# 2. Описываем таблицу users
users = Table(
    "users",                 # Название таблицы в базе данных
    metadata,
    Column("id", Integer, primary_key=True),          # Внутренний ID записи
    Column("telegram_id", String, unique=True),  # ID пользователя в Telegram
    Column("username", String),
    Column("last_purchase_date", Date),               # Дата последней покупки
    Column("last_item", String),                      # Последний купленный товар
    Column("promo_sent", Integer, default=0),         # Был ли отправлен промо-бонус (0 — нет, 1 — да)
    Column("welcome_promo_sent", Integer, default=0),
)

admins = Table(
    "admins",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("telegram_id", String, unique=True),
)

orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("telegram_id", String),  # связка с пользователем (можно добавить ForeignKey, если хочешь)
    Column("username", String, nullable=True),
    Column("item_name", String),    # название товара
    Column("price", Integer),       # цена (в рублях, можно float если надо копейки)
    Column("order_date", Date),
    Column("created_by_admin_id", String)
)     # дата заказа

async def add_user(telegram_id: str, username: str):
    query = select(users).where(users.c.telegram_id == telegram_id)
    existing_user = await database.fetch_one(query)
    if not existing_user:
        query = users.insert().values(
            telegram_id=telegram_id,
            username=username,
            last_purchase_date=None,
            last_item=None,
            promo_sent=0
    )
    await database.execute(query)

# 4. Функция для инициализации базы (создаёт таблицы, если их нет)
def create_tables():
    metadata.create_all(engine)
