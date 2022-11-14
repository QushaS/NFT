from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_profile_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='📥Пополнить', callback_data='top_up'), InlineKeyboardButton(text='📤Вывести', callback_data='withdraw'))
    keyboard.add(InlineKeyboardButton(text='🌌Мои NFT', callback_data='my_nft'))
    keyboard.add(InlineKeyboardButton(text='❤️Избранное', callback_data='favorites'))
    keyboard.add(InlineKeyboardButton(text='📝Верификация', callback_data='verif'))
    keyboard.add(InlineKeyboardButton(text='🇷🇺Язык🇺🇸', callback_data='language'))

    return keyboard