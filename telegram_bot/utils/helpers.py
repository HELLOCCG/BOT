from datetime import datetime
import re
from typing import Optional, Tuple

async def validate_input(buffer: str, input_type: str) -> Tuple[bool, Optional[str]]:
    """Проверяет введенные данные."""
    try:
        if input_type == 'distance':
            value = float(buffer)
            if value <= 0 or value > 100:
                return False, "Недопустимое значение расстояния"
            return True, f"{value:.2f}"
            
        elif input_type == 'time':
            if not re.match(r'^\d{2}:\d{2}:\d{2}$', buffer):
                return False, "Неверный формат времени (чч:мм:сс)"
            h, m, s = map(int, buffer.split(':'))
            if h > 23 or m > 59 or s > 59:
                return False, "Некорректное время"
            return True, buffer
            
        elif input_type == 'pace':
            if not re.match(r'^\d{1}:\d{2}$', buffer):
                return False, "Неверный формат темпа (м:сс)"
            m, s = map(int, buffer.split(':'))
            if s >= 60:
                return False, "Секунды не могут быть больше 59"
            return True, buffer
            
        elif input_type == 'heart_rate':
            value = int(buffer)
            if value < 40 or value > 220:
                return False, "Недопустимое значение пульса"
            return True, str(value)
            
    except ValueError:
        return False, "Неверный формат"
    
    return False, "Неизвестный тип ввода"

def format_training_summary(data: dict) -> str:
    """Форматирует сводку тренировки."""
    summary = [
        "📝 Проверьте введенные данные:\n",
        f"📅 Дата: {data['date']}",
        f"🏃 Тип: {data['training_type_name']}"
    ]
    
    if data['training_type'] != 'rest':
        summary.extend([
            f"📏 Расстояние: {data['distance']} км",
            f"⏱ Время: {data['time']}",
            f"🏃 Темп: {data['pace']} мин/км",
            f"❤️ Пульс: {data['heart_rate']} уд/мин"
        ])
    
    summary.extend([
        f"✍️ Доп. инфо: {data['additional_info']}",
        f"🤔 Ощущения: {data['sensations']}"
    ])
    
    return "\n".join(summary)

def handle_digit_input(buffer: str, char: str, input_type: str) -> str:
    """Обрабатывает ввод цифр с автоматическим форматированием."""
    if input_type == 'distance':
        if len(buffer) >= 5:  # Максимум 99.99
            return buffer
        if len(buffer) == 2 and '.' not in buffer:
            buffer += '.'
            
    elif input_type == 'time':
        if len(buffer) >= 8:  # Максимум 23:59:59
            return buffer
        if len(buffer) in [2, 5]:
            buffer += ':'
            
    elif input_type == 'pace':
        if len(buffer) >= 4:  # Максимум 9:59
            return buffer
        if len(buffer) == 1:
            buffer += ':'
            
    elif input_type == 'heart_rate':
        if len(buffer) >= 3:  # Максимум 999
            return buffer
            
    return buffer + char

async def calculate_pace(distance: float, time_str: str) -> Optional[str]:
    """Рассчитывает темп на основе расстояния и времени."""
    try:
        h, m, s = map(int, time_str.split(':'))
        total_seconds = h * 3600 + m * 60 + s
        pace_seconds = total_seconds / float(distance)
        pace_minutes = pace_seconds / 60
        pace_min = int(pace_minutes)
        pace_sec = int((pace_minutes - pace_min) * 60)
        return f"{pace_min}:{pace_sec:02d}"
    except:
        return None
