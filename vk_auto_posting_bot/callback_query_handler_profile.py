import time

from importt import *
import main
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from aiogram.dispatcher.filters import Command

######## ЛОВИТ НАЖАТИЕ КНОПКИ ПРОВЕРИТЬ ПОДПИСКУ И ПРОВЕРЯЕТ ЕЁ ########
@dp.callback_query_handler(lambda c: c.data.startswith('profile'))
async def process_callback_check_subs(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if await subscription_verification(callback_query.from_user.id) == True:
        await process_callback_check_subs_1(callback_query.from_user.id, callback_query.message.message_id)
    else:
        await subscription_verification_send_link(callback_query.from_user.id)

async def process_callback_check_subs_1(user_id, message_id):

    with sq.connect(f'{pat}db_main.db') as con:
        sql = con.cursor()
        sql.execute(f"SELECT * FROM users WHERE chat_id == {str(user_id)}")
        b = sql.fetchall()
    subscription = await db_select_sys('subscription', user_id)
    back = InlineKeyboardButton(text="меню", callback_data='back_p:1')
    if subscription[0] == 'отсутствует':
        button1 = InlineKeyboardButton(text="Купить подписку", callback_data='Buy_a_subscription:Buy')
    else:
        c = datetime.utcfromtimestamp(float(subscription[0]))
        if float(subscription[0]) <= time.time():
            await db_update_sys('subscription', user_id, 'отсутствует')
            button1 = InlineKeyboardButton(text="Купить подписку", callback_data='Buy_a_subscription:Buy')
            subscription = ['отсутствует']
        else:
            subscription = [f"до {c.day}.{c.month}.{c.year}"]
            button1 = InlineKeyboardButton(text="Продлить подписку", callback_data='Buy_a_subscription:renewal')
    keyboard1 = InlineKeyboardMarkup(row_width=1).add(button1, back)

    a = subscription[0][3::].split('.')[::-1]
    aa = dt.date(int(a[0]), int(a[1]), int(a[2]))
    bb = dt.date.today()
    cc = aa - bb
    dd = f"{cc.days + 1} дней"
    if message_id != 0:
        await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=f'Ваш id:{user_id}\nКолличество ваших систем: {len(b)}\nПодписка: {subscription[0]} ({dd})', reply_markup=keyboard1)
    else:
        await bot.send_message(chat_id=user_id, text=f'Ваш id:{user_id}\nКолличество ваших систем: {len(b)}\nПодписка: {subscription[0]} ({dd})',reply_markup=keyboard1)

@dp.callback_query_handler(lambda c: c.data.startswith('Buy_a_subscription'))
async def process_callback_Buy_a_subscription(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    var = callback_query.data.split(':')
    await process_callback_Buy_a_subscription_1(callback_query.from_user.id, callback_query.message.message_id, 1, var[1])

async def process_callback_Buy_a_subscription_1(user_id, message_id, num, subs):
    one_month_period = InlineKeyboardButton(text="1 мес - 500 руб", callback_data=f'Pay:1:{subs}')
    three_month_period = InlineKeyboardButton(text="3 мес - 1200руб (-10%)", callback_data=f'Pay:3:{subs}')
    six_month_period = InlineKeyboardButton(text="6 мес - 2550 руб (-15%)", callback_data=f'Pay:6:{subs}')
    twelve_month_period = InlineKeyboardButton(text="12 мес - 4800 руб (-20%)", callback_data=f'Pay:12:{subs}')
    back = InlineKeyboardButton(text="Назад", callback_data=f'backpr:1:{subs}')
    keyboard1 = InlineKeyboardMarkup(row_width=1).add(one_month_period, three_month_period, six_month_period, twelve_month_period, back)
    if subs == 'Buy':
        if num != 0:
            await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=f'Выберите период подписки: ',reply_markup=keyboard1)
        else:
            await bot.send_message(chat_id=user_id,  text=f'Выберите период подписки: ',reply_markup=keyboard1)
    elif subs == 'renewal':
        if num != 0:
            await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=f'Выберите период на который хотите продлить подписку: ',reply_markup=keyboard1)
        else:
            await bot.send_message(chat_id=user_id,  text=f'Выберите период на который хотите продлить подписку: ',reply_markup=keyboard1)

