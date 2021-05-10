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
        '영웅': (8, 1),
        '전설': (8, 6),
        '신': (20, 1),
        '불멸': (20, 6)
    }
    HAVE_MOUNT_CRIT_CHANCE = ['영웅', '전설', '신', '불멸']
    HAVE_MOUNT_CRIT_DAMAGE = ['신', '불멸']
    HAVE_OWN_SIDE = ['영웅', '전설', '신', '불멸']
    SIDE_EFFECT = {
        '전설': ['HP 증가', 'MP 증가', '회피율', 'HP 회복'],
        '신': ['회피율', '드랍률', '공격력 추가', '마력 추가'],
        '불멸': ['HP 증가', '치명타 데미지', '공격력 추가', '마력 추가']
    }
    STAT_KEYS = {
        '물공 보유효과': '공격력',
        '마공 보유효과': '마력',
        '자연회복률': 'HP 회복',
        '아이템 드랍률': '드랍률',
        'HP 증가': 'HP 증가',
        'MP 증가': 'MP 증가',
        '회피율 증가': '회피율',
        '치명타 데미지': '치명타 데미지'
    }
    def __init__(self, master):
        super().__init__(bg='white')

        self.master = master
        self.img_size = (90, 90)

        self._initialize_variables(master)
        self.update_data(master.userdata)

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
                strvar.set('')
                self.levels[key].append(strvar)

        self.req_ups = {}
        for key in WeaponPage.GRID_POS.keys():
            self.req_ups[key] = []
            for i in range(4):
                strvar = tk.StringVar()
                strvar.set('-')
                self.req_ups[key].append(strvar)

        self.full_req_ups = {}
        for key in WeaponPage.GRID_POS.keys():
            self.full_req_ups[key] = []
            for i in range(4):
                strvar = tk.StringVar()
                strvar.set('-')
                self.full_req_ups[key].append(strvar)

        self.mount_effect = {}
        for key in WeaponPage.GRID_POS.keys():
            self.mount_effect[key] = []
            for i in range(4):
                strvar = tk.StringVar()
                strvar.set('-')
                self.mount_effect[key].append(strvar)
                
        self.mount_crit_chance_effect = {}
        for key in WeaponPage.GRID_POS.keys():
            self.mount_crit_chance_effect[key] = []
            for i in range(4):
                strvar = tk.StringVar()
                strvar.set('-')
                self.mount_crit_chance_effect[key].append(strvar)

        self.mount_crit_dmg_effect = {}
        for key in WeaponPage.GRID_POS.keys():
            self.mount_crit_dmg_effect[key] = []
            for i in range(4):
                strvar = tk.StringVar()
                strvar.set('-')
                self.mount_crit_dmg_effect[key].append(strvar)

        self.side_effect = {}
        for key in WeaponPage.GRID_POS.keys():
            self.side_effect[key] = []
            for i in range(4):
                strvar = tk.StringVar()
                strvar.set('-')
                self.side_effect[key].append(strvar)

        self.own_effect = {}
        for key in WeaponPage.GRID_POS.keys():
            self.own_effect[key] = []
            for i in range(4):
                strvar = tk.StringVar()
                strvar.set('-')
                self.own_effect[key].append(strvar)

        self.efficiency = {}
        for key in WeaponPage.GRID_POS.keys():
            self.efficiency[key] = []
            for i in range(4):
                strvar = tk.StringVar()
                strvar.set('-')
                self.efficiency[key].append(strvar)

        self.own_efficiency = {}
        for key in WeaponPage.GRID_POS.keys():
            self.own_efficiency[key] = []
            for i in range(4):
                strvar = tk.StringVar()
                strvar.set('-')
                self.own_efficiency[key].append(strvar)

        self.own_stats = {}
        for key in WeaponPage.STAT_KEYS.keys():
            strvar = tk.StringVar()
            strvar.set('-')
            self.own_stats[key] = strvar

    def update_userdata(self):
        for key in WeaponPage.GRID_POS.keys():
            for i in range(4):
                input_level = self.levels[key][i].get()
                try:
                    level = int(input_level)
                    self.master.userdata['장비'][key][i] = level
                except:
                    self.master.userdata['장비'][key][i] = 0

    def _render_frame(self):
        self._render_context()
        self._render_image()
        self._render_level_slot()
        self._render_needed_upstone()
        self._render_mount_effect()
        self._render_own_effect()
        self._render_upgrade_efficiency()
        self._render_side_effect()
        self._render_whole_own_effect()

    def _render_context(self):
        label_texts = ['레벨 (미 보유시 0)', '현재 필요한 업스톤', '풀업글 시 필요 업스톤', '현재 장착효과', '현재 보유효과', '개당 업스톤 업그레이드 효율']
        for i, t in enumerate(label_texts):
            label = tk.Label(self, text=t, font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
            label.grid(row=i+1, column=0, sticky='e')

        label_texts = ['레벨 (미 보유시 0)', '현재 필요한 업스톤', '풀업글 시 필요 업스톤', '현재 장착효과', '장착 시 치명타 확률', 'HP/MP/회피/회복 증가율', '현재 보유효과', '개당 업스톤 업그레이드 효율']
        for i, t in enumerate(label_texts):
            label = tk.Label(self, text=t, font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
            label.grid(row=i+9, column=0, sticky='e')

        label_texts = ['레벨 (미 보유시 0)', '현재 필요한 업스톤', '풀업글 시 필요 업스톤', '현재 장착효과', '장착 시 치명타 확률', '장착 시 치명타 피해 증가율', '회피(HP)/드랍(치피)/물공/마공 증가율', '현재 보유효과', '개당 업스톤 업그레이드 효율', '보유2 공/마 업그레이드 효율']
        for i, t in enumerate(label_texts):
            label = tk.Label(self, text=t, font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
            label.grid(row=i+21, column=0, sticky='e')

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

        for key in WeaponPage.HAVE_MOUNT_CRIT_CHANCE:
            for i in range(4): 
                label = tk.Label(self, textvariable=self.mount_crit_chance_effect[key][i], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
                r_offset, c_offset = WeaponPage.GRID_POS[key]
                label.grid(row=r_offset+5, column=c_offset + i, sticky='e')

        for key in WeaponPage.HAVE_MOUNT_CRIT_DAMAGE:
            for i in range(4):  
                label = tk.Label(self, textvariable=self.mount_crit_dmg_effect[key][i], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
                r_offset, c_offset = WeaponPage.GRID_POS[key]
                label.grid(row=r_offset+6, column=c_offset + i, sticky='e')

    def _render_own_effect(self):
        for key in WeaponPage.GRID_POS.keys():
            for i in range(4):
                label = tk.Label(self, textvariable=self.own_effect[key][i], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
                r_offset, c_offset = WeaponPage.GRID_POS[key]
                if key in ['저급', '일반', '고급']:
                    r_adder = 5
                elif key in ['영웅', '전설']:
                    r_adder = 7
                else:
                    r_adder = 8
                label.grid(row=r_offset + r_adder, column=c_offset + i, sticky='e')

    def _render_upgrade_efficiency(self):
        for key in WeaponPage.GRID_POS.keys():
            for i in range(4):
                label = tk.Label(self, textvariable=self.efficiency[key][i], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
                r_offset, c_offset = WeaponPage.GRID_POS[key]
                r_adder = 6 if key in ['저급', '일반', '고급'] else 8 if key in ['영웅', '전설'] else 9
                label.grid(row=r_offset + r_adder, column=c_offset + i, sticky='e')

        for key in WeaponPage.HAVE_MOUNT_CRIT_DAMAGE:
            for i in range(4):
                label = tk.Label(self, textvariable=self.own_efficiency[key][i], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
                r_offset, c_offset = WeaponPage.GRID_POS[key]
                r_adder = 10
                label.grid(row=r_offset + r_adder, column=c_offset + i, sticky='e')

    def _render_side_effect(self):
        for key in WeaponPage.HAVE_OWN_SIDE:
            for i in range(4):
                label = tk.Label(self, textvariable=self.side_effect[key][i], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
                r_offset, c_offset = WeaponPage.GRID_POS[key]
                r_adder = 6 if key in ['영웅', '전설'] else 7
                label.grid(row=r_offset + r_adder, column=c_offset + i, sticky='e')

    def _render_image(self):
        for key in WeaponPage.GRID_POS.keys():
            for i in range(4):
                img = self.imgs[key][i]
                label = tk.Label(self, bg='white', image=img)
                r_offset, c_offset = WeaponPage.GRID_POS[key]
                label.grid(row=r_offset, column=c_offset + i, padx=3)

        for i in [7, 17]:
            label = tk.Label(self, bg='white', text='')
            label.grid(row=i, column=0, pady=3)

        for i in [5, 10]:
            label = tk.Label(self, bg='white', text='')
            label.grid(row=0, column=i, padx=3)

    def _render_whole_own_effect(self):
        label0 = tk.Label(self, text='장비 보유효과', font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
        label0.grid(row=21, column=12, columnspan=2)
        for idx, key in enumerate(WeaponPage.STAT_KEYS.keys()):
            label1 = tk.Label(self, text=key, font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
            label1.grid(row=22+idx, column=12, sticky='e')

            label2 = tk.Label(self, textvariable=self.own_stats[key], font=tkf.Font(family="Maplestory", size=10), bg='white', fg="#202020")
            label2.grid(row=22+idx, column=13, sticky='e')

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
                own_effect = calc_weapon_own_effect(key, i, level)
                self.own_effect[key][i].set(
                    transform_english_amount_string(
                        own_effect['공격력']
                    ) + '%'
                )
                if key in WeaponPage.SIDE_EFFECT.keys():
                    self.side_effect[key][i].set(
                        transform_english_amount_string(
                            own_effect[WeaponPage.SIDE_EFFECT[key][i]]
                        ) + '%'
                    )

                if level not in [200, 0]:                
                    next_own_effect = calc_weapon_own_effect(key, i, level+1)
                    efficiency = (next_own_effect['공격력'] - own_effect['공격력']) / int(self.req_ups[key][i].get().replace(',', ''))

                    if efficiency >= 0.0001:
                        self.efficiency[key][i].set(
                            transform_english_amount_string(
                                efficiency,
                                r=4
                            ) + '%'
                        )
                    else:
                        self.efficiency[key][i].set(
                            '< 0.0001%'
                        )

                    if key in WeaponPage.HAVE_MOUNT_CRIT_DAMAGE and i in [2, 3]:
                        efficiency = (next_own_effect['공격력 추가'] - own_effect['공격력 추가']) / int(self.req_ups[key][i].get().replace(',', '')) if i == 2 else \
                                        (next_own_effect['마력 추가'] - own_effect['마력 추가']) / int(self.req_ups[key][i].get().replace(',', ''))

                        if efficiency >= 0.0001:
                            self.own_efficiency[key][i].set(
                                transform_english_amount_string(
                                    efficiency,
                                    r=4
                                ) + '%'
                            )
                        else:
                            self.own_efficiency[key][i].set(
                                '< 0.0001%'
                            )
                else:
                    self.efficiency[key][i].set(
                        transform_english_amount_string(
                            0,
                            r=4
                        ) + '%'
                    )
                    self.own_efficiency[key][i].set(
                        transform_english_amount_string(
                            0,
                            r=4
                        ) + '%'
                    )
                
        self.update_userdata()

        all_own_effect = calc_all_weapon_own_effect(self.master.userdata)
        for key in WeaponPage.STAT_KEYS.keys():
            self.own_stats[key].set(
                transform_english_amount_string(
                            all_own_effect[WeaponPage.STAT_KEYS[key]],
                            r=0
                        ) + '%'
            )


    def update_data(self, userdata):
        for key in WeaponPage.GRID_POS.keys():
            for i in range(4):
                self.levels[key][i].set(userdata['장비'][key][i])

        self._calculate_variables()
