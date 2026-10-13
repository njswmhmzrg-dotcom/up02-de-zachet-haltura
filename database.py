"""Работа с БД."""
import sqlite3
from config import DB_PATH


import os
import sqlite3

import os
import sqlite3

def get_connection():
    base = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base, "databases", "db_variant_1.db")
    return sqlite3.connect(db_path)


def get_all_products():
    """Возвращает список всех товаров."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_product_quantity(product_id):
    """Возвращает количество товара по id."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0


def get_user_by_login(login):
    """Ищет пользователя по логину."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT Пользователь.id, Пользователь.фамилия,
               Пользователь.имя, Пользователь.отчество,
               Пользователь.логин, Роль.название
        FROM Пользователь
        JOIN Роль ON Пользователь.роль_id = Роль.id
        WHERE Пользователь.логин = ?
    """, (login,))
    row = cur.fetchone()
    conn.close()
    return row