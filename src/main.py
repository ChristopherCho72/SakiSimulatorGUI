import tkinter as tk
import tkinter.font as tkf
import json
import math
import os
import csv
import re

from tkinter import filedialog
from PIL import ImageTk, Image

from utils import *
from main_page import MainPage
from weapon_page import WeaponPage
from spirit_page import SpiritPage

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.window_width = 1600
        self.window_height = 900

        self._initialize_window()
        self.userdata = initial_load_data()

        self.upper_bar = UpperBar(self)
        self.main_frame = None
        self.upper_bar.grid(row=0, column=0)
        self.switch_frame(MainPage)

    def _initialize_window(self):
        self.title('Saki Simulator')
        self.geometry('%dx%d'%(self.window_width,self.window_height))
        self.resizable(True, True)
        self.configure(bg='white')
        self._setup_menu()

    def _setup_menu(self):
        menu = tk.Menu(self)

        menu_file = tk.Menu(menu, tearoff=0)
        menu_file.add_command(label="Load file", command=self._load_file)
        menu_file.add_command(label="Save file", command=self._save_file)

        menu.add_cascade(label="File", menu=menu_file)

        self.config(menu=menu)

    def _load_file(self):
        fname = filedialog.askopenfilename(title="Load configuration file",
                                                filetypes=[("JSON 파일", "*.json")],
                                                initialdir="data/")

        if fname:
            self.userdata = load_data(fname)
            self.main_frame.update_data(self.userdata)

    def _save_file(self):
        fname = filedialog.asksaveasfilename(title="Save configuration file",
                                                filetypes=[("JSON 파일", "*.json")],
                                                defaultextension=[("JSON 파일", "*.json")],
                                                initialdir="data/",
                                                initialfile="userdata.json")

        if fname:
            save_data(fname, self.userdata)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.main_frame is not None:
            self.main_frame.update_userdata()
            self.main_frame.destroy()
        self.main_frame = new_frame
        self.main_frame.grid(row=1, column=0)

class UpperBar(tk.Frame):
    def __init__(self, master):
        super().__init__(bg='white')
        self._render_frame(master)

    def _render_frame(self, master):
        self.pages = {
            '내 능력치 정보': [MainPage, None],
            '능력치 입력': [MainPage, None],
            '액티브/패시브 스킬 입력': [MainPage, None],
            '장비 레벨 입력': [WeaponPage, None],
            '정령 레벨 입력': [SpiritPage, None],
            '펫, 펜던트, 코스튬 입력': [MainPage, None],
            '제물, 컬렉션, 용알 입력': [MainPage, None],
        }

        for i, key in enumerate(self.pages.keys()):
            self.pages[key][1] = tk.Button(self, text=key, font=tkf.Font(family="Maplestory", size=15), 
                                bg='white', command=lambda key=key: master.switch_frame(self.pages[key][0]))
            self.pages[key][1].grid(row=0, column=i, padx=5, pady=5, sticky='nesw')
        
        canvas = tk.Canvas(self, bg='white', bd=0, width=master.window_width, height=10, highlightthickness=0)
        canvas.create_line(1, 3, master.window_width-1, 3, width=2, fill='gray')
        canvas.grid(row=1, column=0, columnspan=len(self.pages))

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()