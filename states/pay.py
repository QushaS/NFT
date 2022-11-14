from aiogram.dispatcher.filters.state import State, StatesGroup

class StoragePayQiwi(StatesGroup):
    price = State()
    
class StoragePayCard(StatesGroup):
    price = State()

class StorageSellNFT(StatesGroup):
    price = State()