import asyncio
from threading import Thread

from callback_query_handler_settings import *
from callback_query_handler_profile import *
from callback_query_handler_admin import *

from importt import *
from work_with_VK_API import *
# from subscription_verification import *


@dp.message_handler(commands=['start'])
async def start_com(message: types.Message):
    await bot.send_message(chat_id='-1001659683421', text=f"{message.chat.mention}") #АКТИВНОСТЬ СКРИПТА

    await start(message.chat.id)#

@dp.message_handler(commands=['check'])
async def check(message: types.Message):
    if message.chat.id == 1277447609:
        await notos()

@dp.message_handler(commands=['help'])
async def start_com(message: types.Message):
    menu = InlineKeyboardButton(text="меню", callback_data='back_p:1')
    keyboard = InlineKeyboardMarkup().add(menu)
    await bot.send_message(chat_id=message.chat.id, text='Если у Вас есть вопросы или вам нужна помощь: @kleget', reply_markup=keyboard) #АКТИВНОСТЬ СКРИПТА
    # await start(message.chat.id)

######## ПРОВЕРЯЕТ НАЛИЧИЕ В БД И ОТПРАВЛЯЕТ ПЕРВУЮ СТРАНИЦУ ИНСТРУКЦИИ ########
async def start(id):
    if await subscription_verification(id) == True:
        with sq.connect(f'{pat}db_main.db') as con:
            sql = con.cursor()
            sql.execute(f"SELECT chat_id FROM users WHERE chat_id == {str(id)}")
            if sql.fetchone() is None:
                name_sys = 'first'
                await manual(id, name_sys)
            else:
                await menu_2(id, 0)
    else:
        await subscription_verification_send_link(id)

async def manual(id, name_sys):
    with sq.connect(f'{pat}db_main.db') as con:
        sql = con.cursor()
        sql.execute("INSERT INTO users (chat_id, systemes, any_msg_params, any_msg) VALUES (?, ?, ?, ?)",(str(id), name_sys, "empty", "empty",))
    with sq.connect(f'{pat}db_sys.db') as con:
        sql = con.cursor()
        sql.execute("INSERT INTO sys (chat_id, systemes, txt, subscription) VALUES (?, ?, ?, ?)", (str(id), 'first', 'o', str(time.time()+day_to_sec(14))))
        await bot.send_message(chat_id=id, text='Вам выдана бесплатная подписка на 14 дней.\nСпасибо, что вы с нами!☺️')
    await bot.send_message(chat_id=id, text='Пройдите настроку, это займет 1 минут')
    next_button = InlineKeyboardButton('>>', callback_data='image:2')
    keyboard = InlineKeyboardMarkup(row_width=1).add(next_button)
    caption = texts_list[1]
    await bot.send_photo(
        chat_id=id,
        photo="AgACAgIAAxkBAAMuZDuJn327Nb8pXndX6RQB90VqB4YAAkTLMRsYKeBJsKEawMoZg14BAAMCAAN4AAMvBA",
        caption=caption,
        reply_markup=keyboard,
        parse_mode="MarkdownV2")

######## УЗНАЕМ ID ГРУППЫ ЧЕРЕЗ КОРОТКОЕ ИМЯ ########
@dp.message_handler(commands=['ch'])
async def check_id(message: types.Message):
    id = await take_ID_group('rvp159', str(message.chat.id))
    await db_update("Basics", str(message.chat.id), str(id))

@dp.message_handler(commands=['menu'])
async def menu(message: types.Message):
    if await subscription_verification(message.chat.id) == True:
        await start(message.chat.id)
        # await menu_2(message.chat.id, 0)
    else:
        await start(message.chat.id)

async def menu_2(id, message_id):
    await db_update_txt_o(id)
    if str(id) == '1277447609':
        settings = InlineKeyboardButton('настройки ⚙', callback_data='settings')
        profile = InlineKeyboardButton('профиль 👤', callback_data='profile')
        mailing = InlineKeyboardButton('рассылка', callback_data='mailing')
        sponsor_management = InlineKeyboardButton('управление спонсорами', callback_data='sponsor_management')
        # if
        # notos = InlineKeyboardButton('notos', callback_data='notos')
        keyboard = InlineKeyboardMarkup(row_width=1).add(profile, settings, mailing, sponsor_management)
    else:
        settings = InlineKeyboardButton('настройки ⚙', callback_data='settings')
        profile = InlineKeyboardButton('профиль 👤', callback_data='profile')
        keyboard = InlineKeyboardMarkup(row_width=1).add(profile, settings)

    text = 'Меню:'
    if message_id == 0:
        await bot.send_message(
            chat_id=id,
            text=text,
            reply_markup=keyboard,
            parse_mode="MarkdownV2")
    elif message_id != 0:
        await bot.edit_message_text(
            chat_id=id,
            text=text,
            reply_markup=keyboard,
            message_id=message_id,
            parse_mode="MarkdownV2"
        )


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
        await bot.send_message(chat_id=id, text='Подпишитесь на канал спонсора, чтобы пользоваться ботом.', reply_markup=keyboard)
    elif len(sponsor_list) >= 2:
        await bot.send_message(chat_id=id, text='Подпишитесь на каналы спонсоров, чтобы пользоваться ботом.', reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith('Checking subscription'))
async def process_callback_check_subs(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if await subscription_verification(callback_query.from_user.id) == True:
        await start(callback_query.from_user.id)
    else:
        await subscription_verification_send_link(callback_query.from_user.id)

async def notos():
    while True:#
        await asyncio.sleep(3600*24)
        with sq.connect(f'{pat}db_sys.db') as con:
            sql = con.cursor()
            sql.execute(f"SELECT chat_id FROM sys")
            arr_id = sql.fetchall()
        for i in range(len(arr_id)):
            with sq.connect(f'{pat}db_sys.db') as con:
                sql = con.cursor()
                sql.execute(f"SELECT subscription FROM sys WHERE chat_id = {str(arr_id[i][0])}")
                sybss = sql.fetchone()
                if sybss != 'отсутствует':
                    one = float(day_to_sec(1))
                    two = float(day_to_sec(2))
                    three = float(day_to_sec(3))
                    now = time.time()
                    if float(sybss[0]) <= now+one:
                        await bot.send_message(chat_id = arr_id[i][0], text = 'До окончания подписки осталось меньше 1 дня. Для непрерывной работы сервиса продлите подписку.')
                    elif float(sybss[0]) <= now+two:
                        await bot.send_message(chat_id = arr_id[i][0], text = 'До окончания подписки осталось меньше 2 деней. Для непрерывной работы сервиса продлите подписку.')
                    elif float(sybss[0]) <= now+three:
                        await bot.send_message(chat_id = arr_id[i][0], text = 'До окончания подписки осталось меньше 3 деней. Для непрерывной работы сервиса продлите подписку.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    # thread1 = Thread(target=lambda: asyncio.run(notos()))
    # thread2 = Thread(target=lambda: executor.start_polling(dp, skip_updates=True))
    # thread1.start()
    # thread2.start()

    # loop = asyncio.get_event_loop()
    # thread1 = Thread(target=lambda: loop.run_until_complete(notos()))
    # thread2 = Thread(target=lambda: executor.start_polling(dp, skip_updates=True))
    # thread1.start()
    # thread2.start()

    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # thread = Thread(target=lambda: loop.run_until_complete(my_function()))
    # thread.start()
