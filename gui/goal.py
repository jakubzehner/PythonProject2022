import tkinter as tk
import customtkinter as ctk
from enums import *
import datetime
from constants import *
from util import load_image, create_popup, color_values, color_names, icons_path, icons_values, color_names_pl, \
    icons_names, removing_popup, watching_popup


class Goal:
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
        self.start += 4
        self.create_frame()

    def prev(self):
        self.start -= 4
        self.create_frame()

    def create_frame(self):
        for child in self.frame.winfo_children():
            child.destroy()

        self.frame.grid_rowconfigure(4, weight=2)
        self.frame.grid_columnconfigure(0, weight=2)

        frames = []
        for i in range(4):
            frames.append(ctk.CTkFrame(master=self.frame, height=(HEIGHT - MENU_HEIGHT - 20) // 5, width=WIDTH,
                                       corner_radius=0, fg_color=COLOR_APP_FOREGROUND, padx=5, pady=1))
            frames[i].grid(row=i, column=0, sticky='nswe')

        last_frame = ctk.CTkFrame(master=self.frame, height=(HEIGHT - MENU_HEIGHT - 20) // 5, width=WIDTH,
                                  corner_radius=0, fg_color=COLOR_APP_FOREGROUND, padx=5, pady=1)
        last_frame.grid(row=4, column=0, sticky='nswe')

        contents = self.app.get_goals(skip=self.start, limit=5)

        if len(contents) == 5:
            active_next = tk.NORMAL
        else:
            active_next = tk.DISABLED

        if self.start > 0:
            active_prev = tk.NORMAL
        else:
            active_prev = tk.DISABLED

        cont_frames = []
        for i in range(min(4, len(contents))):
            cont_frames.append(self.GoalElem(frames[i], self, self.app, contents[i]))

        # last frame
        img_prev = self.controller.img_prev
        button_prev = ctk.CTkButton(master=last_frame, width=0, height=0, image=img_prev, command=self.prev,
                                    text='', state=active_prev, fg_color=last_frame.fg_color,
                                    hover_color=last_frame.fg_color)

        img_next = self.controller.img_next
        button_next = ctk.CTkButton(master=last_frame, width=0, height=0, image=img_next, command=self.next,
                                    text='', state=active_next, fg_color=last_frame.fg_color,
                                    hover_color=last_frame.fg_color)

        button_add = ctk.CTkButton(master=last_frame, width=250, height=40, text='Dodaj nowy cel',
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

            description = entry7.get()
            if description == "":
                description = None

            try:
                datetime.datetime.strptime(entry4.get(), form)
            except ValueError:
                error_label.configure(text='Nieprawidłowa data', width=0)
                error_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
                return

            name = entry1.get()
            if name == "":
                name = None

            if name is None:
                error_label.configure(text='Nazwa celu jest wymagana', width=0)
                error_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
                return

            try:
                if not float(entry3.get()) > 0:
                    error_label.configure(text='Kwota aktualna musi być większa od zera', width=0)
                    error_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
                    return

                if not float(entry2.get()) > 0:
                    error_label.configure(text='Kwota docelowa musi być większa od zera', width=0)
                    error_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
                    return

            except ValueError:
                error_label.configure(text='Kwota musi być liczbą', width=0)
                error_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
                return

            self.app.add_goal(name, float(entry2.get()), float(entry3.get()), entry4.get(), color_values[entry5.get()],
                              icons_values[entry6.get()], description)
            on_closing()
            self.restart()
            self.create_frame()

        popup = create_popup(400, 400, 'Dodawanie nowego celu', on_closing)

        label1 = ctk.CTkLabel(master=popup, width=0, height=0, text='Nazwa celu')
        label2 = ctk.CTkLabel(master=popup, width=0, height=0, text='Docelowa kwota')
        label3 = ctk.CTkLabel(master=popup, width=0, height=0, text='Aktualna kwota')
        label4 = ctk.CTkLabel(master=popup, width=0, height=0, text='Data celu')
        label5 = ctk.CTkLabel(master=popup, width=0, height=0, text='Kolor celu')
        label6 = ctk.CTkLabel(master=popup, width=0, height=0, text='Ikona celu')
        label7 = ctk.CTkLabel(master=popup, width=0, height=0, text='Opis celu')

        entry1 = ctk.CTkEntry(master=popup, width=250, placeholder_text='nazwa')
        entry2 = ctk.CTkEntry(master=popup, width=250, placeholder_text='docelowa kwota')
        entry3 = ctk.CTkEntry(master=popup, width=250, placeholder_text='aktualna kwota')
        entry4 = ctk.CTkEntry(master=popup, width=250, placeholder_text='data')
        entry5 = ctk.CTkComboBox(master=popup, width=250, values=[*color_values.keys()])
        entry6 = ctk.CTkComboBox(master=popup, width=250, values=[*icons_values.keys()])
        entry7 = ctk.CTkEntry(master=popup, width=250, placeholder_text='opis')

        entry4.insert(tk.END, datetime.date.today().strftime('%Y-%m-%d'))

        button1 = ctk.CTkButton(master=popup, text='Dodaj', command=add)
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

    class GoalElem:
        def __init__(self, parent, controller, app, content):
            self.app = app
            self.controller = controller
            self.content = content

            self.img = load_image(icons_path[content['icon']], (80, 80))
            self.img_watch = self.controller.controller.img_watch
            self.img_remove = self.controller.controller.img_remove
            self.img_edit = self.controller.controller.img_edit

            button_watch = ctk.CTkButton(master=parent, width=0, height=0, image=self.img_watch, command=self.watch,
                                         text='',
                                         fg_color=parent.fg_color, hover_color=parent.fg_color)
            button_edit = ctk.CTkButton(master=parent, width=0, height=0, image=self.img_edit, command=self.edit,
                                        text='',
                                        fg_color=parent.fg_color, hover_color=parent.fg_color)
            button_remove = ctk.CTkButton(master=parent, width=0, height=0, image=self.img_remove, command=self.remove,
                                          text='', fg_color=parent.fg_color, hover_color=parent.fg_color)

            name = content['name']
            t_amount = content['target_amount']
            a_amount = content['actual_amount']
            color = None
            if content['color'] != Color.default.value:
                color = color_names[content['color']]
            width = a_amount / t_amount
            if width >= 1:
                width = 1

            self.label_img = ctk.CTkLabel(master=parent, width=0, image=self.img)
            self.label = ctk.CTkLabel(master=parent, width=0, text=name, text_font=MEDIUM_TITLE_FONT)
            self.label_amounts = ctk.CTkLabel(master=parent, width=0, text=f'{a_amount} / {t_amount}',
                                              text_font=MEDIUM_TITLE_FONT)
            self.progressbar = ctk.CTkProgressBar(master=parent, width=850)
            self.progressbar.set(width)
            if color is not None:
                self.label.configure(text_color=color)
                self.label_amounts.configure(text_color=color)
                self.progressbar.configure(progress_color=color)

            self.label_img.place(relx=0.015, rely=0.5, anchor=tk.W)
            self.label.place(relx=0.15, rely=0.5, anchor=tk.W)
            self.label_amounts.place(relx=0.8, rely=0.5, anchor=tk.E)
            self.progressbar.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

            button_watch.place(relx=0.81, rely=0.5, anchor=tk.W)
            button_edit.place(relx=0.88, rely=0.5, anchor=tk.W)
            button_remove.place(relx=0.95, rely=0.5, anchor=tk.W)

        def watch(self):
            content = self.app.get_goal(self.content['id'])

            description = ''
            if content['description'] is not None:
                description = content['description']

            texts = [f'Nazwa celu: {content["name"]}', f'Docelowa kwota: {content["target_amount"]}',
                     f'Aktualna kwota: {content["actual_amount"]}', f'Data celu: {content["date"]}',
                     f'Kolor celu: {color_names_pl[content["color"]]}', f'Ikona celu: {icons_names[content["icon"]]}',
                     f'Opis celu: {description}']
            watching_popup('Podgląd celu', texts)

        def edit(self):
            def on_closing():
                popup.destroy()

            def edit_goal():
                error_label = ctk.CTkLabel(master=popup, width=0, height=0, text_color=('red', 'red'))
                form = '%Y-%m-%d'

                name = entry1.get()
                if name == "":
                    name = None

                description = entry7.get()
                if description == "":
                    description = None

                if name is None:
                    error_label.configure(text='Nazwa celu jest wymagana', width=0)
                    error_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
                    return

                try:
                    datetime.datetime.strptime(entry4.get(), form)
                except ValueError:
                    error_label.configure(text='Nieprawidłowa data', width=0)
                    error_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
                    return

                try:
                    float(entry2.get())
                    float(entry3.get())
                except ValueError:
                    error_label.configure(text='Kwota musi być liczbą', width=0)
                    error_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
                    return

                if not float(entry2.get()) > 0:
                    error_label.configure(text='Kwota docelowa musi być większa od zera', width=0)
                    error_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
                    return

                if not float(entry3.get()) > 0:
                    error_label.configure(text='Kwota aktualna musi być większa od zera', width=0)
                    error_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
                    return

                self.app.edit_goal(self.content['id'], name, float(entry2.get()), float(entry3.get()), entry4.get(),
                                   color_values[entry5.get()],
                                   icons_values[entry6.get()], description)
                on_closing()
                self.controller.restart()
                self.controller.create_frame()

            popup = create_popup(400, 400, 'Edycja celu', on_closing)
            content = self.app.get_goal(self.content['id'])

            label1 = ctk.CTkLabel(master=popup, width=0, height=0, text='Nazwa celu')
            label2 = ctk.CTkLabel(master=popup, width=0, height=0, text='Docelowa kwota')
            label3 = ctk.CTkLabel(master=popup, width=0, height=0, text='Aktualna kwota')
            label4 = ctk.CTkLabel(master=popup, width=0, height=0, text='Data celu')
            label5 = ctk.CTkLabel(master=popup, width=0, height=0, text='Kolor celu')
            label6 = ctk.CTkLabel(master=popup, width=0, height=0, text='Ikona celu')
            label7 = ctk.CTkLabel(master=popup, width=0, height=0, text='Opis celu')

            entry1 = ctk.CTkEntry(master=popup, width=250, placeholder_text='nazwa')
            entry2 = ctk.CTkEntry(master=popup, width=250, placeholder_text='docelowa kwota')
            entry3 = ctk.CTkEntry(master=popup, width=250, placeholder_text='aktualna kwota')
            entry4 = ctk.CTkEntry(master=popup, width=250, placeholder_text='data')
            entry5 = ctk.CTkComboBox(master=popup, width=250, values=[*color_values.keys()])
            entry6 = ctk.CTkComboBox(master=popup, width=250, values=[*icons_values.keys()])
            entry7 = ctk.CTkEntry(master=popup, width=250, placeholder_text='opis')

            description = ''
            if content['description'] is not None:
                description = content['description']

            entry1.insert(tk.END, content['name'])
            entry2.insert(tk.END, content['target_amount'])
            entry3.insert(tk.END, content['actual_amount'])
            entry4.insert(tk.END, content['date'])
            entry5.set(color_names_pl[content['color']])
            entry6.set(icons_names[content['icon']])
            entry7.insert(tk.END, description)

            button2 = ctk.CTkButton(master=popup, text='Anuluj', command=on_closing)
            button1 = ctk.CTkButton(master=popup, text='Edytuj', command=edit_goal)

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
            removing_popup(self.app.delete_goal, self.content['id'], 'Usuwanie celu',
                           'Czy na pewno\n chcesz usunąć cel?', [self.controller.restart, self.controller.create_frame])
