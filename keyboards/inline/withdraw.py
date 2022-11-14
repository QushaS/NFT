from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_withdraw_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Банковская карта', callback_data=f'withdraw:Банковская карта'))
    keyboard.add(InlineKeyboardButton(text='QIWI', callback_data=f'withdraw:QIWI Кошелек'))
    keyboard.add(InlineKeyboardButton(text='ЮMoney (Яндекс деньги)', callback_data=f'withdraw:ЮMoney (Яндекс деньги)'))
    keyboard.add(InlineKeyboardButton(text='WebMoney', callback_data=f'withdraw:WebMoney Кошелек'))
    keyboard.add(InlineKeyboardButton(text='Bitcoin', callback_data=f'withdraw:Bitcoin'))
    keyboard.add(InlineKeyboardButton(text='Ethereum', callback_data=f'withdraw:Ethereum'))
    keyboard.add(InlineKeyboardButton(text='USDT TRC20', callback_data=f'withdraw:USDT TRC20'))

    return keyboard