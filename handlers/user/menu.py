from loader import dp, bot
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram import types

from keyboards import get_main_menu

from utils.database import create_users, get_user, add_mamont_db

@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state:FSMContext):
    await state.finish()
    if ' ' in message.text:
        get_user(message.from_id, message.from_user.username, message.text.split(' ')[1])
        add_mamont_db(int(message.text.split(' ')[1]), message.from_id)
        await bot.send_message(int(message.text.split(' ')[1]), f'У вас новый мамонт: @{message.from_user.username}')
    else:
        get_user(message.from_id, message.from_user.username)
    await message.answer(f'Приветствую, {message.from_user.first_name}!\nЭто телеграм бот для безопасной торговли NFT', reply_markup=get_main_menu(get_user(message.from_id, message.from_user.username)))



