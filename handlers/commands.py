from data.loader import bot
from keyboards.reply import start_kb
from telebot import types
from database.db import get_user_by_chat_id, insert_user


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name

    is_exists = get_user_by_chat_id(chat_id)
    if not is_exists:
        insert_user(first_name, chat_id)
        print('user is added to database')

    bot.send_message(chat_id, f"Hello,{first_name}. Click, to start", reply_markup=start_kb())