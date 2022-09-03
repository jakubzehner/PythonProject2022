import random
import tkinter as tk
import customtkinter as ctk
from enums import *
import app.helper as helper
import datetime
from util import create_popup, load_image, category_names, category_values, periodicity_names, color_names, icons_path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from constants import *


class Home:
    def __init__(self, parent, controller, app):
        self.controller = controller
        self.app = app

        parent.grid_rowconfigure(1, weight=2)
        parent.grid_columnconfigure(1, weight=2)

        self.frame_lu = ctk.CTkFrame(master=parent, height=(HEIGHT - MENU_HEIGHT - 15) // 2, corner_radius=0,
                                     width=(WIDTH - 10) // 2, padx=5, pady=5, fg_color=COLOR_APP_FOREGROUND)
        self.frame_lu.grid(row=0, column=0, sticky='nsew')

        self.frame_ld = ctk.CTkFrame(master=parent, height=(HEIGHT - MENU_HEIGHT - 15) // 2, corner_radius=0,
                                     width=(WIDTH - 10) // 2, padx=5, pady=5, fg_color=COLOR_APP_FOREGROUND)
        self.frame_ld.grid(row=1, column=0, sticky='nsew')

        self.frame_ru = ctk.CTkFrame(master=parent, height=(HEIGHT - MENU_HEIGHT - 15) // 2, corner_radius=0,
                                     width=(WIDTH - 10) // 2, padx=5, pady=5, fg_color=COLOR_APP_FOREGROUND)
        self.frame_ru.grid(row=0, column=1, sticky='nsew')

        self.frame_rd = ctk.CTkFrame(master=parent, height=(HEIGHT - MENU_HEIGHT - 15) // 2, corner_radius=0,
                                     width=(WIDTH - 10) // 2, padx=5, pady=5, fg_color=COLOR_APP_FOREGROUND)
        self.frame_rd.grid(row=1, column=1, sticky='nsew')

        self.flu: ctk.CTkFrame | None = None
        self.fld: ctk.CTkFrame | None = None
        self.fru: ctk.CTkFrame | None = None
        self.frd: ctk.CTkFrame | None = None

        self.create_frame_lu()
        self.create_frame_ld()
        self.create_frame_ru()
        self.create_frame_rd()

    def create_frame_lu(self):
        for child in self.frame_lu.winfo_children():
            child.destroy()

        self.flu = LUFrame(self.frame_lu, self, self.app)

    def create_frame_ld(self):
        for child in self.frame_ld.winfo_children():
            child.destroy()

        self.fld = LDFrame(self.frame_ld, self, self.app)

    def create_frame_ru(self):
        for child in self.frame_ru.winfo_children():
            child.destroy()

        self.fru = RUFrame(self.frame_ru, self, self.app)

    def create_frame_rd(self):
        for child in self.frame_rd.winfo_children():
            child.destroy()

        self.frd = RDFrame(self.frame_rd, self, self.app)


class LUFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, app):
        ctk.CTkFrame.__init__(self, parent)
        self.app = app
        self.controller = controller

        balance = self.app.get_current_user()['balance']

        self.label = ctk.CTkLabel(master=parent, text=f'Stan konta: {balance}', text_font=TITLE_FONT)
        self.label.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

        self.button1 = ctk.CTkButton(master=parent, text='Skoryguj stan konta', corner_radius=8, text_font=FONT,
                                     command=self.change)
        self.button2 = ctk.CTkButton(master=parent, text='Zmień stan konta', corner_radius=8, text_font=FONT,
                                     command=self.set)
        self.button3 = ctk.CTkButton(master=parent, text='Dodaj wpis', corner_radius=8, text_font=FONT,
                                     command=self.add_entry)

        self.button1.place(relx=0.5, rely=0.82, anchor=tk.CENTER)
        self.button2.place(relx=0.5, rely=0.62, anchor=tk.CENTER)
        self.button3.place(relx=0.5, rely=0.42, anchor=tk.CENTER)

    def manage_account_balance(self, window_title, description, placeholder, insert, function):
        def on_closing():
            popup.destroy()

        def manage_balance():
            try:
                float(entry.get())
            except ValueError:
                error_label = ctk.CTkLabel(master=popup, width=0, height=0, text_color=('red', 'red'),
                                           text='Stan konta musi być liczbą')
                error_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
                return

            function(float(entry.get()))
            on_closing()
            self.controller.create_frame_lu()
            self.controller.create_frame_ru()

        balance = self.app.get_current_user()['balance']
        popup = create_popup(350, 150, window_title, on_closing)
        label = ctk.CTkLabel(master=popup, text=description, text_font=FONT)
        entry = ctk.CTkEntry(master=popup, corner_radius=8, width=200, placeholder_text=placeholder)
        if insert:
            entry.insert(tk.END, balance)
        button1 = ctk.CTkButton(master=popup, corner_radius=8, text='OK', command=manage_balance)
        button2 = ctk.CTkButton(master=popup, corner_radius=8, text='Anuluj', command=on_closing)

        label.place(relx=0.5, rely=0.12, anchor=tk.CENTER)
        entry.place(relx=0.5, rely=0.42, anchor=tk.CENTER)
        button1.place(relx=0.25, rely=0.8, anchor=tk.CENTER)
        button2.place(relx=0.75, rely=0.8, anchor=tk.CENTER)

    def change(self):
        self.manage_account_balance('Zmiana stanu konta', 'Podaj korektę stanu konta', 'korekta stanu konta', False,
                                    self.app.change_balance)

    def set(self):
        self.manage_account_balance('Zmiana stanu konta', 'Podaj nowy stan konta', 'stan konta', True,
                                    self.app.set_balance)

    def add_entry(self):
        def on_closing():
            popup.destroy()

        def add():
            error_label = ctk.CTkLabel(master=popup, width=0, height=0, text_color=('red', 'red'))
            form = '%Y-%m-%d'
            try:
                datetime.datetime.strptime(entry4.get(), form)
            except ValueError:
                error_label.configure(text='Nieprawidłowa data', width=0)
                error_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
                return

            try:
                float(entry5.get())
            except ValueError:
                error_label.configure(text='Kwota musi być liczbą', width=0)
                error_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
                return

            if not float(entry5.get()) > 0:
                error_label.configure(text='Kwota musi być większa od zera', width=0)
                error_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
                return

            outcome = entry3.get() == 'Tak'
            name = entry2.get()
            if name == "":
                name = None

            description = entry6.get()
            if description == "":
                description = None

            self.app.add_entry(category_values[entry1.get()], name, outcome, entry4.get(), float(entry5.get()),
                               description)
            on_closing()
            self.controller.create_frame_lu()
            self.controller.create_frame_ru()
            self.controller.create_frame_ld()

        popup = create_popup(400, 400, 'Dodawanie nowego wpisu', on_closing)

        label1 = ctk.CTkLabel(master=popup, width=0, height=0, text='Kategoria wpisu')
        label2 = ctk.CTkLabel(master=popup, width=0, height=0, text='Nazwa wpisu')
        label3 = ctk.CTkLabel(master=popup, width=0, height=0, text='Czy to wydatek')
        label4 = ctk.CTkLabel(master=popup, width=0, height=0, text='Data wpisu')
        label5 = ctk.CTkLabel(master=popup, width=0, height=0, text='Kwota wpisu')
        label6 = ctk.CTkLabel(master=popup, width=0, height=0, text='Opis wpisu')

        entry1 = ctk.CTkComboBox(master=popup, values=[*category_values.keys()], width=250)
        entry2 = ctk.CTkEntry(master=popup, width=250, placeholder_text='nazwa')
        entry3 = ctk.CTkComboBox(master=popup, values=['Tak', 'Nie'], width=250)
        entry4 = ctk.CTkEntry(master=popup, width=250, placeholder_text='data')
        entry5 = ctk.CTkEntry(master=popup, width=250, placeholder_text='kwota')
        entry6 = ctk.CTkEntry(master=popup, width=250, placeholder_text='opis')

        button1 = ctk.CTkButton(master=popup, text='Dodaj', command=add)
        button2 = ctk.CTkButton(master=popup, text='Anuluj', command=on_closing)

        entry4.insert(tk.END, datetime.date.today().strftime('%Y-%m-%d'))

        label1.place(relx=0, rely=0.1, anchor=tk.W)
        label2.place(relx=0, rely=0.2, anchor=tk.W)
        label3.place(relx=0, rely=0.3, anchor=tk.W)
        label4.place(relx=0, rely=0.4, anchor=tk.W)
        label5.place(relx=0, rely=0.5, anchor=tk.W)
        label6.place(relx=0, rely=0.6, anchor=tk.W)

        entry1.place(relx=0.3, rely=0.1, anchor=tk.W)
        entry2.place(relx=0.3, rely=0.2, anchor=tk.W)
        entry3.place(relx=0.3, rely=0.3, anchor=tk.W)
        entry4.place(relx=0.3, rely=0.4, anchor=tk.W)
        entry5.place(relx=0.3, rely=0.5, anchor=tk.W)
        entry6.place(relx=0.3, rely=0.6, anchor=tk.W)

        button1.place(relx=0.3, rely=0.9, anchor=tk.CENTER)
        button2.place(relx=0.7, rely=0.9, anchor=tk.CENTER)


class LDFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, app):
        ctk.CTkFrame.__init__(self, parent)
        self.app = app
        self.controller = controller

        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(5, weight=1)

        self.first_frame = ctk.CTkFrame(master=parent, fg_color=COLOR_APP_FOREGROUND, width=440, height=45,
                                        bg_color=COLOR_APP_BACKGROUND)
        self.first_frame.grid(row=0, column=0, sticky='nsew')

        self.label = ctk.CTkLabel(master=self.first_frame, text='Ostatnie 5 wpisów', text_font=FONT)
        self.label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.frames = []
        for i in range(5):
            self.frames.append(ctk.CTkFrame(master=parent, fg_color=COLOR_APP_FOREGROUND, width=440, height=45,
                                            bg_color=COLOR_APP_BACKGROUND))
            self.frames[i].grid(row=i + 1, column=0, sticky='nsew')

        contents = self.app.get_entries(skip=0, limit=5)
        self.f = []
        for i in range(min(5, len(contents))):
            self.f.append(self.SingleEntry(self.frames[i], contents[i]))

    class SingleEntry:
        def __init__(self, parent, content):
            if content['is_outcome']:
                color = ('red', 'red')
            else:
                color = ('green', 'green')

            self.label_cat = ctk.CTkLabel(master=parent, text=f'Kategoria: {category_names[content["category"]]}',
                                          width=0, text_font=SMALL_FONT)
            self.amount = ctk.CTkLabel(master=parent, text=f'Kwota: {content["amount"]}', text_color=color, width=0,
                                       text_font=SMALL_FONT)

            self.label_cat.place(relx=0.01, rely=0.5, anchor=tk.W)
            self.amount.place(relx=0.99, rely=0.5, anchor=tk.E)


class RUFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, app):
        ctk.CTkFrame.__init__(self, parent)
        self.app = app
        self.controller = controller

        amount = self.app.get_current_user()['balance']
        entries = self.app.get_entries(skip=0, limit=100)
        figure = helper.get_small_plot(amount, entries)
        self.img = FigureCanvasTkAgg(figure, parent)
        self.img.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tk.CENTER)


class RDFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, app):
        ctk.CTkFrame.__init__(self, parent)
        self.app = app
        self.controller = controller

        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)

        self.frame_up = ctk.CTkFrame(master=parent, width=440, height=134, bg_color=COLOR_APP_BACKGROUND, pady=2)
        self.frame_up.grid(row=0, column=0, sticky='nsew')
        self.frame_up.grid_columnconfigure(0, weight=1)
        self.frame_up.grid_rowconfigure(1, weight=1)

        self.frame_down = ctk.CTkFrame(master=parent, width=440, height=134, bg_color=COLOR_APP_BACKGROUND, pady=2)
        self.frame_down.grid(row=1, column=0, sticky='nsew')
        self.frame_down.grid_columnconfigure(0, weight=1)
        self.frame_down.grid_rowconfigure(1, weight=1)

        self.frame_1 = ctk.CTkFrame(master=self.frame_up, width=440, height=42, corner_radius=0,
                                    fg_color=COLOR_APP_FOREGROUND)
        self.frame_1.grid(row=0, column=0, sticky='nsew')

        self.frame_2 = ctk.CTkFrame(master=self.frame_up, width=440, height=90, corner_radius=0,
                                    fg_color=COLOR_APP_FOREGROUND)
        self.frame_2.grid(row=1, column=0, sticky='nsew')

        self.frame_3 = ctk.CTkFrame(master=self.frame_down, width=440, height=42, corner_radius=0,
                                    fg_color=COLOR_APP_FOREGROUND)
        self.frame_3.grid(row=0, column=0, sticky='nsew')

        self.frame_4 = ctk.CTkFrame(master=self.frame_down, width=440, height=90, corner_radius=0,
                                    fg_color=COLOR_APP_FOREGROUND)
        self.frame_4.grid(row=1, column=0, sticky='nsew')

        self.label_1 = ctk.CTkLabel(master=self.frame_1, text_font=FONT, text='Cel dnia:')
        self.label_1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.goals = self.app.get_goals()
        if len(self.goals) == 0:
            self.label_2 = ctk.CTkLabel(master=self.frame_2, text='Nie masz jeszcze żadnych celów!', text_font=FONT)
            self.label_2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        else:
            self.go = self.SingleGoal(self.frame_2, self.goals[random.randint(0, len(self.goals) - 1)])

        self.label_3 = ctk.CTkLabel(master=self.frame_3, text='Najbliższy zaplanowany wpis:', text_font=FONT)
        self.label_3.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.planned_entry = self.app.get_planned_entries(skip=0, limit=1)
        if len(self.planned_entry) == 0:
            self.label_4 = ctk.CTkLabel(master=self.frame_4, text='Nie masz żadnych planowanych wpisów', text_font=FONT)
            self.label_4.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        else:
            idx = int(self.planned_entry[0]['id'])
            self.planned_entry = self.app.get_planned_entry(idx)
            self.pe = self.SinglePlannedEntry(self.frame_4, self.planned_entry)

    class SinglePlannedEntry:
        font = ('Arial', 10)

        def __init__(self, parent, content):
            if content['is_outcome']:
                color = ('red', 'red')
            else:
                color = ('green', 'green')

            if content['name'] is None:
                name = ''
            else:
                name = content['name']

            self.label_cat = ctk.CTkLabel(master=parent, text=f'Kategoria: {category_names[content["category"]]}',
                                          width=0, text_font=VERY_SMALL_FONT)
            self.label_name = ctk.CTkLabel(master=parent, text=f'Nazwa: {name}', width=0, text_font=VERY_SMALL_FONT)
            self.label_date = ctk.CTkLabel(master=parent, text=f'Data: {content["date"]}', width=0,
                                           text_font=VERY_SMALL_FONT)
            self.label_amount = ctk.CTkLabel(master=parent, text=f'Kwota: {content["amount"]}', text_color=color,
                                             width=0, text_font=VERY_SMALL_FONT)
            self.label_period = ctk.CTkLabel(master=parent, width=0, text_font=VERY_SMALL_FONT,
                                             text=f'Powtarzalność: {periodicity_names[content["periodicity"]]}')

            self.label_cat.place(relx=0.01, rely=0.33, anchor=tk.W)
            if content['name'] is not None:
                self.label_name.place(relx=0.99, rely=0.33, anchor=tk.E)
            self.label_date.place(relx=0.01, rely=0.66, anchor=tk.W)
            self.label_amount.place(relx=0.99, rely=0.66, anchor=tk.E)
            self.label_period.place(relx=0.5, rely=0.66, anchor=tk.CENTER)

    class SingleGoal:
        def __init__(self, parent, content):
            self.img = load_image(icons_path[content['icon']], (80, 80))
            self.label_img = ctk.CTkLabel(master=parent, width=0, image=self.img)
            self.label_img.place(relx=0.015, rely=0.35, anchor=tk.W)

            color = None
            if content['color'] != Color.default.value:
                color = color_names[content['color']]

            self.label = ctk.CTkLabel(master=parent, width=0, text=content['name'], text_font=TITLE_FONT)

            width = content['actual_amount'] / content['target_amount']
            if width >= 1:
                width = 1

            self.progressbar = ctk.CTkProgressBar(master=parent, width=400)
            self.progressbar.set(width)
            if color is not None:
                self.label.configure(text_color=color)
                self.progressbar.configure(progress_color=color)

            self.label.place(relx=0.27, rely=0.35, anchor=tk.W)
            self.progressbar.place(relx=0.5, rely=0.85, anchor=tk.CENTER)
