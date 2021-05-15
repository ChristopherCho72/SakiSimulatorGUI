import math
import json
import os
import csv

from userdata_template import template

def make_spirit_upstone_dict():
    r = csv.reader(open('data/spirit.csv', encoding='utf-8'))
    d = {
        '일반': dict(),
        '고급': dict(),
        '영웅': dict(),
        '전설': dict()
    }
    for l in r:
        level, normal, high, hero, legend = l
        level, normal, high, hero, legend = int(level), int(normal), int(high), int(hero), int(legend)
        d['일반'][level] = normal
        d['고급'][level] = high
        d['영웅'][level] = hero
        d['전설'][level] = legend

    return d

spirit_upstone = make_spirit_upstone_dict()

def calc_phys_atk(userdata, costume_option, pet_option, egg_option,
                  weapon_own, weapon_mount, spirit_own, spirit_mount):
    # calculate atk +
    atk = 17 \
        + userdata['능력치']['공격력'] \
        + userdata['펜던트']['유혹'] \
        + userdata['펜던트']['독수리'] \
        + userdata['스킬-패시브']['플루토의 낫'] * 50

    # calculate atk *
    atk *= (userdata['스킬-패시브']['주피터의 지혜'] / 100 + 1) * \
            (costume_option['공격력'] / 100 + 1) * \
            (pet_option['공격력'] / 100 + 1) * \
            (userdata['제물']['벌집'] * 4 / 100 + 1) * \
            (userdata['컬렉션']['공격력'] / 100 + 1) * \
            (egg_option / 100 + 1) * \
            ((weapon_mount['공격력'] + weapon_own['공격력']) / 100 + 1) * \
            ((spirit_mount['공격력'] + spirit_own['공격력']) / 100 + 1) * \
            (userdata['스킬-패시브']['만해'] / 100 + 1)
    
    return atk

def calc_magi_atk(userdata, costume_option, pet_option, egg_option,
                  weapon_own, weapon_mount, spirit_own, spirit_mount):
    # calculate atk +
    atk = userdata['능력치']['마력'] \
        + userdata['펜던트']['숲'] \
        + userdata['펜던트']['십자가'] \
        + userdata['스킬-패시브']['플루토의 보주'] * 50

    # calculate atk *
    atk *= (userdata['스킬-패시브']['넵튠의 지혜'] * 2 / 100 + 1) * \
            (costume_option['마력'] / 100 + 1) * \
            (pet_option['마력'] / 100 + 1) * \
            (userdata['제물']['해골'] * 4 / 100 + 1) * \
            (userdata['컬렉션']['마력'] / 100 + 1) * \
            (egg_option / 100 + 1) * \
            ((weapon_mount['마력'] + weapon_own['마력']) / 100 + 1) * \
            ((spirit_mount['마력'] + spirit_own['마력']) / 100 + 1) * \
            (userdata['스킬-패시브']['만해'] / 100 + 1)
    
    return atk

def calc_hp(userdata, costume_option,
                weapon_own, spirit_own, spirit_mount):
    # calculate HP +
    hp = userdata['능력치']['HP 증가'] + \
            userdata['스킬-패시브']['플루토의 옷'] * 50

    # calculate HP *
    hp *= (userdata['스킬-패시브']['불칸의 지혜'] / 100 + 1) * \
            (costume_option['체력'] / 100 + 1) * \
            (userdata['제물']['식기'] * 10 / 100 + 1) * \
            (weapon_own['HP 증가'] / 100 + 1) * \
            ((spirit_mount['HP 증가'] + spirit_own['HP 증가']) / 100 + 1) * \
            (userdata['스킬-패시브']['만해'] / 100 + 1)
    
    return hp

def calc_mp(userdata, weapon_own):
    mp = userdata['능력치']['MP 증가'] + \
            userdata['스킬-패시브']['사신의 의무'] * 5 + \
            userdata['제물']['술잔'] * 20 + \
            weapon_own['MP 증가'] + \
            userdata['펜던트']['사신의 눈물']

    return mp

def calc_crit_chance(userdata, offering_option, weapon_mount):
    crit_chance = userdata['능력치']['치명타 확률 증가'] + \
                    userdata['스킬-패시브']['아폴로의 지혜'] * 0.2 + \
                    offering_option['치명타 확률'] + \
                    weapon_mount['치명타 확률']
                    
    return crit_chance

