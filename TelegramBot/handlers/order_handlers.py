from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import date

from services.order_service import create_order
from keyboards.admin_keyboards import get_admin_panel

order_router = Router()

class OrderFSM(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_username = State()
    waiting_for_item_name = State()
    waiting_for_price = State()
    waiting_for_date = State()

@order_router.message(F.text == "📦 Создать первый заказ пользователя")
async def start_order_creation(message: Message, state: FSMContext):
    await state.set_state(OrderFSM.waiting_for_user_id)
    await message.answer("Введите telegram_id пользователя:")

@order_router.message(OrderFSM.waiting_for_user_id)
async def order_user_id_entered(message: Message, state: FSMContext):
    await state.update_data(telegram_id=message.text)
    await state.set_state(OrderFSM.waiting_for_username)
    await message.answer("Введите username (если нет, отправьте -):")

@order_router.message(OrderFSM.waiting_for_username)
async def order_username_entered(message: Message, state: FSMContext):
    username = message.text if message.text != "-" else ""
    await state.update_data(username=username)
    await state.set_state(OrderFSM.waiting_for_item_name)
    await message.answer("Введите название товара:")

@order_router.message(OrderFSM.waiting_for_item_name)
async def order_item_entered(message: Message, state: FSMContext):
    await state.update_data(item_name=message.text)
    await state.set_state(OrderFSM.waiting_for_price)
    await message.answer("Введите цену товара (числом):")

@order_router.message(OrderFSM.waiting_for_price)
async def order_price_entered(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Цена должна быть числом. Попробуйте снова.")

    await state.update_data(price=int(message.text))
    await state.set_state(OrderFSM.waiting_for_date)
    await message.answer("Введите дату заказа в формате ГГГГ-ММ-ДД:")

@order_router.message(OrderFSM.waiting_for_date)
async def order_date_manual(message: Message, state: FSMContext):
    try:
        entered_date = date.fromisoformat(message.text)
    except ValueError:
        await message.answer("Неверный формат даты. Используйте ГГГГ-ММ-ДД.")
        return

    user_data = await state.get_data()

    await create_order(
        telegram_id=user_data["telegram_id"],
        username=None if user_data["username"].lower() == "нет" else user_data["username"],
        item_name=user_data["item_name"],
        price=int(user_data["price"]),
        date_value=entered_date,
        admin_id=str(message.from_user.id)
    )

    await message.answer("✅ Заказ создан!", reply_markup=get_admin_panel())
    await state.clear()