import tkinter as tk
import tkinter.font as tkf
import PIL
import re

from PIL import ImageTk, Image
from utils import *

class SpiritPage(tk.Frame):
    GRID_POS = {
        '일반': (0, 1),
        '고급': (0, 6),
        '영웅': (7, 1),
        '전설': (7, 6),
    }

    def __init__(self, master):
        super().__init__(bg='white')

        self.img_size = (90, 90)
        self._initialize_variables(master)
        self.update_data(master.userdata)
        self.master = master

        self._render_frame()

    def _initialize_variables(self, master):
        self.imgs = {}
        for key in SpiritPage.GRID_POS.keys():
            self.imgs[key] = []
            for i in reversed(range(1, 5)):
                img = PIL.Image.open('data/img/spirit/%s%d.png'%(key, i)).resize(self.img_size, PIL.Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(img)
                self.imgs[key].append(photo)

        self.levels = {}
        for key in SpiritPage.GRID_POS.keys():
            self.levels[key] = []
            for i in range(4):
                strvar = tk.StringVar()
                strvar.set('')
                self.levels[key].append(strvar)

    def _render_frame(self):
        self._render_image()
        self._render_context()
        self._render_level_slot()

    def _render_image(self):
        for key in SpiritPage.GRID_POS.keys():
            for i in range(4):
                img = self.imgs[key][i]
                label = tk.Label(self, bg='white', image=img)
                r_offset, c_offset = SpiritPage.GRID_POS[key]
                label.grid(row=r_offset, column=c_offset + i)

        label = tk.Label(self, bg='white', text='')
        label.grid(row=6, column=0, columnspan=10, pady=3)

        label = tk.Label(self, bg='white', text='')
        label.grid(row=0, column=5, rowspan=6, padx=3)

    def _render_context(self):
        label_texts = ['레벨 (미 보유시 -1)', '현재 필요한 업스톤&전리품', '풀업글 시 필요 재료', '현재 장착효과(체/공/마/치)', '현재 보유효과(체/공/마/치)']
        for i, t in enumerate(label_texts):
            label = tk.Label(self, text=t, font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
            label.grid(row=i+1, column=0, sticky='e')

        label_texts = ['레벨 (미 보유시 -1)', '현재 필요한 업스톤&전리품', '풀업글 시 필요 재료', '현재 장착효과(체/공/마/치)', '현재 장착효과(영1-공&마)', '현재 보유효과(체/공/마/치)', '최종 치명타 증가(+)']
        for i, t in enumerate(label_texts):
            label = tk.Label(self, text=t, font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
            label.grid(row=i+8, column=0, sticky='e')

    def _render_level_slot(self):
        for key in SpiritPage.GRID_POS.keys():
            for i in range(4):
                vcmd = (self.register(self._validate_level), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
                entry = tk.Entry(self, width=10, textvariable=self.levels[key][i], font=tkf.Font(family="Maplestory", size=10),
                                    justify='right', validate = 'key', validatecommand = vcmd)
                entry.bind('<Return>', self._calculate_variables)
                entry.bind('<FocusOut>', self._calculate_variables)
                r_offset, c_offset = SpiritPage.GRID_POS[key]
                entry.grid(row=r_offset+1, column=c_offset + i, sticky='we')

    def update_data(self, userdata):
        pass

    def _calculate_variables(self, event=None):
        pass

    
    def _validate_level(self, action, index, value_if_allowed,
                    prior_value, text, validation_type, trigger_type, widget_name):
        only_digit = re.match(r'^-$|^-1$|^[0-9]*$', value_if_allowed) is not None 
        if not only_digit:
            return False

        if value_if_allowed:
            if value_if_allowed == '-':
                return True
            
            val = int(value_if_allowed)
            right_range = (val in range(201)) or (val == -1)

            return right_range
        else:
            return True