def calc_crit_dmg(userdata, costume_option, offering_option,
                    weapon_own, weapon_mount, spirit_own, spirit_mount):
    crit_dmg = userdata['능력치']['치명타 데미지 증가'] + \
                userdata['펜던트']['천둥'] + \
                userdata['스킬-패시브']['영웅의 기운'] * 2 + \
                costume_option['치명타 데미지'] + \
                offering_option['치명타 데미지'] + \
                weapon_own['치명타 데미지'] + \
                weapon_mount['치명타 데미지'] + \
                spirit_own['치명타 데미지'] + \
                spirit_mount['치명타 데미지'] + \
                100

    crit_dmg *= (spirit_own['치명타 데미지 곱'] / 100 + 1)

    return crit_dmg

def calc_reaper_chance(userdata):
    reapear_chance = userdata['능력치']['사신타 확률 증가'] + \
                        userdata['펜던트']['광기'] + \
                        userdata['스킬-패시브']['타나토스의 손길'] * 0.02 + \
                        userdata['제물']['귀걸이'] * 0.2

    return reapear_chance

def calc_reaper_dmg (userdata):
    reapear_dmg = 150 * \
                    (userdata['능력치']['사신타 데미지 증가'] / 100 + 1) * \
                    (userdata['스킬-패시브']['타나토스의 분노'] * 0.02 / 100 + 1)

    return reapear_dmg

def calc_immune(userdata, costume_option):
    immune = costume_option['상태이상 면역']

    return immune

def calc_hp_regen(userdata, weapon_own):
    hp_regen = userdata['스킬-패시브']['지상의 기도'] * 0.25 + \
                weapon_own['HP 회복']

    return hp_regen

def calc_evade(userdata, costume_option, weapon_own):
    evade = costume_option['회피율'] + \
            userdata['스킬-패시브']['미네르바의 지혜'] * 2 + \
            weapon_own['회피율']

    return evade

def calc_exp(userdata, costume_option, pet_option):
    exp = userdata['스킬-패시브']['전설의 주문'] * 2 + \
            costume_option['경험치'] + \
            pet_option['경험치'] + \
            userdata['제물']['반지'] * 10

    return exp 

def calc_gold(userdata, costume_option, pet_option):
    gold = userdata['펜던트']['행운'] + \
            userdata['스킬-패시브']['블레싱'] * 20 + \
            costume_option['골드'] + \
            pet_option['경험치'] + \
            userdata['제물']['촛대'] * 10

    return gold
            
def calc_weapon_drop(userdata, weapon_own):
    drop = 6 * \
            (weapon_own['드랍률'] / 100 + 1)

    return drop

def calc_spirit_drop(userdata):
    drop = 2

    return drop

def calc_min_max_dmg(userdata):
    min_dmg = 80 + \
                userdata['펜던트']['성검']
    
    max_dmg = 120

    return min_dmg, max_dmg

