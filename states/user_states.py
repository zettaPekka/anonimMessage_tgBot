from aiogram.fsm.state import StatesGroup, State


class AnsMessage(StatesGroup):
    writing = State()