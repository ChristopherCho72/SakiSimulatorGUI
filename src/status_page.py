import tkinter as tk
import tkinter.font as tkf
import re

from PIL import ImageTk, Image
from utils import *

class StatusPage(tk.Frame):
    STAT_LIST = [('공격력', '공격력', '공격력 증가'),
                    ('마력', '마력', '마력 증가'),
                    ('HP 증가', 'HP', 'HP 증가'),
                    ('치명타 확률 증가', '치명타 확률', '치명타 확률 증가'),
                    ('치명타 데미지 증가', '치명타 데미지', '치명타 데미지 증가(+)'),
                    ('MP 증가', 'MP', 'MP 증가'),
                    ('사신타 확률 증가', '사신타 확률', '사신타 확률 증가'),
                    ('사신타 데미지 증가', '사신타 데미지', '사신타 데미지 증가')]
    STAT_MAX = [float('inf'), float('inf'), 100000, 30, 550, 1020, 20, 40]

    ACTIVE_LIST = ['사신의낫', '포터', '홀리 실드', '홀리 스나이퍼', '홀리 팅글',
                    '라이트닝샷', '라이트닝 마그넷', '스카이 라이트닝', '소울 파이어', '점화',
                    '미스틱블래스', '프리즘 스모크', '홀리 붐', '메테오 오리지널', '천계의 계약']
    ACTIVE_MAX = [(140, 6), 1, 30, 30, 50,
                    50, 50, 50, 50, 50,
                    30, 50, (100, 5), 50, 50]

    PASSIVE_LIST = ['주피터의 지혜', '넵튠의 지혜', '불칸의 지혜', '아폴로의 지혜', '사신의 의무',
                    '지상의 기도', '영웅의 기운', '미네르바의 지혜', '전설의 주문', '블레싱',
                    '플루토의 낫', '플루토의 보주', '플루토의 옷', '만해', '타나토스의 손길',
                    '타나토스의 분노']
    PASSIVE_MAX = [300, 250, 150, 100, 100,
                    100, 100, 10, 30, 30,
                    5000, 5000, 5000, 50, 1000,
                    1000]

    GRID_COL_POS = [0, 3, 9]
    
    def __init__(self, master, main_frame):
        super().__init__(master, bg='white')

        self.main_frame = main_frame
        self.img_size = (90, 90)

        self._initialize_variables(main_frame)
        self.update_data(main_frame.userdata)

        self._render_frame()
    
    def _initialize_variables(self, master):
        self.imgs = {}
        for key, filename, _ in StatusPage.STAT_LIST:
            img = Image.open('data/img/stat/%s.png'%(filename)).resize(self.img_size, Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            self.imgs[key] = photo

        for key in StatusPage.PASSIVE_LIST + StatusPage.ACTIVE_LIST:
            img = Image.open('data/img/skill/%s.png'%(key)).resize(self.img_size, Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            self.imgs[key] = photo

        self.levels = {}
        for key in [k for k, _, _ in StatusPage.STAT_LIST] + StatusPage.PASSIVE_LIST + StatusPage.ACTIVE_LIST:
            if key in ['사신의낫', '홀리 붐']:
                strvar1 = tk.StringVar()
                strvar1.set('')
                strvar2 = tk.StringVar()
                strvar2.set('')
                self.levels[key] = [strvar1, strvar2]
            else:
                strvar = tk.StringVar()
                strvar.set('')
                self.levels[key] = strvar
    
    def update_userdata(self):
        for key, _, _ in StatusPage.STAT_LIST:
            input_level = self.levels[key].get()
            try:
                level = int(input_level)
                self.main_frame.userdata['능력치'][key] = level
            except:
                self.main_frame.userdata['능력치'][key] = 0

        for key in StatusPage.PASSIVE_LIST:
            input_level = self.levels[key].get()
            try:
                level = int(input_level)
                self.main_frame.userdata['스킬-패시브'][key] = level
            except:
                self.main_frame.userdata['스킬-패시브'][key] = 0
            
        for key in StatusPage.ACTIVE_LIST:
            if key in ['사신의낫', '홀리 붐']:
                input_level1 = self.levels[key][0].get()
                input_level2 = self.levels[key][1].get()
                try:
                    level1 = int(input_level1)
                    level2 = int(input_level2)
                    self.main_frame.userdata['스킬-액티브'][key] = [level1, level2]
                except:
                    self.main_frame.userdata['스킬-액티브'][key] = [0, 0]
            else:
                input_level = self.levels[key].get()
                try:
                    level = int(input_level)
                    self.main_frame.userdata['스킬-액티브'][key] = level
                except:
                    self.main_frame.userdata['스킬-액티브'][key] = 0
        

    def _render_frame(self):
        self._render_image()
        self._render_text()

    def _render_image(self):
        label = tk.Label(self, text='능력치', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
        label.grid(row=0, column=StatusPage.GRID_COL_POS[0], columnspan=2, sticky='we')
        
        label = tk.Label(self, text='', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
        label.grid(row=0, column=StatusPage.GRID_COL_POS[1] - 1, sticky='we', padx=5)

        label = tk.Label(self, text='액티브 스킬', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
        label.grid(row=0, column=StatusPage.GRID_COL_POS[1], columnspan=5, sticky='we')
        
        label = tk.Label(self, text='', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
        label.grid(row=0, column=StatusPage.GRID_COL_POS[2] - 1, sticky='we', padx=5)

        label = tk.Label(self, text='패시브 스킬', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
        label.grid(row=0, column=StatusPage.GRID_COL_POS[2], columnspan=3, sticky='we')

        for i, (key, _, _) in enumerate(StatusPage.STAT_LIST):
            img = self.imgs[key]
            label = tk.Label(self, bg='white', image=img)
            label.grid(row=2 * i + 1, column=StatusPage.GRID_COL_POS[0], rowspan=2, padx=3)

        for i, key in enumerate(StatusPage.ACTIVE_LIST):
            img = self.imgs[key]
            label = tk.Label(self, bg='white', image=img)
            label.grid(row=2 * i + 1, column=StatusPage.GRID_COL_POS[1], rowspan=2, padx=3)

        for i, key in enumerate(StatusPage.PASSIVE_LIST):
            img = self.imgs[key]
            label = tk.Label(self, bg='white', image=img)
            label.grid(row=2 * i + 1, column=StatusPage.GRID_COL_POS[2], rowspan=2, padx=3)

    def _render_text(self):
        for i, (key, _, text) in enumerate(StatusPage.STAT_LIST):
            text = text + ' (MAX-%d)'%(StatusPage.STAT_MAX[i]) if i not in [0, 1] else text
            label = tk.Label(self, text=text, font=tkf.Font(family="Maplestory", size=15), bg='white', fg="#202020")
            label.grid(row=2 * i + 1, column=StatusPage.GRID_COL_POS[0] + 1, sticky='w')
            
            entry = tk.Entry(self, width=8, textvariable=self.levels[key], font=tkf.Font(family="Maplestory", size=15),
                                justify='left')
            entry.bind('<Return>', self._calculate_variables)
            entry.bind('<FocusOut>', self._calculate_variables)
            entry.grid(row=2 * i + 2, column=StatusPage.GRID_COL_POS[0] + 1, sticky='w')

        for i, key in enumerate(StatusPage.ACTIVE_LIST):
            if key in ['사신의낫', '홀리 붐']:
                label = tk.Label(self, text=key, font=tkf.Font(family="Maplestory", size=15), bg='white', fg="#202020")
                label.grid(row=2 * i + 1, column=StatusPage.GRID_COL_POS[1] + 1, columnspan=4, sticky='w')

                label = tk.Label(self, text='스킬 레벨: ', font=tkf.Font(family="Maplestory", size=15), bg='white', fg="#202020")
                label.grid(row=2 * i + 2, column=StatusPage.GRID_COL_POS[1] + 1, sticky='w')
                
                label = tk.Label(self, text='각성 회차: ', font=tkf.Font(family="Maplestory", size=15), bg='white', fg="#202020")
                label.grid(row=2 * i + 2, column=StatusPage.GRID_COL_POS[1] + 3, sticky='w', padx=(5,0))
                
                entry = tk.Entry(self, width=4, textvariable=self.levels[key][0], font=tkf.Font(family="Maplestory", size=15),
                                    justify='left')
                entry.bind('<Return>', self._calculate_variables)
                entry.bind('<FocusOut>', self._calculate_variables)
                entry.grid(row=2 * i + 2, column=StatusPage.GRID_COL_POS[1] + 2, sticky='w')

                entry = tk.Entry(self, width=4, textvariable=self.levels[key][1], font=tkf.Font(family="Maplestory", size=15),
                                    justify='left')
                entry.bind('<Return>', self._calculate_variables)
                entry.bind('<FocusOut>', self._calculate_variables)
                entry.grid(row=2 * i + 2, column=StatusPage.GRID_COL_POS[1] + 4, sticky='w')

            else:
                label = tk.Label(self, text=key, font=tkf.Font(family="Maplestory", size=15), bg='white', fg="#202020")
                label.grid(row=2 * i + 1, column=StatusPage.GRID_COL_POS[1] + 1, columnspan=4, sticky='w')

                label = tk.Label(self, text='스킬 레벨: ', font=tkf.Font(family="Maplestory", size=15), bg='white', fg="#202020")
                label.grid(row=2 * i + 2, column=StatusPage.GRID_COL_POS[1] + 1, sticky='w')
                
                entry = tk.Entry(self, width=4, textvariable=self.levels[key], font=tkf.Font(family="Maplestory", size=15),
                                    justify='left')
                entry.bind('<Return>', self._calculate_variables)
                entry.bind('<FocusOut>', self._calculate_variables)
                entry.grid(row=2 * i + 2, column=StatusPage.GRID_COL_POS[1] + 2, sticky='w')

        for i, key in enumerate(StatusPage.PASSIVE_LIST):
            text = key + ' (MAX-%d)'%(StatusPage.PASSIVE_MAX[i])
            label = tk.Label(self, text=text, font=tkf.Font(family="Maplestory", size=15), bg='white', fg="#202020")
            label.grid(row=2 * i + 1, column=StatusPage.GRID_COL_POS[2] + 1, columnspan=2, sticky='w')

            label = tk.Label(self, text='스킬 레벨: ', font=tkf.Font(family="Maplestory", size=15), bg='white', fg="#202020")
            label.grid(row=2 * i + 2, column=StatusPage.GRID_COL_POS[2] + 1, sticky='w')
            
            entry = tk.Entry(self, width=5, textvariable=self.levels[key], font=tkf.Font(family="Maplestory", size=15),
                                justify='left')
            entry.bind('<Return>', self._calculate_variables)
            entry.bind('<FocusOut>', self._calculate_variables)
            entry.grid(row=2 * i + 2, column=StatusPage.GRID_COL_POS[2] + 2, sticky='w')
    
    def _calculate_variables(self, event=None):
        self.update_userdata()
        
    def update_data(self, userdata):
        for key, _, _ in StatusPage.STAT_LIST:
            self.levels[key].set(userdata['능력치'][key])

        for key in StatusPage.ACTIVE_LIST:
            if key in ['사신의낫', '홀리 붐']:
                self.levels[key][0].set(userdata['스킬-액티브'][key][0])
                self.levels[key][1].set(userdata['스킬-액티브'][key][1])
            else:
                self.levels[key].set(userdata['스킬-액티브'][key])

        for key in StatusPage.PASSIVE_LIST:
            self.levels[key].set(userdata['스킬-패시브'][key])

        self._calculate_variables()