def calc_status(userdata, costume_option, pet_option, egg_option, offering_option,
                weapon_own, weapon_mount, spirit_own, spirit_mount):
    phys_atk = calc_phys_atk(userdata, costume_option, pet_option, egg_option,
                                weapon_own, weapon_mount, spirit_own, spirit_mount)
    magi_atk = calc_magi_atk(userdata, costume_option, pet_option, egg_option,
                                weapon_own, weapon_mount, spirit_own, spirit_mount)
    crit_chance = calc_crit_chance(userdata, offering_option, weapon_mount)
    crit_dmg = calc_crit_dmg(userdata, costume_option, offering_option,
                    weapon_own, weapon_mount, spirit_own, spirit_mount)
    reaper_chance = calc_reaper_chance(userdata)
    reaper_dmg = calc_reaper_dmg (userdata)

    phys_power = phys_atk * \
                    ((crit_dmg / 100 - 1) * crit_chance / 100 + 1) * \
                    ((reaper_dmg / 100 - 1) * reaper_chance / 100 + 1)

    magi_power = magi_atk * \
                    ((crit_dmg / 100 - 1) * crit_chance / 100 + 1) * \
                    ((reaper_dmg / 100 - 1) * reaper_chance / 100 + 1)

    whole_power = phys_power + magi_power

    return {
        '총 전투력': whole_power,
        '물공 전투력': phys_power,
        '마공 전투력': magi_power,
        '물리공격력': phys_atk,
        '마력': magi_atk,
        'HP': calc_hp(userdata, costume_option, weapon_own, spirit_own, spirit_mount),
        '치명타 확률(%)': crit_chance,
        '치명타 데미지(%)': crit_dmg,
        '사신타 확률(%)': reaper_chance,
        '사신타 데미지(%)': reaper_dmg,
        'MP': calc_mp(userdata, weapon_own),
        '상태이상 면역(%)': calc_immune(userdata, costume_option),
        'HP회복력(%)': calc_hp_regen(userdata, weapon_own),
        '회피(%)': calc_evade(userdata, costume_option, weapon_own),
        '경험치 추가 획득(%)': calc_exp(userdata, costume_option, pet_option),
        '골드 추가 획득(%)': calc_gold(userdata, costume_option, pet_option),
        '장비 드랍 확률(%)': calc_weapon_drop(userdata, weapon_own),
        '정령 드랍 확률(%)': calc_spirit_drop(userdata),
        '용의 알 적용 / 최대(%)': calc_dragon_egg(userdata),
        '최소/최대 데미지(%)': calc_min_max_dmg(userdata)
    }

def calc_costume(userdata):
    normal = userdata['코스튬']['일반']
    normal_value = userdata['코스튬']['일반수치']
    high = userdata['코스튬']['고급']
    high_value = userdata['코스튬']['고급수치']

    phys = (normal_value[0] if normal[0] == '공격력' else 0) + \
            (normal_value[1] if normal[1] == '공격력' else 0) + \
            (high_value[0] if high[0] == '공격력' else 0) + \
            (high_value[1] if high[1] == '공격력' else 0)

    magi = (normal_value[0] if normal[0] == '마력' else 0) + \
            (normal_value[4] if normal[4] == '마력' else 0) + \
            (high_value[0] if high[0] == '마력' else 0) + \
            (high_value[1] if high[1] == '마력' else 0)

    hp = (normal_value[1] if normal[1] == '체력' else 0) + \
            (high_value[0] if high[0] == '체력' else 0) + \
            (high_value[1] if high[1] == '체력' else 0)

    immune = normal_value[2] if normal[2] == '상태이상 면역' else 0
    evade = normal_value[2] if normal[2] == '회피율' else 0
    gold = normal_value[3] if normal[3] == '골드' else 0
    exp = normal_value[3] if normal[3] == '경험치' else 0

    crit_dmg = (normal_value[4] if normal[4] == '치명타 데미지' else 0) + \
            (high_value[0] if high[0] == '치명타 데미지' else 0) + \
            (high_value[1] if high[1] == '치명타 데미지' else 0)

    return {
        '공격력': phys,
        '마력': magi,
        '체력': hp,
        '상태이상 면역': immune,
        '회피율': evade,
        '골드': gold,
        '경험치': exp,
        '치명타 데미지': crit_dmg
    }

def calc_pet(userdata):
    pet = {}
    for key in userdata['펫'].keys():
        pet[key] = 0 if key != userdata['펫']['active'] else userdata['펫'][key]

    return pet

