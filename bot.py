from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import json
import re
import logging
from config import get_config
from db import *

bot_token = get_config()['bot_token']
bot = Bot(bot_token) #Telegram bot token
dp = Dispatcher(bot)

#logging.basicConfig(level=logging.INFO, filename="log.log",filemode="a",
#                    format="%(asctime)s %(levelname)s %(message)s")



with open('songs.json', 'r', encoding='utf8') as file:
    data = json.load(file)
data_songs = set()
for artist, song in data.items():
    for s in song:
        data_songs.add(s)


async def send_msg(usr_id:int, text:str):
    try:
        firs = 0
        last = 100
        msg_c = len(text.split('\n'))
        while True:
            if msg_c - last < 0:
                await bot.send_message(usr_id, '\n'.join(text.split('\n')[firs:]), parse_mode="Markdown")
                break

            elif msg_c < last:
                await bot.send_message(usr_id, '\n'.join(text.split('\n')[firs:]), parse_mode="Markdown")
                break

            await bot.send_message(usr_id, '\n'.join(text.split('\n')[firs:last]), parse_mode="Markdown")

            firs += 100
            last += 100

    except Exception as e:
        logging.exception(e)



@dp.message_handler(commands=['list_order'])
async def send_welcome(msg: types.Message):
    text = get_order_book()
    usr_id = msg.from_user.id

    await send_msg(usr_id, text)



@dp.message_handler(commands=['clear_order_book'])
async def send_welcome(msg: types.Message):
    if clear_order_book():
        await bot.send_message(msg.from_user.id, "Список заказов очищен")

    else:
        await bot.send_message(msg.from_user.id, "Что-то пошло не так")




@dp.message_handler(commands=['order'])
async def send_welcome(msg: types.Message):
    usr_id = str(msg.from_user.id)

    if len(msg.text.split(' ')) > 1:
        song = msg.text[7:]
        name = get_name(usr_id)

        if name != None:
            if add_order(name, song):
                await bot.send_message(msg.from_user.id, f'Заказ на песню {song} записан')
            else:
                await bot.send_message(msg.from_user.id, "Что-то пошло не так")

        else:
            await bot.send_message(msg.from_user.id, "Ты не ввел име, для указания имя нужно ввести команду так: /name Иван")

    else:
        await bot.send_message(msg.from_user.id, "Ты не ввел название песни которую хочешь заказать, для указания песни нужно ввести команду так: /order ABBA")




@dp.message_handler(commands=['name'])
async def send_welcome(msg: types.Message):
    usr_id = str(msg.from_user.id)

    if len(msg.text.split(' ')) > 1:
        name = msg.text[6:]
        if set_name(name, usr_id):
            await bot.send_message(msg.from_user.id, f"Ты установил себе име {name}")
        else:
            await bot.send_message(msg.from_user.id, "Что-то пошло не так(")

    else:
        await bot.send_message(msg.from_user.id, "Ты не ввел име, для указания имя нужно ввести команду так: /name Иван")






@dp.message_handler(commands=['not_in_db'])
async def send_welcome(msg: types.Message):
    usr_id = msg.from_user.id
    await bot.send_message(usr_id, "Я проверяю, подожди.")
    text = not_in_db(data, data_songs)


    await send_msg(usr_id, text)



@dp.message_handler(commands=['get_log'])
async def send_welcome(msg: types.Message):
    text, _ = data_log()
    usr_id = msg.from_user.id

    await send_msg(usr_id, text)



@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg: types.Message):
    text = """Для поиска отправьте боту часть названия песни или исполнителя.
Также по нажатию на песню или исполнителя текст копируется и вы можете вставить его в поиск.
По всем вопросам: @yastr
    """
    await bot.send_message(msg.from_user.id,text)




@dp.message_handler()
async def all_msg(msg: types.Message):
    logging.info(f"user_id: {msg.from_user.id} text: {msg.text.strip()}")
    songs_list, artist_list = search(str(msg.text).strip(), data, data_songs)
    r = r'\(.*\)|#|\d{5,}|\{.*\}|•|\[.*\]'


    text = ''
    #получение песен из списка артистов и запись их
    for art in artist_list:
        song_artist = data[art]
        text += f'\n🎤 `{art}`:\n'
        text += ''.join([f'- `{re.sub(r, "", song.capitalize())}`\n' for song in sorted(song_artist)])


    #получение списка артистов из песен и записить их
    if len(songs_list) > 0:
        other_dict, songs_list = get_sing_from_other(songs_list, data)

        for art, songs in other_dict.items():
            text += f'\n🎤 `{art}`:\n'
            text += ''.join([f'- `{re.sub(r, "", song.capitalize())}`\n' for song in sorted(songs)])


    #запись песен если не найден исполнитель
    if len(songs_list) > 0:
        text += '\n🎤 - OTHER -:\n'
        text += ''.join([f'- `{re.sub(r, "", s.capitalize())}`\n' for s in sorted(songs_list)])


    #запись есть ничего не найдено
    if text == '':
        text = 'Песня или исполнитель не найдены\n'

    usr_id = msg.from_user.id
    await send_msg(usr_id, text)





if __name__ == '__main__':
    executor.start_polling(dp)
