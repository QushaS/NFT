from loader import dp
from aiogram.dispatcher import FSMContext
from aiogram import types

from keyboards import get_support_menu

@dp.message_handler(text='Тех. Поддержка 🌐')
async def bot_start(message: types.Message, state:FSMContext):
    await state.finish()
    await message.answer_photo(open('src/support.jfif', 'rb'), caption=f'Правила обращения в Техническую Поддержку:\n\n🔹1. Представьтесь, изложите проблему своими словами - мы постараемся Вам помочь.\n\n🔹2.  Напишите свой ID - нам это нужно, чтобы увидеть ваш профиль, и узнать актуальность вашей проблемы.\n\n🔹3. Будьте вежливы, наши консультанты не роботы, мы постараемся помочь Вам, и сделать все возможное, чтобы сберечь ваше время и обеспечить максимальную оперативность в работе.\n\nНапишите нам, ответ Поддержки, не заставит вас долго ждать!', reply_markup=get_support_menu())
