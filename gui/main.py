import tkinter
import login_gui
import app_gui
import customtkinter as ctk
from gui.app import app
from parser import *
from constants import APP_NAME, WIDTH, HEIGHT

ctk.set_appearance_mode(cfg['appearance_mode'])
ctk.set_default_color_theme(cfg['color_theme'])

ctk.deactivate_automatic_dpi_awareness()


class Gui(ctk.CTk):

    def __init__(self, app=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app

        self.title(APP_NAME)
        self.geometry(f'{WIDTH}x{HEIGHT}+{cfg["app_pos_x"]}+{cfg["app_pos_y"]}')
        self.minsize(WIDTH, HEIGHT)
        self.maxsize(WIDTH, HEIGHT)
        self.resizable(False, False)

        self.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.view: ctk.CTkFrame | None = None
        self.create_login_screen()

    def create_login_screen(self):
        self.view = login_gui.LoginMenu(self, self, self.app)
        self.view.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    def create_app_gui(self):
        self.view.destroy()
        self.app.perform_planned_entries()
        self.view = app_gui.App(self, self, self.app)
        self.view.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    def on_closing(self, event=0):
        config['DEFAULT']['app_pos_x'] = str(self.winfo_x())
        config['DEFAULT']['app_pos_y'] = str(self.winfo_y())

        with open('config.conf', 'w') as configfile:
            config.write(configfile)

        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == '__main__':
    app = app.App()
    gui = Gui(app)
    gui.start()
