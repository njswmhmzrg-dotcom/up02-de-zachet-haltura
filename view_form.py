"""Форма просмотра товара."""
import tkinter as tk
from tkinter import messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
from resources import get_product_image
from database import get_product_quantity
from order_manager import create_order
from error_handler import validate_positive_int


class ViewForm:
    """Форма просмотра товара."""

    def __init__(self, parent, product, on_add_to_order=None):
        self.product = product
        self.on_add_to_order = on_add_to_order

        self.window = tk.Toplevel(parent)
        self.window.title(f"Просмотр — {product[1]}")
        self.window.geometry("700x600")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()

    def build_ui(self):
        """Строит интерфейс формы."""
        # Шапка — ГОТОВО
        # ... (готовый код шапки и изображения)

        # TODO: 6 вызовов _add_field
        # TODO: поле ввода количества
        # TODO: кнопки

    def _add_field(self, parent, label, value):
        """Добавляет поле в форму."""
        row = tk.Frame(parent, bg=???)
        row.pack(fill="x", pady=2)
        tk.Label(row, text=f"{???}:", font=font(bold=???),
                 width=???, anchor="w").pack(side="left")
        tk.Label(row, text=str(???), font=font(),
                 anchor="w").pack(side=???)

    def add_to_order(self):
        """Обработчик кнопки «Добавить в заказ»."""
        if not ???:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return
        ok, result = validate_positive_int(self.qty_var.??? (), "Количество")
        if not ok:
            messagebox.???("Ошибка ввода", result)
            return
        qty = ???
        current_qty = get_product_quantity(self.product[???])
        if qty ??? current_qty:
            messagebox.showwarning("Ошибка", f"Доступно только {???} шт.")
            return
        try:
            items = [(self.product[???], self.product[???], qty, self.product[???])]
            order_id = create_order("Клиент", ???)
            if order_id:
                messagebox.???("Успех", f"Заказ №{order_id} оформлен")
                if self.on_add_to_order:
                    self.on_add_to_order()
                self.window.??? ()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка заказа:\n{e}")