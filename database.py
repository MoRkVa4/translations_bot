import sqlite3

connect = sqlite3.connect("translator.db", check_same_thread=False)
cursor = connect.cursor()


# создание таблицы users
# cursor.executescript("""
#     DROP TABLE IF EXISTS users;
#     CREATE TABLE IF NOT EXISTS users(
#         user_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         full_name TEXT,
#         age INTEGER,
#         phone_number TEXT,
#         telegram_id BIGINT NOT NULL UNIQUE
#     );
# """)
# connect.commit()


def is_user_exists(chat_id: int):
    """Проверяем есть ли в БД пользователь с chat_id."""
    cursor.execute("""
        SELECT user_id FROM users WHERE telegram_id = ?;
    """, (chat_id,))
    user_id = cursor.fetchone()
    if not user_id:
        return
    return user_id[0]


def insert_user(full_name: str, age: int, phone_number: str, telegram_id: int):
    """Добавление пользователя в БД."""
    cursor.execute("""
        INSERT INTO users(full_name, age, phone_number, telegram_id)
        VALUES(?, ?, ?, ?);
    """, (full_name, age, phone_number, telegram_id))
    connect.commit()


# создаем таблицу для переводов
# cursor.executescript("""
#     DROP TABLE IF EXISTS translations;
#     CREATE TABLE IF NOT EXISTS translations(
#         translation_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         lang_from VARCHAR(3),
#         lang_to VARCHAR(3),
#         original TEXT,
#         translated TEXT,
#         user_id REFERENCES users(user_id)
#     );
# """)
# connect.commit()

def insert_translation(lang_from, lang_to, original, translated, chat_id):
    """Добавляем перевод в БД."""

    # получаем id пользователя из БД.
    user_id = is_user_exists(chat_id)

    cursor.execute("""
        INSERT INTO translations(lang_from, lang_to, original, translated, user_id)
        VALUES(?, ?, ?, ?, ?);
    """, (lang_from, lang_to, original, translated, user_id))
    connect.commit()


def get_users_translations(chat_id):
    """Получаем все переводы пользователя."""
    user_id = is_user_exists(chat_id)
    cursor.execute("""
        SELECT translation_id, lang_from, lang_to, original, translated
        FROM translations
        WHERE user_id = ?;
    """, (user_id,))
    translations = cursor.fetchall()  # [(1,2,3,4,5),(1,2,3,4,5),(1,2,3,4,5),(1,2,3,4,5)]
    return translations


def delete_translation(translation_id):
    cursor.execute("""DELETE FROM translations WHERE translation_id = ?;""", (translation_id,))
    connect.commit()
