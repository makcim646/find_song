import configparser
import os


def create_config(path='setting.ini', bot_token=''):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("setting")
    config.set("setting", "bot_token", f'{bot_token}')

    with open(path, "w") as config_file:
        config.write(config_file)


def get_config(path='setting.ini'):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        bot_token = str(input('Input telegram bot token: '))
        create_config(path, bot_token)

    config = configparser.ConfigParser()
    config.read(path)
    out = {}
    for key in config['setting']:
        out[key] = config['setting'][key]

    return out


def update_config(kwarg, path='setting.ini'):
    config = configparser.ConfigParser()
    config.read(path)
    for key in kwarg.keys():
        config.set('setting', key, kwarg[key])

    with open(path, "w") as config_file:
        config.write(config_file)
        return True
