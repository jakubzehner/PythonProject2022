import tkinter as tk
import customtkinter as ctk
from enums import *
import app.helper as helper
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from util import create_popup, category_names, category_values, removing_popup, watching_popup
from constants import *


def create_label_with_amount(master, rely, text, amount):
    label = ctk.CTkLabel(master=master, text_font=SMALL_FONT, width=0,
                         text=f'{text}: {amount}')
    label.place(relx=0, rely=rely, anchor=tk.W)
    return label


def update_label_with_amount(label, text, amount, rely):
    label.configure(text=f'{text}: {amount}', width=0, anchor=tk.W)
    label.configure(width=0)
    label.place(relx=0, rely=rely, anchor=tk.W)


class Entry:
    def __init__(self, parent, controller, app):
        self.app = app
        self.controller = controller

        # Configure layot and create frames
        parent.grid_rowconfigure(0, weight=2)
        parent.grid_columnconfigure(1, weight=2)

        self.frame_left = ctk.CTkFrame(master=parent, height=HEIGHT - MENU_HEIGHT, corner_radius=0,
                                       width=ENTRY_LEFT_WIDTH, padx=5, pady=10, fg_color=COLOR_APP_FOREGROUND)
        self.frame_left.grid(row=0, column=0, sticky='nsew')
        self.frame_right = ctk.CTkFrame(master=parent, height=HEIGHT - MENU_HEIGHT, corner_radius=0,
                                        width=WIDTH - ENTRY_LEFT_WIDTH - 10, padx=5, pady=10,
                                        fg_color=COLOR_APP_BACKGROUND)
        self.frame_right.grid(row=0, column=1, sticky='nsew')

        # Left frame
        self.label = ctk.CTkLabel(master=self.frame_left, text='Dane ze 100 ostatnich wpisów:',
                                  text_font=('Roboto Medium', 14))
        self.label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        self.last_100_entries = self.app.get_entries(skip=0, limit=100)

        self.label1 = create_label_with_amount(self.frame_left, 0.15, 'Suma wydatków',
                                               helper.get_outcome(self.last_100_entries))
        self.label2 = create_label_with_amount(self.frame_left, 0.2, 'Suma przychodów',
                                               helper.get_income(self.last_100_entries))
        self.label3 = create_label_with_amount(self.frame_left, 0.25, 'Jedzenie i napoje',
                                               helper.get_category(self.last_100_entries, Category.food_and_drink))
        self.label4 = create_label_with_amount(self.frame_left, 0.3, 'Zakupy',
                                               helper.get_category(self.last_100_entries, Category.shopping))
        self.label5 = create_label_with_amount(self.frame_left, 0.35, 'Dom i mieszkanie',
                                               helper.get_category(self.last_100_entries, Category.accommodation))
        self.label6 = create_label_with_amount(self.frame_left, 0.4, 'Transport i podróże',
                                               helper.get_category(self.last_100_entries, Category.transport))
        self.label7 = create_label_with_amount(self.frame_left, 0.45, 'Samochód',
                                               helper.get_category(self.last_100_entries, Category.car))
        self.label8 = create_label_with_amount(self.frame_left, 0.5, 'Życie i rozrywka',
                                               helper.get_category(self.last_100_entries, Category.entertainment))
        self.label9 = create_label_with_amount(self.frame_left, 0.55, 'Elektronika',
                                               helper.get_category(self.last_100_entries, Category.electronic))
        self.label10 = create_label_with_amount(self.frame_left, 0.6, 'Nakłady finansowe',
                                                helper.get_category(self.last_100_entries, Category.funding))
        self.label11 = create_label_with_amount(self.frame_left, 0.65, 'Inwestycje',
                                                helper.get_category(self.last_100_entries, Category.investments))
        self.label12 = create_label_with_amount(self.frame_left, 0.7, 'Przychód',
                                                helper.get_category(self.last_100_entries, Category.income))
        self.label13 = create_label_with_amount(self.frame_left, 0.75, 'Inne',
                                                helper.get_category(self.last_100_entries, Category.other))

        self.button = ctk.CTkButton(master=self.frame_left, text='Zobacz wykres', command=self.show_plot,
                                    text_font=SMALL_FONT)
        self.button.place(relx=0.5, rely=0.84, anchor=tk.CENTER)

        self.button1 = ctk.CTkButton(master=self.frame_left, text='Dodaj wpis', command=self.add_entry,
                                     text_font=SMALL_FONT)
        self.button1.place(relx=0.5, rely=0.93, anchor=tk.CENTER)

        # Right frame
        self.f: ctk.CTkFrame | None = None
        self.create_right_frame()

    def create_right_frame(self):
        for child in self.frame_right.winfo_children():
            child.destroy()

        self.f = RightFrame(self.frame_right, self, self.app)

    def show_plot(self):
        def on_closing():
            popup.destroy()

        popup = create_popup(900, 400, 'Ostatnie 100 wpisów', on_closing)

        amount = self.app.get_current_user()['balance']

        figure = helper.get_plot(amount, self.last_100_entries)
        img = FigureCanvasTkAgg(figure, popup)
        img.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tk.CENTER)

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
            self.update_summary()
            self.create_right_frame()
            on_closing()

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

    def update_summary(self):
        self.last_100_entries = self.app.get_entries(skip=0, limit=100)

        update_label_with_amount(self.label1, 'Suma wydatków', helper.get_outcome(self.last_100_entries), 0.15)
        update_label_with_amount(self.label2, 'Suma przychodów', helper.get_income(self.last_100_entries), 0.2)
        update_label_with_amount(self.label3, 'Jedzenie i napoje',
                                 helper.get_category(self.last_100_entries, Category.food_and_drink), 0.25)
        update_label_with_amount(self.label4, 'Zakupy',
                                 helper.get_category(self.last_100_entries, Category.shopping), 0.3)
        update_label_with_amount(self.label5, 'Dom i mieszkanie',
                                 helper.get_category(self.last_100_entries, Category.accommodation), 0.35)
        update_label_with_amount(self.label6, 'Transport i podróże',
                                 helper.get_category(self.last_100_entries, Category.transport), 0.4)
        update_label_with_amount(self.label7, 'Samochód', helper.get_category(self.last_100_entries, Category.car),
                                 0.45)
        update_label_with_amount(self.label8, 'Życie i rozrywka',
                                 helper.get_category(self.last_100_entries, Category.entertainment), 0.5)
        update_label_with_amount(self.label9, 'Elektronika',
                                 helper.get_category(self.last_100_entries, Category.electronic), 0.55)
        update_label_with_amount(self.label10, 'Nakłady finansowe',
                                 helper.get_category(self.last_100_entries, Category.funding), 0.6)
        update_label_with_amount(self.label11, 'Inwestycje',
                                 helper.get_category(self.last_100_entries, Category.investments), 0.65)
        update_label_with_amount(self.label12, 'Przychód',
                                 helper.get_category(self.last_100_entries, Category.income), 0.7)
        update_label_with_amount(self.label13, 'Inne', helper.get_category(self.last_100_entries, Category.other),
                                 0.75)


class RightFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, app):
        ctk.CTkFrame.__init__(self, parent, width=WIDTH - ENTRY_LEFT_WIDTH, height=HEIGHT - MENU_HEIGHT, padx=5,
                              pady=10)
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.app = app
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        self.start = 0
        self.create()

    def restart(self):
        self.start = 0

    def create(self):
        for child in self.winfo_children():
            child.destroy()

        contents = self.app.get_entries(skip=self.start, limit=7)

        if len(contents) == 7:
            active_next = tk.NORMAL
        else:
            active_next = tk.DISABLED

        if self.start > 0:
            active_prev = tk.NORMAL
        else:
            active_prev = tk.DISABLED

        frames = []
        for i in range(6):
            frames.append(ctk.CTkFrame(master=self, corner_radius=0, height=(HEIGHT - MENU_HEIGHT - 18) // 7,
                                       width=WIDTH - ENTRY_LEFT_WIDTH, padx=5, pady=1, fg_color=COLOR_APP_FOREGROUND))
            frames[i].grid(row=i, column=0, sticky='nswe')

        last_frame = ctk.CTkFrame(master=self, corner_radius=0, height=(HEIGHT - MENU_HEIGHT - 20) // 7,
                                  width=WIDTH - ENTRY_LEFT_WIDTH, padx=5, pady=1, fg_color=COLOR_APP_FOREGROUND)
        last_frame.grid(row=6, column=0, sticky='nswe')

        # frames
        cont_frames = []
        for i in range(min(len(contents), 6)):
            cont_frames.append(EntryElem(frames[i], self, self.app, contents[i]))

        # last frame
        img_prev = self.controller.controller.img_prev
        img_next = self.controller.controller.img_next

        button_prev = ctk.CTkButton(master=last_frame, width=0, height=0, image=img_prev, command=self.prev, text='',
                                    fg_color=last_frame.fg_color, hover_color=last_frame.fg_color, state=active_prev)
        button_next = ctk.CTkButton(master=last_frame, width=0, height=0, image=img_next, command=self.next, text='',
                                    fg_color=last_frame.fg_color, hover_color=last_frame.fg_color, state=active_next)

        button_prev.place(relx=0.1, rely=0.5, anchor=tk.CENTER)
        button_next.place(relx=0.9, rely=0.5, anchor=tk.CENTER)

    def next(self):
        self.start += 6
        self.create()

    def prev(self):
        self.start -= 6
        self.create()


