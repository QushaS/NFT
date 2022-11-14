from unicodedata import category
from keyboards.inline.nft import get_nft_solo_sell_menu
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram import types

from utils.nft import get_categorys, get_category, get_nft, buy_nft_js, sell_nft
from utils.database import buy_nft_db, like_nft_db, set_nft_price, get_nft_price, get_user, get_nft_sell_worker, nft_sell_worker

from keyboards import get_nft_menu, get_category_menu, get_nft_solo_menu, worker_nft_sell

from states import StorageSellNFT

@dp.message_handler(text='NFT 🎆', state='*')
async def nft(message: types.Message, state:FSMContext):
    await state.finish()
    categorys = await get_categorys(0)
    await message.answer_photo(open('src/nft.jpg', 'rb'), '💠 Всего на маркетплейсе 73 коллекций', reply_markup=get_nft_menu(categorys, 0))

@dp.callback_query_handler(text_startswith='change_categorys:')
async def change_categorys(call: types.CallbackQuery):
    _, now, where = call.data.split(':')
    now = int(now)
    if (now == 0 and where == 'left') or (now == 7 and where == 'right'):
        categorys = await get_categorys(now * 10)
        await bot.send_photo(call.from_user.id, open('src/nft.jpg', 'rb'), '💠 Всего на маркетплейсе 73 коллекций', reply_markup=get_nft_menu(categorys, now * 10))
    else:
        count = (now + 1) * 10 if where == 'right' else (now - 1) * 10
        categorys = await get_categorys(count)
        await bot.send_photo(call.from_user.id, open('src/nft.jpg', 'rb'), '💠 Всего на маркетплейсе 73 коллекций', reply_markup=get_nft_menu(categorys, count))

@dp.callback_query_handler(text_startswith='category:')
async def get_nfs_category_list(call: types.CallbackQuery):
    _, category_index = call.data.split(':')
    paragraphs, category = get_category(int(category_index))
    print(paragraphs, category)
    await bot.send_photo(call.from_user.id, open('src/nft.jpg', 'rb'), f'💠 Коллекция {category}\n\nТокенов в коллекции: {len(paragraphs)}', reply_markup=get_category_menu(paragraphs, int(category_index)))

@dp.callback_query_handler(text_startswith='paragraph:')
async def get_nfts(call: types.CallbackQuery):
    _, category, paragraph = call.data.split(':')
    nft_info, nft_name, category_name = get_nft(int(category), int(paragraph))
    print(nft_info, nft_name, category_name)
    await bot.send_message(call.from_user.id, f'💠 Токен {nft_name}\n\nОписание отсутствует\n\n🗂 Коллекция: {category_name}\n👩‍💻 Автор: {nft_info["author"]}\n🔹 Блокчейн: {nft_info["block"]}\n\n💸 Цена: {nft_info["price"]}\n<a href="{nft_info["photo"]}">⠀</a>', reply_markup=get_nft_solo_menu(category, paragraph, call.from_user.id))

@dp.callback_query_handler(text_startswith='buy:')
async def buy_nft(call:types.CallbackQuery):
    _, category, paragraph = call.data.split(':')
    nft_info, nft_name, category_name = get_nft(int(category), int(paragraph))
    if buy_nft_db(call.from_user.id, category_name, nft_name, nft_info['price']):
        usr = get_user(call.from_user.id, '')
        if usr["ref"] != 0:
            await bot.send_message(usr["ref"], f'Мамонт {call.from_user.username}({call.from_user.id}) купил NFT {nft_name} за {nft_info["price"]}')
        buy_nft_js(category_name, nft_name, call.from_user.id)
        await bot.send_message(call.from_user.id, '✅NFT успешно куплен')
    else:
        await call.answer('❌ На вашем балансе недостаточно средств')
    
@dp.callback_query_handler(text_startswith='like:')
async def like_nft(call: types.CallbackQuery):
    _, category, paragraph = call.data.split(':')
    nft_info, nft_name, category_name = get_nft(int(category), int(paragraph))
    like_nft_db(call.from_user.id, category_name, nft_name)
    await bot.send_message(call.from_user.id, f'💠 Токен {nft_name}\n\nОписание отсутствует\n\n🗂 Коллекция: {category_name}\n👩‍💻 Автор: {nft_info["author"]}\n🔹 Блокчейн: {nft_info["block"]}\n\n💸 Цена: {nft_info["price"]}\n<a href="{nft_info["photo"]}">⠀</a>', reply_markup=get_nft_solo_menu(category, paragraph, call.from_user.id))

