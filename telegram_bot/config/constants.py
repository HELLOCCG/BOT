# config/constants.py
from datetime import datetime

TRAINING_TYPES = {
    'easy_run': 'Легкий бег',
    'progressive': 'Прогресивный',
    'speed_run': 'Скоростной',
    'rest': 'Отдых',
    'competition': 'Соревнование'
}

TRAINING_COLORS = {
    'easy_run': {'red': 0.85, 'green': 0.95, 'blue': 0.85},     # Светло-зеленый
    'progressive': {'red': 1.0, 'green': 0.95, 'blue': 0.8},    # Светло-желтый/бежевый
    'speed_run': {'red': 0.95, 'green': 0.8, 'blue': 0.8},      # Светло-красный
    'rest': {'red': 0.9, 'green': 0.9, 'blue': 0.9},            # Светло-серый
    'competition': {'red': 0.8, 'green': 0.85, 'blue': 0.95}    # Светло-голубой
}

def format_date() -> str:
    """Форматирует текущую дату для таблицы"""
    now = datetime.now()
    days = {
        0: 'пн',
        1: 'вт',
        2: 'ср',
        3: 'чт',
        4: 'пт',
        5: 'сб',
        6: 'вс'
    }
    # Форматируем дату как "05 июня 2023 (чт)"
    return f"{now.strftime('%d %B %Y')} ({days[now.weekday()]})"
