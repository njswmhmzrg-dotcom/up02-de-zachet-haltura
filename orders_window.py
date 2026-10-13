"""Окно списка заказов."""
import tkinter as tk
from tkinter import ttk, messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
import order_manager as om


class OrdersWindow:
    """Окно списка заказов."""

    def __init__(self, parent, current_user=None):
        self.current_user = current_user

        self.window = tk.Toplevel(parent)
        self.window.title("Список заказов")
        self.window.geometry("800x500")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()
        self.load_orders()

    def is_admin(self):
        """Проверяет роль Администратора."""
        return (self.current_user and
                self.current_user[???] == "???")

    def build_ui(self):
        """Строит интерфейс."""
        # Шапка — ГОТОВО

        columns = ("id", "date", "client")
        self.tree = ttk.Treeview(self.window, columns=???,
                                  show="headings", height=15)
        self.tree.heading("id", text="???")
        self.tree.heading("date", text="???")
        self.tree.heading("client", text="???")
        self.tree.column("id", width=???)
        self.tree.column("date", width=???)
        self.tree.column("client", width=???)
        self.tree.pack(fill="???", expand=True, padx=20, pady=20)
        self.tree.bind("???", self.on_order_select)

        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)
        tk.Button(btn_frame, text="Просмотр состава",
                  command=self.??? , bg=COLOR_ACCENT, fg="white").pack(side="left")
        tk.Button(btn_frame, text="Обновить",
                  command=self.??? , bg=COLOR_ACCENT, fg="white").pack(side="left")
        tk.Button(btn_frame, text="Назад",
                  command=self.window.??? , bg=COLOR_ACCENT, fg="white").pack(side="right")

    def load_orders(self):
        """Загружает заказы из БД."""
        for row in self.tree.??? ():
            self.tree.??? (row)
        orders = om.??? ()
        for order in orders:
            self.tree.??? ("", tk.END, values=???)

    def on_order_select(self, event=None):
        """Обработчик выбора заказа."""
        selected = self.tree.??? ()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите заказ")
            return
        item = self.tree.??? (selected[0])
        order_id = item["values"][???]
        from order_items_window import ???
        ??? (self.window, order_id, self.current_user)