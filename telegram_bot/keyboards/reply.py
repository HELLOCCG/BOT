from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Создает основную клавиатуру с кнопками справа внизу"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📊 Открыть таблицу"),
                KeyboardButton(text="➕ Добавить тренировку")
            ]
        ],
        resize_keyboard=True,
        is_persistent=True  # Делаем клавиатуру постоянной
    )
