from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Messages:
    START: str = """
👋 Добро пожаловать в бот для учета тренировок!

Выберите действие:
"""

    PROMPTS: Dict[str, str] = field(default_factory=lambda: {
        'distance': "📏 Введите расстояние (км, например 10.10):",
        'time': "⏱ Введите время тренировки (чч:мм:сс):",
        'pace': "🏃 Введите темп (м:сс):",
        'heart_rate': "❤️ Введите пульс (уд/мин):",
        'additional_info': "✍️ Введите доп. информацию:",
        'sensations': "🤔 Опишите ощущения:"
    })

    ERRORS: Dict[str, str] = field(default_factory=lambda: {
        'past_date': "Нельзя выбрать прошедшую дату",
        'invalid_distance': "Недопустимое значение расстояния",
        'invalid_time': "Неверный формат времени",
        'invalid_pace': "Неверный формат темпа",
        'invalid_heart_rate': "Недопустимое значение пульса",
        'save_error': "Ошибка при сохранении. Попробуйте еще раз."
    })

    SUCCESS: Dict[str, str] = field(default_factory=lambda: {
        'saved': "✅ Тренировка успешно сохранена!",
        'cancelled': "❌ Добавление тренировки отменено"
    })

messages = Messages()
