from googletrans import Translator, LANGCODES, LANGUAGES
from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove, CallbackQuery

from database import insert_user, insert_translation, get_users_translations, delete_translation
from keyboards.default import show_start_menu, show_languages_menu, send_contact
from keyboards.inline import delete_button

# ТОКЕН БОТА ПОЛУЧЕННЫЙ В BOTFATHER
BOT_TOKEN = "5611417538:AAF8YfLR74owOoT9TF3xdYfx6Z7TWjwA0KM"

# инициализация бота
bot = TeleBot(token=BOT_TOKEN)

translator = Translator()


# @bot.message_handler() слушатель сообщения
@bot.message_handler(commands=["start"])
def command_start(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    bot.send_photo(chat_id,
                   photo="https://images.wallpaperscraft.com/image/single/city_aerial_view_road_156925_4000x6000.jpg")
    bot.send_message(chat_id, f"Привет, {full_name}", reply_markup=show_start_menu(chat_id))


@bot.message_handler(func=lambda msg: msg.text == "Регистрация")
def handle_registration(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Напишите ваше Ф.И.О", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_full_name)


def get_full_name(message: Message):
    """Получаем от пользователя его полное имя."""
    chat_id = message.chat.id
    full_name = message.text.title()
    bot.send_message(chat_id, "Напишите возраст")
    bot.register_next_step_handler(message, get_age, full_name)


def get_age(message: Message, full_name: str):
    chat_id = message.chat.id
    age = int(message.text)
    bot.send_message(chat_id, "Отправьте контакт", reply_markup=send_contact())
    bot.register_next_step_handler(message, get_phone_number, full_name, age)


def get_phone_number(message: Message, full_name: str, age: int):
    """Получаем номер пользователя и регистрируем его в БД."""
    chat_id = message.chat.id
    phone_number = message.contact.phone_number
    # TODO: вызвать функцию для добавления пользователя в БД
    insert_user(full_name, age, phone_number, chat_id)

    bot.send_message(chat_id, "Регистрация завершена", reply_markup=show_start_menu(chat_id))


@bot.message_handler(func=lambda msg: msg.text == "Перевод")
def handle_translation(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Выберите язык, с которого будем переводить", reply_markup=show_languages_menu())
    bot.register_next_step_handler(message, get_lang_from)


def get_lang_from(message: Message):
    """Получаем название языка с которого будем делать перевод."""
    chat_id = message.chat.id
    bot.send_message(chat_id, "Выберите язык, на который будем переводить", reply_markup=show_languages_menu())
    bot.register_next_step_handler(message, get_lang_to, message.text)


def get_lang_to(message: Message, lang_from: str):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Напишите слово или текст для перевода", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, translate_message, lang_from, message.text)


def translate_message(message: Message, lang_from: str, lang_to: str):
    chat_id = message.chat.id

    code_from = LANGCODES[lang_from]
    code_to = LANGCODES[lang_to]
    translated_text = translator.translate(text=message.text, dest=code_to, src=code_from).text
    # добавляем перевод в БД.
    insert_translation(code_from, code_to, message.text, translated_text, chat_id)

    bot.send_message(chat_id, f"""
Переведено с: {lang_from}
Переведено на: {lang_to}
Оригинал: {message.text}
Перевод: {translated_text}
""", reply_markup=show_start_menu(chat_id))


@bot.message_handler(func=lambda msg: msg.text == "История переводов")
def handle_translation_history(message: Message):
    chat_id = message.chat.id
    translations = get_users_translations(chat_id)
    if not translations:
        bot.send_message(chat_id, "А это уже совсем другая история")
        return
    for translation_id, lang_from, lang_to, original, translated in translations:
        bot.send_message(chat_id, f"""
Переведено с: {LANGUAGES[lang_from]}
Переведено на: {LANGUAGES[lang_to]}
Оригинал: {original}
Перевод: {translated}
""", reply_markup=delete_button(translation_id))

    # bot.send_message(chat_id, "ДИМООООООН ТУРУРУРУ")


@bot.callback_query_handler(func=lambda call: "del" in call.data)
def handle_deletion_button(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, translation_id = callback.data.split("_")
    delete_translation(translation_id)
    bot.answer_callback_query(callback.id, f"Удалили перевод с id: {translation_id}")
    bot.delete_message(chat_id, callback.message.message_id)


# запуск бота
bot.infinity_polling()
# pip install telebot
