import sqlite3
import hashlib
from flask import url_for


# Функция для хэширования пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def db_connection(username, email, password):
    conn = sqlite3.connect('app/static/db/users.db')
    c = conn.cursor()
    # Хэширование пароля
    hashed_password = hash_password(password)

    # Проверка наличия имени пользователя в БД
    c.execute('SELECT * FROM users WHERE email=? OR username=?', (email, username))
    data = c.fetchone()
    return hashed_password, data, c, conn


def db_reg(username, email, password):
    if len(username) > 15:
        return 'TOO_MANY_SYMBOLS'
    # Соединение с БД
    hashed_password, data, c, conn = db_connection(username, email, password)

    # Если имя пользователя ещё не существует в БД, то проверяем пароль на соответствие
    if data:
        conn.close()
        return 'EMAIL_EXISTS'
    else:
        # Добавление новой записи в БД
        c.execute('INSERT INTO users VALUES (?, ?, ?)', (username, email, hashed_password))
        conn.commit()
        conn.close()
        return False


def db_log(email, password):
    # Соединение с БД
    hashed_password, data, _, conn = db_connection(email, password)
    conn.close()
    # Если имя пользователя существует в БД, то проверяем пароль на соответствие
    if data and hashed_password == data[2]:
        return False
    return True