class EntryElem(ctk.CTkFrame):
    def __init__(self, parent, controller, app, content):
        ctk.CTkFrame.__init__(self, parent)
        self.app = app
        self.controller = controller
        self.content = content

        self.img_watch = self.controller.controller.controller.img_watch
        self.img_remove = self.controller.controller.controller.img_remove
        self.img_edit = self.controller.controller.controller.img_edit

        if self.content['is_outcome']:
            color = ('red', 'red')
        else:
            color = ('green', 'green')

        cat_name = category_names[self.content['category']]
        amount = self.content['amount']

        button1 = ctk.CTkButton(master=parent, width=0, height=0, image=self.img_watch, command=self.watch, text='',
                                fg_color=parent.fg_color, hover_color=parent.fg_color)
        button2 = ctk.CTkButton(master=parent, width=0, height=0, image=self.img_edit, command=self.edit, text='',
                                fg_color=parent.fg_color, hover_color=parent.fg_color)
        button3 = ctk.CTkButton(master=parent, width=0, height=0, image=self.img_remove, command=self.remove, text='',
                                fg_color=parent.fg_color, hover_color=parent.fg_color)

        button1.place(relx=0.7, rely=0.5, anchor=tk.W)
        button2.place(relx=0.8, rely=0.5, anchor=tk.W)
        button3.place(relx=0.9, rely=0.5, anchor=tk.W)

        name = self.content['name']
        if name is not None:
            label3 = ctk.CTkLabel(master=parent, width=0, height=0, text=f'Nazwa: {name}', text_font=('Arial', 13))
            label1 = ctk.CTkLabel(master=parent, width=0, height=0, text=f'Kategoria: {cat_name}',
                                  text_font=('Arial', 13))
            label2 = ctk.CTkLabel(master=parent, width=0, height=0, text=f'Kwota: {amount}', text_font=('Arial', 13),
                                  text_color=color)
            label3.place(relx=0.01, rely=0.2, anchor=tk.W)
            label1.place(relx=0.01, rely=0.5, anchor=tk.W)
            label2.place(relx=0.01, rely=0.8, anchor=tk.W)

        else:
            label1 = ctk.CTkLabel(master=parent, width=0, height=0, text=f'Kategoria: {cat_name}',
                                  text_font=('Arial', 13))
            label2 = ctk.CTkLabel(master=parent, width=0, height=0, text=f'Kwota: {amount}', text_font=('Arial', 13),
                                  text_color=color)
            label1.place(relx=0.01, rely=0.27, anchor=tk.W)
            label2.place(relx=0.01, rely=0.63, anchor=tk.W)

    def watch(self):
        content = self.app.get_entry(self.content['id'])

        name = content['name']
        if name is None:
            name = ''
        if content['is_outcome']:
            outcome = 'Tak'
        else:
            outcome = 'Nie'
        description = content['description']
        if description is None:
            description = ''

        texts = [f'Kategoria: {category_names[content["category"]]}', f'Nazwa: {name}', f'Czy to wydatek: {outcome}',
                 f'Data wpisu: {content["date"]}', f'Kwota: {content["amount"]}', f'Opis: {description}']
        watching_popup('Podgląd planowanego wpisu', texts)

    def edit(self):
        def on_closing():
            popup.destroy()

        def edit():
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

            self.app.edit_entry(self.content['id'], category_values[entry1.get()], name, outcome, entry4.get(),
                                float(entry5.get()), description)
            self.controller.controller.update_summary()
            self.controller.controller.create_right_frame()
            on_closing()

        popup = create_popup(400, 400, 'Edycja wpisu', on_closing)
        content = self.app.get_entry(self.content['id'])

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

        entry1.set(category_names[content['category']])
        if content['name'] is None:
            name = ''
        else:
            name = content['name']
        entry2.insert(tk.END, name)
        if content['is_outcome']:
            out = 'Tak'
        else:
            out = 'Nie'
        entry3.set(out)
        entry4.insert(tk.END, content['date'])
        entry5.insert(tk.END, content['amount'])
        if content['description'] is None:
            description = ''
        else:
            description = content['description']
        entry6.insert(tk.END, description)

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

        button1 = ctk.CTkButton(master=popup, text='Edytuj', command=edit)
        button2 = ctk.CTkButton(master=popup, text='Anuluj', command=on_closing)

        button1.place(relx=0.3, rely=0.9, anchor=tk.CENTER)
        button2.place(relx=0.7, rely=0.9, anchor=tk.CENTER)

    def remove(self):
        removing_popup(self.app.delete_entry, self.content['id'], 'Usuwanie wpisu', 'Czy na pewno\nchcesz usunąć wpis?',
                       [self.controller.restart, self.controller.create, self.controller.controller.update_summary])
