from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from datetime import date

from services.admin_service import is_main_admin, add_admin, get_all_admins, remove_admin, is_admin
from keyboards.admin_keyboards import get_main_admin_panel, generate_admin_delete_keyboard, get_admin_panel

admin_router = Router()

class MainAdminFSM(StatesGroup):
    waiting_for_admin_id = State()

@admin_router.message(F.text == "/main_admin")
async def show_main_admin_panel(message: Message):
    if not await is_main_admin(message.from_user.id):
        return await message.answer("❌ У вас нет доступа к этой команде.")
    await message.answer("👑 Панель главного администратора", reply_markup=get_main_admin_panel())

@admin_router.callback_query(F.data == "add_admin")
async def prompt_for_admin_id(callback: CallbackQuery, state: FSMContext):
    if not await is_main_admin(callback.from_user.id):
        return await callback.answer("❌ Нет доступа.")
    await callback.message.edit_text("🔢 Введите telegram ID нового администратора:")
    await state.set_state(MainAdminFSM.waiting_for_admin_id)

@admin_router.message(MainAdminFSM.waiting_for_admin_id)
async def process_new_admin_id(message: Message, state: FSMContext):
    try:
        new_admin_id = int(message.text.strip())
        await add_admin(new_admin_id)
        await message.answer(f"✅ Админ с ID {new_admin_id} успешно добавлен.")
    except ValueError:
        await message.answer("❌ Введите корректный числовой ID.")
    await state.clear()

@admin_router.callback_query(F.data == "list_admins")
async def list_admins(callback: CallbackQuery):
    admins = await get_all_admins()
    if not admins:
        await callback.message.edit_text("❌ Список админов пуст.")
    else:
        text = "📋 Список админов:\n" + "\n".join([f"• {row['telegram_id']}" for row in admins])
        await callback.message.edit_text(text, reply_markup=get_main_admin_panel())

@admin_router.callback_query(F.data == "delete_admin")
async def choose_admin_to_delete(callback: CallbackQuery):
    admins = await get_all_admins()
    if len(admins) <= 1:
        return await callback.message.edit_text("❌ Нельзя удалить последнего админа.")
    markup = generate_admin_delete_keyboard(admins)
    await callback.message.edit_text("Выбери админа для удаления:", reply_markup=markup)

@admin_router.callback_query(F.data.startswith("confirm_delete:"))
async def confirm_delete_admin(callback: CallbackQuery):
    telegram_id = callback.data.split(":")[1]
    await remove_admin(telegram_id)
    await callback.message.edit_text(f"✅ Админ с ID {telegram_id} удалён.", reply_markup=get_main_admin_panel())

@admin_router.callback_query(F.data == "exit_main_admin")
@admin_router.callback_query(F.data == "main_admin_panel")
async def exit_panel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Вы в панели главного администратора.", reply_markup=get_main_admin_panel())

@admin_router.message(F.text == "/admin")
async def admin_entry(message: Message):
    if await is_admin(message.from_user.id):
        await message.answer("Добро пожаловать в админ-панель 👮", reply_markup=get_admin_panel())
    else:
        await message.answer("У вас нет прав администратора.")

