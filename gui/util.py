import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from parser import PATH, cfg
from enums import *


def create_popup(x, y, title, on_closing, parent=None):
    popup = ctk.CTkToplevel(master=parent)
    popup.geometry(f'{x}x{y}+{int(cfg["app_pos_x"]) + (900 - x) // 2}+{int(cfg["app_pos_y"]) + (600 - y) // 2}')
    popup.resizable(False, False)
    popup.title(title)
    popup.lift()
    popup.focus_force()
    popup.protocol('WM_DELETE_WINDOW', on_closing)
    return popup


def load_image(path, image_size):
    return ImageTk.PhotoImage(Image.open(PATH + path).resize(image_size), Image.LANCZOS)


category_names = {Category.food_and_drink.value: 'Jedzenie i napoje', Category.shopping.value: 'Zakupy',
                  Category.accommodation.value: 'Dom i mieszkanie',
                  Category.transport.value: 'Transport i podróże',
                  Category.car.value: 'Samochód', Category.entertainment.value: 'Życie i rozrywka',
                  Category.electronic.value: 'Elektronika', Category.funding.value: 'Nakłady finansowe',
                  Category.investments.value: 'Inwestycje', Category.income.value: 'Przychód',
                  Category.other.value: 'Inne'}

category_values = {'Jedzenie i napoje': Category.food_and_drink.value, 'Zakupy': Category.shopping.value,
                   'Dom i mieszkanie': Category.accommodation.value, 'Transport i podróże': Category.transport.value,
                   'Samochód': Category.car.value, 'Życie i rozrywka': Category.entertainment.value,
                   'Elektronika': Category.electronic.value, 'Nakłady finansowe': Category.funding.value,
                   'Inwestycje': Category.investments.value, 'Przychód': Category.income.value,
                   'Inne': Category.other.value}

periodicity_names = {Period.none.value: "Jednorazowa", Period.daily.value: "Codzienna",
                     Period.monthly.value: "Comiesięczna", Period.yearly.value: "Coroczna"}

periodicity_values = {"Jednorazowa": Period.none.value, "Codzienna": Period.daily.value,
                      "Comiesięczna": Period.monthly.value, "Coroczna": Period.yearly.value}

color_names = {Color.white.value: 'white', Color.black.value: 'black', Color.red.value: 'red',
               Color.green.value: 'green', Color.blue.value: 'blue', Color.cyan.value: 'cyan',
               Color.yellow.value: 'yellow', Color.magenta.value: 'magenta', Color.default.value: 'default'}

color_names_pl = {Color.white.value: 'Biały', Color.black.value: 'Czarny', Color.red.value: 'Czerwony',
                  Color.green.value: 'Zielony', Color.blue.value: 'Niebieski', Color.cyan.value: 'Cyjan',
                  Color.yellow.value: 'Żółty', Color.magenta.value: 'Magenta', Color.default.value: 'Domyślny'}

color_values = {'Domyślny': Color.default.value, 'Biały': Color.white.value, 'Czarny': Color.black.value,
                'Czerwony': Color.red.value, 'Zielony': Color.green.value, 'Niebieski': Color.blue.value,
                'Cyjan': Color.cyan.value, 'Żółty': Color.yellow.value, 'Magenta': Color.magenta.value}

icons_path = {Icon.car.value: '\\img\\car.png', Icon.home.value: '\\img\\accomodation.png',
              Icon.holiday.value: '\\img\\holiday.png', Icon.education.value: '\\img\\education.png',
              Icon.health.value: '\\img\\health.png', Icon.fun.value: '\\img\\fun.png',
              Icon.kids.value: '\\img\\kids.png', Icon.gifts.value: '\\img\\gift.png',
              Icon.other.value: '\\img\\other.png'}

icons_names = {Icon.car.value: 'Samochód', Icon.home.value: 'Dom i mieszkanie',
               Icon.holiday.value: 'Wakacje', Icon.education.value: 'Edukacja',
               Icon.health.value: 'Zdrowie', Icon.fun.value: 'Rozrywka',
               Icon.kids.value: 'Dzieci', Icon.gifts.value: 'Prezenty',
               Icon.other.value: 'Inne'}

icons_values = {'Samochód': Icon.car.value, 'Dom i mieszkanie': Icon.home.value, 'Wakacje': Icon.holiday.value,
                'Edukacja': Icon.education.value, 'Zdrowie': Icon.health.value, 'Rozrywka': Icon.fun.value,
                'Dzieci': Icon.kids.value, 'Prezenty': Icon.gifts.value, 'Inne': Icon.other.value}


def removing_popup(removing_function, content_id, title, description, actions_after_removing):
    def on_closing():
        popup.destroy()

    def remove():
        removing_function(content_id)
        on_closing()
        for action in actions_after_removing:
            action()

    popup = create_popup(300, 100, title, on_closing)
    label = ctk.CTkLabel(master=popup, text=description, text_font=('Arial', 16))
    button1 = ctk.CTkButton(master=popup, text='Tak', command=remove, corner_radius=8)
    button2 = ctk.CTkButton(master=popup, text='Nie', command=on_closing, corner_radius=8)

    label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    button1.place(relx=0.25, rely=0.8, anchor=tk.CENTER)
    button2.place(relx=0.75, rely=0.8, anchor=tk.CENTER)


def watching_popup(title, texts):
    def on_closing():
        popup.destroy()

    popup = create_popup(300, 300, title, on_closing)
    for idx, text in enumerate(texts):
        label = ctk.CTkLabel(master=popup, width=0, height=0, text=text)
        label.place(relx=0, rely=round(0.1 * (idx + 1), 1), anchor=tk.W)

    button = ctk.CTkButton(master=popup, text='OK', command=on_closing)
    button.place(relx=0.5, rely=0.85, anchor=tk.CENTER)
