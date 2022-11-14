from aiogram import executor
from handlers import dp

from utils.database import create_tables

async def on_sturtup(dp):
    print('Бот запущен!')

if __name__ == '__main__':
    create_tables()
    executor.start_polling(dp, on_startup=on_sturtup)