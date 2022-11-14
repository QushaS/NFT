from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_worker_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Мои мамонты', callback_data='my_mamonts'), InlineKeyboardButton(text='Добавить мамонта', callback_data='add_mamonts'))
    #keyboard.add(InlineKeyboardButton(text='Минимальный депозит для мамонта: 1000Р', callback_data='min_depos'))
    #keyboard.add(InlineKeyboardButton(text='Создать промокод', callback_data='create_promo'), InlineKeyboardButton(text='Мои промокоды', callback_data='my_promo'))

    return keyboard

def get_mamonts_menu(mamonts):
    keyboard = InlineKeyboardMarkup()
    for mamont in mamonts:
        keyboard.add(InlineKeyboardButton(text=mamont['username'], callback_data=f'setting:{mamont["tg_id"]}'))

    return keyboard

def setting_mamont_menu(mamont_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Баланс', callback_data=f'set:balance:{mamont_id}'))
    keyboard.add(InlineKeyboardButton(text='Заблокировать вывод', callback_data=f'set:vivod:{mamont_id}'))
    keyboard.add(InlineKeyboardButton(text='Верификация', callback_data=f'set:verif:{mamont_id}'))
    keyboard.add(InlineKeyboardButton(text='Удалить мамонта', callback_data=f'set:delete:{mamont_id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'my_mamonts'))

    return keyboard