from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import config

def get_support_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Поддержка 🧑‍💻', url=f'tg://resolve?domain={config.owner_username}'))

    return keyboard