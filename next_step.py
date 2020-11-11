from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    start: State = State()
    id: State = State()
    grade: State = State()
    phone: State = State()
    lang: State = State()
    delete: State = State()