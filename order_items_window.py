"""Окно состава заказа."""
import tkinter as tk
from tkinter import ttk, messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
import order_manager as om
from datetime import datetime


class OrderItemsWindow:
    """Окно состава заказа."""

    def __init__(self, parent, order_id, current_user=None):
        self.order_id = order_id
        self.current_user = current_user

        self.window = tk.Toplevel(parent)
        self.window.title(f"Состав заказа №{order_id}")
        self.window.geometry("900x600")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()
        self.load_order_info()
        self.load_items()

    def is_admin(self):
        """Проверяет роль Администратора."""
        return (self.current_user and
                self.current_user[???] == "???")

    def build_ui(self):
        """Строит интерфейс."""
        # Шапка — ГОТОВО

        info_frame = tk.Frame(self.window, bg=???)
        info_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(info_frame, text="???", font=font(bold=True),
                 bg=COLOR_MAIN_BG).pack(side="left")
        self.date_var = tk.StringVar()
        self.date_entry = tk.Entry(info_frame, textvariable=???,
                                    width=15, state="???")
        self.date_entry.pack(side="left", padx=5)
        if self.??? ():
            self.date_entry.config(state="???")
            tk.Button(info_frame, text="Сохранить дату",
                      command=self.??? , bg=COLOR_ACCENT, fg="white").pack(side="left")
        tk.Label(info_frame, text="???", ...).pack(side="left")
        self.client_label = tk.Label(info_frame, text="", ...)
        self.client_label.pack(side="left")

        columns = ("id", "name", "production", "model",
                   "quantity", "price", "total")
        self.tree = ttk.Treeview(self.window, columns=???,
                                  show="headings", height=12)
        self.tree.heading("id", text="???")
        self.tree.heading("name", text="???")
        self.tree.heading("production", text="???")
        self.tree.heading("model", text="???")
        self.tree.heading("quantity", text="???")
        self.tree.heading("price", text="???")
        self.tree.heading("total", text="???")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.total_label = tk.Label(self.window, text="",
                                     font=font(FONT_SIZE_NORMAL, bold=True),
                                     fg=COLOR_ACCENT, bg=COLOR_MAIN_BG)
        self.total_label.pack(pady=5)

        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)
        if self.??? ():
            tk.Button(btn_frame, text="Удалить позицию",
                      command=self.??? , bg="#ff8080", fg="white").pack(side="left")
        tk.Button(btn_frame, text="Обновить", ...).pack(side="left")
        tk.Button(btn_frame, text="Назад", command=self.window.??? ).pack(side="right")

    def load_order_info(self):
        """Загружает дату и клиента."""
        order = om.??? (self.order_id)
        if order:
            self.date_var.??? (order[???])
            self.client_label.config(text=order[???])

    def load_items(self):
        """Загружает позиции заказа."""
        for row in self.tree.??? ():
            self.tree.??? (row)
        try:
            items = om.??? (self.order_id)
            if not items:
                self.total_label.config(text="???")
                return
            total = ???
            for item in items:
                item_id, name, production, model, quantity, price = item
                item_total = ??? * ???
                total ??? item_total
                self.tree.insert("", tk.END,
                                 values=(item_id, name, production, model,
                                         quantity, f"{???:.2f}", f"{???:.2f}"))
            self.total_label.config(text=f"ИТОГО: {???:.2f} руб.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")

    def save_date(self):
        """Сохраняет изменённую дату."""
        new_date = self.date_var.??? ()
        try:
            datetime.??? (new_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Формат: ГГГГ-ММ-ДД")
            return
        if om.??? (self.order_id, new_date):
            messagebox.???("Успех", "Дата обновлена")

    def delete_item(self):
        """Удаляет выбранную позицию."""
        selected = self.tree.??? ()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите позицию")
            return
        item_id = self.tree.item(selected[0])["values"][???]
        if not messagebox.???("Подтверждение", f"Удалить позицию №{item_id}?"):
            return
        if om.??? (item_id):
            messagebox.???("Успех", "Позиция удалена")
            self.??? ()

    def refresh_all(self):
        """Обновляет всё."""
        self.load_order_info()
        self.load_items()