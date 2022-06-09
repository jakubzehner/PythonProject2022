import tkinter as tk
import tkinter.messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
from parser import *
from constants import *


def create_button(master, width=200, height=40, corner_radius=8, text_font=LS_ENTRY_FONT, command=None, relx=0.5,
                  rely=0.5, anchor=tk.CENTER, text=None):
    button = ctk.CTkButton(master=master, text=text, corner_radius=corner_radius, width=width, height=height,
                           command=command, text_font=text_font)
    button.place(relx=relx, rely=rely, anchor=anchor)
    return button


def create_entry(master, corner_radius=8, width=200, height=40, placeholder_text=None, text_font=LS_ENTRY_FONT,
                 relx=0.5, rely=0.5, anchor=tk.CENTER, show=None):
    entry = ctk.CTkEntry(master=master, corner_radius=corner_radius, width=width, height=height, show=show,
                         placeholder_text=placeholder_text, text_font=text_font)
    entry.place(relx=relx, rely=rely, anchor=anchor)
    return entry


def create_label(master, width=200, height=40, text_font=LS_LABEL_FONT, relx=0.5, rely=0.5, anchor=tk.E, text=None):
    label = ctk.CTkLabel(master=master, width=width, height=height, text=text, text_font=text_font)
    label.place(relx=relx, rely=rely, anchor=anchor)
    return label


# Klasa zawierająca widok ekranu logowania
class LoginMenu(ctk.CTkFrame):
    def __init__(self, parent, controller, app):
        ctk.CTkFrame.__init__(self, parent, width=parent.winfo_width(), height=parent.winfo_height(),
                              fg_color=COLOR_APP_BACKGROUND)
        self.app = app
        self.controller = controller

        image = Image.open(PATH + '\\img\\login_background.png').resize((WIDTH, HEIGHT))
        self.bg_image = ImageTk.PhotoImage(image)

        # background image
        self.image_label = tk.Label(master=self, image=self.bg_image)
        self.image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # content frame
        self.frame = ctk.CTkFrame(master=self, width=300, height=HEIGHT, corner_radius=0, fg_color=COLOR_APP_FOREGROUND)
        self.frame.place(relx=1, rely=0.5, anchor=tk.E)

        self.f: ctk.CTkFrame | None = None
        self.show_frame(Login)

    def show_frame(self, cont):
        for child in self.frame.winfo_children():
            child.destroy()

        if cont in [Login, Register, Register_Success]:
            self.f = cont(self.frame, self, self.app)


class Login:
    def __init__(self, parent, controller, app):
        self.app = app
        self.controller = controller

        self.label_title = create_label(parent, height=60, text='LOGOWANIE', rely=0.17, anchor=tk.CENTER,
                                        text_font=LS_TITLE_FONT)

        # Username
        self.label_login = create_label(parent, text='Nazwa użytkownika', relx=0.7, rely=0.33)
        self.entry_login = create_entry(parent, placeholder_text='username', rely=0.385)

        # Password
        self.label_pass = create_label(parent, text='Hasło', relx=0.56, rely=0.48)
        self.entry_pass = create_entry(parent, placeholder_text='password', show='*', rely=0.535)

        # Incorrect
        self.label_incorrect = ctk.CTkLabel(master=parent, width=200, text_font=('Arial', 10), text_color='red',
                                            text='Nazwa użytkownika, bądź hasło\n jest nieprawidłowa')

        # Button
        self.button_login = create_button(parent, text='Zaloguj się', command=self.button_event, rely=0.72)

        # Register
        self.button_register = ctk.CTkButton(master=parent, fg_color=parent.fg_color, hover_color=parent.fg_color,
                                             corner_radius=0, hover=True, text='Nie masz konta? Zarejestruj się',
                                             text_font=('Arial', 10), command=lambda: controller.show_frame(Register))
        self.button_register.place(relx=0.5, rely=0.93, anchor=tkinter.CENTER)

    def button_event(self):
        if self.app.logging(self.entry_login.get(), self.entry_pass.get()) == 200:
            self.controller.controller.create_app_gui()
            return

        self.label_incorrect.place(relx=0.5, rely=0.635, anchor=tk.CENTER)


class Register:
    def __init__(self, parent, controller, app):
        self.app = app
        self.controller = controller

        self.label_title = create_label(parent, height=60, text='REJESTRACJA', rely=0.17, anchor=tk.CENTER,
                                        text_font=LS_TITLE_FONT)

        # Username
        self.label_login = create_label(parent, text='Nazwa użytkownika', relx=0.7, rely=0.26, height=0)
        self.entry_login = create_entry(parent, placeholder_text='username', rely=0.315)

        # Password
        self.label_pass = create_label(parent, text='Hasło', relx=0.56, rely=0.38, height=0)
        self.entry_pass = create_entry(parent, placeholder_text='password', show='*', rely=0.435)

        # Password 2
        self.label_pass_2 = create_label(parent, text='Powtórz hasło', relx=0.65, rely=0.5, height=0)
        self.entry_pass_2 = create_entry(parent, placeholder_text='password', show='*', rely=0.555)

        # Incorrect
        self.label_incorrect = ctk.CTkLabel(master=parent, width=200, text_font=('Arial', 10), text_color='red')

        # Button
        self.button_register = create_button(parent, text='Zarejestruj się', command=self.button_event, rely=0.72)

        # Register
        self.button_login = ctk.CTkButton(master=parent, fg_color=parent.fg_color, hover_color=parent.fg_color,
                                          corner_radius=0, hover=True, text='Masz już konto? Zaloguj się',
                                          text_font=('Arial', 10), command=lambda: controller.show_frame(Login))
        self.button_login.place(relx=0.5, rely=0.93, anchor=tkinter.CENTER)

    def button_event(self):
        if not self.entry_pass.get() == self.entry_pass_2.get():
            self.label_incorrect.configure(text='Podane hasła muszą być identyczne')
            self.label_incorrect.place(relx=0.5, rely=0.645, anchor=tk.CENTER)
            return

        if self.app.register(self.entry_login.get(), self.entry_pass.get()) != 200:
            self.label_incorrect.configure(text='Podana nazwa już istnieje')
            self.label_incorrect.place(relx=0.5, rely=0.645, anchor=tk.CENTER)
            return

        self.controller.show_frame(Register_Success)


class Register_Success(ctk.CTkFrame):
    def __init__(self, parent, controller, app):
        ctk.CTkFrame.__init__(self, parent, bg_color=parent.bg_color, fg_color=parent.fg_color)
        self.app = app
        self.controller = controller

        self.label_title = create_label(parent, height=60, text='Udało się\nzałożyć konto', rely=0.37, anchor=tk.CENTER,
                                        text_font=LS_TITLE_FONT)

        self.button_register = create_button(parent, text='OK', command=self.button_event, rely=0.72)

    def button_event(self):
        self.controller.show_frame(Login)
