# pat = '/root/PROJECT/'
pat = '/root/PROJECT/'
######## AIOGRAM ########
from aiogram.types.message import ContentType
import aiogram.utils.markdown
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ParseMode, InlineKeyboardMarkup, PhotoSize, InputFile, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import link
import logging

######## IMPORTING ########
from importt import *

from db_manage import *


######## OTHER IMPORTS ########
import os
import time
import random
import sqlite3 as sq
import re
from datetime import datetime


import datetime as dt

#
######## CONST ########
TOKEN = '6160769606:AAG4nyeecO_RpCj64QB6Z_lvTHBM8O1uTUs'
YOOTOKEN = "381764678:TEST:55345"
v = 5.131
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


######## CLASS ########
class actions(StatesGroup):
    ID_APP = State()
    URL = State()
    change_link = State()
    FIO = State()


######## SHEETS ########
import httplib2

######## LISTS ########
photo_list = \
{1:"AgACAgIAAxkBAAMuZDuJn327Nb8pXndX6RQB90VqB4YAAkTLMRsYKeBJsKEawMoZg14BAAMCAAN4AAMvBA",
2:"AgACAgIAAxkBAAMwZDuJqdLnnGEzzkZVi77mcAKQ7DAAAkXLMRsYKeBJkL9paaEpi10BAAMCAAN5AAMvBA",
3:"AgACAgIAAxkBAAMyZDuJuDV4SYAhobj4BCrj0nyEuiEAAkbLMRsYKeBJttJ5vvoQWOwBAAMCAAN5AAMvBA",
4:"AgACAgIAAxkBAAM0ZDuJwK_cRNb9uIyLw_sUMSDmS7cAAkfLMRsYKeBJEtmQpC4GLbsBAAMCAAN5AAMvBA",
5:"AgACAgIAAxkBAAM2ZDuJyB85QLtD35eorAaHa-R3sdEAAkjLMRsYKeBJ_kUsWneWFSoBAAMCAAN4AAMvBA",
6:"AgACAgIAAxkBAANMZDuVgLxyo0iolZbtyJV5LqKfBC0AAqDIMRu8DOBJsSzVNZlRTv4BAAMCAAN4AAMvBA",
7:"AgACAgIAAxkBAANVZDubS1KzzmX2k-poqc11Pr5Cg18AArnIMRu8DOBJUF0NqRTsj3YBAAMCAAN4AAMvBA"}

texts_list = \
{1:'Для работы бота необходимо создать acess token\. Для этого зайдите на оффициальный сайт ' + link("VK", "https://vk\.com") + ' с компьютера и с лева в низу найдите раздел для '+ link("Разработчиков", "https://dev\.vk\.com") + ' и перейдите в него\.',
2:'После нужно создать приложение\. Просто нажмите на синюю кнопку\.',
3:'Теперь напишите название для вашего будущего приложения, это ни на что не влияет, пишите что угодно\.\nОбязательным условия является выбрать пункт \"Standalone\-приложение\", выбираем его и нажимаем \"Подключить приложение\"',
4:'Подтверждаем действия при помощи своего телефона',
5:'далее переходим в настройки\.',
6:'в найстройках обязательно должен быть \"Включен\" Open API\. Если он выключен, меняем на \"Включен\", листаем ниже и сохраняем настройки\.',
7:'После, нужно скопировать ID приложения и прислать его сообщением без лишних символов\. Перед отправкой ID приложения, нажмите на соответсвующуу кнопку ниже\.'}

hints = {'Ключевые слова': 'Напишите слова, который должны быть обязательно в тексте поста разделяя их знаком +\nПример: Дамблдор+Хагрид\nЕсли ключевых слов не будет в тексте поста, то его пересылка осуществляться не будет.\n<b>Чтобы изменить, скопируйте слова в буфер обмена, нажмите изменить, отредактируйте слова как вам нужно и отпарвьте. Слова можно заменить только целиком.</b>',
'Запретные слова': 'Напишите слова, которых не должно быть в тексте поста разделяя их знаком +\nПример: Казино+дурак+букмекер\nЕсли хотыбы 1 запретное слово будет в тексте поста, то его пересылка осуществляться не будет, даже при наличии ключевых слов. Если ключевые слова отсутствуют отсатьвьте пустым или знак -.\n<b>Чтобы изменить, скопируйте слова в буфер обмена, нажмите изменить, отредактируйте слова как вам нужно и отпарвьте. Слова можно заменить только целиком.</b>',
'Ссылка на основу': 'Ссылкана вашу группу ВК. В нее будет осуществляться переслка постов. Вы должны быть в ней администратором.',
'Хэштеги': 'В конец каждого поста будут добавленны хэштеги, который нужно указать через пробел.\nПример: #бизнес #книги #инвестиции\nЕсли хэштегов нет, то оставьте пустым или поставьте В таком случае мы удалим имеющийеся хэштеги в конце поста и ничего не добавим.\n<b>Чтобы изменить, скопируйте хэштеги в буфер обмена, нажмите изменить, отредактируйте хэштеги как вам нужно и отпарвьте. Хэштеги можно заменить только целиком.</b>',
'Группы доноры': 'Это группы, из которых мы будем брать новые посты и выкладывать в вашу основную группу.\nПример: https://vk.com/mivоcompany'}

params_list = \
['Ключевые слова',
'Запретные слова',
'Ссылка на основу',
'Хэштеги',
#'access_token',
'Группы доноры',
'Состояние']

stata = {'ON': '✅',
        'OFF': '❌'}

params_dict_for_db = \
{'Ключевые слова': 'Keywords',
'Запретные слова': 'Forbidden_words',
'Ссылка на основу': 'link_to_the_basis',
'Хэштеги':'Hashtag',
'Группы доноры':'Группы доноры',
'Состояние':"state",
'Keywords':'Ключевые слова',
'Forbidden_words':'Запретные слова',
'link_to_the_basis':'Ссылка на основу',
'Hashtag':'Хэштеги',
"state":'Состояние',
1:'one',
2:'two',
3:'three',
4:'four',
5:'five',
6:'six',
7:'seven',
8:'eight',
9:'nine',
10:'ten',
11:'eleven',
12:'twelve',
13:'thirteen',
14:'fourteen',
15:'fifteen',
'one': 'one',
'two': 'two',
'three': 'three',
'four': 'four',
'five': 'five',
'six': 'six',
'seven': 'seven',
'eight': 'eight',
'nine': 'nine',
'ten': 'ten',
'eleven': 'eleven',
'twelve': 'twelve',
'thirteen': 'thirteen',
'fourteen': 'fourteen',
'fifteen': 'fifteen'}

params_dict_for_db_2 = \
{'one': 1,
'two': 2,
'three': 3,
'four': 4,
'five': 5,
'six': 6,
'seven': 7,
'eight': 8,
'nine': 9,
'ten': 10,
'eleven': 11,
'twelve': 12,
'thirteen': 13,
'fourteen': 14,
'fifteen': 15}

linkl = {None: "пуста "}
