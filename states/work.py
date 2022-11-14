from aiogram.dispatcher.filters.state import State, StatesGroup

class StorageCreatePromo(StatesGroup):
    price = State()

class StorageAddMamonts(StatesGroup):
    mamont = State()

class StorageBalanceMamont(StatesGroup):
    value = State()