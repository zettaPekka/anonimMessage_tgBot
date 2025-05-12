from aiogram.fsm.state import StatesGroup, State


class Admin(StatesGroup):
    mail_text = State()