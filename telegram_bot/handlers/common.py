from aiogram import Router, F, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.reply import get_main_keyboard
from config.messages import messages

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start."""
    await message.answer(
        text=messages.START,
        reply_markup=get_main_keyboard()
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help."""
    help_text = """
🏃‍♂️ Бот для учета тренировок

Команды:
/start - Начать работу
/help - Показать эту справку

Для добавления тренировки нажмите кнопку "➕ Добавить тренировку"
"""
    await message.answer(help_text)

def register_common_handlers(dp: Dispatcher):
    dp.include_router(router)
