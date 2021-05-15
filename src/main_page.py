import tkinter as tk
import tkinter.font as tkf

from utils import *

class MainPage(tk.Frame):
    def __init__(self, master, main_frame):
        super().__init__(master, bg='white')

        self.left_page = StatPage(self, main_frame)
        self.left_page.grid(row=0, column=0, sticky='n')

        label = tk.Label(self, text='', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
        label.grid(row=0, column=1, padx=5, sticky='we')

        self.right_page = HuntPage(self, main_frame)
        self.right_page.grid(row=0, column=2, sticky='n')

    def update_userdata(self):
        self.left_page.update_userdata()
        self.right_page.update_userdata()

    def update_data(self, userdata):
        self.left_page.update_data(userdata)
        self.right_page.update_data(userdata)


class StatPage(tk.Frame):
    def __init__(self, master, main_frame):
        super().__init__(master, bg='white')

        self.main_frame = main_frame
        self._initialize_variables()
        self._calculate_variables(main_frame.userdata)

        self._render_frame()

    def _initialize_variables(self):
        self.status = {
            '레벨': tk.StringVar(),
            '총 전투력': tk.StringVar(),
            '물공 전투력': tk.StringVar(),
            '마공 전투력': tk.StringVar(),
            '물리공격력': tk.StringVar(),
            '마력': tk.StringVar(),
            'HP': tk.StringVar(),
            '치명타 확률(%)': tk.StringVar(),
            '치명타 데미지(%)': tk.StringVar(),
            '사신타 확률(%)': tk.StringVar(),
            '사신타 데미지(%)': tk.StringVar(),
            'MP': tk.StringVar(),
            '상태이상 면역(%)': tk.StringVar(),
            'HP회복력(%)': tk.StringVar(),
            '회피(%)': tk.StringVar(),
            '경험치 추가 획득(%)': tk.StringVar(),
            '골드 추가 획득(%)': tk.StringVar(),
            '장비 드랍 확률(%)': tk.StringVar(),
            '정령 드랍 확률(%)': tk.StringVar(),
            '용의 알 적용 / 최대(%)': (tk.StringVar(), tk.StringVar()),
            '최소/최대 데미지(%)': (tk.StringVar(), tk.StringVar())
        }

    def _render_frame(self):
        row_idx = 0

        level = tk.Label(self, text='레벨', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
        level.grid(row=row_idx, column=0, sticky='w', padx=10, pady=3)

        level_num = tk.Label(self, text='Lv. ', font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#FF843A")
        level_num.grid(row=row_idx, column=1, sticky='e', padx=10, pady=3)

        entry = tk.Entry(self, width=5, textvariable=self.status['레벨'], font=tkf.Font(family="Maplestory", size=22),
                        justify='center', fg='#FF843A')
        entry.bind('<Return>', self.update_userdata)
        entry.bind('<FocusOut>', self.update_userdata)
        entry.grid(row=row_idx, column=2, padx=3, sticky='e')

        row_idx += 1

        for key in ['총 전투력', '물공 전투력', '마공 전투력']:
            label = tk.Label(self, text=key, font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#202020")
            label_num = tk.Label(self, textvariable=self.status[key], font=tkf.Font(family="Maplestory", size=20), bg='white', fg="#FF0000")
            label.grid(row=row_idx, column=0, sticky='w', padx=10, pady=3)
            label_num.grid(row=row_idx, column=1, columnspan=2, sticky='e', padx=10, pady=3)
            row_idx += 1

        canvas = tk.Canvas(self, bg='white', bd=0, width=700, height=10, highlightthickness=0)
        canvas.create_line(15, 5, 685, 5, width=3)
        canvas.grid(row=row_idx, column=0, columnspan=3)
        row_idx += 1

        for key in ['물리공격력',
                    '마력',
                    'HP',
                    '치명타 확률(%)',
                    '치명타 데미지(%)',
                    '사신타 확률(%)',
                    '사신타 데미지(%)',
                    'MP',
                    '상태이상 면역(%)',
                    'HP회복력(%)',
                    '회피(%)',
                    '경험치 추가 획득(%)',
                    '골드 추가 획득(%)',
                    '장비 드랍 확률(%)',
                    '정령 드랍 확률(%)']:
            label = tk.Label(self, text=key, font=tkf.Font(family="Maplestory", size=15), bg='white', fg="#202020")
            label_num = tk.Label(self, textvariable=self.status[key], font=tkf.Font(family="Maplestory", size=15), bg='white', fg="#FF843A")
            label.grid(row=row_idx, column=0, sticky='w', padx=10, pady=3)
            label_num.grid(row=row_idx, column=1, columnspan=2, sticky='e', padx=10, pady=3)
            row_idx += 1

        for key in ['용의 알 적용 / 최대(%)',
                    '최소/최대 데미지(%)']:
            label = tk.Label(self, text=key, font=tkf.Font(family="Maplestory", size=15), bg='white', fg="#202020")
            label_num_1 = tk.Label(self, textvariable=self.status[key][0], font=tkf.Font(family="Maplestory", size=15), bg='white', fg="#FF843A")
            label_num_2 = tk.Label(self, textvariable=self.status[key][1], font=tkf.Font(family="Maplestory", size=15), bg='white', fg="#FF843A")
            label.grid(row=row_idx, column=0, sticky='w', padx=10, pady=3)
            label_num_1.grid(row=row_idx, column=1, sticky='e', padx=10, pady=3)
            label_num_2.grid(row=row_idx, column=2, sticky='e', padx=10, pady=3)
            row_idx += 1

    def update_data(self, userdata):
        self.status['레벨'].set(userdata['레벨'])

        self._calculate_variables(userdata)

    def _calculate_variables(self, userdata):
        self.costume_option = calc_costume(userdata)
        self.pet_option = calc_pet(userdata)
        self.egg_option, max_egg_option = calc_dragon_egg(userdata)
        self.offering_option = calc_offering(userdata)
        self.weapon_own = calc_all_weapon_own_effect(userdata)
        self.weapon_mount = get_weapon_effect(userdata)
        self.spirit_own = calc_all_spirit_own_effect(userdata)
        self.spirit_mount = get_spirit_effect(userdata)

        level = userdata['레벨']
        status = calc_status(userdata, self.costume_option, self.pet_option, self.egg_option, self.offering_option,
                        self.weapon_own, self.weapon_mount, self.spirit_own, self.spirit_mount)

        self.status['레벨'].set(str(level))
        self.status['총 전투력'].set(transform_korean_amount_string(keep_seven_digits(status['총 전투력'])))
        self.status['물공 전투력'].set(transform_korean_amount_string(keep_seven_digits(status['물공 전투력'])))
        self.status['마공 전투력'].set(transform_korean_amount_string(keep_seven_digits(status['마공 전투력'])))
        self.status['물리공격력'].set(transform_korean_amount_string(keep_seven_digits(status['물리공격력'])))
        self.status['마력'].set(transform_korean_amount_string(keep_seven_digits(status['마력'])))

        for key in status.keys():
            if key in ['레벨', '총 전투력', '물공 전투력', '마공 전투력', '물리공격력', '마력']:
                continue
            if key in ['용의 알 적용 / 최대(%)', '최소/최대 데미지(%)']:
                self.status[key][0].set(transform_english_amount_string(status[key][0]))
                self.status[key][1].set(transform_english_amount_string(status[key][1]))
            elif key == 'HP':
                self.status[key].set(transform_english_amount_string(keep_seven_digits(status[key])))
            else:
                self.status[key].set(transform_english_amount_string(status[key]))

        self.update_userdata()

    def update_userdata(self, event=None):
        input_level = self.status['레벨'].get()
        try:
            level = int(input_level)
            self.main_frame.userdata['레벨'] = level
        except:
            self.main_frame.userdata['레벨'] = 0


class HuntPage(tk.Frame):
    def __init__(self, master, main_frame):
        super().__init__(master, bg='white')

        self.main_frame = main_frame
        self.img_size = (90, 90)

        self._initialize_variables(main_frame)
        self.update_data(main_frame.userdata)

        self._render_frame()

    def _initialize_variables(self, master):
        pass

    def update_data(self, userdata):
        pass

    def update_userdata(self):
        pass

    def _render_frame(self):
        pass