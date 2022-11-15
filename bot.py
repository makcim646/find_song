from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import json
import re
import logging
from config import get_config

bot_token = get_config()['bot_token']

bot = Bot(bot_token) #Telegram bot token
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO, filename="log.log",filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")

with open('songs.json', 'r', encoding='utf8') as file:
    data = json.load(file)
data_songs = set()
for artist, song in data.items():
    for s in song:
        data_songs.add(str(s))


def search(text:str):
    text = text.upper()
    r = re.compile(f".*{text}.*")
    song_list = list(filter(r.match, data_songs))
    artist_list = list(filter(r.match, data))

    if len(artist_list) == 0:
        for key in data.keys():
            if key == text:
                artist_list.append(key)

    return song_list, artist_list


def get_sing_from_other(songs:dict):
    other_dict = {}
    remov = set()
    for key, items in data.items():

        for s in songs:
            if s in items:
                if other_dict.get(key) == None:
                    other_dict[key] = [s]
                    remov.add(s)
                else:
                    other_dict[key].append(s)
                    remov.add(s)

    for r in remov:
        songs.remove(r)

    return other_dict, songs



def data_log():
    with open('log.log', 'r') as file:
        lines = file.readlines()

    answ = {}
    for line in lines:
        find_text = re.findall(r'text: .*', line)
        if find_text:
            text = find_text[0].split(': ')[1]
            if answ.get(text) == None:
                answ[text] = 1
            else:
                answ[text] += 1

    text = 'Список запросов пользователей:\n'
    for key, items in answ.items():
        text += f'TEXT: `{key}` искали {items}\n'

    list_text = [key for key in answ.keys()]
    return text, list_text




@dp.message_handler(commands=['get_log'])
async def send_welcome(msg: types.Message):

    text, _ = data_log()

    try:
        firs = 0
        last = 100
        msg_c = len(text.split('\n'))
        while True:
            if msg_c - last < 0:
                await bot.send_message(msg.from_user.id, '\n'.join(text.split('\n')[firs:]), parse_mode="Markdown")
                break

            await bot.send_message(msg.from_user.id, '\n'.join(text.split('\n')[firs:last]), parse_mode="Markdown")

            firs += 100
            last += 100

    except Exception as e:
        logging.exception(e)


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
    songs_list, artist_list = search(str(msg.text).strip())
    r = r'\(.*\)|#|\d{5,}|\{.*\}|•|\[.*\]'


    text = ''
    #получение песен из списка артистов и запись их
    for art in artist_list:
        song_artist = data[art]
        text += f'\n🎤 `{art}`:\n'
        text += ''.join([f'- `{re.sub(r, "", song.capitalize())}`\n' for song in sorted(song_artist)])


    #получение списка артистов из песен и записить их
    if len(songs_list) > 0:
        other_dict, songs_list = get_sing_from_other(songs_list)

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


    try:
        firs = 0
        last = 100
        msg_c = len(text.split('\n'))
        while True:
            if msg_c - last < 0:
                await bot.send_message(msg.from_user.id, '\n'.join(text.split('\n')[firs:]), parse_mode="Markdown")
                break

            await bot.send_message(msg.from_user.id, '\n'.join(text.split('\n')[firs:last]), parse_mode="Markdown")

            firs += 100
            last += 100

    except Exception as e:
        #print(e)
        logging.exception(e)





if __name__ == '__main__':
    executor.start_polling(dp)
