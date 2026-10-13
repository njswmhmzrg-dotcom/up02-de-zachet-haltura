import tkinter as tk
from tkinter import messagebox
from styles import COLOR_MAIN_BG, COLOR_ACCENT, FONT_SIZE_NORMAL, font
from database import get_product_quantity
from order_manager import create_order
from error_handler import validate_positive_int

class ViewForm:
    def __init__(self, parent, product, on_add_to_order=None):
        self.product = product
        self.on_add_to_order = on_add_to_order
        self.window = tk.Toplevel(parent)
        self.window.title("Просмотр товара")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.window.geometry("500x450")
        self._build_ui()

    def _build_ui(self):
        main_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self._add_field(main_frame, "Название", self.product[1])
        self._add_field(main_frame, "Категория", self.product[2])
        self._add_field(main_frame, "Производитель", self.product[3])
        self._add_field(main_frame, "Характеристики", self.product[4])
        self._add_field(main_frame, "Модель", self.product[8])
        self._add_field(main_frame, "Цена", f"{self.product[5]} руб.")
        self._add_field(main_frame, "Количество", self.product[6])

        qty_frame = tk.Frame(main_frame, bg=COLOR_MAIN_BG)
        qty_frame.pack(fill="x", pady=10)
        tk.Label(qty_frame, text="Количество для заказа:", bg=COLOR_MAIN_BG, font=font()).pack(side="left")
        self.qty_var = tk.StringVar(value="1")
        tk.Entry(qty_frame, textvariable=self.qty_var, width=10).pack(side="left", padx=5)

        tk.Button(main_frame, text="Добавить в заказ", command=self.add_to_order,
                  bg=COLOR_ACCENT, fg="white", font=font(bold=True)).pack(pady=10)
        tk.Button(main_frame, text="Закрыть", command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white").pack()

    def _add_field(self, parent, label, value):
        row = tk.Frame(parent, bg=COLOR_MAIN_BG)
        row.pack(fill="x", pady=2)
        tk.Label(row, text=f"{label}:", font=font(bold=True), width=15, anchor="w",
                 bg=COLOR_MAIN_BG).pack(side="left")
        tk.Label(row, text=str(value), font=font(), anchor="w",
                 bg=COLOR_MAIN_BG).pack(side="left")

    def add_to_order(self):
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return
        ok, result = validate_positive_int(self.qty_var.get(), "Количество")
        if not ok:
            messagebox.showwarning("Ошибка ввода", result)
            return
        qty = int(result)
        current_qty = get_product_quantity(self.product[0])
        if qty > current_qty:
            messagebox.showwarning("Ошибка", f"Доступно только {current_qty} шт.")
            return
        try:
            items = [(self.product[0], self.product[8], qty, self.product[5])]
            order_id = create_order("Клиент", items)
            if order_id:
                messagebox.showinfo("Успех", f"Заказ №{order_id} оформлен")
                if self.on_add_to_order:
                    self.on_add_to_order()
                self.window.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка заказа:\n{e}")