from data.loader import bot, translator
from telebot import types

from keyboards.reply import lang_kb
from googletrans import LANGCODES
from .commands import start
from database.db import get_user_translations, add_user_translation


@bot.message_handler(func=lambda msg: msg.text == 'Start')
def start_action(message: types.Message):
    chat_id = message.chat.id

    bot.send_message(chat_id, "Choose the language that will be translated", reply_markup=lang_kb())
    bot.register_next_step_handler(message, get_lang_from)


def get_lang_from(message: types.Message):
    chat_id = message.chat.id
    lang_from = message.text
    bot.send_message(chat_id, "Choose the translation language", reply_markup=lang_kb())
    bot.register_next_step_handler(message, get_lang_to, lang_from )


def get_lang_to(message: types.Message, lang_from):
    chat_id = message.chat.id
    lang_to = message.text

    bot.send_message(chat_id, "Please write the word or sentence(s).", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, translate, lang_from, lang_to)


def translate(message: types.Message, lang_from, lang_to):
    chat_id = message.chat.id
    code_from = LANGCODES.get(lang_from)
    code_to = LANGCODES.get(lang_to)
    translated_text = translator.translate(message.text, code_to, code_from).text
    bot.send_message(chat_id, f"""
<i>FROM:<b>{lang_from.title()}</b></i>
<i>TO:<b>{lang_to.title()}</b></i>
<i>ORIGINAL:
<b>{message.text}</b></i>
<i>TRANSLATED:
<b>{translated_text}</b></i>

""", parse_mode='html')
    add_user_translation(lang_from,lang_to,message.text, translated_text, chat_id)
    print("translations are added")
    start(message)


@bot.message_handler(func=lambda msg: msg.text == 'History')
def show_history(message: types.Message):
    chat_id = message.chat.id
    translations = get_user_translations(chat_id)
    for lang_from, lang_to, original, translated in translations:
        bot.send_message(chat_id, f"""
<i>FROM:<b>{lang_from.title()}</b></i>
<i>TO:<b>{lang_to.title()}</b></i>
<i>ORIGINAL:
<b>{original}</b></i>
<i>TRANSLATED:
<b>{translated}</b></i>

""", parse_mode='html')

