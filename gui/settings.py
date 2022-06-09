import tkinter as tk
import customtkinter as ctk
from main import cfg, config
from util import create_popup
from constants import *


def create_label(master, text, relx, rely, anchor=tk.W, font=SMALL_FONT, width=0):
    label = ctk.CTkLabel(master=master, text=text, text_font=font, width=width)
    label.place(relx=relx, rely=rely, anchor=anchor)
    return label


# Klasa zawierająca widok zakładki "Ustawienia"

class Settings:
    def __init__(self, parent, controller, app):
        self.parent = parent
        self.controller = controller
        self.app = app

        f_name = ""
        l_name = ""
        user = self.app.get_current_user()
        if user['first_name'] is not None:
            f_name = user['first_name']
        if user['last_name'] is not None:
            l_name = user['last_name']

        # User settings
        self.label_title_1 = create_label(master=parent, text='DANE UŻYTKOWNIA', font=SMALL_TITLE_FONT, relx=0.01,
                                          rely=0.075)
        # First name
        self.label_f_name = create_label(master=parent, text=f'Imię:  {f_name}', relx=0.02, rely=0.15)

        # Last name
        self.label_l_name = create_label(master=parent, text=f'Nazwisko:  {l_name}', relx=0.02, rely=0.22)

        # Change names
        self.button_names = ctk.CTkButton(master=parent, text='Edytuj dane', text_font=SMALL_FONT, width=120,
                                          command=self.change_names)
        self.button_names.place(relx=0.03, rely=0.28)

        # Change password
        self.button_pass = ctk.CTkButton(master=parent, text='Zmień hasło', text_font=SMALL_FONT, width=120,
                                         command=self.change_password)
        self.button_pass.place(relx=0.03, rely=0.36)

        # Delete account
        self.button_delete = ctk.CTkButton(master=parent, text='Usuń konto', text_font=SMALL_FONT, width=120,
                                           command=self.delete_account, fg_color=('red', 'red'),
                                           hover_color=('darkred', 'darkred'))
        self.button_delete.place(relx=0.03, rely=0.44)

        # App settings
        self.label_title_2 = create_label(master=parent, text='USTAWIENIA APLIKACJI', relx=0.01, rely=0.6,
                                          font=SMALL_TITLE_FONT)

        # Theme
        self.label_theme = create_label(master=parent, text='Motyw', relx=0.02, rely=0.7)

        self.counter = 0
        colors = {'blue': 'Niebieski', 'green': 'Zielony', 'dark-blue': 'Ciemno-niebieski'}
        self.option_theme = ctk.CTkOptionMenu(master=parent, values=[*colors.values()],
                                              command=self.change_theme, text_font=SMALL_FONT)
        self.option_theme.place(relx=0.12, rely=0.7, anchor=tk.W)
        self.option_theme.set(colors[cfg['color_theme']])

        # Appearance
        self.label_appearance = create_label(master=parent, text='Tryb', relx=0.02, rely=0.8)

        appearances = {'System': 'Systemowy', 'Light': 'Jasny', 'Dark': 'Ciemny'}
        self.option_appearance = ctk.CTkOptionMenu(master=parent, values=[*appearances.values()],
                                                   command=self.change_appearance, text_font=SMALL_FONT)
        self.option_appearance.place(relx=0.12, rely=0.8, anchor=tk.W)
        self.option_appearance.set(f'{appearances[ctk.get_appearance_mode()]}')

    def change_theme(self, choice):
        self.counter += 1
        colors = {'Niebieski': 'blue', 'Zielony': 'green', 'Ciemno-niebieski': 'dark-blue'}
        config['DEFAULT']['color_theme'] = colors[choice]
        with open('config.conf', 'w') as configfile:
            config.write(configfile)

        label = ctk.CTkLabel(master=self.parent, text='Zmiany zostaną zastosowane po ponownym uruchomieniu',
                             text_font=('Roboto Medium', 10), width=0, text_color='red')
        if self.counter > 1:
            label.place(relx=0.02, rely=0.98, anchor=tk.W)

    @staticmethod
    def change_appearance(choice):
        appearances = {'Systemowy': 'System', 'Jasny': 'Light', 'Ciemny': 'Dark'}
        config['DEFAULT']['appearance_mode'] = appearances[choice]
        with open('config.conf', 'w') as configfile:
            config.write(configfile)
        ctk.set_appearance_mode(appearances[choice])

    def change_names(self):
        def on_closing():
            popup.destroy()

        def edit():
            first_name, last_name = self.app.edit_personalities(entry1.get(), entry2.get())
            self.label_f_name.configure(text=f'Imię:  {first_name}', width=0, anchor=tk.W)
            self.label_l_name.configure(text=f'Nazwisko:  {last_name}', width=0, anchor=tk.W)
            on_closing()

        f_name = ""
        l_name = ""
        user = self.app.get_current_user()
        if user['first_name'] is not None:
            f_name = user['first_name']
        if user['last_name'] is not None:
            l_name = user['last_name']

        popup = create_popup(400, 200, 'Edycja danych', on_closing)

        label1 = ctk.CTkLabel(master=popup, text='Imię', width=0, height=0)
        label2 = ctk.CTkLabel(master=popup, text='Nazwisko', width=0, height=0)
        entry1 = ctk.CTkEntry(master=popup, corner_radius=8, placeholder_text='first name')
        entry2 = ctk.CTkEntry(master=popup, corner_radius=8, placeholder_text='last name')
        button1 = ctk.CTkButton(master=popup, corner_radius=8, text='Zatwierdź', command=edit)
        button2 = ctk.CTkButton(master=popup, corner_radius=8, text='Anuluj', command=on_closing)

        if user['first_name'] is not None:
            entry1.insert(tk.END, f_name)
        if user['last_name'] is not None:
            entry2.insert(tk.END, l_name)

        label1.place(relx=0.1, rely=0.2, anchor=tk.W)
        label2.place(relx=0.1, rely=0.4, anchor=tk.W)

        entry1.place(relx=0.525, rely=0.2, anchor=tk.W)
        entry2.place(relx=0.525, rely=0.4, anchor=tk.W)

        button1.place(relx=0.3, rely=0.8, anchor=tk.CENTER)
        button2.place(relx=0.7, rely=0.8, anchor=tk.CENTER)

    def change_password(self):
        def on_closing():
            popup.destroy()

        def change_pass():
            if entry2.get() != entry3.get():
                label = ctk.CTkLabel(master=popup, text='Hasła nie są identyczne', width=300, height=0,
                                     text_color=('red', 'red'))
                label.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
                return
            if self.app.change_password(entry1.get(), entry2.get()) != 200:
                label = ctk.CTkLabel(master=popup, text='Nie udało się zmienić hasła', width=300, height=0,
                                     text_color=('red', 'red'))
                label.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
                return
            on_closing()

        popup = create_popup(400, 250, 'Zmiana hasła', on_closing)

        label1 = ctk.CTkLabel(master=popup, text='Stare hasło', width=0, height=0)
        label2 = ctk.CTkLabel(master=popup, text='Nowe hasło', width=0, height=0)
        label3 = ctk.CTkLabel(master=popup, text='Nowe hasło', width=0, height=0)
        entry1 = ctk.CTkEntry(master=popup, corner_radius=8, placeholder_text='old password', show='*')
        entry2 = ctk.CTkEntry(master=popup, corner_radius=8, placeholder_text='new password', show='*')
        entry3 = ctk.CTkEntry(master=popup, corner_radius=8, placeholder_text='new password', show='*')
        button1 = ctk.CTkButton(master=popup, corner_radius=8, text='Zatwierdź', command=change_pass)
        button2 = ctk.CTkButton(master=popup, corner_radius=8, text='Anuluj', command=on_closing)

        label1.place(relx=0.1, rely=0.15, anchor=tk.W)
        label2.place(relx=0.1, rely=0.35, anchor=tk.W)
        label3.place(relx=0.1, rely=0.55, anchor=tk.W)

        entry1.place(relx=0.525, rely=0.15, anchor=tk.W)
        entry2.place(relx=0.525, rely=0.35, anchor=tk.W)
        entry3.place(relx=0.525, rely=0.55, anchor=tk.W)

        button1.place(relx=0.3, rely=0.85, anchor=tk.CENTER)
        button2.place(relx=0.7, rely=0.85, anchor=tk.CENTER)

    def delete_account(self):
        def on_closing():
            popup.destroy()

        def remove():
            self.app.delete_user()
            on_closing()
            self.controller.controller.on_closing()

        popup = create_popup(400, 200, 'Usuwanie konta', on_closing)

        label = ctk.CTkLabel(master=popup, text='Czy na pewno\n chcesz usunąć konto?', width=0, height=0,
                             text_font=('Arial', 16))
        button1 = ctk.CTkButton(master=popup, corner_radius=8, text='TAK', command=remove)
        button2 = ctk.CTkButton(master=popup, corner_radius=8, text='NIE', command=on_closing)

        label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        button1.place(relx=0.3, rely=0.8, anchor=tk.CENTER)
        button2.place(relx=0.7, rely=0.8, anchor=tk.CENTER)
