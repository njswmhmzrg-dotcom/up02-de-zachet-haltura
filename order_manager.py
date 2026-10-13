from datetime import datetime
from database import get_connection

def get_all_orders():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, дата, клиент FROM Заказ ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_order_items(order_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT Состав_заказа.id, Товар.название, Товар.производитель,
               Состав_заказа.модель, Состав_заказа.количество, Состав_заказа.цена
        FROM Состав_заказа
        JOIN Товар ON Состав_заказа.товар_id = Товар.id
        WHERE Состав_заказа.заказ_id = ?
        ORDER BY Состав_заказа.id
    """, (order_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_order_total(order_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT SUM(количество * цена) FROM Состав_заказа WHERE заказ_id = ?", (order_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] or 0.0

def create_order(client, items):
    conn = get_connection()
    cur = conn.cursor()
    try:
        date = datetime.now().strftime("%Y-%m-%d")
        cur.execute("INSERT INTO Заказ (дата, клиент) VALUES (?, ?)", (date, client))
        order_id = cur.lastrowid
        for product_id, model, quantity, price in items:
            cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
            row = cur.fetchone()
            if not row or row[0] < quantity:
                raise ValueError(f"Недостаточно товара id={product_id}")
            cur.execute("""
                INSERT INTO Состав_заказа (заказ_id, товар_id, модель, количество, цена)
                VALUES (?, ?, ?, ?, ?)
            """, (order_id, product_id, model, quantity, price))
            cur.execute("UPDATE Товар SET количество = количество - ? WHERE id = ?", (quantity, product_id))
        conn.commit()
        return order_id
    except Exception:
        conn.rollback()
        return None
    finally:
        conn.close()

def delete_order(order_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT товар_id, количество FROM Состав_заказа WHERE заказ_id = ?", (order_id,))
        items = cur.fetchall()
        for product_id, quantity in items:
            cur.execute("UPDATE Товар SET количество = количество + ? WHERE id = ?", (quantity, product_id))
        cur.execute("DELETE FROM Состав_заказа WHERE заказ_id = ?", (order_id,))
        cur.execute("DELETE FROM Заказ WHERE id = ?", (order_id,))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()

def update_order_date(order_id, new_date):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE Заказ SET дата = ? WHERE id = ?", (new_date, order_id))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()

def delete_order_item(item_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT товар_id, количество FROM Состав_заказа WHERE id = ?", (item_id,))
        row = cur.fetchone()
        if not row:
            return False
        product_id, quantity = row
        cur.execute("DELETE FROM Состав_заказа WHERE id = ?", (item_id,))
        cur.execute("UPDATE Товар SET количество = количество + ? WHERE id = ?", (quantity, product_id))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()