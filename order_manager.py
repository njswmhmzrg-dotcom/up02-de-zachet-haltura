"""Работа с заказами."""
import sqlite3
from datetime import datetime
from config import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_all_orders():
    """
    Возвращает список всех заказов.
    :return: список кортежей (id, дата, клиент)
    """
    conn = get_connection()
    cur = conn.??? ()
    cur.execute("SELECT id, дата, клиент FROM Заказ ORDER BY id ???")
    rows = cur.??? ()
    conn.??? ()
    return ???

def get_order_by_id(order_id):
    """
    Возвращает заказ по id.
    :param order_id: id заказа
    :return: кортеж (id, дата, клиент) или None
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, дата, клиент FROM Заказ WHERE id = ?", (order_id,))
    row = cur.fetchone()
    conn.close()
    return row



def get_order_items(order_id):
    """
    Возвращает состав заказа через JOIN.
    :param order_id: id заказа
    :return: список (id, название, производитель, модель, количество, цена)
    """
    conn = get_connection()
    cur = conn.??? ()
    cur.execute("""
        SELECT Состав_заказа.id, Товар.название, Товар.производитель,
               Состав_заказа.модель, Состав_заказа.количество,
               Состав_заказа.цена
        FROM Состав_заказа
        JOIN Товар ON Состав_заказа.??? = Товар.???
        WHERE Состав_заказа.??? = ?
        ORDER BY Состав_заказа.id
    """, (???,))
    rows = cur.fetchall()
    conn.close()
    return ???


def get_order_total(order_id):
    """
    Возвращает итоговую сумму заказа.
    :param order_id: id заказа
    :return: сумма (float)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT SUM(??? * ???) FROM Состав_заказа WHERE заказ_id = ?",
                (???,))
    row = cur.??? ()
    conn.close()
    return row[0] ??? 0.0


def create_order(client, items):
    """
    Создаёт заказ с несколькими позициями.
    :param client: ФИО клиента
    :param items: список (product_id, model, quantity, price)
    :return: id заказа или None
    """
    conn = get_connection()
    cur = conn.??? ()
    ???:
        date = datetime.now().strftime("%Y-%m-%d")
        cur.execute("INSERT INTO Заказ (???, ???) VALUES (?, ?)",
                    (???, client))
        order_id = cur.??? 
        ??? product_id, model, quantity, price in items:
            cur.execute("SELECT количество FROM Товар WHERE id = ?",
                        (product_id,))
            row = cur.??? ()
            if not row or row[0] ??? quantity:
                raise ValueError(f"Недостаточно товара id={product_id}")
            cur.execute("""
                INSERT INTO Состав_заказа
                (заказ_id, товар_id, модель, количество, цена)
                VALUES (?, ?, ?, ?, ?)
            """, (???, product_id, ???, quantity, ???))
            cur.execute("""
                UPDATE Товар SET количество = количество - ?
                WHERE id = ?
            """, (???, ???))
        conn.??? ()
        return ???
    except Exception as e:
        conn.??? ()
        return ???
    finally:
        conn.??? ()


def delete_order(order_id):
    """
    Удаляет заказ и восстанавливает остатки.
    :param order_id: id заказа
    :return: True или False
    """
    conn = get_connection()
    cur = conn.??? ()
    try:
        cur.execute("SELECT товар_id, количество FROM Состав_заказа WHERE заказ_id = ?",
                    (???,))
        items = cur.??? ()
        for product_id, quantity in items:
            cur.execute("""
                UPDATE Товар SET количество = количество + ?
                WHERE id = ?
            """, (???, ???))
        cur.execute("DELETE FROM Состав_заказа WHERE заказ_id = ?", (???,))
        cur.execute("DELETE FROM Заказ WHERE id = ?", (???,))
        conn.??? ()
        return ???
    except Exception as e:
        conn.??? ()
        return ???
    finally:
        conn.??? ()


def update_order_date(order_id, new_date):
    """
    Обновляет дату заказа.
    :param order_id: id заказа
    :param new_date: новая дата (YYYY-MM-DD)
    :return: True
    """
    conn = get_connection()
    cur = conn.??? ()
    cur.execute("UPDATE Заказ SET ??? = ? WHERE ??? = ?",
                (???, order_id))
    conn.??? ()
    conn.??? ()
    return ???


def delete_order_item(item_id):
    """
    Удаляет позицию и восстанавливает остаток.
    :param item_id: id позиции в Состав_заказа
    :return: True или False
    """
    conn = get_connection()
    cur = conn.??? ()
    try:
        cur.execute("SELECT ???, ??? FROM Состав_заказа WHERE id = ?",
                    (???,))
        product_id, quantity = cur.??? ()
        cur.execute("DELETE FROM Состав_заказа WHERE ??? = ?", (???,))
        cur.execute("""
            UPDATE Товар SET количество = количество + ?
            WHERE id = ?
        """, (???, ???))
        conn.??? ()
        return ???
    except Exception as e:
        conn.??? ()
        return ???
    finally:
        conn.??? ()