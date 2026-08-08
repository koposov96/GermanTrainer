from aiogram.fsm.state import StatesGroup, State


class ImportState(StatesGroup):
    waiting_json = State()