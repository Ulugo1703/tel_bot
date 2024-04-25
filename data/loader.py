import config

from telebot import TeleBot
from googletrans import Translator

bot = TeleBot(token=config.BOT_TOKEN)
translator = Translator()