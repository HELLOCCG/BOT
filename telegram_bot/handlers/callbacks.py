from aiogram import Router, F, types
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from states.training import TrainingStates
from config.constants import TRAINING_TYPES
from keyboards.inline import get_training_types_keyboard, get_skip_button
from keyboards.reply import get_main_keyboard
from services.google_sheets import sheets_service
import re

# Создаем роутер
router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        "👋 Добро пожаловать в бот для учета тренировок!",
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == "📊 Открыть таблицу")
async def show_table(message: Message):
    """Обработчик кнопки показа таблицы"""
    table_url = sheets_service.get_table_url()
    await message.answer(f"📊 Ваша таблица тренировок:\n{table_url}")

@router.message(F.text == "➕ Добавить тренировку")
async def add_training(message: Message):
    """Обработчик кнопки добавления тренировки"""
    await message.answer(
        "🏃 Выберите тип тренировки:",
        reply_markup=get_training_types_keyboard()
    )

@router.callback_query(F.data.startswith("training_type:"))
async def process_training_type(callback: CallbackQuery, state: FSMContext):
    """Обработчик выбора типа тренировки"""
    training_type = callback.data.split(":")[1]
    
    await state.update_data(
        training_type=training_type,
        training_type_name=TRAINING_TYPES[training_type]
    )
    await state.set_state(TrainingStates.waiting_for_distance)
    
    await callback.message.edit_text(
        "📏 Введите дистанцию в километрах (например: 5.2):"
    )

@router.message(TrainingStates.waiting_for_distance)
async def process_distance(message: Message, state: FSMContext):
    """Обработчик ввода дистанции"""
    try:
        distance = float(message.text.replace(',', '.'))
        if distance <= 0:
            await message.answer("❌ Дистанция должна быть положительным числом!")
            return
        
        await state.update_data(distance=distance)
        await state.set_state(TrainingStates.waiting_for_pace)
        
        await message.answer(
            "⏱ Введите темп в формате М:СС/км (например: 4:30):",
            reply_markup=types.ReplyKeyboardRemove()
        )
    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректное число!")

@router.message(TrainingStates.waiting_for_pace)
async def process_pace(message: Message, state: FSMContext):
    """Обработчик ввода темпа"""
    pace_pattern = re.compile(r'^\d{1,2}:\d{2}$')
    if not pace_pattern.match(message.text):
        await message.answer(
            "❌ Пожалуйста, введите темп в правильном формате (М:СС)!"
        )
        return

    minutes, seconds = map(int, message.text.split(':'))
    if seconds >= 60:
        await message.answer("❌ Количество секунд не может быть больше 59!")
        return

    data = await state.get_data()
    # Рассчитываем общее время тренировки
    total_minutes = (minutes + seconds/60) * data['distance']
    
    await state.update_data(
        pace=f"{message.text}/км",
        time=round(total_minutes, 2)
    )
    
    await state.set_state(TrainingStates.waiting_for_pulse)
    await message.answer("❤️ Введите средний пульс (уд/мин):")

@router.message(TrainingStates.waiting_for_pulse)
async def process_pulse(message: Message, state: FSMContext):
    """Обработчик ввода пульса"""
    try:
        pulse = int(message.text)
        if not 30 <= pulse <= 250:
            await message.answer("❌ Пульс должен быть в диапазоне 30-250!")
            return
        
        await state.update_data(pulse=pulse)
        await state.set_state(TrainingStates.waiting_for_additional)
        
        await message.answer(
            "📝 Введите дополнительную информацию:",
            reply_markup=get_skip_button()
        )
    except ValueError:
        await message.answer("❌ Пожалуйста, введите целое число!")

@router.message(TrainingStates.waiting_for_additional)
async def process_additional(message: Message, state: FSMContext):
    """Обработчик ввода доп. информации"""
    additional_info = message.text
    await state.update_data(additional_info=additional_info)
    await state.set_state(TrainingStates.waiting_for_feelings)
    
    await message.answer(
        "🤔 Опишите ваши ощущения:",
        reply_markup=get_skip_button()
    )

@router.callback_query(F.data == "skip")
async def process_skip(callback: CallbackQuery, state: FSMContext):
    """Обработчик кнопки пропуска"""
    current_state = await state.get_state()
    
    if current_state == TrainingStates.waiting_for_additional:
        await state.update_data(additional_info="-")
        await state.set_state(TrainingStates.waiting_for_feelings)
        await callback.message.edit_text(
            "🤔 Опишите ваши ощущения:",
            reply_markup=get_skip_button()
        )
    
    elif current_state == TrainingStates.waiting_for_feelings:
        await state.update_data(feelings="-")
        data = await state.get_data()
        success = await sheets_service.append_row(data)
        
        if success:
            await callback.message.edit_text(
                "✅ Тренировка успешно сохранена!\n\n"
                f"Тип: {data['training_type_name']}\n"
                f"Дистанция: {data['distance']} км\n"
                f"Темп: {data['pace']}\n"
                f"Время: {data['time']} мин\n"
                f"Пульс: {data['pulse']} уд/мин\n"
                f"Доп. информация: {data['additional_info']}\n"
                f"Ощущения: {data['feelings']}"
            )
        else:
            await callback.message.edit_text(
                "❌ Произошла ошибка при сохранении тренировки. "
                "Пожалуйста, попробуйте позже."
            )
        
        await state.clear()
    
    await callback.answer()

@router.message(TrainingStates.waiting_for_feelings)
async def process_feelings(message: Message, state: FSMContext):
    """Обработчик ввода ощущений"""
    feelings = message.text
    data = await state.get_data()
    data['feelings'] = feelings
    
    # Сохраняем тренировку в таблицу
    success = await sheets_service.append_row(data)
    
    if success:
        await message.answer(
            "✅ Тренировка успешно сохранена!\n\n"
            f"Тип: {data['training_type_name']}\n"
            f"Дистанция: {data['distance']} км\n"
            f"Темп: {data['pace']}\n"
            f"Время: {data['time']} мин\n"
            f"Пульс: {data['pulse']} уд/мин\n"
            f"Доп. информация: {data['additional_info']}\n"
            f"Ощущения: {data['feelings']}"
        )
    else:
        await message.answer(
            "❌ Произошла ошибка при сохранении тренировки. "
            "Пожалуйста, попробуйте позже."
        )
    
    await state.clear()
