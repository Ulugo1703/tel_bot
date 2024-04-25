from telebot import types
from googletrans import LANGCODES


def start_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(
        types.KeyboardButton(text="Start"),
        types.KeyboardButton(text="History")
    )
    return kb


def lang_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = []
    for lang in LANGCODES:
        buttons.append(
            types.KeyboardButton(text=lang)
        )
    kb.add(*buttons)
    return kb