@dp.callback_query_handler(lambda c: c.data.startswith('Pay'))
async def process_callback_Pay(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    pay_num = callback_query.data.split(':')
    keyboard = InlineKeyboardMarkup()
    t, d, l = '-', '-', '-'
    back = InlineKeyboardButton(text="Назад", callback_data=f'backpr:2:{pay_num[2]}')
    if pay_num[1] == '1':
        keyboard.add(InlineKeyboardButton("Заплатить 500,00 RUB", pay=True))
        keyboard.add(back)
        if pay_num[2] == 'Buy':
            t='Оформление подписки на 1 месяц'
            d='1 месяц подписки'
            l='Оформление подписки на 1 месяц'
        elif pay_num[2] == 'renewal':
            t = 'Продление подписки на 1 месяц'
            d = '1 месяц подписки'
            l = 'Продление подписки на 1 месяц'
        await bot.send_invoice(chat_id=callback_query.from_user.id,
                         title=t,
                         description=d,
                         provider_token=YOOTOKEN,
                         currency='RUB',
                         photo_url=None,
                         need_phone_number=False,
                         need_email=False,
                         is_flexible=False,
                         prices=[LabeledPrice(label=l,amount=int(50000))],
                         start_parameter='start_parameter',
                         payload=l,
                         reply_markup=keyboard
                         )
    elif pay_num[1] == '3':
        keyboard.add(InlineKeyboardButton("Заплатить 500,00 RUB", pay=True))
        keyboard.add(back)
        if pay_num[2] == 'Buy':
            t='Оформление подписки на 3 месяца'
            d='3 месяца подписки'
            l='Оформление подписки на 3 месяца'
        elif pay_num[2] == 'renewal':
            t = 'Продление подписки на 3 месяца'
            d = '3 месяца подписки'
            l = 'Продление подписки на 3 месяца'
        await bot.send_invoice(chat_id=callback_query.from_user.id,
                               title=t,
                               description=d,
                               provider_token=YOOTOKEN,
                               currency='RUB',
                               photo_url=None,
                               need_phone_number=False,
                               need_email=False,
                               is_flexible=False,
                               prices=[LabeledPrice(label=l, amount=int(120000))],
                               start_parameter='3_months',
                               payload=l,
                               reply_markup=keyboard
                               )
    elif pay_num[1] == '6':
        keyboard.add(InlineKeyboardButton("Заплатить 500,00 RUB", pay=True))
        keyboard.add(back)
        if pay_num[2] == 'Buy':
            t='Оформление подписки на 6 месяцев'
            d='6 месяцев подписки'
            l='Оформление подписки на 6 месяцев'
        elif pay_num[2] == 'renewal':
            t = 'Продление подписки на 6 месяцев'
            d = '6 месяцев подписки'
            l = 'Продление подписки на 6 месяцев'
        await bot.send_invoice(chat_id=callback_query.from_user.id,
                               title=t,
                               description=d,
                               provider_token=YOOTOKEN,
                               currency='RUB',
                               photo_url=None,
                               need_phone_number=False,
                               need_email=False,
                               is_flexible=False,
                               prices=[LabeledPrice(label=l, amount=int(255000))],
                               start_parameter='6_months',
                               payload=l,
                               reply_markup=keyboard
                               )
    elif pay_num[1] == '12':
        keyboard.add(InlineKeyboardButton("Заплатить 500,00 RUB", pay=True))
        keyboard.add(back)
        if pay_num[2] == 'Buy':
            t='Оформление подписки на 12 месяцев'
            d='12 месяцев подписки'
            l='Оформление подписки на 12 месяцев'
        elif pay_num[2] == 'renewal':
            t = 'Продление подписки на 12 месяцев'
            d = '12 месяцев подписки'
            l = 'Продление подписки на 12 месяцев'
        await bot.send_invoice(chat_id=callback_query.from_user.id,
                               title=t,
                               description=d,
                               provider_token=YOOTOKEN,
                               currency='RUB',
                               photo_url=None,
                               need_phone_number=False,
                               need_email=False,
                               is_flexible=False,
                               prices=[LabeledPrice(label=l, amount=int(480000))],
                               start_parameter='12_months',
                               payload=l,
                               reply_markup=keyboard
                               )

######## ХЗ ЧЕ ЭТО, НО БЕЗ НЕГО НЕ РАБОТАЕТ ########
@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)#########################################################################################################

