from openpyxl import load_workbook
import json
import re
import os
import glob



def load_lxsx(file_xlsx):
    if not os.path.exists('songs.json'):
        with open('songs.json', 'w', encoding='utf8') as file:
            json.dump({}, file, ensure_ascii=False)


    with open('songs.json', 'r', encoding='utf8') as file:
        data_r = json.load(file)

    wb = load_workbook(file_xlsx)
    ws = wb.active

    r = r'\(.*\)|#|\d{5,}|\{.*\}|•|\[.*\]'
    data = set()
    for a,b,c,d,e in ws.rows:
        data.add((re.sub(r, '', str(b.value)).strip(), str(c.value)))

    wb.close()
    #print(data)
    data1 = sorted(data, key=lambda x: x[1])
    first = data1[0][1]
    artist_dict = {}
    songs = set()
    for song, artist in data1:
        if first == artist:

            songs.add(song)
        else:
            artist_dict[first] = [s for s in songs]
            count_song
            first = artist
            songs = {song}

    save = {**data_r, **artist_dict}

    with open('songs.json', 'w', encoding='utf8') as file:
        json.dump(save, file, ensure_ascii=False)



def add_order(user:str, song:str):
    with open('order.txt', 'a+', encoding='utf8') as file:
        file.write(f'{user} заказал {song}\n')
        return True

    return False


def get_order_book():
    with open('order.txt', 'r', encoding='utf8') as file:
        lines = file.readlines()
        text = 'Список заказов:\n'
        text += ''.join(lines)

        return text



def clear_order_book():
    with open('order.txt', 'w', encoding='utf8') as file:
        return True


def set_name(name:str, usr_id:str):
    if not os.path.exists('user.json'):
        with open('user.json', 'w', encoding='utf8') as file:
            json.dump({}, file, ensure_ascii=False)

    with open('user.json', 'r', encoding='utf8') as file:
        data_user = json.load(file)


    data_user[usr_id] = name

    with open('user.json', 'w', encoding='utf8') as file:
            json.dump(data_user, file, ensure_ascii=False)

    return True




def get_name(usr_id:str):
    if not os.path.exists('user.json'):
        with open('user.json', 'w', encoding='utf8') as file:
            json.dump({}, file, ensure_ascii=False)

    with open('user.json', 'r', encoding='utf8') as file:
        data_user = json.load(file)

    if data_user.get(usr_id) == None:
        return None
    else:
        return data_user[usr_id]




def get_sing_from_other(songs:dict, data:dict):
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



def search(text:str, data:dict, data_songs:set):
    text = text.upper()
    r = re.compile(f".*{text}.*")
    song_list = list(filter(r.match, data_songs))
    artist_list = list(filter(r.match, data))

    if len(artist_list) == 0:
        for key in data.keys():
            if key == text:
                artist_list.append(key)

    return song_list, artist_list


def not_in_db(data:dict, data_songs:set):
    _, list_text = data_log()
    answ_text = 'Люди это искали и не нашли:\n'
    for text in list_text:
        art, song = search(text, data, data_songs)
        if len(art) == 0 and len(song) == 0:
           answ_text += f'`{text}`\n'

    return answ_text


def song_count():
    with open('songs.json', 'r', encoding='utf8') as file:
        data_r = json.load(file)

    data_songs = set()
    for artist, song in data_r.items():
        for s in song:
            data_songs.add(s)

    print(len(data_songs))





if __name__ == "__main__":
    #get_sing_from_other(['ДАЙ РУКУ МНЕ'])
    song_count()
    pass
    # полное название файла с таблицей table.xlsx
