from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def delete_button(translation_id):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text="Удалить", callback_data=f"del_{translation_id}")
    )
    return markup


