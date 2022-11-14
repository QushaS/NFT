from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import config


def get_pay_type_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='💳Метод пополнения №1', callback_data='pay_type:qiwi'))
    keyboard.add(InlineKeyboardButton(text='💳Метод пополнения №2', callback_data='pay_type:card'))
    #keyboard.add(InlineKeyboardButton(text='💱Криптовалюта', callback_data='pay_type:crypto'))
    #keyboard.add(InlineKeyboardButton(text='🎁Промокод', callback_data='pay_type:promo'))

    return keyboard

def get_check_pay_card(id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Проверить оплату', callback_data=f'check_cardpay:{id}'))

    return keyboard

def get_check_pay_qiwi(amount, comment):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Перейти к оплате", url=f"https://qiwi.com/payment/form/99?extra['account']=+{config.qiwi_number}&amountInteger={int(amount)}&amountFraction=0&currency=643&extra['comment']={comment}&blocked[0]=sum&blocked[1]=account&blocked[2]=comment"))
    keyboard.add(InlineKeyboardButton(text='Проверить оплату', callback_data=f'check_qiwipay:{amount}:{comment}'))

    return keyboard

def get_pay_crypto_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='BTC', callback_data='crypto:btc'))
    keyboard.add(InlineKeyboardButton(text='ETH', callback_data='crypto:eth'))
    keyboard.add(InlineKeyboardButton(text='USDT', callback_data='crypto:usdt'))

    return keyboard