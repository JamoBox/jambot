#!/usr/bin/env python

from sys import exit
from config.irc_config import IrcConfig
from lib.bot import Bot


def start_application():
    try:
        config = IrcConfig()
        bot = Bot(config)
        bot.run()
    except KeyboardInterrupt:
        exit()



if __name__ == '__main__':
    start_application()
