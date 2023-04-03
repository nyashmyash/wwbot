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
    5: [5, "📥модуль хп"],
    6: [10, "📥модуль дохода"]
}

text_mess_go = ["Вы обследовали разрушенный дом, но ничего интересного не обнаружили.",
                "Выбежала дикая собака, но вы на нее крикнули и она поджав хвост спряталась. Вы заметили проем в заборе.",
                "Пройдя около обугленных машин вы посмотрели на кости которые остались от водителя и пассажира. Страшное зрелище, лучше идти дальше.",
                "Вы увидели разрушенный дом, облазили его и там ничего интересного.",
                "Вы прошли по небольшому парку от которого остались только обугленные пеньки деревьев и искареженные статуи и аттракционы."
                "Пробираясь по чаще вы встретили мутанта, который забоялся вас и побежал по своим делам.",
                "Кто-то стал кричать за домом, возможно это опасный монстр или бандит приманивающий жертву, лучше идите дальше.",
                "Вы спокойно прошли по тропинке и отдохнули возле большого дерева",
                "Пройдя пару шагов на вас набросился какой-то псих, но получив по шее, он сбежал выкрикивая непонятные фразы.",
                "Вы зашли в остатки от банка, полазили по шкафчикам, но денег там давно нет.",
                "Насвистывая песенку вы подошли к школе, что там может быть интересного не понятно. Но вы решили заглянуть туда. Там только лазил свинокрыс и ел что-то.",
                "Возле вас просвистела пуля, это какой-то снайпер. Вы легли на землю и перекатились в кусты пережидая опасность.",
                "Гулять хорошо, но и отдыхать надо иногда. Вы перевели дух и выпили воды.",
                "Вы проголодались и сели в разрушенном кафе перекусить радиоактивной картошкой.",
                "Идя возле разрушенного дома, вы попробовали зайти в нутрь, но на вас набросился свинокрыс. Вы метко ему пробили бошку и исследовав дом побрели дальше",
                "Кажется машина которую вы нашли на ходу, можно поехать. Но когда двигатель завелся, он взорвался, туда залез какой-то опасный рад-таракан. Обидно((.",
                "Что-то издает крик. По звуку похоже на летающего мутанта, лучше ускориться и идти дальше.",
                "В дали вы увидели радиоактивного скунза, лучше надеть противогаз и держаться от него подальше.",
                "Где-то слышна стрельба, наверное это разборки местных банд. Надо свернуть.",
                "Вы услышали как квакает очень опасная мифическая жаба, наверное нажравшаяся рад тараканов и довольная. Лучше обойти место откуда ее слышно.",
                "Вы прошли по небольшому кладбищу, тут ничего интересного.",
                "Вы прошли по разрушающемуся мосту, несколько раз пришлось изрядно попрыгать чтобы не упасть.",
                "Думать вредно в пустоши, вдруг нападет голодный монстр. Так что надо быть на готове.",
                "Сложно сказать зачем нужна меткость, но если промахиваешься по свинокрысу очень обидно. Вы решили попрактиковать стрельбу по железным банкам.",
                "Опять какие-то разборки бандитов, но в итоге мутанты их всех сожрали. Сурово в пустоши.",
                "На вас уставился чужой, надо бежать, фиг знает как он сюда попал, вы стрельнули из бластера и спугнули его.",
                "Рад-пустошь страшное место, напасть может кто угодно. Надо идти дальше.",
                "Уже ночь, надо отдохнуть. Рядом заброшенный дом, обследуя его обнаружили целую кровать и легли поспать немного.",
                "Чертовые рад тараканы съели всю еду из рюкзака. Надо искать еду.",
                "За аптечками Вы зашли в больницу, но там давно ничего нет и все сгнило.",
                "Вы увидели автобус с людьми, а нет это не люди - это скелеты. А рядом снуют опасные собаки.",
                "За вами шел мутант, он напал но релексы не подвели и вы метким выстрелом снесли ему бошку.",
                "Зайдя в обгоревшую библиотеку, Вы обнаружили несколько уцелевших книг. 'Надо взять их с собой почитать' - подумали вы",
                "Лес казался бесконечным и страшным, но вы смело пробирались и надеялись, что местные радиоактивные волки вас не учуят.",
                "Вчера лил дождь, и сегодня, и, кажется, он будет бесконечным. Укрывшись в плащ палатку вы сидели и грустили.",
                "Пройдя немного вы заметили несколько рад собак, они растеразли бедного свинокрыса. Лучше обойти их стороной."

                ]


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
    modul = 0  # 11111 есть 5 модулей
    zone = 0
    km_heal = 0

    def go(self):
        self.km += 1
        self.all_km += 1
        # self.hp += 2 if self.modul//int(pow(10, 4)) == 2 else 0
        self.hp += self.get_module(5)
        if self.km_heal>0:
            self.km_heal -= 1
            self.hp += round(self.max_hp*0.05)
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
            if self.armor[i] and self.armor[0].type_stack != self.armor[i].type_stack:
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
        mod = self.get_module(i + 1)

        out += "+" + str(stack) if stack else ""
        out += "+" + str(mod) if mod else ""

        if self.buffs[i]:
            out += f"({self.buffs[i]})"
        return out

    def add_module(self):
        if self.modul != 0:
            k = len(str(self.modul)) + 1
            self.modul = int('1' * k) + int(pow(10, k - 1))
        else:
            self.modul = 2

    def activate_module(self, i):  # 1 2 3 4..
        if not self.modul:
            return "нет такого модуля\n"
        k = len(str(self.modul))
        if i <= k:
            self.modul = int('1' * k) + int(pow(10, i - 1))
            return f"{self.get_str_modul()} активирован\n"
        return "нет такого модуля\n"

    def return_data(self):
        data = """
        👤{0} 
        ├ ❤ {1}/{2}  🍗{14}% | ⚔️{15} | 🛡 {16} 
        ├ 👣{17}
        ├ 💪{3} | 🤸🏽‍♂️{4} | 🗣{5} 
        ├ 👼{6} | 🎯{7}
        ├ {19}
        ├ {20}
        ├ 🗡{8}
        ├ 🪖{9}
        ├ 🧥{10}
        ├ 🧤{11}
        ├ 📦{12}
        └ 🕳{13} 👣👣{18}"""

        weapon = self.weapon.get_data_hero() if self.weapon else "нет оружия"
        armor = self.calc_armor()
        drone = self.drone.get_drone_text_line() if self.drone else "нет дрона"
        return data.format(self.name, round(self.hp), self.max_hp,
                           self.get_str(self.force, 0), self.get_str(self.dexterity, 1), self.charisma,
                           self.get_str(self.luck, 2), self.get_str(self.accuracy, 3), weapon,
                           self.arm_str(self.armor[0]),
                           self.arm_str(self.armor[1]), self.arm_str(self.armor[2]), self.materials,
                           round(self.coins), self.hungry, self.calc_attack(),
                           armor, self.km, self.all_km, self.get_str_modul(), drone)

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
        r = 200 - self.km * 2 if self.km < 80 else 40
        if random.randint(0, 400) < r:
            k = self.km // 5
            if k >= len(list_mobs):
                k = len(list_mobs) - 1
            list_m = list_mobs[k]
            i = random.randint(0, len(list_m) - 1)
            self.mob_fight = copy.copy(list_m[i])
            if self.zone == 1:
                self.mob_fight.hp *= 2
                if ')' in self.mob_fight.name:
                    self.mob_fight.name = self.mob_fight.name.replace(")", "☢️)")
                else:
                    self.mob_fight.name += '☢'
                self.mob_fight.attack *= 2
                self.mob_fight.dexterity *= 2
                self.mob_fight.luck *= 2
                self.mob_fight.accuracy *= 2
                self.mob_fight.coins *= 2

            self.mob_fight.hp = round(self.mob_fight.hp * random.uniform(0.85, 1.15))

    def learn_data(self):
        out = f"🕳Крышки: {round(self.coins)}\n"
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
        buffed = "*бафф*" if self.km_buff > 0 else ""
        zoned = "☢" if self.zone == 1 else ""
        return f"{zoned}❤️ {round(self.hp)}\{self.max_hp} 🍗{self.hungry}% {buffed} 👣{self.km} \n"

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
                dmg = dmg if dmg > 0 else 1
                drone_hit = ""
                if self.drone:
                    drone_hit = self.drone.get_hit(dmg, armor)
                if drone_hit =="":
                    out += f"{mob.name} нанес тебе удар 💔-{round(dmg)}\n"
                    self.hp -= dmg
                    self.get_hit_armor()
                else:
                    out += drone_hit


        while round(self.hp) > 0:
            cnt_attack += 1
            if self.get_miss(mob.dexterity):
                if cnt_attack < self.CNT_LOG:
                    out += "👤Ты промахнулся\n"
            else:
                drone_hit = ""
                drone_dmg = 0
                if self.drone:
                    drone_dmg, drone_hit = self.drone.get_attack(mob)
                att = self.get_attack()
                if cnt_attack < self.CNT_LOG:
                    out += f"👤Ты ударил 💥{round(att)}\n"
                    out += drone_hit
                hp_mob -= att + drone_dmg
                if hp_mob <= 0:
                    if cnt_attack > self.CNT_LOG:
                        out += " ......... ....... ....\n"
                    out += f"{mob.name} повержен\n"
                    bonus_mod = self.get_module(6)
                    coins = round(mob.calc_mob_coins(self.km) * (1 + bonus_mod / 100))
                    mats = round(mob.calc_mob_mat(self.km) * (1 + bonus_mod / 100))
                    if not is_dange:
                        self.coins += coins
                        self.materials += mats
                        bonus_str = f"+{bonus_mod}%" if bonus_mod else ""
                        out += f"получено 🕳 {coins}{bonus_str} 📦 {mats}{bonus_str}\n"
                        chanse = 0
                        if not self.zone:
                            chanse = random.randint(0, 20)
                        else:
                            chanse = random.randint(0, 7)
                        if chanse == 5:
                            rkey, ritem = get_random_item()
                            out += f"✅✅вам выпал {ritem['name']} /ustf_{rkey}✅✅\n"
                            self.stock.add_stuff(rkey)
                        if self.km >= 30 and self.zone == 1:
                            chanse = random.randint(0, 7)
                            if chanse == 5:
                                rkey, ritem = get_random_item(True)
                                out += f"💉💉вам выпал {ritem['name']} /ustf_{rkey}💉💉\n"
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
            if self.zone == 1:
                out += f"потеряно: 🕳 {round(self.coins * 0.5)}"
                self.coins *= 0.5
            else:
                if self.km >= 30:
                    out += f"потеряно: 🕳 {round(self.coins * 0.25)}"
                    self.coins = round(self.coins*0.75)

            self.died_hero()

        self.km = 0
        return out

    def died_hero(self):
        self.km = 0
        self.died += 1
        self.hp = 1
        self.zone = 0
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
                drone_hit = ""
                if self.drone:
                    drone_hit = self.drone.get_hit(dmg, armor)
                if drone_hit == "":
                    out += f"❤️ {hero.name} {round(hero.hp)} {self.log_hit()} 💔-{round(dmg)}\n"
                    self.hp -= dmg
                    self.get_hit_armor()
                else:
                    out += drone_hit

        while round(self.hp) > 0:
            cnt_attack += 1
            if self.get_miss(hero.get_dexterity()):
                if cnt_attack < self.CNT_LOG:
                    out += f"❤️ {round(self.hp)} {self.name} 🌀промахнулся\n"
            else:
                drone_hit = ""
                drone_dmg = 0
                if self.drone:
                    drone_dmg, drone_hit = self.drone.get_attack(hero)

                dmg = self.get_attack() - armor_hero
                if dmg < 0:
                    dmg = 1
                    # out += "❤️ {0} урон {1} заблокировал враг\n".format(round(self.hp), round(dmg))

                if cnt_attack < self.CNT_LOG:
                    out += f"❤️ {round(self.hp)} {self.name} {self.log_hit()} 💥{round(dmg)}\n"
                    out += drone_hit

                hero.hp -= dmg + drone_dmg
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
        self.zone = hero_db.zone

    def to_db(self):
        return HeroDB(name=self.name, user_id=self.id,
                      hp=self.hp, max_hp=self.max_hp,
                      force=self.force, dexterity=self.dexterity,
                      charisma=self.charisma, luck=self.luck,
                      accuracy=self.accuracy, materials=self.materials,
                      coins=self.coins, hungry=self.hungry, km=self.km, mob="",
                      all_km=self.all_km, modul=self.modul, zone=self.zone)
