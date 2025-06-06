from aiogram.fsm.state import State, StatesGroup

class TrainingStates(StatesGroup):
    """Состояния для процесса добавления тренировки"""
    waiting_for_date = State()       # Добавляем состояние для даты
    waiting_for_distance = State()
    waiting_for_pace = State()
    waiting_for_pulse = State()
    waiting_for_additional = State()
    waiting_for_feelings = State()
    waiting_for_confirmation = State()  # Добавляем состояние для подтверждения
