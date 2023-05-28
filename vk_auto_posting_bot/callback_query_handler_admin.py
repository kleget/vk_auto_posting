from importt import *
from main import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from aiogram.dispatcher.filters import Command

######## ЛОВИТ НАЖАТИЕ КНОПКИ ПРОВЕРИТЬ ПОДПИСКУ И ПРОВЕРЯЕТ ЕЁ ########
@dp.callback_query_handler(lambda c: c.data.startswith('mailing'))
async def mailing_1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await mailing_2(callback_query.from_user.id, callback_query.message.message_id)

async def mailing_2(user_id, id):
    keyboard = InlineKeyboardMarkup(row_width=2).add((InlineKeyboardButton('меню', callback_data=f'back:1')))
    await bot.edit_message_text(chat_id=user_id, text='Пришли пост для рассылки. Текст и можно картинку. Одним постом.', message_id=id, reply_markup=keyboard)
    await db_update_sys('txt', user_id, 'mailing')

@dp.callback_query_handler(lambda c: c.data.startswith('sponsor_management'))
async def sponsor_management_1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await sponsor_management_2(callback_query.message.message_id)

async def sponsor_management_2(msg_id):
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
    keyboard = []
    while '' in sponsor_list:
        sponsor_list.remove('')
    if len(sponsor_list) >= 1:
        listt = [types.InlineKeyboardButton(sponsor_list[x], callback_data=f'sponsor#{sponsor_list[x]}#{x+1}') for x in range(len(sponsor_list))]
        keyboard = InlineKeyboardMarkup(row_width=1).add(*listt)
    if len(sponsor_list) <= 5:
        keyboard.add(InlineKeyboardButton('Добавить спонсора', callback_data=f'add_sponsor:{len(sponsor_list)+1}'))
    keyboard.add(InlineKeyboardButton('Назад', callback_data=f'back:6'))
    if msg_id != '0':
        await bot.edit_message_text(chat_id='1277447609', text='Спонсоры:', message_id=msg_id, reply_markup=keyboard)
    else:
        await bot.send_message(chat_id='1277447609', text='Спонсоры:', reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith('sponsor'))
async def change_sponsor_1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    cc = callback_query.data.split('#')
    await change_sponsor_2(callback_query.message.message_id, cc[1], cc[2])

#ЛОВИТ НАЖАТИЕ ЛЮБОГО ПАРАМЕТРА КРОМЕ КРОМЕ ГРУПП ДОНОРОВ
async def change_sponsor_2(msg_id, spons, ind):
    await db_update_txt_o('1277447609')
    change = InlineKeyboardButton('Изменить', callback_data=f'change_sponsor:{ind}')
    back = InlineKeyboardButton('Назад', callback_data=f'back:7')
    keyboard = InlineKeyboardMarkup(row_width=1).add(change, back)
    await bot.edit_message_text(chat_id='1277447609', text=spons, message_id=msg_id, reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith('change_sponsor'))
async def change_sponsor_3(callback_query: types.CallbackQuery):
    ff = callback_query.data.split(':')
    await bot.answer_callback_query(callback_query.id)
    await db_update_sys('txt', '1277447609', f'change_sponsor:{ff[1]}')
    keyboard = (InlineKeyboardButton('Назад', callback_data=f'back:7'))
    await bot.edit_message_text(chat_id='1277447609', message_id=callback_query.message.message_id, text='Отправь нового спонсора:', reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith('add_sponsor'))
async def add_sponsor_3(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    ff = callback_query.data.split(':')
    await db_update_sys('txt', '1277447609', f'add_sponsor:{ff[1]}')
    keyboard = (InlineKeyboardButton('Назад', callback_data=f'back:7'))
    await bot.edit_message_text(chat_id='1277447609', message_id=callback_query.message.message_id, text='Отправь нового спонсора для добавления:', reply_markup=keyboard)

