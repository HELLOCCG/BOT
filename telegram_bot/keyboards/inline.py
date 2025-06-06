from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.constants import TRAINING_TYPES
from datetime import datetime, timedelta

def get_training_types_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру с типами тренировок"""
    keyboard = []
    for callback, name in TRAINING_TYPES.items():
        keyboard.append([
            InlineKeyboardButton(
                text=name,
                callback_data=f"training_type:{callback}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_date_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру с выбором даты"""
    keyboard = []
    today = datetime.now()
    
    # Добавляем кнопки для последних 3 дней
    for i in range(3):
        date = today - timedelta(days=i)
        date_str = date.strftime("%d %b. %Y")
        keyboard.append([
            InlineKeyboardButton(
                text=f"{'Сегодня' if i == 0 else 'Вчера' if i == 1 else date_str}",
                callback_data=f"date:{date_str}"
            )
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру подтверждения"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm"),
                InlineKeyboardButton(text="❌ Отменить", callback_data="cancel")
            ],
            [
                InlineKeyboardButton(text="📝 Редактировать", callback_data="edit")
            ]
        ]
    )

def get_edit_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру редактирования"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📅 Дата", callback_data="edit:date"),
                InlineKeyboardButton(text="📏 Дистанция", callback_data="edit:distance")
            ],
            [
                InlineKeyboardButton(text="⏱ Темп", callback_data="edit:pace"),
                InlineKeyboardButton(text="❤️ Пульс", callback_data="edit:pulse")
            ],
            [
                InlineKeyboardButton(text="📝 Доп. инфо", callback_data="edit:additional"),
                InlineKeyboardButton(text="🤔 Ощущения", callback_data="edit:feelings")
            ],
            [
                InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_confirm")
            ]
        ]
    )

def get_skip_button() -> InlineKeyboardMarkup:
    """Создает инлайн-кнопку пропуска"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="Пропустить", callback_data="skip")
        ]]
    )
