from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token='', parse_mode='html')
blurValue = 10 # recommended value from 10 to 15

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)