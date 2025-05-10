from aiogram.fsm.state import StatesGroup, State

class OrderCreation(StatesGroup):
    telegram_id = State()
    username = State()
    item_name = State()
    price = State()
    date = State()