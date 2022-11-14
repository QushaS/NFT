from aiogram.types import ReplyKeyboardMarkup

def get_canced_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('❌Отмена')

    return keyboard