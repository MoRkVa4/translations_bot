# Текстовая клавиатура для бота

from googletrans import LANGCODES
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from database import is_user_exists


# English -> en
# Russian -> ru
# "russian": "ru"


def show_start_menu(chat_id=None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    if not is_user_exists(chat_id):
        markup.row(
            KeyboardButton(text="Регистрация")
        )
    else:
        markup.row(
            KeyboardButton(text="Перевод"),
            KeyboardButton(text="История переводов"),
        )
    return markup


def show_languages_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(
        KeyboardButton(text="Назад")
    )

    buttons = [KeyboardButton(text=lang) for lang in LANGCODES.keys()]
    markup.add(*buttons)
    return markup


def send_contact():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton(text="Отправить контакт", request_contact=True)
    )
    return markup
