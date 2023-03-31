from string import ascii_lowercase
from random import sample
from mob import *
import random
import copy
from armor import stack_buff
from stock import get_random_item
from db.models import HeroDB, WeaponDB

all_modules = {
    1: [25, "📥модуль силы"],
    2: [50, "📥модуль ловкости"],
    3: [50, "📥модуль удачи"],
    4: [50, "📥модуль точности"],
    5: [2, "📥модуль хп"],
}


class Hero:
    id = ""
    name = ""
    base_id = 0
    hp = 10
    max_hp = 10  # здоровье 1500
    force = 10  # cила 1300
    dexterity = 10  # ловкость 1200
    charisma = 10  # харизма 1200
    luck = 10  # удача 1200
    accuracy = 10  # меткость 1200
    weapon = None
    armor = None
    drone = None
    materials = 0
    coins = 0
    hungry = 0
    all_km = 0
    km = 0
    kl_pl = 0
    kl_mb = 0
    died = 0
    mob_fight = None
    in_dange = 0
    stock = None
    CNT_LOG = 10
    buffs = None
    km_buff = 0
    modul = 0 #11111 есть 5 модулей

    def go(self):
        self.km += 1
        self.all_km += 1
        self.hp += 2 if self.modul//int(pow(10, 4)) == 2 else 0
        if self.km_buff:
            self.km_buff -= 1
        else:
            for i in range(0, len(self.buffs)):
                self.buffs[i] = 0

    def calc_armor(self):
        ret = 0
        for i in range(0, 3):
            if self.armor[i]:
                ret += self.armor[i].arm
        return ret

    def get_stack(self, index):
        if not self.armor[0]:
            return 0
        if self.armor[0].type_stack == 0:
            return 0

        for i in range(1, 3):
            if self.armor[0].type_stack != self.armor[i].type_stack:
                return 0

        return stack_buff[self.armor[0].type_stack - 1][index]

    def get_module(self, i=0):
        if self.modul:
            modul = self.modul
            k = 1
            while modul % 10 != 2 or modul == 0 and k <= len(all_modules.keys()):
                modul //= 10
                k += 1
            if not i:
                return all_modules[k]
            elif i == k:
                return all_modules[k][0]
        return 0

    def get_force(self):
        return self.force + self.get_stack(0) + self.buffs[0] + self.get_module(1)

    def get_dexterity(self):
        return self.dexterity + self.get_stack(1) + self.buffs[1] + self.get_module(2)

    def get_luck(self):
        return self.luck + self.get_stack(2) + self.buffs[2] + self.get_module(3)

    def get_accuracy(self):
        return self.accuracy + self.get_stack(3) + self.buffs[3] + self.get_module(4)

    def get_str_modul(self):
        mod = self.get_module()
        return mod[1] if mod else "нет модуля"

    def get_str(self, val, i):
        out = str(val)
        stack = self.get_stack(i)
        mod = self.get_module(i+1)

        out += "+" + str(stack) if stack else ""
        out += "+" + str(mod) if mod else ""

        if self.buffs[i]:
            out += f"({self.buffs[i]})"
        return out

    def add_module(self):
        if self.modul != 0:
            k = len(str(self.modul)) + 1
            self.modul += int('1'*k) + int(pow(10, k-1))
        else:
            self.modul = 2

    def activate_module(self, i):#1 2 3 4..
        k = len(str(self.modul))
        if k<=i:
            self.modul = int('1'*k) + int(pow(10, i-1))

    def return_data(self):
        data = """
        👤{0} 
        ├ ❤ {1}/{2}  🍗{14}% | ⚔️{15} | 🛡 {16} 
        ├ 👣{17}
        ├ 💪{3} | 🤸🏽‍♂️{4} | 🗣{5} 
        ├ 👼{6} | 🎯{7}
        ├ {19}
        ├ 🗡{8}
        ├ 🪖{9}
        ├ 🧥{10}
        ├ 🧤{11}
        ├ 📦{12}
        └ 🕳{13} 👣👣{18}"""

        weapon = self.weapon.get_data_hero() if self.weapon else "нет оружия"
        armor = self.calc_armor()
        return data.format(self.name, round(self.hp), self.max_hp,
                           self.get_str(self.force, 0), self.get_str(self.dexterity, 1), self.charisma,
                           self.get_str(self.luck, 2), self.get_str(self.accuracy, 3), weapon,
                           self.arm_str(self.armor[0]),
                           self.arm_str(self.armor[1]), self.arm_str(self.armor[2]), self.materials,
                           self.coins, self.hungry, self.calc_attack(),
                           armor, self.km, self.all_km, self.get_str_modul())

    @staticmethod
    def generate_name():
        return "hero.." + "".join(sample(ascii_lowercase, 5))

    def arm_str(self, arm):
        return arm.get_data_hero() if arm else "нет брони"

    def calc_attack(self):
        if self.weapon:
            if self.force < 50:
                return (self.weapon.dmg + self.get_force())
            else:
                return (round(50 + self.weapon.dmg * pow(1.03, self.get_force() / 50)))
        else:
            return 1

    def get_hit_armor(self):
        for i in range(0, 3):
            if self.armor[i]:
                if self.armor[i].life <= 0:
                    self.armor[i] = None
                else:
                    self.armor[i].life -= 1

    def get_attack(self):
        if self.weapon and self.weapon.life > 0:
            self.weapon.life -= 0.5
            return self.calc_attack() * random.uniform(0.85, 1.15)
        else:
            self.weapon = None
            return 1

    def get_miss(self, dex):  # dex шанс уворота для героя 0.1%
        if dex - self.get_accuracy() < 0:
            return random.randint(0, 100) == 1
        return random.randint(0, 1000) < dex - self.get_accuracy()


    def calc_cost(self, val):
        out = 13 * val - 3 * self.charisma
        return 10 if out < 10 else round(13 * val - 3 * self.charisma);

    def select_mob(self):
        k = self.km // 5
        if k >= len(list_mobs):
            k = len(list_mobs) - 1
        list_m = list_mobs[k]
        i = random.randint(0, len(list_m) - 1)
        self.mob_fight = copy.copy(list_m[i])

    def learn_data(self):
        out = f"🕳Крышки: {self.coins}\n"
        out += f"💪Сила({self.force}): 🕳{self.calc_cost(self.force)}\n"
        out += f"🎯Меткость({self.accuracy}): 🕳{self.calc_cost(self.accuracy)}\n"
        out += f"🤸🏽‍♂️Ловкость({self.dexterity}): 🕳{self.calc_cost(self.dexterity)}\n"
        out += f"❤️Живучесть({self.max_hp}): 🕳{self.calc_cost(self.max_hp)}\n"
        out += f"🗣Харизма({self.charisma}): 🕳{10 * self.charisma}\n"
        out += f"👼Удача({self.luck}): 🕳{self.calc_cost(self.luck)}\n\n"
        out += "Выбирай желаемый навык:"
        return out

    def check_max(self):
        if self.hp > 1500:
            return "error"
        if self.force > 1300:
            return "error"
        if self.dexterity > 1200:
            return "error"
        if self.charisma > 1200:
            return "error"
        if self.accuracy > 1200:
            return "error"

    def is_first_hit(self, luck):
        return random.randint(0, 1000) - 500 < self.get_luck() - luck


    def make_header(self):
        buffed = ""
        if self.km_buff > 0:
            buffed = "*бафф*"
        return f"❤️ {round(self.hp)}\{self.max_hp} 🍗{self.hungry}% {buffed} 👣{self.km}\n"

    def attack_mob(self, mob: Mob, is_dange=False):
        out = f"Сражение с {mob.name} ❤{mob.hp}\n"
        armor = self.calc_armor()
        hp_mob = mob.hp
        cnt_attack = 0
        if mob.is_first_hit(luck=self.get_luck()):
            if mob.get_miss(self.get_dexterity()):
                out += "🌀моб промахнулся\n"
            else:
                dmg = mob.get_attack() - armor
                if dmg < 0:
                    dmg = 1
                    # out += "урон заблокирован\n"

                out += f"{mob.name} нанес тебе удар 💔-{round(dmg)}\n"
                self.hp -= dmg
                self.get_hit_armor()

        while round(self.hp) > 0:
            cnt_attack += 1
            if self.get_miss(mob.dexterity):
                if cnt_attack < self.CNT_LOG:
                    out += "👤Ты промахнулся\n"
            else:
                att = self.get_attack()
                if cnt_attack < self.CNT_LOG:
                    out += f"👤Ты ударил 💥{round(att)}\n"
                hp_mob -= att
                if hp_mob <= 0:
                    if cnt_attack > self.CNT_LOG:
                        out += " ......... ....... ....\n"
                    out += f"{mob.name} повержен\n"
                    coins = round(mob.calc_mob_coins(self.km))
                    mats = round(mob.calc_mob_mat(self.km))
                    if not is_dange:
                        self.coins += coins
                        self.materials += mats
                        out += f"получено 🕳 {coins} 📦 {mats}\n"
                        if random.randint(0, 20) == 7:
                            rkey, ritem = get_random_item()
                            out += f"✅✅вам выпал {ritem['name']}✅✅\n"
                            self.stock.add_stuff(rkey)
                    return out

            if mob.get_miss(self.get_dexterity()):
                if cnt_attack < self.CNT_LOG:
                    out += "🌀моб промахнулся\n"
            else:
                dmg = mob.get_attack() - armor
                if dmg < 0:
                    dmg = 1
                    # out += "урон заблокирован\n"
                if cnt_attack < self.CNT_LOG:
                    out += f"{mob.name} нанес тебе удар 💔-{round(dmg)}\n"
                self.hp -= dmg
                self.get_hit_armor()

        if cnt_attack > self.CNT_LOG:
            out += " ......... ....... ....\n"

        if round(self.hp) <= 0:
            out += "ты помер :((((((\n"
            self.died_hero()

        self.km = 0
        return out

    def died_hero(self):
        self.km = 0
        self.died += 1
        self.hp = 1
        self.mob_fight = None

    def log_hit(self):
        text_hit = ["сильно ударил",
                    "пунькнул по носу",
                    "переебал в щи",
                    "вмазал",
                    "хитро подкрался и врезал",
                    "отбежал и из укрытия атаковал",
                    "напал со спины",
                    "ебнул по почкам",
                    "переебал вертушкой",
                    "схватил за шею",
                    "сделал хитрый прием"]
        return text_hit[random.randint(0, len(text_hit) - 1)]

    def attack_player(self, hero):
        out = ""
        armor = self.calc_armor()
        armor_hero = hero.calc_armor()
        cnt_attack = 0
        if hero.is_first_hit(luck=self.get_luck()):
            if hero.get_miss(self.get_dexterity()):
                out += f"{hero.name} ❤️ {round(hero.hp)} 🌀промахнулся\n"
            else:
                dmg = hero.get_attack() - armor
                if dmg < 0:
                    dmg = 1
                    # out += "{0} ❤️ {1}  урон {2} заблокирован\n".format(hero.name, round(hero.hp), round(dmg))

                out += f"❤️ {hero.name} {round(hero.hp)} {self.log_hit()} 💔-{round(dmg)}\n"
                self.hp -= dmg
                self.get_hit_armor()

        while round(self.hp) > 0:
            cnt_attack += 1
            if self.get_miss(hero.get_dexterity()):
                if cnt_attack < self.CNT_LOG:
                    out += f"❤️ {round(self.hp)} {self.name} 🌀промахнулся\n"
            else:
                dmg = self.get_attack() - armor_hero
                if dmg < 0:
                    dmg = 1
                    # out += "❤️ {0} урон {1} заблокировал враг\n".format(round(self.hp), round(dmg))

                if cnt_attack < self.CNT_LOG:
                    out += f"❤️ {round(self.hp)} {self.name} {self.log_hit()} 💥{round(dmg)}\n"
                hero.hp -= dmg
                hero.get_hit_armor()
                if hero.hp <= 0:
                    if cnt_attack > self.CNT_LOG:
                        out += " ......... ....... ....\n"
                    out += f"{hero.name} повержен\n"
                    return out

            if hero.get_miss(self.get_dexterity()):
                if cnt_attack < self.CNT_LOG:
                    out += f"{hero.name} ❤️ {round(hero.hp)} 🌀промахнулся\n"
            else:
                dmg = hero.get_attack() - armor
                if dmg < 0:
                    dmg = 1
                    # out += "{0} ❤️ {1} урон {2} заблокирован\n".format(hero.name, round(hero.hp), round(dmg))

                if cnt_attack < self.CNT_LOG:
                    out += f"❤️ {round(hero.hp)} {hero.name} {self.log_hit()} 💔-{round(dmg)}\n"
                self.hp -= dmg
                self.get_hit_armor()

        if cnt_attack > self.CNT_LOG:
            out += " ......... ....... ....\n"

        if round(self.hp) <= 0:
            out += f"{self.name} помер :((((((\n"
            hero.kl_pl += 1
        return out

    def from_db(self, hero_db):
        self.base_id = hero_db.id
        self.name = hero_db.name
        self.id = hero_db.user_id
        self.hp = hero_db.hp
        self.max_hp = hero_db.max_hp
        self.force = hero_db.force
        self.dexterity = hero_db.dexterity
        self.charisma = hero_db.charisma
        self.luck = hero_db.luck
        self.accuracy = hero_db.accuracy
        self.materials = hero_db.materials
        self.coins = hero_db.coins
        self.hungry = hero_db.hungry
        self.km = hero_db.km
        self.all_km = hero_db.all_km
        self.modul = hero_db.modul


    def to_db(self):
        return HeroDB(name=self.name, user_id=self.id,
                      hp=self.hp, max_hp=self.max_hp,
                      force=self.force, dexterity=self.dexterity,
                      charisma=self.charisma, luck=self.luck,
                      accuracy=self.accuracy, materials=self.materials,
                      coins=self.coins, hungry=self.hungry, km=self.km, mob="", all_km=self.all_km, modul=self.modul)
