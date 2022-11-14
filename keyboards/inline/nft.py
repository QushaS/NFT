from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.database import get_like, get_likes
from utils.nft import get_nft, get_category_index, get_paragraph_index

def get_nft_menu(categorys, start):
    keyboard = InlineKeyboardMarkup()
    for index, category in enumerate(categorys):
        keyboard.add(InlineKeyboardButton(text=category, callback_data=f'category:{index + start}'))
    
    keyboard.add(InlineKeyboardButton(text=f'⬅️', callback_data=f'change_categorys:{int(start/10)}:left'), InlineKeyboardButton(text=f'{int(start/10+1)}/8', callback_data='null'), InlineKeyboardButton(text=f'➡️', callback_data=f'change_categorys:{int(start/10)}:right'))

    return keyboard

def get_favorite_menu(likes):
    keyboard = InlineKeyboardMarkup()
    for index, like in enumerate(likes):
        if (index + 1) % 2 == 0:
            keyboard.add(InlineKeyboardButton(text=button['paragraph'], callback_data=f'paragraph:{get_category_index(button["category"])}:{get_paragraph_index(like["category"], button["paragraph"])}'), InlineKeyboardButton(text=like['paragraph'], callback_data=f'paragraph:{get_category_index(like["category"])}:{get_paragraph_index(like["category"], like["paragraph"])}'))
            continue
        button = like

        if len(likes) == index + 1:
            keyboard.add(InlineKeyboardButton(text=like['paragraph'], callback_data=f'paragraph:{get_category_index(like["category"])}:{get_paragraph_index(like["category"], like["paragraph"])}'))
    return keyboard

def get_my_nft_menu(nfts):
    keyboard = InlineKeyboardMarkup()
    for index, like in enumerate(nfts):
        if (index + 1) % 2 == 0:
            print(f'edit:{get_category_index(button["category"])}:{get_paragraph_index(like["category"], button["paragraph"])}')
            keyboard.add(InlineKeyboardButton(text=button['paragraph'], callback_data=f'edit:{get_category_index(button["category"])}:{get_paragraph_index(like["category"], button["paragraph"])}'), InlineKeyboardButton(text=like['paragraph'], callback_data=f'edit:{get_category_index(like["category"])}:{get_paragraph_index(like["category"], like["paragraph"])}'))
            continue
        button = like

        if len(nfts) == index + 1:
            keyboard.add(InlineKeyboardButton(text=like['paragraph'], callback_data=f'edit:{get_category_index(like["category"])}:{get_paragraph_index(like["category"], like["paragraph"])}'))
    return keyboard

def get_category_menu(paragraphs, category_index):
    keyboard = InlineKeyboardMarkup()
    for index, paragraph in enumerate(paragraphs):
        if (index + 1) % 2 == 0:
            keyboard.add(InlineKeyboardButton(text=button, callback_data=f'paragraph:{category_index}:{index - 1}'), InlineKeyboardButton(text=paragraph, callback_data=f'paragraph:{category_index}:{index}'))
            continue
        button = paragraph

        if len(paragraphs) == index + 1:
            keyboard.add(InlineKeyboardButton(text=button, callback_data=f'paragraph:{category_index}:{index}'))
    keyboard.add(InlineKeyboardButton(text='↩️Вернуться', callback_data=f'change_categorys:{int((category_index+10)/10)}:left'))
    return keyboard

def get_nft_solo_menu(category_index, paragraph_index, tg_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='✅ Купить', callback_data=f'buy:{category_index}:{paragraph_index}'))
    _, nft_name, category_name = get_nft(int(category_index), int(paragraph_index))
    likes = get_likes(category_name, nft_name)
    if get_like(tg_id, category_name, nft_name):
        keyboard.add(InlineKeyboardButton(text=f'❤️ ( {len(likes)} )', callback_data=f'like:{category_index}:{paragraph_index}'))
    else:
        keyboard.add(InlineKeyboardButton(text=f'🤍 ( {len(likes)} )', callback_data=f'like:{category_index}:{paragraph_index}'))
    keyboard.add(InlineKeyboardButton(text='↩️Вернуться', callback_data=f'category:{category_index}'))

    return keyboard

def get_nft_solo_sell_menu(category_index, paragraph_index, nft_info):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f'{"Выставить на продажу" if nft_info["is_sell"] == False else "Снять с продажи"}', callback_data=f'sell_my_nft:{category_index}:{paragraph_index}'))
    keyboard.add(InlineKeyboardButton(text='Вернуться', callback_data=f'my_nft'))

    return keyboard

def worker_nft_sell(category_index, paragraph_index, tg_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f"Купить", callback_data=f'sell_worker_nft:{category_index}:{paragraph_index}:{tg_id}'))
    return keyboard