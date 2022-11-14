from aiogram.types import ReplyKeyboardMarkup

def get_main_menu(user):
    print(user)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('NFT 🎆')
    keyboard.row('Личный кабинет 📁')
    keyboard.row('Информация ℹ️', 'Тех. Поддержка 🌐')
    if user['is_worker']:
        keyboard.row('⚡️ Меню воркера')

    return keyboard