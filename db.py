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

    data = set()
    for a,b,c,d,e in ws.rows:
        data.add((str(b.value), str(c.value)))

    wb.close()
    #print(data)
    data1 = sorted(data, key=lambda x: x[1])
    first = data1[0][1]
    artist_dict = {}
    songs = []
    for song, artist in data1:
        if first == artist:

            songs.append(song)
        else:
            artist_dict[first] = songs
            first = artist
            songs = [song]

    save = {**data_r, **artist_dict}

    with open('songs.json', 'w', encoding='utf8') as file:
        json.dump(save, file, ensure_ascii=False)





def search(text:str):
    with open('songs.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    songs = set()
    for artist, song in data.items():
        for s in song:
            songs.add(s)

    text = text.upper()
    r = re.compile(f".*{text}.*")
    song_list = list(filter(r.match, songs))
    artist_list = list(filter(r.match, data))
    print(song_list)
    print(artist_list)


def get_sing_from_other(songs:list):
    with open('songs.json', 'r', encoding='utf8') as file:
        data = json.load(file)



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

    print(other_dict, songs)




if __name__ == "__main__":
    #search('ДОЛИНА ЛАРИСА, ПАНАЙОТОВ АЛЕКСАНДР')
    #get_sing_from_other(['ДАЙ РУКУ МНЕ'])
    pass
    # полное название файла с таблицей table.xlsx
