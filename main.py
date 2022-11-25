import os
import logging
import subprocess
from db import load_lxsx
import glob



logging.basicConfig(level=logging.INFO, filename="main_log.log",filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")

def bot_start():
    if os.name == 'nt':
        proc = subprocess.Popen('python.exe bot.py', shell=True, stdout=subprocess.PIPE)
    else:
        proc = subprocess.Popen('python3 bot.py', shell=True)


if __name__ == "__main__":
    for file in glob.glob('*.xlsx'): # создает базу из всех найденых . таблиц в дериктории
        print(f'file {file} load')
        load_lxsx(file)
        print('add')

    bot_start()