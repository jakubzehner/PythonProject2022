import tkinter as tk
import customtkinter as ctk
from entry import Entry
from home import Home
from planned_entry import PlannedEntry
from goal import Goal
from settings import Settings
from util import load_image, ImageTk
from constants import *


def create_menu_button(master, text, command, image, column):
    frame = ctk.CTkFrame(master=master, width=WIDTH // 5, height=MENU_HEIGHT, corner_radius=0)
    frame.grid(row=0, column=column, sticky='nswe')
    button = ctk.CTkButton(master=frame, width=WIDTH // 5, height=MENU_HEIGHT, fg_color=COLOR_UNCLICKED_MENU_BUTTON,
                           image=image, text_font=FONT, corner_radius=0, text=text, command=command)
    button.grid(sticky='nswe', padx=1)
    return frame, button


class App(ctk.CTkFrame):
    def __init__(self, parent, controller, app):
        ctk.CTkFrame.__init__(self, parent, width=parent.winfo_width(), height=parent.winfo_height(),
                              fg_color=COLOR_APP_BACKGROUND)
        self.app = app
        self.controller = controller

        # images
        self.img_home, self.img_entry, self.img_p_entry, self.img_goal, self.img_settings = self.load_images()
        # kids images
        self.img_watch, self.img_remove, self.img_edit, self.img_prev, self.img_next = self.load_kids_images()

        # configure layout and create frames
        self.grid_columnconfigure(0, minsize=WIDTH)
        self.grid_rowconfigure(0, minsize=MENU_HEIGHT)
        self.grid_rowconfigure(1, minsize=HEIGHT - MENU_HEIGHT)

        self.frame_upper = ctk.CTkFrame(master=self, height=MENU_HEIGHT, width=WIDTH, corner_radius=0)
        self.frame_upper.grid(row=0, column=0, sticky='nsew')

        self.frame_lower = ctk.CTkFrame(master=self, height=HEIGHT - MENU_HEIGHT, width=WIDTH, corner_radius=0)
        self.frame_lower.grid(row=1, column=0, sticky='nsew')

        self.frame = ctk.CTkFrame(master=self.frame_lower, corner_radius=0, padx=5, pady=5,
                                  fg_color=COLOR_APP_BACKGROUND)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # frame_upper
        self.frame_upper.grid_columnconfigure(4)
        self.frame_upper.grid_rowconfigure(0)

        # --home button
        self.frame_upper_home, self.button_home = create_menu_button(self.frame_upper, 'Strona główna',
                                                                     lambda: self.show_frame(Home), self.img_home, 0)
        # --entry button
        self.frame_upper_entry, self.button_entry = create_menu_button(self.frame_upper, 'Wpisy',
                                                                       lambda: self.show_frame(Entry), self.img_entry,
                                                                       1)
        # --planned entry button
        self.frame_upper_p_entry, self.button_p_entry = create_menu_button(self.frame_upper, 'Zaplanowane',
                                                                           lambda: self.show_frame(PlannedEntry),
                                                                           self.img_entry, 2)
        # --goal button
        self.frame_upper_goal, self.button_goal = create_menu_button(self.frame_upper, 'Cele',
                                                                     lambda: self.show_frame(Goal), self.img_goal, 3)
        # --settings button
        self.frame_upper_settings, self.button_settings = create_menu_button(self.frame_upper, 'Ustawienia',
                                                                             lambda: self.show_frame(Settings),
                                                                             self.img_settings, 4)
        # frame (lower - main)
        self.f: ctk.CTkFrame | None = None
        self.show_frame(Home)

    def show_frame(self, cont):
        for child in self.frame.winfo_children():
            child.destroy()

        buttons = {Home: self.button_home, Entry: self.button_entry, PlannedEntry: self.button_p_entry,
                   Goal: self.button_goal, Settings: self.button_settings}

        for button in buttons.values():
            button.configure(fg_color=COLOR_UNCLICKED_MENU_BUTTON, state=tk.NORMAL)
            button.hover = True

        if cont in buttons:
            self.f = cont(self.frame, self, self.app)
            buttons[cont].configure(fg_color=COLOR_CLICKED_MENU_BUTTON, state=tk.DISABLED)
            buttons[cont].hover = False

    def load_images(self):
        img_home = load_image('\\img\\home_white.png', IMAGE_SIZE)
        img_entry = load_image('\\img\\entry_white.png', IMAGE_SIZE)
        img_p_entry = load_image('\\img\\p_entry_white.png', IMAGE_SIZE)
        img_goal = load_image('\\img\\goal_white.png', IMAGE_SIZE)
        img_settings = load_image('\\img\\settings_white.png', IMAGE_SIZE)
        return img_home, img_entry, img_p_entry, img_goal, img_settings

    def load_kids_images(self):
        img_watch = load_image('\\img\\watch.png', MEDIUM_IMAGE_SIZE)
        img_remove = load_image('\\img\\remove.png', MEDIUM_IMAGE_SIZE)
        img_edit = load_image('\\img\\edit.png', MEDIUM_IMAGE_SIZE)
        img_prev = load_image('\\img\\prev.png', LARGE_IMAGE_SIZE)
        img_next = load_image('\\img\\next.png', LARGE_IMAGE_SIZE)
        return img_watch, img_remove, img_edit, img_prev, img_next
