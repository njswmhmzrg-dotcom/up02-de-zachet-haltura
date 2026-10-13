from datetime import datetime, timedelta
from database import get_connection

def get_previous_month_range(date):
    """Возвращает (начало, конец) предыдущего месяца в формате YYYY-MM-DD."""
    first_day = date.replace(day=1)
    last_day_prev = first_day - timedelta(days=1)
    first_day_prev = last_day_prev.replace(day=1)
    return (first_day_prev.strftime("%Y-%m-%d"), last_day_prev.strftime("%Y-%m-%d"))

def has_orders_in_previous_month(product_id, date):
    """Есть ли заказы товара в предыдущем месяце?"""
    start, end = get_previous_month_range(date)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) 
        FROM Состав_заказа 
        JOIN Заказ ON Состав_заказа.заказ_id = Заказ.id 
        WHERE Состав_заказа.товар_id = ? AND Заказ.дата BETWEEN ? AND ?
    """, (product_id, start, end))
    count = cur.fetchone()[0]
    conn.close()
    return count > 0

def calculate_price_with_discount(product_id, price, date):
    """Рассчитывает цену со скидкой 25%."""
    if has_orders_in_previous_month(product_id, date):
        return price
    return price * 0.75