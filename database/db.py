import sqlite3


def connect(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    return connection, cursor


def create_user_table():
    connection, cursor = connect("../translation.db")

    sql = """
    CREATE TABLE IF NOT EXISTS users(
        user_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        chat_id BIGINT NOT NULL UNIQUE
    );"""
    cursor.execute(sql)
    connection.commit()
    connection.close()


def create_translation_table():
    connection, cursor = connect('../translation.db')
    sql = """
    DROP TABLE IF EXISTS translations;
    CREATE TABLE IF NOT EXISTS translations(
        id  INTEGER PRIMARY KEY AUTOINCREMENT,
        lang_from TEXT,
        lang_to TEXT,
        original TEXT,
        translated TEXT,
        user_id INTEGER REFERENCES users(user_id)
    )
    """
    cursor.executescript(sql)
    connection.commit()
    connection.close()


create_user_table()
create_translation_table()
def insert_user(first_name, chat_id):
    connection, cursor = connect('translation.db')

    sql = 'INSERT INTO users(first_name, chat_id) VALUES(?, ?);'
    cursor.execute(sql, (first_name, chat_id))
    connection.commit()
    connection.close()


def get_user_by_chat_id(chat_id):
    connection, cursor = connect('translation.db')
    sql = "SELECT user_id FROM users WHERE chat_id = ?"
    cursor.execute(sql, (chat_id,))
    user = cursor.fetchone()
    return user[0] if user else False


def get_user_translations(chat_id):
    connection, cursor = connect('translation.db')
    user_id = get_user_by_chat_id(chat_id)
    print(user_id)
    sql = 'SELECT lang_from, lang_to, original, translated FROM translations WHERE user_id = ?'
    cursor.execute(sql, (user_id,))
    translations = cursor.fetchall()
    return translations


def add_user_translation(lang_from, lang_to, original, translated, chat_id):
    connection, cursor = connect('translation.db')
    user_id = get_user_by_chat_id(chat_id)
    sql = 'INSERT INTO translations(lang_from, lang_to, original, translated, user_id) VALUES(?,?,?,?,?)'
    cursor.execute(sql, (lang_from, lang_to, original, translated, user_id))
    connection.commit()
    connection.close()


