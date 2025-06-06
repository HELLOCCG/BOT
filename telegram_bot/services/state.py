from aiogram.fsm.state import State, StatesGroup
from typing import Dict, Any
from dataclasses import dataclass, field

@dataclass
class UserState:
    step: str = 'date'
    input_buffer: str = ''
    data: Dict[str, Any] = field(default_factory=dict)
    last_msg_id: int = None

class StateManager:
    def __init__(self):
        self._states: Dict[int, UserState] = {}

    def get_state(self, user_id: int) -> UserState:
        if user_id not in self._states:
            self._states[user_id] = UserState()
        return self._states[user_id]

    def update_state(self, user_id: int, **kwargs):
        state = self.get_state(user_id)
        for key, value in kwargs.items():
            setattr(state, key, value)

    def clear_state(self, user_id: int):
        if user_id in self._states:
            del self._states[user_id]

state_manager = StateManager()

class TrainingStates(StatesGroup):
    waiting_for_date = State()
    waiting_for_type = State()
    waiting_for_distance = State()
    waiting_for_time = State()
    waiting_for_pace = State()
    waiting_for_heart_rate = State()
    waiting_for_additional_info = State()
    waiting_for_sensations = State()
