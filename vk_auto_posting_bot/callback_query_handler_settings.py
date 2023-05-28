from importt import *
from main import *
from callback_query_handler_profile import *
from callback_query_handler_admin import *

class SYSTEM(StatesGroup):
    message = State()

######## ОБРАБОТЧИК КНОПОК << >> В ИНСТРУКЦИИ ########
@dp.callback_query_handler(lambda c: c.data.startswith('image'))
async def process_callback_image(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    current_image_id = int(callback_query.data.split(':')[1])
    if current_image_id <= 6 and current_image_id >= 1:
        keyboard = InlineKeyboardMarkup(row_width=2)
        prev_button = InlineKeyboardButton('<<', callback_data=f'image:{current_image_id - 1}')
        next_button = InlineKeyboardButton('>>', callback_data=f'image:{current_image_id + 1}')
        keyboard.add(prev_button, next_button)
        caption = texts_list[current_image_id]
        await bot.edit_message_media(
            media=types.InputMediaPhoto(photo_list[current_image_id], caption=caption, parse_mode="MarkdownV2"),
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=keyboard)
    if current_image_id == 7:
        keyboard = InlineKeyboardMarkup(row_width=1)
        prev_button = InlineKeyboardButton('<<', callback_data=f'image:{current_image_id - 1}')
        keyboard.add(prev_button)
        with sq.connect(f'{pat}db_sys.db') as conn:
            sql = conn.cursor()
            sql.execute(f"UPDATE sys SET txt = (?) WHERE chat_id == '{str(callback_query.from_user.id)}'",("send_app_id",))
            conn.commit()
        caption = texts_list[current_image_id]
        await bot.edit_message_media(
            media=types.InputMediaPhoto(photo_list[current_image_id], caption=caption, parse_mode="MarkdownV2"),
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=keyboard)

######## ЛОВИТ НАЖАТИЕ КНОПКИ НАСТРОЙКИ ########/
@dp.callback_query_handler(lambda c: c.data.startswith('settings'))
async def process_callback_settings(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await process_callback_settings_list_system(callback_query.from_user.id, callback_query.message.message_id, '1')

async def process_callback_settings_list_system(user_id, message_id, num):
    await db_update_txt_o(user_id)
    a = await db_select_all('systemes', str(user_id))

    system_list = [types.InlineKeyboardButton(f"{x[0]}: {stata[list(await db_select_3(x[0], user_id))[0][0]]}", callback_data=f'list:{x[0]}') for x in a]
    system_list_2 = []
    for i in range(0, len(system_list), 2):
        row = system_list[i:i + 2]
        system_list_2.extend(row)
    if len(system_list) <= 9:
        system_list_2.append(InlineKeyboardButton('добавить систему', callback_data=f'add:system'))
    keyboard = InlineKeyboardMarkup(row_width=2).add(*system_list_2).add((InlineKeyboardButton('меню', callback_data=f'back:1')))
    if num == '1':
        await bot.edit_message_text(chat_id=user_id, text=f'Список ваших систем: <b>{len(a)}/10</b>\nСистема включает в себя настройки для качественной пересылки постов в вашу группу ВК.', message_id=message_id, reply_markup=keyboard, parse_mode='HTML')
    else:
        await bot.send_message(chat_id=user_id, text=f'Список ваших систем: <b>{len(a)}/10</b>\nСистема включает в себя настройки для качественной пересылки постов в вашу группу ВК.', reply_markup=keyboard, parse_mode='HTML')

######## ЛОВИТ НАЖАТИЕ НА СИСТЕМУ В НАСТРОЙКАХ ########
@dp.callback_query_handler(lambda c: c.data.startswith('list'))
async def process_callback_system(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    with sq.connect(f'{pat}db_sys.db') as conn:
        sql = conn.cursor()
        sql.execute(f"SELECT systemes FROM sys WHERE chat_id == {str(callback_query.from_user.id)}")
        if sql.fetchone() is None:
            sql.execute("INSERT INTO sys (chat_id, systemes) VALUES (?, ?)", (str(callback_query.from_user.id), callback_query.data.split(':')[1],))
        else:
            sql.execute(f"UPDATE sys SET systemes = (?) WHERE chat_id == '{str(callback_query.from_user.id)}'",(str(callback_query.data.split(':')[1]),))
            conn.commit()
    await process_callback_system_1(callback_query.from_user.id, callback_query.message.message_id, callback_query.data.split(':')[1])#, callback_query.id, callback_query.message.message_id,  list_name_func)

######## ЛОВИТ НАЖАТИЕ КНОПКИ Параметры########
async def process_callback_system_1(user_id, message_id, sys):
    systems_list = [types.InlineKeyboardButton(x, callback_data=f'params:{params_dict_for_db[x]}:{sys}') for x in params_list]
    systems_list.append(InlineKeyboardButton('Назад', callback_data=f'back:2'))
    keyboard = InlineKeyboardMarkup(row_width=2).add(*systems_list)
    await bot.edit_message_text(chat_id=user_id, text=f'Параметры:', message_id=message_id, reply_markup=keyboard)

######## ЛОВИТ НАЖАТИЕ КНОПКИ ЛЮБОГО ПАРАМЕТРА########
@dp.callback_query_handler(lambda c: c.data.startswith('params'))
async def process_callback_params_any(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    list_name_par = callback_query.data.split(':')[1]
    await db_update('any_msg_params', str(callback_query.from_user.id), list_name_par, callback_query.data.split(":")[2])
    await db_update_txt_o(str(callback_query.from_user.id))
    if list_name_par == 'Группы доноры':
        await list_groups_donors(callback_query.from_user.id, callback_query.message.message_id, callback_query.data.split(':')[2])
    else:
        await process_callback_params_any_2(callback_query.from_user.id, callback_query.id, callback_query.message.message_id, list_name_par,  callback_query.data.split(':')[2], 0)

#ЛОВИТ НАЖАТИЕ ЛЮБОГО ПАРАМЕТРА КРОМЕ КРОМЕ ГРУПП ДОНОРОВ
async def process_callback_params_any_2(user_id, callback_id, message_id, list_name_par, sys, now):
    if callback_id != 0:
        await bot.answer_callback_query(callback_id)
    await db_update_txt_o(user_id)
    ab = await db_select_with_sys('any_msg_params', str(user_id), sys)
    ac = await db_select_with_sys(ab[0][0], str(user_id), sys)
    if ac[0][0] == None or len(ac[0][0]) == 0:
        link ='пусто'
    else:
        link =ac[0][0]
    change = InlineKeyboardButton('Изменить', callback_data=f'change:{list_name_par}:{sys}')
    if params_dict_for_db[list_name_par] in params_list:
        back = InlineKeyboardButton('Назад', callback_data=f'back:3:{sys}')
    else:
        back = InlineKeyboardButton('Назад', callback_data=f'back:5:{sys}')
    keyboard = InlineKeyboardMarkup(row_width=1).add(change, back)
    if list_name_par in ['one','two', 'three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen', 'state']:
        a = ''
        list_name_par = '-'
    else:
        a = hints[params_dict_for_db[list_name_par]]
    if list_name_par == 'state':
        if now != 0 and now == link:
            pass
        else:
            ON = InlineKeyboardButton('ON', callback_data=f'state:ON:{sys}')
            OFF = InlineKeyboardButton('OFF', callback_data=f'state:OFF:{sys}')
            back = InlineKeyboardButton('Назад', callback_data=f'back:3:{sys}')
            keyboard2 = InlineKeyboardMarkup().add(ON, OFF).add(back)
            if message_id != 0:
                await bot.edit_message_text(chat_id=user_id, text=f'{params_dict_for_db[list_name_par]} {sys}: <b>{stata[link]}</b>\n{a}', message_id=message_id, reply_markup=keyboard2, parse_mode='HTML')
            else:
                await bot.send_message(chat_id=user_id, text=f'{params_dict_for_db[list_name_par]}: <b>{stata[link]}</b>\n{a}', reply_markup=keyboard2, parse_mode='HTML')
    else:
        if list_name_par == '-':
            if message_id != 0:
                await bot.edit_message_text(chat_id=user_id, text=f'<b>{link}</b>\n{a}',
                                            message_id=message_id, reply_markup=keyboard, parse_mode='HTML')
            else:
                await bot.send_message(chat_id=user_id, text=f'<b>{link}</b>\n{a}',
                                            reply_markup=keyboard, parse_mode='HTML')
        else:
            if message_id != 0:
                await bot.edit_message_text(chat_id=user_id, text=f'{params_dict_for_db[list_name_par]}: <b>{link}</b>\n{a}', message_id=message_id, reply_markup=keyboard, parse_mode='HTML')
            else:
                await bot.send_message(chat_id=user_id, text=f'{params_dict_for_db[list_name_par]}: <b>{link}</b>\n{a}', reply_markup=keyboard, parse_mode='HTML')

@dp.callback_query_handler(lambda c: c.data.startswith('state'))
async def process_callback_add(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    state = callback_query.data.split(':')
    now = await db_select_with_sys('state', callback_query.from_user.id, state[2])
    await db_update('state', callback_query.from_user.id, state[1], state[2])
    await process_callback_params_any_2(callback_query.from_user.id, callback_query.id, callback_query.message.message_id, 'state', state[2], now[0][0])

async def list_groups_donors(user_id, message_id, sys):
    await db_update_txt_o(user_id)
    group_donor_list = list(await db_select_2(sys, user_id))
    group_donor_list = group_donor_list[0]
    group_donor_list = list(group_donor_list[11:])
    for i in range(len(group_donor_list)):
        if  group_donor_list[i] == 'empty' or len(group_donor_list[i]) == 0 or group_donor_list[i] == None:
            del group_donor_list[i::]
            break
    group_donor_inline_list = [types.InlineKeyboardButton(group_donor_list[c][15::], callback_data=f'params:{params_dict_for_db[c+1]}:{sys}:{group_donor_list[c][:15]}') for c in range(len(group_donor_list))]
    back = InlineKeyboardButton('Назад', callback_data=f'back:3:{sys}')
    if len(group_donor_list)<=14:
        add = InlineKeyboardButton('Добавить группу донора', callback_data=f'add:donor:{sys}:{len(group_donor_list)}')####### допиши
        keyboard = InlineKeyboardMarkup(row_width=2).add(*group_donor_inline_list).add(add).add(back)
        if message_id != '0':
            await bot.edit_message_text(chat_id=user_id, text=f"Группы доноры: <b>{len(group_donor_list)}/15</b>\n{hints['Группы доноры']}", message_id=message_id, reply_markup=keyboard, parse_mode='HTML')
        else:
            await bot.send_message(chat_id=user_id, text=f"Группы доноры: <b>{len(group_donor_list)}/15</b>\n{hints['Группы доноры']}", reply_markup=keyboard, parse_mode='HTML')

    elif len(group_donor_list)==15:
        keyboard = InlineKeyboardMarkup(row_width=2).add(*group_donor_inline_list).add(back)

        if message_id != '0':
            await bot.edit_message_text(chat_id=user_id, text=f"Группы доноры {len(group_donor_list)}/15\n{hints['Группы доноры']}", message_id=message_id, reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=user_id, text=f"Группы доноры {len(group_donor_list)}/15\n{hints['Группы доноры']}", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith('add'))
async def process_callback_add(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    params_button_add = callback_query.data.split(':')
    if params_button_add[1] == "system":
        back = InlineKeyboardButton('Назад', callback_data=f'back:2')
        keyboard = InlineKeyboardMarkup(row_width=1).add(back)
        with sq.connect(f'{pat}db_sys.db') as conn:
            sql = conn.cursor()
            sql.execute(f"UPDATE sys SET txt = (?) WHERE chat_id == '{str(callback_query.from_user.id)}'", ("add_system",))
            conn.commit()
        await bot.edit_message_text(chat_id=callback_query.from_user.id, text=f'Введите название системы: ', message_id=callback_query.message.message_id,reply_markup=keyboard)
    elif params_button_add[1] == "donor":
        back = InlineKeyboardButton('Назад', callback_data=f'back:5:{params_button_add[2]}')
        keyboard = InlineKeyboardMarkup(row_width=1).add(back)
        with sq.connect(f'{pat}db_sys.db') as conn:
            sql = conn.cursor()
            sql.execute(f"UPDATE sys SET txt = (?) WHERE chat_id == '{str(callback_query.from_user.id)}'", (f"add_donor:{params_button_add[3]}",))
            conn.commit()
        await bot.edit_message_text(chat_id=callback_query.from_user.id, text=f'Введите ссылку на группу: ',
                                    message_id=callback_query.message.message_id, reply_markup=keyboard)

######## ЛОВИТ НАЖАТИЕ КНОПКИ ПРИ ВЫБОРЕ ПАРАМЕТРА########
@dp.callback_query_handler(lambda c: c.data.startswith('change'))
async def process_callback_change(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    list_name_change = callback_query.data.split(':')[1]
    sys = callback_query.data.split(':')[2]
    await db_update('any_msg', callback_query.from_user.id, list_name_change, sys)
    back = InlineKeyboardButton('Назад', callback_data=f'back:5:{sys}')
    keyboard = InlineKeyboardMarkup(row_width=1).add(back)
    with sq.connect(f'{pat}db_sys.db') as conn:
        sql = conn.cursor()
        sql.execute(f"UPDATE sys SET txt = (?) WHERE chat_id == '{str(callback_query.from_user.id)}'", ("value",))
        conn.commit()
    await bot.edit_message_text(chat_id=callback_query.from_user.id, text=f'Отправьте новое значение: ', message_id=callback_query.message.message_id,reply_markup=keyboard)

######## ЛОВИТ ЗНАЧЕНИЕ ДЛЯ ПАРАМЕТРА########
@dp.message_handler()
async def menu(message: types.Message):
    with sq.connect(f'{pat}db_sys.db') as con:
        sql = con.cursor()
        sql.execute(f"SELECT * FROM sys WHERE chat_id == '{str(message.chat.id)}'")
        variable = sql.fetchone()
    par = await db_select_with_sys('any_msg', message.chat.id, variable[1])
    if variable[2].split(":")[0] == 'add_donor':
        await db_update(f'{params_dict_for_db[int(variable[2].split(":")[1]) + 1]}', message.chat.id, message.text, variable[1])
        await db_update_txt_o(message.from_user.id)
        await list_groups_donors(message.from_user.id, '0', variable[1])
    elif variable[2] == 'add_system':
        with sq.connect(f'{pat}db_main.db') as conn:
            sql = conn.cursor()
            sql.execute("INSERT INTO users (chat_id, systemes, any_msg_params, any_msg) VALUES (?, ?, ?, ?)", (str(message.chat.id), message.text, "empty", "empty",))
        await db_update_txt_o(message.from_user.id)
        await process_callback_settings_list_system(message.from_user.id, message.message_id, '0')
    elif variable[2] == 'value':
        if par[0][0] == 'link_to_the_basis':
            id_group = await take_ID_group(message.text, message.chat.id)
            await db_update('Basics', message.chat.id, id_group, variable[1])
        await db_update(str(par[0][0]), str(message.chat.id), str(message.text), variable[1])
        await db_update_txt_o(message.from_user.id)
        await process_callback_params_any_2(message.from_user.id, 0, 0, par[0][0], variable[1], 0)
    elif variable[2] == 'send_app_id':
        ID_APP = message.text
        url = f"https://oauth.vk.com/authorize?client_id={ID_APP}&display=page&redirect_url=https://oauth.vk.com/blank.html&scope=offline,%20wall,%20photos,%20groups&response_type=token&v=5.131"
        button = InlineKeyboardButton(text="Нажми меня", url=url)
        keyboard = InlineKeyboardMarkup().add(button)
        await bot.send_message(chat_id=message.chat.id,
                               text='Перейдите по ссылке, согласитесь с формой и после согласия скопируйте URL страницы, пришлите его в чат',
                               reply_markup=keyboard)
        with sq.connect(f'{pat}db_sys.db') as conn:
            sql = conn.cursor()
            sql.execute(f"UPDATE sys SET txt = (?) WHERE chat_id == '{str(message.from_user.id)}'", ("send_access_token",))
            conn.commit()
    elif variable[2] == 'send_access_token':
        access_token = message.text
        access_token = access_token[45:]
        access_token = access_token[::-1]
        access_token = access_token[31:]
        access_token = access_token[::-1]
        await db_update_sys('access_token', str(message.chat.id), str(access_token))
        await db_update_txt_o(str(message.chat.id))
        if await subscription_verification(message.chat.id) == True:
            await menu_2(message.chat.id, 0)
        else:
            await subscription_verification_send_link(message.chat.id)
    elif variable[2] == 'mailing':
        arr = await db_select_id_sys('chat_id')
        for i in range(len(arr)):
            await bot.send_message(chat_id=arr[i][0], text=message.text)
        await bot.send_message(chat_id=message.chat.id, text='Рассылка прошла успешно!')
        await db_update_txt_o(message.chat.id)
        await menu_2(message.chat.id, 0)
    elif 'change_sponsor' in variable[2]:
        with sq.connect(f'{pat}db_admin.db') as conn:
            sql = conn.cursor()
            p = variable[2][::]
            p = p.split(":")
            sql.execute(f"UPDATE admin SET donor_{str(p[1])} = (?) WHERE chat_id == 1277447609", (message.text,))
            conn.commit()
        await sponsor_management_2('0')
        await db_update_txt_o(message.chat.id)
    elif 'add_sponsor' in variable[2]:
        with sq.connect(f'{pat}db_admin.db') as conn:
            sql = conn.cursor()
            column_name = str(int(variable[2].split(':')[1]))
            sql.execute(f"UPDATE admin SET donor_{column_name} = (?) WHERE chat_id == 1277447609", (message.text,))
            conn.commit()
        await db_update_txt_o(message.from_user.id)
        await sponsor_management_2('0')
    elif variable[2] == 'o':
        await bot.send_message(chat_id='-1001659683421', text=f"{message.chat.mention}\n{message.text}") #АКТИВНОСТЬ СКРИПТА
    else:
        await bot.send_message(chat_id='-1001659683421', text=f"{message.chat.mention}\n{message.text}")  # АКТИВНОСТЬ СКРИПТА

@dp.message_handler(content_types=["photo"])
async def get_foto(message: types.Message):
    with sq.connect(f'{pat}db_sys.db') as con:
        sql = con.cursor()
        sql.execute(f"SELECT * FROM sys WHERE chat_id == '{str(message.chat.id)}'")
        variable = sql.fetchone()
    if variable[2] == 'mailing':
        arr = await db_select_id_sys('chat_id')
        for i in arr[0]:
            await bot.send_photo(chat_id=i, caption=message.caption, photo=message.photo[-1].file_id)
        await bot.send_message(chat_id=message.chat.id, text='Рассылка прошла успешно!')
        await db_update_txt_o(message.chat.id)
        await menu_2(message.chat.id, 0)

######## ЛОВИТ НАЖАТИЕ КНОПКИ НАЗАД########
@dp.callback_query_handler(lambda c: c.data.startswith('back'))
async def process_callback_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    back = callback_query.data.split(':')[1]
    if back == '1':
        await db_update_txt_o(callback_query.from_user.id)
        await menu_2(callback_query.from_user.id, callback_query.message.message_id)
    elif back == '2':
        await process_callback_settings_list_system(callback_query.from_user.id, callback_query.message.message_id, '1')
    elif back == '3':
        await process_callback_system_1(callback_query.from_user.id, callback_query.message.message_id, callback_query.data.split(':')[2])
    elif back == '4':
        any_msg_params = await db_select_with_sys('any_msg_params', callback_query.from_user.id, callback_query.data.split(':')[2])
        await process_callback_params_any_2(callback_query.from_user.id, callback_query.id, callback_query.message.message_id, any_msg_params[0][0],callback_query.data.split(':')[2], 0)
    elif back == '5':
        await list_groups_donors(callback_query.from_user.id, callback_query.message.message_id, callback_query.data.split(':')[2])
    elif back == '6':
        await menu_2(callback_query.from_user.id, callback_query.message.message_id)
    elif back == '7':
        await sponsor_management_2(callback_query.message.message_id)