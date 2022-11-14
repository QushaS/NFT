from aiogram.dispatcher.filters.state import State, StatesGroup

class StorageWithdraw(StatesGroup):
    price = State()
    requisites = State()
    bad = State()