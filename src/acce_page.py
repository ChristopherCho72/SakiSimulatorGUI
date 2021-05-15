import tkinter as tk
import tkinter.font as tkf
import re

from PIL import ImageTk, Image
from src.utils import *


class AccePage(tk.Frame):
    def __init__(self, master, main_frame):
        super().__init__(master, bg='white')
        self.main_frame = main_frame

        self.left_page = LeftPage(self, main_frame)
        self.left_page.grid(row=0, column=0, sticky='n')
        self.right_page = RightPage(self, main_frame)
        self.right_page.grid(row=0, column=1, sticky='n')

    def update_userdata(self):
        self.left_page.update_userdata()
        self.right_page.update_userdata()

    def update_data(self, userdata):
        self.left_page.update_data(userdata)
        self.right_page.update_data(userdata)


class RightPage(tk.Frame):
    PENDANT_LIST = [('유혹', '고유 공격력'),
                    ('숲', '고유 마력'),
                    ('행운', '골드 획득량'),
                    ('천둥', '치명타 데미지'),
                    ('사신의 눈물', 'MP'),
                    ('성검', '최소 데미지'),
                    ('독수리', '고유 공격력'),
                    ('십자가', '고유 마력'),
                    ('광기', '사신타 확률(%)')]
    PENDANT_MAX = [100000, 100000, 401, 401, 2000, 20, 560000, 560000, 30]
    
    OFFERING_LIST = ["벌집", "해골", "식기", "술잔", "말발굽",
                        "고글", "촛대", "반지", "귀걸이"]
    OFFERING_MAX = [150, 150, 150, 75, 75, 150, 75, 75, 150]

    GRID_POS = {
        'pendant': (0, 0),
        'offering': (0, 4),
    }

    def __init__(self, master, main_frame):
        super().__init__(master, bg='white')

        self.main_frame = main_frame
        self.img_size = (90, 90)

        self._initialize_variables(main_frame)
        self.update_data(main_frame.userdata)

        self._render_frame()

    def _initialize_variables(self, master):
        self.imgs = {
            'pendant': {},
            'offering': {}
        }
        
        for key, _ in RightPage.PENDANT_LIST:
            img = Image.open('data/img/pendant/%s.png'%(key)).resize(self.img_size, Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            self.imgs['pendant'][key] = photo

        for key in RightPage.OFFERING_LIST:
            img = Image.open('data/img/offering/%s.png'%(key)).resize(self.img_size, Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            self.imgs['offering'][key] = photo

        self.inputs = {
            'pendant': {},
            'offering': {}
        }

        for key, _ in RightPage.PENDANT_LIST:
            strvar = tk.StringVar()
            strvar.set('')
            self.inputs['pendant'][key] = strvar
            
        for key in RightPage.OFFERING_LIST:
            strvar = tk.StringVar()
            strvar.set('')
            self.inputs['offering'][key] = strvar

    def update_userdata(self):
        for key, _ in RightPage.PENDANT_LIST:
            input_level = self.inputs['pendant'][key].get()
            try:
                level = int(input_level)
            except:
                level = 0
            self.main_frame.userdata['펜던트'][key] = level

        for key in RightPage.OFFERING_LIST:
            input_level = self.inputs['offering'][key].get()
            try:
                level = int(input_level)
            except:
                level = 0
            self.main_frame.userdata['제물'][key] = level

    def _render_frame(self):
        self._render_pendant()
        self._render_offering()

    def _render_pendant(self):
        label = tk.Label(self, text='펜던트', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
        label.grid(row=RightPage.GRID_POS['pendant'][0], column=RightPage.GRID_POS['pendant'][1], columnspan=3, sticky='we')

        for i, (key, stat) in enumerate(RightPage.PENDANT_LIST):
            img = self.imgs['pendant'][key]
            label = tk.Label(self, bg='white', image=img)
            label.grid(row=2 * (RightPage.GRID_POS['pendant'][0] + i) + 1, column=RightPage.GRID_POS['pendant'][1], rowspan=2)

            name = key + '의 펜던트' if key != '사신의 눈물' else key + ' 펜던트'
            name += ' (MAX-%d)'%(RightPage.PENDANT_MAX[i])
            label = tk.Label(self, text=name, font=tkf.Font(family="Maplestory", size=15), bg='white', fg="#202020")
            label.grid(row=2 * (RightPage.GRID_POS['pendant'][0] + i) + 1, column=RightPage.GRID_POS['pendant'][1] + 1, padx= (3, 0), sticky='w', columnspan=2)

            label = tk.Label(self, text=stat, font=tkf.Font(family="Maplestory", size=12), bg='white', fg="#202020")
            label.grid(row=2 * (RightPage.GRID_POS['pendant'][0] + i) + 2, column=RightPage.GRID_POS['pendant'][1] + 1, padx= (3, 0), sticky='w')

            entry = tk.Entry(self, width=6, textvariable=self.inputs['pendant'][key], font=tkf.Font(family="Maplestory", size=12),
                                justify='left')
            entry.bind('<Return>', self._calculate_variables)
            entry.bind('<FocusOut>', self._calculate_variables)
            entry.grid(row=2 * (RightPage.GRID_POS['pendant'][0] + i) + 2, column=RightPage.GRID_POS['pendant'][1] + 2, sticky='ew')

        label = tk.Label(self, text='', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
        label.grid(row=RightPage.GRID_POS['pendant'][0], column=RightPage.GRID_POS['pendant'][1] + 3, padx=5, sticky='we')

        pass

    def _render_offering(self):
        label = tk.Label(self, text='제물', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
        label.grid(row=RightPage.GRID_POS['offering'][0], column=RightPage.GRID_POS['offering'][1], columnspan=4, sticky='we')

        for i, key in enumerate(RightPage.OFFERING_LIST):
            img = self.imgs['offering'][key]
            label = tk.Label(self, bg='white', image=img)
            label.grid(row=2 * (RightPage.GRID_POS['offering'][0] + i) + 1, column=RightPage.GRID_POS['offering'][1], rowspan=2)

            name = '황금 ' + key
            name += ' (MAX-%d)'%(RightPage.OFFERING_MAX[i])
            label = tk.Label(self, text=name, font=tkf.Font(family="Maplestory", size=15), bg='white', fg="#202020")
            label.grid(row=2 * (RightPage.GRID_POS['offering'][0] + i) + 1, column=RightPage.GRID_POS['offering'][1] + 1, padx= (3, 0), sticky='w', columnspan=2)

            label = tk.Label(self, text='Lv. ', font=tkf.Font(family="Maplestory", size=12), bg='white', fg="#202020")
            label.grid(row=2 * (RightPage.GRID_POS['offering'][0] + i) + 2, column=RightPage.GRID_POS['offering'][1] + 1, padx= (3, 0), sticky='w')

            entry = tk.Entry(self, width=6, textvariable=self.inputs['offering'][key], font=tkf.Font(family="Maplestory", size=12),
                                justify='left')
            entry.bind('<Return>', self._calculate_variables)
            entry.bind('<FocusOut>', self._calculate_variables)
            entry.grid(row=2 * (RightPage.GRID_POS['offering'][0] + i) + 2, column=RightPage.GRID_POS['offering'][1] + 2, sticky='we')
        pass

    def _calculate_variables(self, event=None):
        self.update_userdata()
        
    def update_data(self, userdata):
        for key, _ in RightPage.PENDANT_LIST:
            self.inputs['pendant'][key].set(userdata['펜던트'][key])
            
        for key in RightPage.OFFERING_LIST:
            self.inputs['offering'][key].set(userdata['제물'][key])
            
        self._calculate_variables()

class LeftPage(tk.Frame):
    PET_LIST = ['마력', '공격력', '경험치', '골드']
    COSTUME_LIST = {
        '일반': [
            ('공격력', '마력'),
            ('체력', '공격력'),
            ('회피율', '상태이상 면역'),
            ('골드', '경험치'),
            ('치명타 데미지', '마력')
        ],
        '일반수치': {
            '공격력': (5, 10, 20, 40, 80),
            '마력': (5, 10, 20, 40, 80),
            '체력': (10, 30, 60, 80, 150),
            '회피율': (3, 6, 12, 16, 20),
            '상태이상 면역': (5, 10, 20, 30, 50),
            '골드': (5, 10, 40, 60, 100),
            '경험치': (10, 20, 40, 60, 100),
            '치명타 데미지': (10, 20, 30, 50, 80)
        },
        '고급': [
            ('공격력', '마력', '체력', '치명타 데미지'),
            ('공격력', '마력', '체력', '치명타 데미지')
        ]
    }
    COLLECTION_LIST = ['공격력', '마력']

    GRID_POS = {
        'pet': (0, 0),
        'costume': (4, 0),
        'collection': (15, 0),
        'egg': (19, 0)
    }
    
    def __init__(self, master, main_frame):
        super().__init__(master, bg='white')

        self.main_frame = main_frame
        self.img_size = (90, 90)

        self._initialize_variables(main_frame)
        self.update_data(main_frame.userdata)

        self._render_frame()
    
    def _initialize_variables(self, master):
        self.imgs = {
            'egg': None
        }

        img = Image.open('data/img/용알.png').resize(self.img_size, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.imgs['egg'] = photo

        self.inputs = {
            'pet': {},
            'pet_active': None,
            'costume_option': [],
            'costume_value': [],
            'collection': {},
            'egg': None
        }

        for key in LeftPage.PET_LIST:
            strvar = tk.StringVar()
            strvar.set('')
            self.inputs['pet'][key] = strvar

        strvar = tk.StringVar()
        strvar.set('')
        self.inputs['pet_active'] = strvar
        
        for _ in range(7):
            strvar1 = tk.StringVar()
            strvar1.set('')
            self.inputs['costume_option'].append(strvar1)
            strvar2 = tk.StringVar()
            strvar2.set('')
            self.inputs['costume_value'].append(strvar2)
            
        for key in LeftPage.COLLECTION_LIST:
            strvar = tk.StringVar()
            strvar.set('')
            self.inputs['collection'][key] = strvar
            
        strvar = tk.StringVar()
        strvar.set('')
        self.inputs['egg'] = strvar
            
    def update_userdata(self):
        for key in LeftPage.PET_LIST:
            input_level = self.inputs['pet'][key].get()
            try:
                level = int(input_level)
                self.main_frame.userdata['펫'][key] = level
            except:
                self.main_frame.userdata['펫'][key] = 0

        active_pet = self.inputs['pet_active'].get()
        if active_pet not in LeftPage.PET_LIST:
            active_pet = LeftPage.PET_LIST[0]
        self.main_frame.userdata['펫']['active'] = active_pet

        normal = ([], [])
        high = ([], [])
        for i in range(5):
            option = self.inputs['costume_option'][i].get()
            if option not in LeftPage.COSTUME_LIST['일반'][i]:
                option = LeftPage.COSTUME_LIST['일반'][i][0]
            value = self.inputs['costume_value'][i].get()
            try:
                value = int(value)
                if value not in LeftPage.COSTUME_LIST['일반수치'][option]:
                    value = LeftPage.COSTUME_LIST['일반수치'][option][0]
            except:
                value = LeftPage.COSTUME_LIST['일반수치'][option][0]

            normal[0].append(option)
            normal[1].append(value)

        self.main_frame.userdata['코스튬']['일반'] = normal[0]
        self.main_frame.userdata['코스튬']['일반수치'] = normal[1]

        for i in range(2):
            option = self.inputs['costume_option'][i+5].get()
            if option not in LeftPage.COSTUME_LIST['고급'][i]:
                option = LeftPage.COSTUME_LIST['고급'][i][0]
            value = self.inputs['costume_value'][i+5].get()
            try:
                value = int(value)
            except:
                value = 0

            high[0].append(option)
            high[1].append(value)

        self.main_frame.userdata['코스튬']['고급'] = high[0]
        self.main_frame.userdata['코스튬']['고급수치'] = high[1]

        for key in LeftPage.COLLECTION_LIST:
            input_level = self.inputs['collection'][key].get()
            try:
                level = int(input_level)
            except:
                level = 0
            self.main_frame.userdata['컬렉션'][key] = level

        input_level = self.inputs['egg'].get()
        try:
            level = int(input_level)
        except:
            level = 0
        self.main_frame.userdata['용알'] = level

    def _render_frame(self):
        self._render_pet()
        self._render_costume()
        self._render_collection()
        self._render_egg()

    def _render_pet(self):
        label = tk.Label(self, text='펫', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
        label.grid(row=LeftPage.GRID_POS['pet'][0], column=LeftPage.GRID_POS['pet'][1], columnspan=4, sticky='we')

        self.buttons = []
        
        def OnClick(i, key):
            self.inputs['pet_active'].set(key)
            for b in self.buttons:
                b.configure(bg='#202020')
            self.buttons[i].config(bg='#FF843A')

        for i, key in enumerate(LeftPage.PET_LIST):
            button = tk.Button(self, bg='#202020', fg='white', text=key, font=tkf.Font(family="Maplestory", size=12),
                                command=lambda i=i, key=key: OnClick(i, key))
            button.config(width=6)
            button.grid(row=LeftPage.GRID_POS['pet'][0] + 1, column=LeftPage.GRID_POS['pet'][1] + i, padx=3, sticky='we')

            entry = tk.Entry(self, width=4, textvariable=self.inputs['pet'][key], font=tkf.Font(family="Maplestory", size=12),
                            justify='center')
            entry.bind('<Return>', self._calculate_variables)
            entry.bind('<FocusOut>', self._calculate_variables)
            entry.grid(row=LeftPage.GRID_POS['pet'][0] + 2, column=LeftPage.GRID_POS['pet'][1] + i, padx=3, sticky='we')

            self.buttons.append(button)

        self.buttons[0].config(bg='#FF843A')

        label = tk.Label(self, text='', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
        label.grid(row=LeftPage.GRID_POS['pet'][0] + 3, column=LeftPage.GRID_POS['pet'][1], columnspan=4, pady=3, sticky='we')
        label = tk.Label(self, text='', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
        label.grid(row=LeftPage.GRID_POS['pet'][0], column=LeftPage.GRID_POS['pet'][1] + 4, padx=5, sticky='we')

    def _render_costume(self):
        label = tk.Label(self, text='코스튬', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
        label.grid(row=LeftPage.GRID_POS['costume'][0], column=LeftPage.GRID_POS['costume'][1], columnspan=4, sticky='we')

        label = tk.Label(self, text='일반', font=tkf.Font(family="Maplestory", size=15), bg='white', fg="#202020")
        label.grid(row=LeftPage.GRID_POS['costume'][0] + 1, column=LeftPage.GRID_POS['costume'][1], columnspan=4, sticky='we')

        label = tk.Label(self, text='고급', font=tkf.Font(family="Maplestory", size=15), bg='white', fg="#202020")
        label.grid(row=LeftPage.GRID_POS['costume'][0] + 7, column=LeftPage.GRID_POS['costume'][1], columnspan=4, sticky='we')

        for i in range(5):
            opt = tk.OptionMenu(self, self.inputs['costume_option'][i], *(LeftPage.COSTUME_LIST['일반'][i]))
            opt.config(width=10, font=tkf.Font(family="Maplestory", size=12), bg='white', fg="#202020", highlightthickness=0)
            opt.grid(row=LeftPage.GRID_POS['costume'][0] + 2 + i, column=LeftPage.GRID_POS['costume'][1], columnspan=2, sticky='we')

            entry = tk.Entry(self, width=4, textvariable=self.inputs['costume_value'][i], font=tkf.Font(family="Maplestory", size=12),
                            justify='center')
            entry.bind('<Return>', self._calculate_variables)
            entry.bind('<FocusOut>', self._calculate_variables)
            entry.grid(row=LeftPage.GRID_POS['costume'][0] + 2 + i, column=LeftPage.GRID_POS['costume'][1] + 2, columnspan=2, padx=3, sticky='news')

        for i in range(2):
            opt = tk.OptionMenu(self, self.inputs['costume_option'][i+5], *(LeftPage.COSTUME_LIST['고급'][i]))
            opt.config(width=10, font=tkf.Font(family="Maplestory", size=12), bg='white', fg="#202020", highlightthickness=0)
            opt.grid(row=LeftPage.GRID_POS['costume'][0] + 8 + i, column=LeftPage.GRID_POS['costume'][1], columnspan=2, sticky='we')

            entry = tk.Entry(self, width=4, textvariable=self.inputs['costume_value'][i+5], font=tkf.Font(family="Maplestory", size=12),
                            justify='center')
            entry.bind('<Return>', self._calculate_variables)
            entry.bind('<FocusOut>', self._calculate_variables)
            entry.grid(row=LeftPage.GRID_POS['costume'][0] + 8 + i, column=LeftPage.GRID_POS['costume'][1] + 2, columnspan=2, padx=3, sticky='news')

        label = tk.Label(self, text='', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
        label.grid(row=LeftPage.GRID_POS['costume'][0] + 10, column=LeftPage.GRID_POS['costume'][1], columnspan=4, pady=3, sticky='we')

    def _render_collection(self):
        label = tk.Label(self, text='컬렉션', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
        label.grid(row=LeftPage.GRID_POS['collection'][0], column=LeftPage.GRID_POS['collection'][1], columnspan=4, sticky='we')

        for i, key in enumerate(LeftPage.COLLECTION_LIST):
            label = tk.Label(self, text=key, font=tkf.Font(family="Maplestory", size=12), bg='white', fg="#202020")
            label.grid(row=LeftPage.GRID_POS['collection'][0] + 1 + i, column=LeftPage.GRID_POS['collection'][1], columnspan=2, sticky='we')

            entry = tk.Entry(self, width=4, textvariable=self.inputs['collection'][key], font=tkf.Font(family="Maplestory", size=12),
                            justify='center')
            entry.bind('<Return>', self._calculate_variables)
            entry.bind('<FocusOut>', self._calculate_variables)
            entry.grid(row=LeftPage.GRID_POS['collection'][0] + 1 + i, column=LeftPage.GRID_POS['collection'][1] + 2, columnspan=2, padx=3, sticky='news')

        label = tk.Label(self, text='', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
        label.grid(row=LeftPage.GRID_POS['collection'][0] + 3, column=LeftPage.GRID_POS['collection'][1], columnspan=4, pady=3, sticky='we')

    def _render_egg(self):
        label = tk.Label(self, text='용알', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
        label.grid(row=LeftPage.GRID_POS['egg'][0], column=LeftPage.GRID_POS['egg'][1], columnspan=4, sticky='we')
        
        img = self.imgs['egg']
        label = tk.Label(self, bg='white', image=img)
        label.grid(row=LeftPage.GRID_POS['egg'][0] + 1, column=LeftPage.GRID_POS['egg'][1], columnspan=2)

        entry = tk.Entry(self, width=4, textvariable=self.inputs['egg'], font=tkf.Font(family="Maplestory", size=12),
                            justify='center')
        entry.bind('<Return>', self._calculate_variables)
        entry.bind('<FocusOut>', self._calculate_variables)
        entry.grid(row=LeftPage.GRID_POS['egg'][0] + 1, column=LeftPage.GRID_POS['egg'][1] + 2, columnspan=2, padx=3, sticky='ew')

    def _calculate_variables(self, event=None):
        self.update_userdata()
        
    def update_data(self, userdata):
        for key in LeftPage.PET_LIST:
            self.inputs['pet'][key].set(userdata['펫'][key])

        self.inputs['pet_active'].set(userdata['펫']['active'])

        for i in range(5):
            self.inputs['costume_option'][i].set(userdata['코스튬']['일반'][i])
            self.inputs['costume_value'][i].set(userdata['코스튬']['일반수치'][i])
            
        for i in range(2):
            self.inputs['costume_option'][i+5].set(userdata['코스튬']['고급'][i])
            self.inputs['costume_value'][i+5].set(userdata['코스튬']['고급수치'][i])
            
        for key in LeftPage.COLLECTION_LIST:
            self.inputs['collection'][key].set(userdata['컬렉션'][key])

        self.inputs['egg'].set(userdata['용알'])
            
        self._calculate_variables()