def calc_dragon_egg(userdata):
    egg_limit = (userdata['레벨'] // 3) * 3 * 5 + 6000
    egg = userdata['용알']

    valid_egg = min(egg, egg_limit)

    return math.trunc(valid_egg/15), math.trunc(egg_limit/15)

def calc_all_weapon_own_effect(userdata):
    result = {
        '공격력': 0.0,
        '마력': 0.0,
        'HP 회복': 0.0,
        '드랍률': 0.0,
        'HP 증가': 0.0,
        'MP 증가': 0.0,
        '회피율': 0.0,
        '치명타 데미지': 0.0,
        '공격력 추가': 0.0,
        '마력 추가': 0.0
    }
    for key in ['저급', '일반', '고급', '영웅', '전설', '신', '불멸']:
        for i in range(4):
            own_effect = calc_weapon_own_effect(key, i, userdata['장비'][key][i])
            for effect in result.keys():
                result[effect] += own_effect[effect]

    result['공격력'] += result['공격력 추가']
    result['마력'] += result['마력 추가']

    del result['공격력 추가']
    del result['마력 추가']

    return result

def calc_weapon_own_effect(rank, idx, level):
    base = {
        "저급": [10, 13, 17, 20],
        "일반": [70, 90, 110, 140],
        "고급": [300, 400, 500, 600],
        "영웅": [800, 1000, 1200, 1400],
        "전설": [2000, 2400, 2800, 3200],
        "신": [9000, 12000, 15000, 20000],
        "불멸": [68000, 238000, 807500, 4675000]
    }
    constants = {
        '저급': (0.33, 3),
        '일반': (0.33, 2),
        '고급': (0.33, 0),
        '영웅': (0.33, 0),
        '전설': (0.33, 0),
        '신': (1, 0),
        '불멸': (1, 0),
    }

    phys_n_magi = round(base[rank][idx] * (level ** 0.461) * constants[rank][0], constants[rank][1])

    phys = phys_n_magi
    magi = phys_n_magi
    hp_regen, item_drop, hp, mp, evade, crit_dmg, phys2, magi2 = 0, 0, 0, 0, 0, 0, 0, 0
    if rank == '전설' and idx == 0:
        hp += level * 10
    elif rank == '전설' and idx == 1:
        mp += level * 5
    elif rank == '전설' and idx == 2:
        evade += min(level * 0.1, 10)
    elif rank == '전설' and idx == 3:
        hp_regen = 0.25 * level
    elif rank == '신' and idx == 0:
        evade += min(level * 0.1, 10)
    elif rank == '신' and idx == 1:
        item_drop = min(level, 100)
    elif rank == '신' and idx == 2:
        phys2 += round(base[rank][idx] * (level ** 0.461) * 0.33, 3)
    elif rank == '신' and idx == 3:
        magi2 += round(base[rank][idx] * (level ** 0.461) * 0.33, 3)
    elif rank == '불멸' and idx == 0:
        hp += level * 15
    elif rank == '불멸' and idx == 1:
        crit_dmg = level * 2.45
    elif rank == '불멸' and idx == 2:
        phys2 += round(base[rank][idx] * (level ** 0.461) * 0.388235294117647, 0)
    elif rank == '불멸' and idx == 3:
        magi2 += round(base[rank][idx] * (level ** 0.461) * 0.388235294117647, 0)

    return {
        '공격력': phys,
        '마력': magi,
        'HP 회복': hp_regen,
        '드랍률': item_drop,
        'HP 증가': hp,
        'MP 증가': mp,
        '회피율': evade,
        '치명타 데미지': crit_dmg,
        '공격력 추가': phys2,
        '마력 추가': magi2
    }

def calc_all_spirit_own_effect(userdata):
    result = {
        '공격력': 0.0,
        '마력': 0.0,
        'HP 증가': 0.0,
        '치명타 데미지': 0.0,
        '치명타 데미지 곱': 0.0
    }

    for rank in ['일반', '고급', '영웅', '전설']:
        for i in range(4):
            spirit_effect = calc_spirit_own_effect(rank, i, userdata['정령'][rank][i])
            for key in spirit_effect.keys():
                result[key] += spirit_effect[key]

    return result

def calc_spirit_own_effect(rank, idx, level):
    base = {
        '일반': 2.5,
        '일반_치명': 5,
        '고급': 5.0,
        '고급_치명': 15,
        '영웅': 10,
        '영웅_치명': 30,
        '전설': 30,
        '전설_치명': 90
    }
    base_crit_mult = [(2.5, 0.05), (5, 0.1), (10, 0.2), (20, 0.3)]

    hp, phys, magi, crit_dmg, crit_dmg_mult = 0, 0, 0, 0, 0
    if idx == 0:
        hp += base[rank] + level * base[rank] * 0.01 if level >= 0 else 0
    if idx == 1:
        phys += base[rank] + level * base[rank] * 0.01 if level >= 0 else 0
    if idx == 2:
        magi += base[rank] + level * base[rank] * 0.01 if level >= 0 else 0
    if idx == 3:
        crit_dmg += base[rank + '_치명'] + level * base[rank + '_치명'] * 0.01 if level >= 0 else 0

    if rank == '전설':
        crit_dmg_mult = base_crit_mult[idx][0] + level * base_crit_mult[idx][1] if level >= 0 else 0

    return {
        '공격력': phys,
        '마력': magi,
        'HP 증가': hp,
        '치명타 데미지': crit_dmg,
        '치명타 데미지 곱': crit_dmg_mult
    }

def calc_offering(userdata):
    crit_chance = min(userdata['제물']['말발굽'], 50) * 0.4 + \
                    max(userdata['제물']['말발굽']-50, 0) * 0.2

    crit_dmg = min(userdata['제물']['고글'], 75) * 5 + \
                max(userdata['제물']['고글']-75, 0) * 10

    return {
        '치명타 데미지': crit_dmg,
        '치명타 확률': crit_chance
    }

def calc_needed_upstone(rank, idx, level):
    base = {
        "저급": 1,
        "일반": 11.18035,
        "고급": 31.62279,
        "영웅": 89.44273,
        "전설": 353.55385,
        "신": 1837.1174,
        "불멸": 31622.7779
    }
    immortal_adder = [300000, 5000000, 10000000, 25000000]

    if level == 200:
        return 0
    if level == 0:
        return '-'
    
    adder = immortal_adder[idx] if rank == '불멸' else 0

    return int(base[rank] * (level ** 1.5)) + adder

def calc_spirit_full_needed_upstone(rank, level):
    if level == -1:
        return '-'

    req_ups = 0
    for i in range(level, 201):
        req_ups += calc_spirit_needed_upstone(rank, i)

    return req_ups

def calc_spirit_needed_upstone(rank, level):
    if level == -1:
        return '-'
        
    return spirit_upstone[rank][level]

def calc_full_needed_upstone(rank, idx, level):
    if level == 0:
        return '-'

    req_ups = 0
    for i in range(level, 201):
        req_ups += calc_needed_upstone(rank, idx, i)

    return req_ups

def get_weapon_effect(userdata):
    rank, idx = userdata['장착 무기']
    level = userdata['장비'][rank][idx]

    return calc_weapon_effect(rank, idx, level)

def calc_weapon_effect(rank, idx, level):
    base = {
        "저급": [10, 13, 17, 20],
        "일반": [70, 90, 110, 140],
        "고급": [300, 400, 500, 600],
        "영웅": [800, 1000, 1200, 1400],
        "전설": [2000, 2400, 2800, 3200],
        "신": [9000, 12000, 15000, 20000],
        "불멸": [68000, 238000, 807500, 4675000]
    }
    crit_chance_base = {
        '영웅': [0.1, 0.11, 0.12, 0.13],
        '전설': [0.1, 0.12, 0.14, 0.16],
        '신': [0.1, 0.15, 0.2, 0.25],
        '불멸': [25, 25, 25, 25]
    }
    crit_dmg_base = {
        '신': [2, 2.2, 2.4, 2.7],
        '불멸': [3, 3.5, 4, 4.5]
    }

    phys_n_magi, crit_chance, crit_dmg = 0, 0, 0
    if rank == '저급':
        phys_n_magi = round(base[rank][idx] * \
                        (level ** 0.461), 3)
    elif rank == '일반':
        phys_n_magi = round(base[rank][idx] * \
                        (level ** 0.461), 2)
    else:
        phys_n_magi = round(base[rank][idx] * \
                        (level ** 0.461), 0)

    if rank in crit_chance_base.keys():
        if rank != '불멸':
            crit_chance = crit_chance_base[rank][idx] * \
                            min(level, 100)
        else:
            crit_chance = crit_chance_base[rank][idx]
    
    if rank in crit_dmg_base.keys():
        crit_dmg = crit_dmg_base[rank][idx] * \
                    level

    return {
        '공격력': phys_n_magi,
        '마력': phys_n_magi,
        '치명타 확률': crit_chance,
        '치명타 데미지': crit_dmg
    }

def get_spirit_effect(userdata):
    rank, idx = userdata['장착 정령']
    level = userdata['정령'][rank][idx]

    return calc_spirit_effect(rank, idx, level)
    
def calc_spirit_effect(rank, idx, level):
    base = {
        '일반': (5, 0.05),
        '일반_치명': (50, 0.5),
        '고급': (10, 0.1),
        '고급_치명': (150, 1.5),
        '영웅': (20, 0.2),
        '영웅_치명': (300, 3),
        '전설': (60, 0.6),
        '전설_치명': (900, 6)
    }

    hp, phys, magi, crit_dmg = 0, 0, 0, 0
    if idx == 0:
        hp = base[rank][0] + \
                level * base[rank][1] if level >= 0 else 0
    elif idx == 1:
        phys = base[rank][0] + \
                level * base[rank][1] if level >= 0 else 0
    elif idx == 2:
        magi = base[rank][0] + \
                level * base[rank][1] if level >= 0 else 0
    elif idx == 3:
        phys = base[rank][0] + \
                level * base[rank][1] if level >= 0 else 0
        magi = base[rank][0] + \
                level * base[rank][1] if level >= 0 else 0
        crit_dmg = base[rank + '_치명'][0] + \
                level * base[rank + '_치명'][1] if level >= 0 else 0

    return {
        '공격력': phys,
        '마력': magi,
        'HP 증가': hp,
        '치명타 데미지': crit_dmg
    }

def load_data(path):
    f = open(path, encoding='utf-16')
    dic = json.load(f)

    return dic

def save_data(path, data):
    fp = open(path, 'w', encoding='utf-16')
    json.dump(data, fp, indent=4)
    
def initial_load_data():
    if not os.path.isfile('data/userdata.json'):
        userdata = template
    else:
        userdata = load_data('data/userdata.json')

    return userdata

def keep_seven_digits(num):
    if num == 0:
        return num
    power_of_ten = int(math.log10(num)) + 1 - 7
    num = num // (10 ** power_of_ten) * (10 ** power_of_ten)

    return int(num)

def transform_korean_amount_string(num):
    maj_units = ['만 ', '억 ', '조 ', '경 ', '해 ', '자 ', '양 ', '구 ', '간 ', '정 ', '재 ', '극 ']
    units     = ['']
    for mm in maj_units:
        units.extend(['', '', ''])
        units.append(mm)
    
    list_amount = list(str(num)) # 라운딩한 숫자를 리스트로 바꾼다
    list_amount.reverse() # 일, 십 순서로 읽기 위해 순서를 뒤집는다
    
    str_result = '' # 결과
    num_len_list_amount = len(list_amount)
    
    for i in range(num_len_list_amount):
        str_num = list_amount[i]

        if num_len_list_amount >= 9 and i % 4 == 0 and ''.join(list_amount[i:i+4]) == '0000':
            continue

        if str_num == '0': 
            if i % 4 == 0: 
                str_result = str_num + units[i] + str_result 
            else:
                all_zero = True
                for j in range(i, (i // 4) * 4 + 4):
                    if len(list_amount) > (j+1) and list_amount[j] != '0':
                        all_zero = False

                if not all_zero:
                    str_result = str_num + units[i] + str_result

        else:
            str_result = str_num + units[i] + str_result 

    str_result = str_result.strip() 
    if len(str_result) == 0:
        return None

    return str_result 

def transform_english_amount_string(num, r=2):
    if num == '-':
        return '-'
    int_part = int(num)
    float_part = round(num - int_part, r)
    is_float = float_part != 0 and r != 0

    list_num = list(str(int_part)) 
    list_num += list(str(float_part))[1:] if is_float else []
    list_num.reverse()

    result = ''
    int_start = not is_float
    int_idx = 0
    for i in range(len(list_num)):
        if list_num[i] == '.':
            int_start = True
            result = list_num[i] + result
        elif is_float and not int_start:
            result = list_num[i] + result
        else:
            if int_idx % 3 == 0 and int_idx > 0:
                result = list_num[i] + ',' + result
            else:
                result = list_num[i] + result
            int_idx += 1

    return result

def check_int(num):
    if isinstance(num, str):
        try:
            num = float(num)
        except:
            return False

    if isinstance(num, int) or (isinstance(num, float) and num.is_integer()):
        return True

    return False
