import tkinter as tk
import customtkinter as ctk
from constants import *
import datetime
from util import removing_popup, create_popup, category_names, periodicity_names, category_values, periodicity_values, \
    watching_popup


# Klasa zawierająca widok zakładki "Planowane wpisy"

class PlannedEntry:
    def __init__(self, parent, controller, app):
        self.controller = controller
        self.app = app

        parent.grid_rowconfigure(0, weight=2)
        parent.grid_columnconfigure(0, weight=2)

        self.frame = ctk.CTkFrame(master=parent, height=HEIGHT - MENU_HEIGHT, corner_radius=0, width=WIDTH,
                                  padx=10, pady=10, fg_color=COLOR_APP_BACKGROUND)
        self.frame.grid(row=0, column=0, sticky='nsew')

        self.start = 0
        self.create_frame()

    def restart(self):
        self.start = 0

    def next(self):
        self.start += 6
        self.create_frame()

    def prev(self):
        self.start -= 6
        self.create_frame()

    def create_frame(self):
        for child in self.frame.winfo_children():
            child.destroy()

        self.frame.grid_rowconfigure(6, weight=2)
        self.frame.grid_columnconfigure(0, weight=2)

        frames = []
        for i in range(6):
            frames.append(ctk.CTkFrame(master=self.frame, height=(HEIGHT - MENU_HEIGHT - 16) // 7, width=WIDTH,
                                       corner_radius=0, fg_color=COLOR_APP_FOREGROUND, padx=5, pady=1))
            frames[i].grid(row=i, column=0, sticky='nswe')

        last_frame = ctk.CTkFrame(master=self.frame, height=(HEIGHT - MENU_HEIGHT - 20) // 7, width=WIDTH,
                                  corner_radius=0, fg_color=COLOR_APP_FOREGROUND, padx=5, pady=1)
        last_frame.grid(row=6, column=0, sticky='nswe')

        contents = self.app.get_planned_entries(skip=self.start, limit=7)

        if len(contents) == 7:
            active_next = tk.NORMAL
        else:
            active_next = tk.DISABLED

        if self.start > 0:
            active_prev = tk.NORMAL
        else:
            active_prev = tk.DISABLED

        cont_frames = []
        for i in range(min(6, len(contents))):
            cont_frames.append(self.PlannedEntryElem(frames[i], self, self.app, contents[i]))

        # last frame
        img_prev = self.controller.img_prev
        img_next = self.controller.img_next

        button_prev = ctk.CTkButton(master=last_frame, width=0, height=0, image=img_prev, command=self.prev,
                                    text='', state=active_prev, fg_color=last_frame.fg_color,
                                    hover_color=last_frame.fg_color)
        button_next = ctk.CTkButton(master=last_frame, width=0, height=0, image=img_next, command=self.next,
                                    text='', state=active_next, fg_color=last_frame.fg_color,
                                    hover_color=last_frame.fg_color)

        button_add = ctk.CTkButton(master=last_frame, width=250, height=40, text='Dodaj nowy planowany wpis',
                                   command=self.add, text_font=SMALL_FONT, corner_radius=8)

        button_prev.place(relx=0.1, rely=0.5, anchor=tk.CENTER)
        button_next.place(relx=0.9, rely=0.5, anchor=tk.CENTER)
        button_add.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def add(self):
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

            self.app.add_planned_entry(category_values[entry1.get()], name, outcome, entry4.get(), float(entry5.get()),
                                       description, periodicity_values[entry7.get()])
            on_closing()
            self.restart()
            self.create_frame()

        popup = create_popup(400, 400, 'Dodawanie nowego planowanego wpisu', on_closing)

        label1 = ctk.CTkLabel(master=popup, width=0, height=0, text='Kategoria wpisu')
        label2 = ctk.CTkLabel(master=popup, width=0, height=0, text='Nazwa wpisu')
        label3 = ctk.CTkLabel(master=popup, width=0, height=0, text='Czy to wydatek')
        label4 = ctk.CTkLabel(master=popup, width=0, height=0, text='Data wpisu')
        label5 = ctk.CTkLabel(master=popup, width=0, height=0, text='Kwota wpisu')
        label6 = ctk.CTkLabel(master=popup, width=0, height=0, text='Opis wpisu')
        label7 = ctk.CTkLabel(master=popup, width=0, height=0, text='Powtarzalność')

        entry1 = ctk.CTkComboBox(master=popup, values=[*category_values.keys()], width=250)
        entry2 = ctk.CTkEntry(master=popup, width=250, placeholder_text='nazwa')
        entry3 = ctk.CTkComboBox(master=popup, values=['Tak', 'Nie'], width=250)
        entry4 = ctk.CTkEntry(master=popup, width=250, placeholder_text='data')
        entry5 = ctk.CTkEntry(master=popup, width=250, placeholder_text='kwota')
        entry6 = ctk.CTkEntry(master=popup, width=250, placeholder_text='opis')
        entry7 = ctk.CTkComboBox(master=popup, width=250, values=[*periodicity_values.keys()])

        button1 = ctk.CTkButton(master=popup, text='Dodaj', command=add)
        button2 = ctk.CTkButton(master=popup, text='Anuluj', command=on_closing)

        entry4.insert(tk.END, datetime.date.today().strftime('%Y-%m-%d'))

        label1.place(relx=0, rely=0.1, anchor=tk.W)
        label2.place(relx=0, rely=0.2, anchor=tk.W)
        label3.place(relx=0, rely=0.3, anchor=tk.W)
        label4.place(relx=0, rely=0.4, anchor=tk.W)
        label5.place(relx=0, rely=0.5, anchor=tk.W)
        label7.place(relx=0, rely=0.6, anchor=tk.W)
        label6.place(relx=0, rely=0.7, anchor=tk.W)

        entry1.place(relx=0.3, rely=0.1, anchor=tk.W)
        entry2.place(relx=0.3, rely=0.2, anchor=tk.W)
        entry3.place(relx=0.3, rely=0.3, anchor=tk.W)
        entry4.place(relx=0.3, rely=0.4, anchor=tk.W)
        entry5.place(relx=0.3, rely=0.5, anchor=tk.W)
        entry7.place(relx=0.3, rely=0.6, anchor=tk.W)
        entry6.place(relx=0.3, rely=0.7, anchor=tk.W)

        button1.place(relx=0.3, rely=0.9, anchor=tk.CENTER)
        button2.place(relx=0.7, rely=0.9, anchor=tk.CENTER)

    class PlannedEntryElem:
        def __init__(self, parent, controller, app, content):
            self.app = app
            self.controller = controller
            self.content = self.app.get_planned_entry(content['id'])

            self.img_watch = self.controller.controller.img_watch
            self.img_remove = self.controller.controller.img_remove
            self.img_edit = self.controller.controller.img_edit

            if self.content['is_outcome']:
                color = ('red', 'red')
            else:
                color = ('green', 'green')

            button1 = ctk.CTkButton(master=parent, width=0, height=0, image=self.img_watch, command=self.watch, text='',
                                    fg_color=parent.fg_color, hover_color=parent.fg_color)
            button2 = ctk.CTkButton(master=parent, width=0, height=0, image=self.img_edit, command=self.edit, text='',
                                    fg_color=parent.fg_color, hover_color=parent.fg_color)
            button3 = ctk.CTkButton(master=parent, width=0, height=0, image=self.img_remove, command=self.remove,
                                    text='', fg_color=parent.fg_color, hover_color=parent.fg_color)

            cat_name = category_names[self.content['category']]
            amount = self.content['amount']
            name = self.content['name']

            label1 = ctk.CTkLabel(master=parent, width=0, height=0, text=f'Kategoria: {cat_name}',
                                  text_font=('Arial', 13))
            label2 = ctk.CTkLabel(master=parent, width=0, height=0, text=f'Kwota: {amount}',
                                  text_font=('Arial', 13), text_color=color)
            label4 = ctk.CTkLabel(master=parent, width=0, height=0, text=f'Data: {self.content["date"]}',
                                  text_font=('Arial', 13))
            label5 = ctk.CTkLabel(master=parent, width=0, height=0, text_font=('Arial', 13),
                                  text=f'Powtarzalność: {periodicity_names[content["periodicity"]]}')
            if name is not None:
                label3 = ctk.CTkLabel(master=parent, width=0, height=0, text=f'Nazwa: {name}', text_font=('Arial', 13))
                label3.place(relx=0.01, rely=0.2, anchor=tk.W)
                label1.place(relx=0.01, rely=0.5, anchor=tk.W)
                label2.place(relx=0.01, rely=0.8, anchor=tk.W)
                label4.place(relx=0.35, rely=0.5, anchor=tk.W)
                label5.place(relx=0.35, rely=0.8, anchor=tk.W)

            else:
                label1.place(relx=0.01, rely=0.27, anchor=tk.W)
                label2.place(relx=0.01, rely=0.63, anchor=tk.W)
                label4.place(relx=0.35, rely=0.27, anchor=tk.W)
                label5.place(relx=0.35, rely=0.63, anchor=tk.W)

            button1.place(relx=0.74, rely=0.5, anchor=tk.W)
            button2.place(relx=0.82, rely=0.5, anchor=tk.W)
            button3.place(relx=0.9, rely=0.5, anchor=tk.W)

        def watch(self):
            content = self.app.get_planned_entry(self.content['id'])

            category = category_names[content['category']]
            name = content['name']
            if name is None:
                name = ''
            if content['is_outcome']:
                outcome = 'Tak'
            else:
                outcome = 'Nie'
            date = content['date']
            amount = content['amount']
            description = content['description']
            if description is None:
                description = ''
            periodicity = periodicity_names[content['periodicity']]

            texts = [f'Kategoria: {category}', f'Nazwa: {name}', f'Czy to wydatek: {outcome}', f'Data wpisu: {date}',
                     f'Kwota: {amount}', f'Opis: {description}', f'Powtarzalność: {periodicity}']
            watching_popup('Podgląd planowanego wpisu', texts)

        def edit(self):
            def on_closing():
                popup.destroy()

            def edit_planned_entry():
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

                self.app.edit_planned_entry(self.content['id'], category_values[entry1.get()], name, outcome,
                                            entry4.get(), float(entry5.get()), description,
                                            periodicity_values[entry7.get()])

                on_closing()
                self.controller.restart()
                self.controller.create_frame()

            popup = create_popup(400, 400, 'Edycja planowanego wpisu', on_closing)
            content = self.app.get_planned_entry(self.content['id'])

            label1 = ctk.CTkLabel(master=popup, width=0, height=0, text='Kategoria wpisu')
            label2 = ctk.CTkLabel(master=popup, width=0, height=0, text='Nazwa wpisu')
            label3 = ctk.CTkLabel(master=popup, width=0, height=0, text='Czy to wydatek')
            label4 = ctk.CTkLabel(master=popup, width=0, height=0, text='Data wpisu')
            label5 = ctk.CTkLabel(master=popup, width=0, height=0, text='Kwota wpisu')
            label6 = ctk.CTkLabel(master=popup, width=0, height=0, text='Opis wpisu')
            label7 = ctk.CTkLabel(master=popup, width=0, height=0, text='Powtarzalność')

            entry1 = ctk.CTkComboBox(master=popup, values=[*category_values.keys()], width=250)
            entry2 = ctk.CTkEntry(master=popup, width=250, placeholder_text='nazwa')
            entry3 = ctk.CTkComboBox(master=popup, values=['Tak', 'Nie'], width=250)
            entry4 = ctk.CTkEntry(master=popup, width=250, placeholder_text='data')
            entry5 = ctk.CTkEntry(master=popup, width=250, placeholder_text='kwota')
            entry6 = ctk.CTkEntry(master=popup, width=250, placeholder_text='opis')
            entry7 = ctk.CTkComboBox(master=popup, width=250, values=[*periodicity_values.keys()])

            entry1.set(category_names[content['category']])
            entry7.set(periodicity_names[content['periodicity']])
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

            button1 = ctk.CTkButton(master=popup, text='Edytuj', command=edit_planned_entry)
            button2 = ctk.CTkButton(master=popup, text='Anuluj', command=on_closing)

            label1.place(relx=0, rely=0.1, anchor=tk.W)
            label2.place(relx=0, rely=0.2, anchor=tk.W)
            label3.place(relx=0, rely=0.3, anchor=tk.W)
            label4.place(relx=0, rely=0.4, anchor=tk.W)
            label5.place(relx=0, rely=0.5, anchor=tk.W)
            label6.place(relx=0, rely=0.6, anchor=tk.W)
            label7.place(relx=0, rely=0.7, anchor=tk.W)

            entry1.place(relx=0.3, rely=0.1, anchor=tk.W)
            entry2.place(relx=0.3, rely=0.2, anchor=tk.W)
            entry3.place(relx=0.3, rely=0.3, anchor=tk.W)
            entry4.place(relx=0.3, rely=0.4, anchor=tk.W)
            entry5.place(relx=0.3, rely=0.5, anchor=tk.W)
            entry6.place(relx=0.3, rely=0.6, anchor=tk.W)
            entry7.place(relx=0.3, rely=0.7, anchor=tk.W)

            button1.place(relx=0.3, rely=0.9, anchor=tk.CENTER)
            button2.place(relx=0.7, rely=0.9, anchor=tk.CENTER)

        def remove(self):
            removing_popup(self.app.delete_planned_entry, self.content['id'], 'Usuwanie planowanego wpisu',
                           'Czy na pewno chcesz\nusunąć planowany wpis?',
                           [self.controller.restart, self.controller.create_frame])
