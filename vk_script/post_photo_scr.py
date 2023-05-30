# from importt import *
import requests
import os

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import *

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import asyncio
TOKEN = '5644245123:AAE9C-kCT7rKig7vDAgOYeZVi5FbKehQ0Kw'
v = 5.131
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

def getWallUploadServer(group_id, access_token):
    r = requests.get('https://api.vk.com/method/photos.getWallUploadServer?',
                     params = {'access_token': access_token,
                                      'group_id': group_id,
                                      'v': v}).json()
    return r['response']['upload_url']

def save_r(group_id, upload_response, access_token):
    save_result = requests.get('https://api.vk.com/method/photos.saveWallPhoto?',
                                 params ={'access_token': access_token,
                                          'group_id': group_id,
                                          'photo': upload_response['photo'],
                                          'server': upload_response['server'],
                                          'hash': upload_response['hash'],
                                          'v': v}).json()
    # print(save_result)
    return (f"photo{str(save_result['response'][0]['owner_id'])}_{str(save_result['response'][0]['id'])}&access_key={str(save_result['response'][0]['access_key'])}")

def glavnaya(text, img_url, group_id, access_token, osnova):
    upload_url = getWallUploadServer(group_id, access_token)
    if img_url == 'nonono':
        result2 = requests.get('https://api.vk.com/method/wall.post?',
                               params={"message": text,
                                       'owner_id': -group_id,
                                       'access_token': access_token,
                                       'from_group': '1',
                                       'v': v}).json()
        # print(result2)
    else:
        img = requests.get(url=img_url)
        i = img_url[42:60]
        i = "".join(c for c in i if c.isalpha())#удаляем все симовлы кроме букв
        i = str('1' + i)
        open(f'IMG/{i}.jpg', 'wb').write(img.content)

        file = {'file1': open(f'IMG/{i}.jpg', 'rb')}
        upload_response = requests.post(upload_url, files=file).json()
        save_result = save_r(group_id, upload_response, access_token)
        file['file1'].close()

        result2 = requests.get('https://api.vk.com/method/wall.post?',
                                 params ={'attachments': save_result,
                                          "message": text,
                                          'owner_id': -group_id,
                                          'access_token': access_token,
                                          'from_group': '1',
                                          'v': v}).json()
        # print(result2)
        os.remove(f'IMG/{i}.jpg')
    print(f"https://vk.com/{osnova}?w=wall-{group_id}_{result2['response']['post_id']}\n\n")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mmmmm(f"https://vk.com/{osnova}?w=wall-{group_id}_{result2['response']['post_id']}\n\n", osnova, result2['response']['post_id']))
#
async def mmmmm(a, osnova, b):
    ke = InlineKeyboardButton(f"link", url=a)
    keyboard = InlineKeyboardMarkup(row_width=1).add(ke)
    await bot.send_message(chat_id='1277447609', text=f"{osnova}_{b}", reply_markup=keyboard)

async def xxx(a):
    await bot.send_message(chat_id='1277447609', text=a)

async def fff(a, b):
    await bot.send_message(chat_id='1277447609', text=f"подписка истекла. ID: {a} Group: {b}")