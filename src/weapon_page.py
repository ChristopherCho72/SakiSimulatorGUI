import tkinter as tk
import tkinter.font as tkf
import PIL
import re

from PIL import ImageTk, Image
from utils import *

class WeaponPage(tk.Frame):
    GRID_POS = {
        '저급': (0, 1),
        '일반': (0, 6),
        '고급': (0, 11),
        '영웅': (7, 1),
        '전설': (7, 6),
        '신': (18, 1),
        '불멸': (18, 6)
    }
    def __init__(self, master):
        super().__init__(bg='white')

        self.img_size = (90, 90)
        self._initialize_variables(master)
        self._calculate_variables()

        self._render_frame()

    def _initialize_variables(self, master):
        self.imgs = {}
        for key in WeaponPage.GRID_POS.keys():
            self.imgs[key] = []
            for i in reversed(range(1, 5)):
                img = PIL.Image.open('data/img/weapon/%s%d.png'%(key, i)).resize(self.img_size, PIL.Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(img)
                self.imgs[key].append(photo)

        self.levels = {}
        for key in WeaponPage.GRID_POS.keys():
            self.levels[key] = []
            for i in range(4):
                strvar = tk.StringVar()
                strvar.set(master.userdata['장비'][key][i])
                self.levels[key].append(strvar)

        self.req_ups = {}
        for key in WeaponPage.GRID_POS.keys():
            self.req_ups[key] = []
            for i in range(4):
                self.req_ups[key].append(tk.StringVar())

        self.full_req_ups = {}
        for key in WeaponPage.GRID_POS.keys():
            self.full_req_ups[key] = []
            for i in range(4):
                self.full_req_ups[key].append(tk.StringVar())

        self.mount_effect = {}
        for key in WeaponPage.GRID_POS.keys():
            self.mount_effect[key] = []
            for i in range(4):
                self.mount_effect[key].append(tk.StringVar())
                
        self.mount_crit_chance_effect = {}
        for key in WeaponPage.GRID_POS.keys():
            self.mount_crit_chance_effect[key] = []
            for i in range(4):
                self.mount_crit_chance_effect[key].append(tk.StringVar())

        self.mount_crit_dmg_effect = {}
        for key in WeaponPage.GRID_POS.keys():
            self.mount_crit_dmg_effect[key] = []
            for i in range(4):
                self.mount_crit_dmg_effect[key].append(tk.StringVar())

        self.side_effect = {}
        for key in WeaponPage.GRID_POS.keys():
            self.side_effect[key] = []
            for i in range(4):
                self.side_effect[key].append(tk.StringVar())

    def _update_userdata(self, master):
        pass

    def _render_frame(self):
        self._render_context()
        self._render_image()
        self._render_level_slot()
        self._render_needed_upstone()
        self._render_mount_effect()
        # self._render_own_effect()
        # self._render_upgrade_efficiency()
        # self._render_side_effect()

    def _render_context(self):
        label_texts = ['레벨 (미 보유시 0)', '현재 필요한 업스톤', '풀업글 시 필요 업스톤', '현재 장착효과', '현재 보유효과', '개당 업스톤 업그레이드 효율']
        for i, t in enumerate(label_texts):
            label = tk.Label(self, text=t, font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
            label.grid(row=i+1, column=0, sticky='e')

        label_texts = ['레벨 (미 보유시 0)', '현재 필요한 업스톤', '풀업글 시 필요 업스톤', '현재 장착효과', '장착 시 치명타 확률', 'HP/MP/회피/회복 증가율', '현재 보유효과', '개당 업스톤 업그레이드 효율']
        for i, t in enumerate(label_texts):
            label = tk.Label(self, text=t, font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
            label.grid(row=i+8, column=0, sticky='e')

        label_texts = ['레벨 (미 보유시 0)', '현재 필요한 업스톤', '풀업글 시 필요 업스톤', '현재 장착효과', '장착 시 치명타 확률', '장착 시 치명타 피해 증가율', '회피/드랍/물공/마공 증가율', '현재 보유효과', '개당 업스톤 업그레이드 효율', '보유2 공/마 업그레이드 효율']
        for i, t in enumerate(label_texts):
            label = tk.Label(self, text=t, font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
            label.grid(row=i+19, column=0, sticky='e')

    def _render_level_slot(self):
        for key in WeaponPage.GRID_POS.keys():
            for i in range(4):
                vcmd = (self.register(self._validate_level), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
                entry = tk.Entry(self, width=10, textvariable=self.levels[key][i], font=tkf.Font(family="Maplestory", size=10),
                                    justify='right', validate = 'key', validatecommand = vcmd)
                entry.bind('<Return>', self._calculate_variables)
                entry.bind('<FocusOut>', self._calculate_variables)
                r_offset, c_offset = WeaponPage.GRID_POS[key]
                entry.grid(row=r_offset+1, column=c_offset + i, sticky='we')

    def _render_needed_upstone(self):
        for key in WeaponPage.GRID_POS.keys():
            for i in range(4):
                label = tk.Label(self, textvariable=self.req_ups[key][i], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
                r_offset, c_offset = WeaponPage.GRID_POS[key]
                label.grid(row=r_offset+2, column=c_offset + i, sticky='e')

        for key in WeaponPage.GRID_POS.keys():
            for i in range(4):
                label = tk.Label(self, textvariable=self.full_req_ups[key][i], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
                r_offset, c_offset = WeaponPage.GRID_POS[key]
                label.grid(row=r_offset+3, column=c_offset + i, sticky='e')

    def _render_mount_effect(self):
        for key in WeaponPage.GRID_POS.keys():
            for i in range(4):
                label = tk.Label(self, textvariable=self.mount_effect[key][i], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
                r_offset, c_offset = WeaponPage.GRID_POS[key]
                label.grid(row=r_offset+4, column=c_offset + i, sticky='e')

        for key in ['영웅', '전설', '신', '불멸']:
            for i in range(4): 
                label = tk.Label(self, textvariable=self.mount_crit_chance_effect[key][i], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
                r_offset, c_offset = WeaponPage.GRID_POS[key]
                label.grid(row=r_offset+5, column=c_offset + i, sticky='e')

        for key in ['신', '불멸']:
            for i in range(4):  
                label = tk.Label(self, textvariable=self.mount_crit_dmg_effect[key][i], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
                r_offset, c_offset = WeaponPage.GRID_POS[key]
                label.grid(row=r_offset+6, column=c_offset + i, sticky='e')

    def _render_own_effect(self):
        raise NotImplementedError()

    def _render_upgrade_efficiency(self):
        # TODO upgrade efficiency & own2 upgrade efficiency
        raise NotImplementedError()

    def _render_side_effect(self):
        raise NotImplementedError()

    def _render_image(self):
        for key in WeaponPage.GRID_POS.keys():
            for i in range(4):
                img = self.imgs[key][i]
                label = tk.Label(self, bg='white', image=img)
                r_offset, c_offset = WeaponPage.GRID_POS[key]
                label.grid(row=r_offset, column=c_offset + i)

    def _validate_level(self, action, index, value_if_allowed,
                    prior_value, text, validation_type, trigger_type, widget_name):
        only_digit = re.match(r"^[0-9]*$", value_if_allowed) is not None # r'^-$|^-1$|^[0-9]+$' if allow -1
        if not only_digit:
            return False

        if value_if_allowed:
            val = int(value_if_allowed)
            right_range = val in range(201)

            return right_range
        else:
            return True

    def _calculate_variables(self, event=None):
        for key in WeaponPage.GRID_POS.keys():
            for i in range(4):
                level = self.levels[key][i].get()
                level = int(level) if level else 0
                self.req_ups[key][i].set(
                    transform_english_amount_string(
                        calc_needed_upstone(key, i, level)
                    )
                )
                self.full_req_ups[key][i].set(
                    transform_english_amount_string(
                        calc_full_needed_upstone(key, i, level)
                    )
                )
                weapon_effect = calc_weapon_effect(key, i, level)
                self.mount_effect[key][i].set(
                    transform_english_amount_string(
                        weapon_effect['공격력']
                    ) + '%'
                )
                self.mount_crit_chance_effect[key][i].set(
                    transform_english_amount_string(
                        weapon_effect['치명타 확률']
                    ) + '%'
                )
                self.mount_crit_dmg_effect[key][i].set(
                    transform_english_amount_string(
                        weapon_effect['치명타 데미지']
                    ) + '%'
                )
        
    def update_data(self, userdata):
        for key in WeaponPage.GRID_POS.keys():
            for i in range(4):
                self.levels[key][i].set(userdata['장비'][key][i])

        self._calculate_variables()



    


        
