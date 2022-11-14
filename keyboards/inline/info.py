from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import config

def get_info_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Соглашение 📄', url=f'https://telegra.ph/Terms-Of-Service-06-17-2'), InlineKeyboardButton(text='Поддержка 🧑‍💻', url=f'tg://resolve?domain={config.owner_username}'))
    keyboard.add(InlineKeyboardButton(text='🗞 Новости', url=f'tg://resolve?domain={config.owner_username}'))
    keyboard.add(InlineKeyboardButton(text='Сообщить об ошибке', url=f'tg://resolve?domain={config.owner_username}'))

    return keyboard