"""Каталог товаров."""
import tkinter as tk
from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)
from resources import get_product_image


def create_product_card(parent, product, refresh=None):
    """
    Создаёт карточку товара.
    """
    # TODO: количество (индекс 6)
    qty = product[???]
    # TODO: цвет фона
    bg_color = _get_card_color(???)
    # TODO: Frame с рамкой    card = tk.Frame(parent, bg=???, bd=1, relief="solid")
    card.pack(??? = "x", padx=10, pady=5)
    # TODO: изображение и текст
    _add_image(card, product, ???)
    _add_text_info(card, product, ???, ???)
    # TODO: привязать клик
    card.bind("???", lambda e: _open_view(parent, product, refresh))
    for child in card.??? ():
        child.bind("???", lambda e: _open_view(parent, product, refresh))
    return ???


def _get_card_color(qty):
    """Возвращает цвет фона карточки."""
    # TODO: тернарный оператор
    return ??? if qty ??? 3 else ???


def _add_image(card, product, bg_color):
    """Добавляет изображение товара (или заглушку)."""
    img_frame = tk.Frame(card, bg=???)
    img_frame.pack(side="???", padx=10, pady=10)
    # TODO: индекс 7
    photo = get_product_image(product[???], size=(100, 100))
    if photo:
        img_label = tk.Label(img_frame, image=???, bg=???)
        # TODO: сохранить ссылку
        img_label.??? = ???
        img_label.pack()
    else:
        tk.Label(img_frame, text="???", bg=bg_color,
                 width=10, height=5).pack()


def _add_text_info(card, product, bg_color, qty):
    """Добавляет текстовую информацию о товаре."""
    text_frame = tk.Frame(card, bg=???)
    text_frame.pack(side="left", fill="both", expand=???,
                    padx=10, pady=10)
    name = product[1] if product[1] else "???"
    production = product[???] if product[???] else "[Без производителя]"
    category = product[???] if product[???] else "[Без категории]"
    characteristics = product[???] if product[???] else "[Не указаны]"
    price = product[???] if product[???] is not None else 0
    _add_label(text_frame, f"{???} | {???}",
               bg_color, bold=True, size=FONT_SIZE_HEADER)
    _add_label(text_frame, f"Категория: {???}", bg_color)
    _add_label(text_frame, f"Количество: {_indicator(???)} ({???})", bg_color)
    _add_label(text_frame, f"Характеристики: {???}", bg_color)
    _add_label(text_frame, f"{???} руб.",
               bg_color, bold=True, size=FONT_SIZE_HEADER, align="e")


def _add_label(parent, text, bg_color, bold=False,
               size=FONT_SIZE_NORMAL, align="w"):
    """Добавляет метку с текстом."""
    tk.Label(parent, text=???, font=???(size, bold=bold),
             bg=???, anchor=???).pack(??? = "x")


def _indicator(qty):
    """Индикатор «много/мало» (порог 5)."""
    return ??? if qty ??? 5 else ???


def _open_view(parent, product, refresh=None):
    """Открывает форму просмотра товара."""
    from view_form import ???
    ViewForm(parent, product, on_add_to_order=???)