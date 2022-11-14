from loader import dp
from aiogram.dispatcher import FSMContext
from aiogram import types

from keyboards import get_info_menu

@dp.message_handler(text='Информация ℹ️')
async def bot_start(message: types.Message, state:FSMContext):
    await state.finish()
    await message.answer_photo(open('src/about_service.jfif', 'rb'), caption=f"🔹 О Сервисе\n\n{'<i>'}OpenSea  {'</i>'}{'<b>'}— торговая площадка для невзаимозаменяемых токенов (NFT). Покупайте, продавайте и открывайте для себя эксклюзивные цифровые предметы.{'</b>'}", reply_markup=get_info_menu())