######## ЕСЛИ ОПЛАТА ПРОШЛА УСПЕШНО, ТО СРАБАТЫВАЕТ ЭТОТ БОЛОК КОДА ########
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay (message: types.Message):
    if message.successful_payment.invoice_payload=="Оформление подписки на 1 месяц":
        await db_update_sys('subscription', message.from_user.id, str(time.time()+day_to_sec(31)))
        await process_callback_check_subs_1(message.from_user.id, 0)
    elif message.successful_payment.invoice_payload=="Оформление подписки на 3 месяца":
        await db_update_sys('subscription', message.from_user.id, time.time()+day_to_sec(92))
        await process_callback_check_subs_1(message.from_user.id, 0)
    elif message.successful_payment.invoice_payload=="Оформление подписки на 6 месяцев":
        await db_update_sys('subscription', message.from_user.id, time.time()+day_to_sec(182))
        await process_callback_check_subs_1(message.from_user.id, 0)
    elif message.successful_payment.invoice_payload=="Оформление подписки на 12 месяцев":
        await db_update_sys('subscription', message.from_user.id, time.time()+day_to_sec(365))
        await process_callback_check_subs_1(message.from_user.id, 0)


    elif message.successful_payment.invoice_payload == "Продление подписки на 1 месяц":
        subscripti = await db_select_sys('subscription', message.from_user.id)
        f = float(subscripti[0])
        g = int(day_to_sec(31))
        await db_update_sys('subscription', message.from_user.id, f+g)
        await process_callback_check_subs_1(message.from_user.id, 0)
    elif message.successful_payment.invoice_payload=="Продление подписки на 3 месяца":
        subscripti = await db_select_sys('subscription', message.from_user.id)
        await db_update_sys('subscription', message.from_user.id, subscripti[0][0]+day_to_sec(92))
        await process_callback_check_subs_1(message.from_user.id, 0)
    elif message.successful_payment.invoice_payload=="Продление подписки на 6 месяцев":
        subscripti = await db_select_sys('subscription', message.from_user.id)
        await db_update_sys('subscription', message.from_user.id, subscripti[0][0]+day_to_sec(182))
        await process_callback_check_subs_1(message.from_user.id, 0)
    elif message.successful_payment.invoice_payload=="Продление подписки на 12 месяцев":
        subscripti = await db_select_sys('subscription', message.from_user.id)
        await db_update_sys('subscription', message.from_user.id, subscripti[0][0]+day_to_sec(365))
        await process_callback_check_subs_1(message.from_user.id, 0)

def day_to_sec(day):
    return day*60*60*24+3600*3

@dp.callback_query_handler(lambda c: c.data.startswith('backpr'))
async def process_callback_check_pay(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    back_pr_num = callback_query.data.split(':')
    if back_pr_num[1] == '1':
        await process_callback_check_subs_1(callback_query.from_user.id, callback_query.message.message_id)
    elif back_pr_num[1] == '2':
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

################# ПРОВЕРКА ПОДПИСКИ НА СПОНСОРОВ ##############
async def subscription_verification(id):
    with sq.connect(f'{pat}db_admin.db') as con:
        sql = con.cursor()
        sql.execute(f"SELECT * FROM admin WHERE chat_id == 1277447609")
        sponsor_list = sql.fetchall()
    sponsor_list = list(sponsor_list[0][1::])
    if 'nonee' in sponsor_list:
        with sq.connect(f'{pat}db_admin.db') as con:
            sql = con.cursor()
            sql.execute(f"SELECT * FROM admin WHERE chat_id == '1277447609'")
            a = list(sql.fetchall())
        a = list(a[0])
        del a[0]
        while 'nonee' in a:
            a.remove('nonee')
        while '' in a:
            a.remove('')
        sponsor_list = a[::]
        if len(a) < 6:
            v = 6 - len(a)
            for i in range(v):
                a.append('')
        with sq.connect(f'{pat}db_admin.db') as con:
            sql = con.cursor()
            sql.execute(
                "UPDATE admin SET donor_1 = ?, donor_2 = ?, donor_3 = ?, donor_4 = ?, donor_5 = ?, donor_6 = ?",
                (a[0], a[1], a[2], a[3], a[4], a[5]))
            con.commit()
    while '' in sponsor_list:
        sponsor_list.remove('')
    for i in sponsor_list:
        i = f"@{i[13::]}"
        chat_member = await bot.get_chat_member(chat_id=i, user_id=id)
        if chat_member.status == 'member' or chat_member.status == 'creator' or chat_member.status == 'admin':
            pass
        else:
            return False
    return True

async def subscription_verification_send_link(id):
    with sq.connect(f'{pat}db_admin.db') as con:
        sql = con.cursor()
        sql.execute(f"SELECT * FROM admin WHERE chat_id == 1277447609")
        sponsor_list = sql.fetchall()
    sponsor_list = sponsor_list[0][1::]
    for i in range(len(sponsor_list)):
        if sponsor_list[i] == '':
            sponsor_list = sponsor_list[:i]
            break
    buttons = [types.InlineKeyboardButton(f"Спонсор {x + 1}", url=f"{sponsor_list[x]}") for x in range(len(sponsor_list))]
    buttons_1 = (types.InlineKeyboardButton(text="Проверить подписку", callback_data='Checking subscription'))
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons).add(buttons_1)
    if len(sponsor_list) == 1:
        await bot.send_message(chat_id=id, text='Подпишитесь на канал спонсора, чтобы пользоваться ботом.',
                               reply_markup=keyboard)
    elif len(sponsor_list) >= 2:
        await bot.send_message(chat_id=id, text='Подпишитесь на каналы спонсоров, чтобы пользоваться ботом.',
                               reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith('Checking subscription'))
async def process_callback_check_subs(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if await subscription_verification(callback_query.from_user.id) == True:
        await main.start(callback_query.from_user.id)
    else:
        await subscription_verification_send_link(callback_query.from_user.id)