import tkinter as tk
import tkinter.font as tkf
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
    HAVE_MOUNT_2_EFFECT = {
        '영웅': [3],
        '전설': [3]
    }
    SPIRIT_EFFECT = ['HP 증가', '공격력', '마력', '치명타 데미지']
    STAT_KEYS = {
        '체력 증가율': 'HP 증가',
        '물공 증가': '공격력',
        '마공 증가': '마력',
        '치명타 데미지': '치명타 데미지',
        '최종 치뎀 증가(*)': '치명타 데미지 곱'
    }

    def __init__(self, master, main_frame):
        super().__init__(bg='white')

        self.main_frame = main_frame
        self.img_size = (90, 90)
        self._initialize_variables(main_frame)
        self.update_data(main_frame.userdata)

        self._render_frame()

    def _initialize_variables(self, master):
        self.imgs = {}
        for key in SpiritPage.GRID_POS.keys():
            self.imgs[key] = []
            for i in reversed(range(1, 5)):
                img = Image.open('data/img/spirit/%s%d.png'%(key, i)).resize(self.img_size, Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(img)
                self.imgs[key].append(photo)

        self.levels = {}
        for key in SpiritPage.GRID_POS.keys():
            self.levels[key] = []
            for i in range(4):
                strvar = tk.StringVar()
                strvar.set('')
                self.levels[key].append(strvar)
            
        self.req_ups = {}
        for key in SpiritPage.GRID_POS.keys():
            self.req_ups[key] = []
            for i in range(4):
                strvar = tk.StringVar()
                strvar.set('-')
                self.req_ups[key].append(strvar)

        self.full_req_ups = {}
        for key in SpiritPage.GRID_POS.keys():
            self.full_req_ups[key] = []
            for i in range(4):
                strvar = tk.StringVar()
                strvar.set('-')
                self.full_req_ups[key].append(strvar)

        self.mount_effect = {}
        for key in SpiritPage.GRID_POS.keys():
            self.mount_effect[key] = []
            for i in range(4):
                strvar = tk.StringVar()
                strvar.set('-')
                self.mount_effect[key].append(strvar)

        self.mount_spirit_1_effect = {}
        for key in SpiritPage.GRID_POS.keys():
            self.mount_spirit_1_effect[key] = []
            for i in range(4):
                strvar = tk.StringVar()
                strvar.set('-')
                self.mount_spirit_1_effect[key].append(strvar)

        self.own_effect = {}
        for key in SpiritPage.GRID_POS.keys():
            self.own_effect[key] = []
            for i in range(4):
                strvar = tk.StringVar()
                strvar.set('-')
                self.own_effect[key].append(strvar)

        self.own_crit_effect = {}
        for key in SpiritPage.GRID_POS.keys():
            self.own_crit_effect[key] = []
            for i in range(4):
                strvar = tk.StringVar()
                strvar.set('-')
                self.own_crit_effect[key].append(strvar)

        self.own_stats = {}
        for key in SpiritPage.STAT_KEYS.keys():
            strvar = tk.StringVar()
            strvar.set('-')
            self.own_stats[key] = strvar

        self.mount = {
            'spirit': None,
            'label': None
        }

    def _render_frame(self):
        self._render_image()
        self._render_context()
        self._render_level_slot()
        self._render_needed_upstone()
        self._render_mount_effect()
        self._render_own_effect()
        self._render_own_crit_effect()
        self._render_whole_own_effect()

    def _render_image(self):
        def OnClick(key, i):
            label = tk.Label(self, bg='white', text='장착 중')
            r_offset, c_offset = SpiritPage.GRID_POS[key]
            label.grid(row=r_offset, column=c_offset + i, padx=3, sticky='we')
            if self.mount['label'] is not None:
                self.mount['label'].destroy()
            self.mount['label'] = label
            self.mount['spirit'] = [key, i]

        for key in SpiritPage.GRID_POS.keys():
            for i in range(4):
                img = self.imgs[key][i]
                label = tk.Button(self, bg='white', image=img, command=lambda i=i, key=key: OnClick(key, i))
                r_offset, c_offset = SpiritPage.GRID_POS[key]
                label.grid(row=r_offset, column=c_offset + i)

        key, i = self.mount['spirit']
        label = tk.Label(self, bg='white', text='장착 중')
        r_offset, c_offset = SpiritPage.GRID_POS[key]
        label.grid(row=r_offset, column=c_offset + i, padx=3, sticky='we')
        if self.mount['label'] is not None:
            self.mount['label'].destroy()
        self.mount['label'] = label

        label = tk.Label(self, bg='white', text='')
        label.grid(row=6, column=0, columnspan=10, pady=3)

        label = tk.Label(self, bg='white', text='')
        label.grid(row=0, column=5, rowspan=6, padx=3)

        label = tk.Label(self, bg='white', text='')
        label.grid(row=0, column=10, rowspan=6, padx=3)

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

    def _render_needed_upstone(self):
        for key in SpiritPage.GRID_POS.keys():
            for i in range(4):
                label = tk.Label(self, textvariable=self.req_ups[key][i], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
                r_offset, c_offset = SpiritPage.GRID_POS[key]
                label.grid(row=r_offset+2, column=c_offset + i, sticky='e')

        for key in SpiritPage.GRID_POS.keys():
            for i in range(4):
                label = tk.Label(self, textvariable=self.full_req_ups[key][i], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
                r_offset, c_offset = SpiritPage.GRID_POS[key]
                label.grid(row=r_offset+3, column=c_offset + i, sticky='e')

    def _render_mount_effect(self):
        for key in SpiritPage.GRID_POS.keys():
            for i in range(4):
                label = tk.Label(self, textvariable=self.mount_effect[key][i], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
                r_offset, c_offset = SpiritPage.GRID_POS[key]
                label.grid(row=r_offset+4, column=c_offset + i, sticky='e')
                
                label = tk.Label(self, textvariable=self.mount_spirit_1_effect[key][i], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
                r_offset, c_offset = SpiritPage.GRID_POS[key]
                label.grid(row=r_offset+5, column=c_offset + i, sticky='e')

        # for key in SpiritPage.HAVE_MOUNT_2_EFFECT.keys():
        #     for i in SpiritPage.HAVE_MOUNT_2_EFFECT[key]:
        #         label = tk.Label(self, textvariable=self.mount_spirit_1_effect[key][i], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
        #         r_offset, c_offset = SpiritPage.GRID_POS[key]
        #         label.grid(row=r_offset+5, column=c_offset + i, sticky='e')

    def _render_own_effect(self):
        for key in SpiritPage.GRID_POS.keys():
            for i in range(4):
                label = tk.Label(self, textvariable=self.own_effect[key][i], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
                r_offset, c_offset = SpiritPage.GRID_POS[key]
                if key in ['일반', '고급']:
                    r_adder = 5
                else:
                    r_adder = 6
                label.grid(row=r_offset + r_adder, column=c_offset + i, sticky='e')

    def _render_own_crit_effect(self):
        for key in SpiritPage.HAVE_MOUNT_2_EFFECT.keys():
            for i in range(4):
                label = tk.Label(self, textvariable=self.own_crit_effect[key][i], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
                r_offset, c_offset = SpiritPage.GRID_POS[key]
                r_adder = 7
                label.grid(row=r_offset + r_adder, column=c_offset + i, sticky='e')

    def _render_whole_own_effect(self):
        label0 = tk.Label(self, text='정령 보유효과', font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
        label0.grid(row=8, column=12, columnspan=2, ipadx=100)
        for idx, key in enumerate(SpiritPage.STAT_KEYS.keys()):
            label1 = tk.Label(self, text=key, font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
            label1.grid(row=9+idx, column=12, sticky='e')

            label2 = tk.Label(self, textvariable=self.own_stats[key], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
            label2.grid(row=9+idx, column=13, sticky='e')


    def update_data(self, userdata):
        for key in SpiritPage.GRID_POS.keys():
            for i in range(4):
                self.levels[key][i].set(userdata['정령'][key][i])
        
        self.mount['spirit'] = userdata['장착 정령']

        self._calculate_variables()

    def update_userdata(self):
        for key in SpiritPage.GRID_POS.keys():
            for i in range(4):
                input_level = self.levels[key][i].get()
                try:
                    level = int(input_level)
                    self.main_frame.userdata['정령'][key][i] = level
                except:
                    self.main_frame.userdata['정령'][key][i] = 0

        self.main_frame.userdata['장착 정령'] = self.mount['spirit']

    def _calculate_variables(self, event=None):
        for key in SpiritPage.GRID_POS.keys():
            for i in range(4):
                level = self.levels[key][i].get()
                level = int(level) if level else -1
                self.req_ups[key][i].set(
                    transform_english_amount_string(
                        calc_spirit_needed_upstone(key, level)
                    )
                )
                self.full_req_ups[key][i].set(
                    transform_english_amount_string(
                        calc_spirit_full_needed_upstone(key, level)
                    )
                )
                
                spirit_effect = calc_spirit_effect(key, i, level)
                self.mount_effect[key][i].set(
                    transform_english_amount_string(
                        spirit_effect[SpiritPage.SPIRIT_EFFECT[i]]
                    ) + '%'
                )

                if key in SpiritPage.HAVE_MOUNT_2_EFFECT.keys():
                    if i in SpiritPage.HAVE_MOUNT_2_EFFECT[key]:
                        self.mount_spirit_1_effect[key][i].set(
                            transform_english_amount_string(
                                spirit_effect['공격력']
                            ) + '%'
                        )

                own_effect = calc_spirit_own_effect(key, i, level)
                self.own_effect[key][i].set(
                    transform_english_amount_string(
                        own_effect[SpiritPage.SPIRIT_EFFECT[i]]
                    ) + '%'
                )
                
                if key in ['전설']:
                    self.own_crit_effect[key][i].set(
                        transform_english_amount_string(
                            own_effect['치명타 데미지 곱']
                        ) + '%'
                    )

        self.update_userdata()

        all_own_effect = calc_all_spirit_own_effect(self.main_frame.userdata)
        for key in SpiritPage.STAT_KEYS.keys():
            self.own_stats[key].set(
                transform_english_amount_string(
                            all_own_effect[SpiritPage.STAT_KEYS[key]],
                            r=2
                        ) + '%'
            )

    
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