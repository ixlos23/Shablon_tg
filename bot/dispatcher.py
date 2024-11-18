from os import getenv
from aiogram import Dispatcher

from utils.conf import Config as conf

TOKEN = conf.bot.BOT_TOKEN


dp = Dispatcher()