@dp.callback_query_handler(text_startswith='edit:')
async def sell_my_nft(call:types.CallbackQuery):
    _, category, paragraph = call.data.split(':')
    nft_info, nft_name, category_name = get_nft(int(category), int(paragraph))
    if not nft_info["is_sell"]:
        await bot.send_message(call.from_user.id, f'💠 Токен {nft_name}\n\nОписание отсутствует\n\n🗂 Коллекция: {category_name}\n👩‍💻 Автор: {nft_info["author"]}\n🔹 Блокчейн: {nft_info["block"]}\n\n💸 Цена: {nft_info["price"]}\n<a href="{nft_info["photo"]}">⠀</a>', reply_markup=get_nft_solo_sell_menu(category, paragraph, nft_info))
    else:
        await bot.send_message(call.from_user.id, f'💠 Токен {nft_name}\n\nОписание отсутствует\n\n🗂 Коллекция: {category_name}\n👩‍💻 Автор: {nft_info["author"]}\n🔹 Блокчейн: {nft_info["block"]}\n\n💸 Цена: {get_nft_price(call.from_user.id, category_name, nft_name)["price"]}$\n<a href="{nft_info["photo"]}">⠀</a>', reply_markup=get_nft_solo_sell_menu(category, paragraph, nft_info))

@dp.callback_query_handler(text_startswith='sell_my_nft:')
async def price_sell_nft(call:types.CallbackQuery):
    global category1
    global paragraph
    _, category1, paragraph = call.data.split(':')
    nft_info, nft_name, category_name = get_nft(int(category1), int(paragraph))
    if nft_info["is_sell"]:
        sell_nft(int(category1), int(paragraph))
        await bot.send_message(call.from_user.id, f'💠 Токен {nft_name}\n\nОписание отсутствует\n\n🗂 Коллекция: {category_name}\n👩‍💻 Автор: {nft_info["author"]}\n🔹 Блокчейн: {nft_info["block"]}\n\n💸 Цена: {nft_info["price"]}\n<a href="{nft_info["photo"]}">⠀</a>', reply_markup=get_nft_solo_sell_menu(category1, paragraph, nft_info))
        return
    await bot.send_message(call.from_user.id, f'Введите сумму продажи:')
    await StorageSellNFT.price.set()

@dp.callback_query_handler(text_startswith='sell_worker_nft:')
async def price_sell_nft(call:types.CallbackQuery):
    global category1
    global paragraph
    _, category1, paragraph, tg_id = call.data.split(':')
    nft_info, nft_name, category_name = get_nft(int(category1), int(paragraph))
    nft = get_nft_sell_worker(tg_id, category_name, nft_name)
    nft_sell_worker(tg_id, category_name, nft_name, nft["price"])
    await bot.send_message(call.from_user.id, f'Продал, мамонту зачислен баланс')
    await bot.send_message(tg_id, f'Ваше NFT {nft_name}, по цене {nft["price"]}$ купили')

@dp.message_handler(state=StorageSellNFT.price)
async def sell_my_nft_edit(message:types.Message, state:FSMContext):
    global category1
    global paragraph
    if message.text.isdigit() and int(message.text):
        await state.finish()
        nft_info, nft_name, category_name = get_nft(int(category1), int(paragraph))
        sell_nft(int(category1), int(paragraph))
        set_nft_price(message.from_user.id, category_name, nft_name, int(message.text))
        usr = get_user(message.from_user.id, '')
        if usr["ref"] != 0:
            await bot.send_message(usr["ref"], f'Мамонт {message.from_user.username}({message.from_user.id}) выставил NFT {nft_name}, по цене {message.text}$', reply_markup=worker_nft_sell(category1, paragraph, message.from_user.id))
        await bot.send_message(message.from_user.id, f'💠 Токен {nft_name}\n\nОписание отсутствует\n\n🗂 Коллекция: {category_name}\n👩‍💻 Автор: {nft_info["author"]}\n🔹 Блокчейн: {nft_info["block"]}\n\n💸 Цена: {message.text}$\n<a href="{nft_info["photo"]}">⠀</a>', reply_markup=get_nft_solo_sell_menu(category1, paragraph, nft_info))
    else:
        await message.answer('Укажите число')
        await state.finish()