from string import ascii_lowercase
from random import sample
from mob import *
import random
import copy
from armor import stack_buff, armor_all
from weapon import weapons_all
from stock import get_random_item, used_items
from db.models import HeroDB, WeaponDB
from drone import all_drones, perk_drone_list

all_modules = {
    1: [25, "📥модуль силы"],
    2: [100, "📥модуль ловкости"],
    3: [50, "📥модуль удачи"],
    4: [50, "📥модуль точности"],
    5: [5, "📥модуль хп"],
    6: [15, "📥модуль дохода"],
    7: [5, "📥модуль вампиризма"]
}
perk_dex_list = [1.2, 1.5, 1.8, 2.3]
perk_arm_list = [1.2, 1.5, 1.7, 2]
perk_luck_list = [1.2, 1.4, 1.6, 2]
perk_force_list = [1.2, 1.3, 1.4, 1.5]
perk_accur_list = [1.2, 1.4, 1.6, 2]


text_mess_go = ["Вы обследовали разрушенный дом, но ничего интересного не обнаружили.",
                "Выбежала дикая собака, но вы на нее крикнули и она поджав хвост спряталась. Вы заметили проем в заборе.",
                "Пройдя около обугленных машин, вы посмотрели на кости, которые остались от водителя и пассажира. Страшное зрелище, лучше идти дальше.",
                "Вы увидели разрушенный дом, облазили его и там ничего интересного.",
                "Вы прошли по небольшому парку, от которого остались только обугленные пеньки деревьев и искареженные статуи и аттракционы."
                "Пробираясь по чаще вы встретили мутанта, который забоялся вас и побежал по своим делам.",
                "Кто-то стал кричать за домом, возможно, это опасный монстр или бандит приманивающий жертву, лучше идите дальше.",
                "Вы спокойно прошли по тропинке и отдохнули возле большого дерева",
                "Пройдя пару шагов, на вас набросился какой-то псих, но получив по шее, он сбежал выкрикивая непонятные фразы.",
                "Вы зашли в остатки от банка, полазили по шкафчикам, но денег там давно нет.",
                "Насвистывая песенку вы подошли к школе, что там может быть интересного не понятно. Но вы решили заглянуть туда. Там только лазил свинокрыс и ел что-то.",
                "Возле вас просвистела пуля, это какой-то снайпер. Вы легли на землю и перекатились в кусты пережидая опасность.",
                "Гулять хорошо, но и отдыхать надо иногда. Вы перевели дух и выпили воды.",
                "Вы проголодались и сели в разрушенном кафе перекусить радиоактивной картошкой.",
                "Идя возле разрушенного дома, вы попробовали зайти в нутрь, но на вас набросился свинокрыс. Вы метко ему пробили бошку и исследовав дом побрели дальше",
                "Кажется, машина которую вы нашли на ходу, можно поехать. Но когда двигатель завелся, он взорвался, туда залез какой-то опасный рад-таракан. Обидно.",
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
            "сделал хитрый прием",
            "положил на лопатки",
            "послал на хуй",
            "взорвал гранату",
            "заехал в голову",
            "атаковал в спину",
            "прописал оплеуху",
            "дал подзатыльник",
            "ошарашил метким выстрелом",
            "прописал жесткий удар",
            "пнул ногой в спину",
            "огрел по голове",
            "саданул метко в корпус",
            "припечатал к стене",
            ]

text_hit_mob = ["выстрелил твари в морду",
                "отстрелил щупальце",
                "вмазал по морде",
                "ударил в корпус",
                "наступил на голову",
                "размазал кишки",
                "в прыжке выстрелил и попал",
                "из укрытия выстрелил",
                "хитро подкрался и переебал",
                "оторвал руку",
                "поймал в ловушку",
                "ударил с разворота по морде",
                "деморализировал тварь",
                "накинулся и въебал",
                "разломал челюсть твари",
                "дал пинок",
                "быстро контратаковал",
                "закинул гранату",
                "скинул с обрыва",
                "заехал по морде",
                "атаковал дерзко",
                ]


text_hero_mis = ["смешно упал с оружием",
                 "подскользнулся на ровном месте",
                 "упал в яму",
                 "впал в ступор",
                 "дрогнул и промахнулся",
                 "промахнулся в упор",
                 "меткость качай",
                 "глупо махал руками",
                 "выстрелил в дерево",
                 "считал ворон",
                 "просчитался и промазал",
                 "смазал выстрел",
                 "оружие дало осечку",
                 "не смог ровно держать пуху"]


text_hero_dead = ["умер, стюпид д*б",
                  "ахаха, нуб",
                  "ну умер и умер",
                  "ну ничего, воскресят",
                  "жить будешь, в лагере реанимируют",
                  "F",
                  "R.I.P.",
                  "смерть это только начало",
                  "жизнь это боль, смерть это отсутсвие боли",
                  "в загробном мире ты вечен, но рано еще хоронить, в лагере поднимут"]

class Band:
    name = ""
    note = ""
    points = 0
    user_id = 0



class Hero:
    id = ""
    band_id = 0
    band_name = ""
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
    CNT_LOG = 30
    buffs = None
    km_buff = 0
    modul = 0  # 11111 есть 5 модулей
    zone = 0
    km_heal = 0
    dzen = 0
    mobs = None
    perks = '0'*6
    arm_clc = 0
    text_out_boss = ""
    go_boss = 0
    ef_chat = None
    danges = None

    def go(self, reverse=False) -> None:
        if reverse:
            if self.km < 1:
                return
            self.km -= 1
        else:
            self.km += 1
        self.all_km += 1

        if self.km_heal > 0:
            self.km_heal -= 1
            self.hp += round(self.max_hp * 0.05)

        heal_hp = round(self.max_hp * self.get_module(5) / 100)
        if heal_hp:
            self.hp += heal_hp
            if self.hp > self.max_hp:
                self.hp = self.max_hp

        if self.km_buff:
            self.km_buff -= 1
        else:
            for i in range(0, len(self.buffs)):
                self.buffs[i] = 0

    def get_name(self) -> str:
        return self.name

    def calc_armor(self, use_perk:bool = False) -> int:
        ret = 0
        for i in range(0, 3):
            if self.armor[i]:
                ret += self.armor[i].arm
            if self.armor[i].mod:
                ret += used_items[self.armor[i].mod]["armor"]
        if use_perk and self.perks[1]!='0':
            ret *= perk_arm_list[int(self.perks[1])-1]
        return round(ret)

    def get_stack(self, index: int) -> int:
        if not self.armor[0]:
            return 0
        if self.armor[0].type_stack == 0:
            return 0

        perks = ["force", "dexterity", "luck", "accuracy"]
        eff = 0
        if self.weapon and self.weapon.mod:
            eff += used_items[self.weapon.mod].get(perks[index], 0)
        for i in range(0, 3):
            if self.armor[i] and self.armor[i].mod:
                eff += used_items[self.armor[i].mod].get(perks[index], 0)

        for i in range(1, 3):
            if self.armor[i] and self.armor[0].type_stack != self.armor[i].type_stack:
                return eff

        return stack_buff[self.armor[0].type_stack - 1][index] + eff

    def get_in_dzen(self) -> int:
        return self.dzen - self.get_dzen_lvl() * 500000

    def get_dzen_lvl(self) -> int:
        return self.dzen // 500000

    def get_coins_to_dzen(self) -> int:
        return (self.get_dzen_lvl() + 1) * 500000

    # def get_perk(self, i: int) -> int:
    #     perks = list(self.perks)
    #     return int(perks[i])

    def get_module(self, i: int = 0, value: int = 0) -> int:
        k, mod = self.get_act_modul()
        if k != i:
            return 0
        if k in [2, 3, 4]:
            return 50 if value * 0.1 < 50 else round(value * 0.1)
        if k == 1:
            return 25 if value * 0.05 < 25 else round(value * 0.05)

        return mod[0]

    def get_force(self, use_perk: bool = False) -> int:
        force = self.force
        if use_perk and self.perks[0] != '0':
            force = force * perk_force_list[int(self.perks[0]) - 1]

        return force + self.get_stack(0) + self.buffs[0] + self.get_module(1, self.force)

    def get_dexterity(self, use_perk: bool = False) -> int:
        dexterity = self.dexterity
        if use_perk and self.perks[2] != '0':
            dexterity *= perk_dex_list[int(self.perks[2]) - 1]
        return dexterity + self.get_stack(1) + self.buffs[1] + self.get_module(2, self.dexterity)

    def get_luck(self, use_perk: bool = False) -> int:
        luck = self.luck
        if use_perk and self.perks[5] != '0':
            luck *= perk_luck_list[int(self.perks[5]) - 1]
        return luck + self.get_stack(2) + self.buffs[2] + self.get_module(3, self.luck)

    def get_accuracy(self) -> int:
        return self.accuracy + self.get_stack(3) + self.buffs[3] + self.get_module(4, self.accuracy)

    def get_act_modul(self) -> (int, list):
        if self.modul:
            modul = self.modul
            k = 1
            while modul % 10 != 2 or modul == 0 and k <= len(all_modules.keys()):
                modul //= 10
                k += 1
            return k, all_modules[k]
        else:
            return 0, None

    def get_str_modul(self) -> str:
        k, mod = self.get_act_modul()
        if k:
            return mod[1]
        else:
            return "нет модуля"

    def get_str(self, val: int, i: int) -> str:
        out = str(val)
        stack = self.get_stack(i)
        mod = self.get_module(i + 1, val)

        if stack > 0:
            out += "+" + str(stack)
        elif stack < 0:
            out += str(stack)

        out += "+" + str(mod) if mod else ""

        if self.buffs[i]:
            out += f"({self.buffs[i]})"
        return out

    def add_module(self):
        if self.modul != 0:
            k = len(str(self.modul)) + 1
            self.modul = int("1" * k) + int(pow(10, k - 1))
        else:
            self.modul = 2

    def activate_module(self, i: int) -> str:  # 1 2 3 4..
        if not self.modul:
            return "нет такого модуля\n"
        k = len(str(self.modul))
        if i <= k:
            self.modul = int("1" * k) + int(pow(10, i - 1))
            return f"{self.get_str_modul()} активирован\n"
        return "нет такого модуля\n"

    def ret_cnt_perks(self) -> int:
        out = 0
        for i in self.perks:
            out += int(i)
        return out

    def get_bm(self) -> int:
        return self.max_hp + self.force + self.accuracy + self.luck + self.dexterity + self.charisma

    def free_perks(self) -> int:
        return 1 + self.get_bm()//1250 - self.ret_cnt_perks()

    def inc_perk(self, ind: int) -> str:
        lvls = [250, 550, 850, 1150]
        if int(self.perks[ind]) >= 4:
            return "нельзя увиличить перк!!"
        if ind == 0 and self.force < lvls[int(self.perks[0])]:
            return f"надо увеличить силу до {lvls[int(self.perks[0])]}"
        if ind == 1 and self.max_hp < lvls[int(self.perks[1])]:
            return f"надо увеличить хп до {lvls[int(self.perks[1])]}"
        if ind == 2 and self.dexterity < lvls[int(self.perks[2])]:
            return f"надо увеличить ловку до {lvls[int(self.perks[2])]}"
        if ind == 3 and self.accuracy < lvls[int(self.perks[3])]:
            return f"надо увеличить меткость до {lvls[int(self.perks[3])]}"
        if ind == 4 and self.charisma < lvls[int(self.perks[4])]:
            return f"надо увеличить харизму до {lvls[int(self.perks[4])]}"
        if ind == 5 and self.luck < lvls[int(self.perks[5])]:
            return f"надо увеличить удачу до {lvls[int(self.perks[5])]}"

        lst_perks = list(self.perks)
        lst_perks[ind] = str(int(lst_perks[ind]) + 1)
        self.perks = ''.join(lst_perks)

        return "перк успешно увеличен"

    def return_perks(self) -> str:
        text_data = ["силач (увеличение силы)",
                     "бронированный (усил-ние брони)",
                     "ловкач (увеличение ловкости)",
                     "меткий (разброс урона значительно увеличивается)",
                     "харизматичный (эффективность дронов)",
                     "удачливый (увеличение шанса ударить первым и шанс регенерации 30% от хп)"]
        data = "ваши умения:\n"
        cnt_free = self.free_perks()
        if cnt_free > 0:
            data += f"у вас есть свободные очки: {cnt_free}\n"
            data += "список куда можно использовать очки:\n"
            data += f"/perk_force  {text_data[0]}\n"
            data += f"/perk_arm  {text_data[1]}\n"
            data += f"/perk_dex  {text_data[2]}\n"
            data += f"/perk_accur  {text_data[3]}\n"
            data += f"/perk_char  {text_data[4]}\n"
            data += f"/perk_luck  {text_data[5]}\n"
        else:
            data += f"количество bm до перка {1250*self.ret_cnt_perks() - self.get_bm()}\n"

        if self.perks[0] != '0':
            data += f"{text_data[0]}  {self.perks[0]}, коэф {perk_force_list[int(self.perks[0])-1]}\n"
        if self.perks[1] != '0':
            data += f"{text_data[1]}  {self.perks[1]}, коэф {perk_arm_list[int(self.perks[1])-1]}\n"
        if self.perks[2] != '0':
            data += f"{text_data[2]}  {self.perks[2]}, коэф {perk_dex_list[int(self.perks[2]) - 1]}\n"
        if self.perks[3] != '0':
            data += f"{text_data[3]}  {self.perks[3]}, коэф {perk_accur_list[int(self.perks[3]) - 1]}\n"
        if self.perks[4] != '0':
            data += f"{text_data[4]}  {self.perks[4]}, коэф {perk_drone_list[int(self.perks[4]) - 1]}\n"
        if self.perks[5] != '0':
            data += f"{text_data[5]}  {self.perks[5]}, коэф {perk_arm_list[int(self.perks[5]) - 1]}\n"
        if data == "ваши умения:\n":
            return "у вас нет умений!"

        return data

    def return_data(self) -> str:
        data = """
        👤{0} {21}
        ├ 🤟{22}       умения /perks
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

        dzen = f"🏵{self.get_dzen_lvl()}" if self.get_dzen_lvl() else ""
        weapon = self.weapon.get_data_hero() if self.weapon else "нет оружия"
        armor = self.calc_armor()
        drone = self.drone.get_drone_text_line() if self.drone else "нет дрона"
        band_name = self.band_name + "   /band" if self.band_name not in ["введите имя банды","", None] else "нет банды"
        return data.format(self.name, round(self.hp), self.max_hp,
                           self.get_str(self.force, 0), self.get_str(self.dexterity, 1), self.charisma,
                           self.get_str(self.luck, 2), self.get_str(self.accuracy, 3), weapon,
                           self.arm_str(self.armor[0]),
                           self.arm_str(self.armor[1]), self.arm_str(self.armor[2]), self.materials,
                           round(self.coins), self.hungry, self.calc_attack(),
                           armor, self.km, self.all_km, self.get_str_modul(), drone, dzen, band_name)

    #@staticmethod
    #def generate_name() -> str:
    #    return "hero.." + "".join(sample(ascii_lowercase, 5))

    def arm_str(self, arm) -> str:
        return arm.get_data_hero() if arm else "нет брони"

    def calc_attack(self, use_force=False) -> int:
        if self.weapon:
            dmg = self.weapon.dmg
            if self.weapon.mod:
                dmg += used_items[self.weapon.mod]["damage"]
            if self.force < 50:
                return round(dmg + self.get_force(use_force))
            else:
                return round(50 + dmg * pow(1.03, self.get_force(use_force) / 50))
        else:
            return 1

    def get_hit_armor(self) -> None:
        for i in range(0, 3):
            if self.armor[i]:
                if self.armor[i].life <= 0:
                    self.armor[i] = None
                else:
                    self.armor[i].life -= 1

    def get_attack(self, use_perks: bool = False, test: bool = False) -> int:
        if self.weapon and self.weapon.life > 0:
            if not test:
                self.weapon.life -= 0.5
            if use_perks and self.perks[3] != '0':
                return round(self.calc_attack(use_perks) * random.uniform(0.85, 1.15*perk_accur_list[int(self.perks[3])-1]))
            else:
                return round(self.calc_attack(use_perks) * random.uniform(0.85, 1.15))
        else:
            self.weapon = None
            return 1

    def get_miss(self, dex: int) -> bool:
        acc = self.get_accuracy()
        k = 4 if dex / acc >= 4 else dex / acc
        return random.randint(0, 1000) < 200 * k

    def calc_cost(self, val: int) -> int:
        out = 13 * val - 3 * self.charisma
        return 10 if out < 10 else round(13 * val - 3 * self.charisma)

    def sel_mob_from_zone(self, mobs_zone: list) -> None:
        r = random.randint(0, 100)
        k = len(mobs_zone) - 1
        while k > 0 and r % k != 0:
            k -= 1
        self.mob_fight = copy.copy(mobs_zone[k])

    def select_mob(self) -> None:
        if self.zone == 3 or self.zone == 4:
            r = 200
        else:
            r = round(200 - self.km * 1.5) if self.km < 80 else 80
        if random.randint(0, 400) < r:
            if self.zone == 3:
                self.sel_mob_from_zone(list_mob_clown_zone)
            elif self.zone == 4:
                #self.sel_mob_from_zone(list_mob_painkiller_zone)
                i = random.randint(0, len(list_mob_painkiller_zone) - 1)
                self.mob_fight = copy.copy(list_mob_painkiller_zone[i])
            else:
                k = self.km // 5
                if k >= len(list_mobs):
                    k = len(list_mobs) - 1
                if self.zone == 2:
                    list_m = list_mobs[k+5]
                else:
                    list_m = list_mobs[k]
                i = random.randint(0, len(list_m) - 1)
                self.mob_fight = copy.copy(list_m[i])

            if 3 > self.zone > 0:
                self.mob_fight.hp *= 2
                if self.zone == 1:
                    if ")" in self.mob_fight.get_name():
                        self.mob_fight.name = self.mob_fight.get_name().replace(")", "☢️)")
                    else:
                        self.mob_fight.name = self.mob_fight.get_name() + "☢"
                elif self.zone == 2:
                    self.mob_fight.coins *= 1.5
                    if ")" in self.mob_fight.get_name():
                        self.mob_fight.name = self.mob_fight.get_name().replace(")", "☠)")
                    else:
                        self.mob_fight.name = self.mob_fight.get_name() + "☠"

                self.mob_fight.attack *= 2
                self.mob_fight.dexterity *= 2
                self.mob_fight.luck *= 2
                self.mob_fight.accuracy *= 2
                self.mob_fight.coins *= 2

            self.mob_fight.hp = round(self.mob_fight.hp * random.uniform(0.85, 1.15))
            if not self.in_dange and random.randint(0, 20) == 5:
                self.mob_fight.enfect = True
                self.mob_fight.name += " 🦠🦠🦠"

    def learn_data(self) -> str:
        out = f"🕳Крышки: {round(self.coins)}\n"
        out += f"💪Сила({self.force}): 🕳{self.calc_cost(self.force)}\n"
        out += f"🎯Меткость({self.accuracy}): 🕳{self.calc_cost(self.accuracy)}\n"
        out += f"🤸🏽‍♂️Ловкость({self.dexterity}): 🕳{self.calc_cost(self.dexterity)}\n"
        out += f"❤️Живучесть({self.max_hp}): 🕳{self.calc_cost(self.max_hp)}\n"
        out += f"🗣Харизма({self.charisma}): 🕳{10 * self.charisma}\n"
        out += f"👼Удача({self.luck}): 🕳{self.calc_cost(self.luck)}\n\n"
        out += "Выбирай желаемый навык:"
        return out

    def inc_hp(self) -> bool:
        return True if self.hp < 1500 + self.get_dzen_lvl()*50 else False

    def inc_force(self) -> bool:
        return True if self.force < 1300 + self.get_dzen_lvl() * 50 else False

    def inc_dex(self) -> bool:
        return True if self.dexterity < 1200 + self.get_dzen_lvl() * 50 else False

    def inc_char(self) -> bool:
        return True if self.charisma < 1200 + self.get_dzen_lvl() * 50 else False

    def inc_acc(self) -> bool:
        return True if self.accuracy < 1200 + self.get_dzen_lvl() * 50 else False

    def inc_luck(self) -> bool:
        return True if self.luck < 1200 + self.get_dzen_lvl() * 50 else False

    def is_first_hit(self, luck: int, use_perk: bool = False) -> int:
        return random.randint(0, 1000) - 500 < self.get_luck(use_perk) - luck

    def make_header(self) -> str:
        buffed = "*бафф*" if self.km_buff > 0 else ""
        zoned = "☢" if self.zone == 1 else ""
        zoned = "☠️" if self.zone == 2 else zoned
        zoned = "🤡️" if self.zone == 3 else zoned
        zoned = "🔪" if self.zone == 4 else zoned
        return f"{zoned}❤️ {round(self.hp)}\{self.max_hp} 🍗{self.hungry}% {buffed} 👣{self.km} \n"

    def attack_boss_1rnd(self, mob: Mob, test: bool = False) -> str:
        out = ""
        armor = self.calc_armor()
        is_first = True
        if random.randint(0, 1) == 1:
            is_first = False

        if is_first:
            if self.get_miss(mob.dexterity):
                if not test:
                    out += f"❤️ {round(self.hp)} {self.get_name()} ➰ {self.log_hit(text_hero_mis)}\n"
            else:
                drone_hit = ""
                drone_dmg = 0
                if self.drone:
                    drone_dmg, drone_hit = self.drone.get_attack(mob, self.perks)
                att = self.get_attack(test=test)
                if self.calc_attack() > 250:
                    att = round(250 * random.uniform(0.85, 1.15))

                if not test:
                    out += f"❤️ {round(self.hp)} {self.get_name()} {self.log_hit(text_hit_mob)} 💥{round(att)}\n"
                    out += drone_hit
                mob.hp -= att + drone_dmg
            if mob.hp <= 0:
                if not test:
                    out += f"{mob.get_name()} повержен\n"
                return out
        else:
            if mob.get_miss(self.get_dexterity()):
                if not test:
                    out += f"❤️ {round(mob.hp)} 🌀{mob.get_name()} {self.log_hit(text_mob_mis)}\n"
            else:
                if armor > 100:
                    armor = 100
                if self.max_hp > 400:
                    armor = 0
                dmg = mob.get_attack() - armor

                dmg = dmg if dmg > 0 else 1
                drone_hit = ""
                if self.drone:
                    drone_hit = self.drone.get_hit(dmg, self.perks, test=test)
                    if self.drone.hp <= 0:
                       self.drone = None
                if drone_hit == "":
                    if not test:
                        out += f"❤️ {round(mob.hp)} {mob.get_name()} {mob.log_hit_mob()} {self.get_name()} 💔-{round(dmg)}\n"
                    self.hp -= dmg
                    if not test:
                        self.get_hit_armor()
                else:
                    out += drone_hit
        return out

    @staticmethod
    def attack_boss(list_heroes: list, boss: Mob, test: bool = False, boss_id: int = 0) -> None:
        out = ""
        boss_round = 0
        cnt_dead = 0
        while boss.hp > 0:
            if boss_round > 100:
                break
            boss_round += 1
            if not test:
                out += f"\nраунд {boss_round}\n❤️ {boss.hp} босс {boss.name}\n"
            for i in range(0, len(list_heroes)):
                if list_heroes[i].go_boss == boss_id:
                    out += list_heroes[i].attack_boss_1rnd(boss, test)
                    if boss.hp <= 0:
                        break
                    if list_heroes[i].hp < 0:
                        out_new = out
                        out_new += f"{list_heroes[i].get_name()} {list_heroes[i].log_hit(text_hero_dead)}\n"
                        out_new += f"потеряно: 🕳 {round(list_heroes[i].coins * 0.5)}\n"
                        list_heroes[i].coins *= 0.5
                        list_heroes[i].text_out_boss = out_new
                        list_heroes[i].go_boss = 0
                        cnt_dead += 1
                        out += f"💀{list_heroes[i].name}\n"

            if boss.hp <= 0:
                #out += f"босс повержен игроком {list_heroes[i].name}\n"
                coins = round(boss.calc_mob_coins(boss.km)) * 3
                mats = round(boss.calc_mob_mat(boss.km)) * 3
                for j in range(0, len(list_heroes)):
                    if list_heroes[j].go_boss == boss_id:
                        out_new = out
                        list_heroes[j].coins += coins
                        list_heroes[j].materials += mats
                        out_new += f"получено 🕳 {coins} 📦 {mats}\n"
                        rkey, ritem = get_random_item(True)
                        out_new += f"💉💉вам выпал {ritem['name']} /ustf_{rkey}💉💉\n"
                        list_heroes[j].stock.add_stuff(rkey)
                        list_heroes[j].text_out_boss = out_new
                        list_heroes[j].go_boss = 0
                break

            if cnt_dead == len(list_heroes):
                break

    def attack_mob_pvp(self, mob: Mob) -> str:
        out = f"❤️ {round(self.hp)} {self.get_name()} vs {mob.get_name()} ❤{round(mob.hp)}\n"
        armor = self.calc_armor()
        hp_mob = mob.hp
        cnt_attack = 0
        is_first = True
        if mob.is_first_hit(luck=self.get_luck()):
            is_first = False

        while round(self.hp) > 0:
            cnt_attack += 1
            if is_first:
                is_first = False
                if self.get_miss(mob.dexterity):
                    if cnt_attack < self.CNT_LOG:
                        out += f"❤️ {round(self.hp)} {self.get_name()} ➰ {self.log_hit(text_hero_mis)}\n"
                else:
                    drone_hit = ""
                    drone_dmg = 0
                    if self.drone:
                        drone_dmg, drone_hit = self.drone.get_attack(mob, self.perks)
                    att = self.get_attack()
                    if cnt_attack < self.CNT_LOG:
                        out += f"❤️ {round(self.hp)} {self.get_name()} {self.log_hit(text_hit_mob)} 💥{round(att)}\n"
                        out += drone_hit
                    hp_mob -= att + drone_dmg
                    if hp_mob <= 0:
                        if cnt_attack > self.CNT_LOG:
                            out += " ......... ....... ....\n"
                        self.enfect_hero(mob)
                        out += f"{mob.get_name()} повержен\n"
                        return out
            else:
                is_first = True
                if mob.get_miss(self.get_dexterity()):
                    out += f"🌀{mob.get_name()} {self.log_hit(text_mob_mis)}\n"
                else:
                    dmg = mob.get_attack() - armor
                    dmg = dmg if dmg > 0 else 1
                    drone_hit = ""
                    if self.drone:
                        drone_hit = self.drone.get_hit(dmg, self.perks)
                        if self.drone.hp <= 0:
                            self.drone = None
                    if drone_hit == "":
                        out += f"{mob.get_name()} {mob.log_hit_mob()} {self.get_name()} 💔-{round(dmg)}\n"
                        self.hp -= dmg
                        self.get_hit_armor()
                    else:
                        out += drone_hit

        if cnt_attack > self.CNT_LOG:
            out += " ......... ....... ....\n"

        if round(self.hp) <= 0:
            out += f"{self.get_name()} {self.log_hit(text_hero_dead)}\n"
            self.died_hero()
        self.km = 0
        return out

    def enfect_hero(self, mob: Mob) -> None:
        if mob.enfect:
            i = random.randint(0, 3)
            if i == 0:
                self.buffs[i] = -self.force // 2
            elif i == 1:
                self.buffs[i] = -self.dexterity // 2
            elif i == 2:
                self.buffs[i] = -self.luck // 2
            elif i == 3:
                self.buffs[i] = -self.accuracy // 2
            self.km_buff = random.randint(15, 25)

    def attack_mob(self, mob: Mob, is_dange=False) -> str:
        out = f"Сражение с {mob.get_name()} ❤{mob.hp}\n"
        armor = self.calc_armor()
        hp_mob = mob.hp
        cnt_attack = 0
        is_first = True
        if mob.is_first_hit(luck=self.get_luck()): #первый ли удар моба
            is_first = False

        miss_text = ""
        while round(self.hp) > 0:
            cnt_attack += 1
            if is_first:
                is_first = False
                if self.get_miss(mob.dexterity): #начинаем бить
                    if cnt_attack < self.CNT_LOG:
                        miss_text = f"👤Ты ➰ {self.log_hit(text_hero_mis)}\n"
                else:
                    out += miss_text
                    miss_text = ""
                    drone_hit = ""
                    drone_dmg = 0
                    if self.drone:
                        drone_dmg, drone_hit = self.drone.get_attack(mob, self.perks)
                    att = self.get_attack()
                    regen_mod = self.get_module(7)
                    regen_str = ""
                    if regen_mod:
                        if att < hp_mob:
                            self.hp += att*regen_mod/100
                            regen_str = f"❤+{round(att*regen_mod/100)}"
                        else:
                            self.hp += hp_mob * regen_mod / 100
                            regen_str = f"❤+{round(hp_mob*regen_mod/100)}"

                    if cnt_attack < self.CNT_LOG:
                        out += f"❤ {round(self.hp)} 👤Ты {self.log_hit(text_hit_mob)} 💥{round(att)} {regen_str}\n"
                        out += drone_hit
                    hp_mob -= att + drone_dmg
                    if hp_mob <= 0:
                        if cnt_attack >= self.CNT_LOG:
                            out += " ......... ....... ....\n"
                        out += f"{mob.get_name()} повержен\n"
                        bonus_mod = self.get_module(6)
                        coins = round(mob.calc_mob_coins(self.km) * (1 + bonus_mod / 100))
                        mats = round(mob.calc_mob_mat(self.km) * (1 + bonus_mod / 100))
                        if not is_dange:
                            self.enfect_hero(mob)
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

                            if 4 > self.zone >= 2 or (self.km >= 30 and self.zone == 1):
                                chanse = random.randint(0, 7)
                                if chanse == 5:
                                    rkey, ritem = get_random_item(True)
                                    out += f"💉💉вам выпал {ritem['name']} /ustf_{rkey}💉💉\n"
                                    self.stock.add_stuff(rkey)

                            if 4 == self.zone:
                                chanse = random.randint(0, 4)
                                if chanse == 2:
                                    rkey, ritem = get_random_item(True)
                                    out += f"💉💉вам выпал {ritem['name']} /ustf_{rkey}💉💉\n"
                                    self.stock.add_stuff(rkey)

                            if random.randint(0, 20) == 1:

                                if not self.mobs:
                                    self.mobs = []
                                if len(self.mobs) < 2:
                                    out += f"моб {mob.get_name()} взят в команду!\n"
                                    self.mobs.append(mob)

                            if self.zone >= 1 and not self.drone:
                                if random.randint(0, 1000) == 555:
                                    out += f"🛰{all_drones[1].get_name()} возле поверженного моба лежал дрон, теперь можно его использовать\n"
                                    self.drone = copy.copy(all_drones[1])
                            if self.zone == 2: #death
                                if random.randint(0, 700) == 199:
                                    self.stock.add_stuff(400)
                                    out += f"Вой вой вам выпало кое-что интересное {used_items[400]['name']}"
                                if random.randint(0, 1000) == 666:
                                    type = random.randint(0, 2)
                                    self.stock.add_item(armor_all[type][13])
                                    out += f"Вой вой вам выпало кое-что интересное {armor_all[type][13].get_name()}"
                                if random.randint(0, 1000) == 666:
                                    self.stock.add_item(weapons_all[21])
                                    out += f"Вой вой вам выпало кое-что интересное {weapons_all[21].get_name()}"
                            if self.zone == 3: #clown
                                if random.randint(0, 1000) == 777:
                                    type = random.randint(0, 2)
                                    self.stock.add_item(armor_all[type][12])
                                    out += f"Вой вой вам выпало кое-что интересное {armor_all[type][12].get_name()}"
                                if random.randint(0, 1000) == 777:
                                    self.stock.add_item(weapons_all[22])
                                    out += f"Вой вой вам выпало кое-что интересное {weapons_all[22].get_name()}"
                            if self.zone == 4:
                                if random.randint(0, 700) == 199:
                                    self.stock.add_stuff(401)
                                    out += f"Вой вой вам выпало кое-что интересное {used_items[401]['name']}"

                        return out
            else:
                is_first = True
                if mob.get_miss(self.get_dexterity()):
                    if cnt_attack < self.CNT_LOG:
                        miss_text = f"🌀{self.log_hit(text_mob_mis)}\n"
                else:
                    out += miss_text
                    miss_text = ""
                    dmg = mob.get_attack() - armor
                    dmg = dmg if dmg > 0 else 1
                    drone_hit = ""
                    if self.drone:
                        drone_hit = self.drone.get_hit(dmg, self.perks)
                        if self.drone.hp <= 0:
                            self.drone = None
                    if drone_hit == "":
                        self.hp -= dmg
                        if cnt_attack < self.CNT_LOG:
                            out += f"{mob.log_hit_mob()} 💔-{round(dmg)}\n"
                        self.get_hit_armor()
                    else:
                        if cnt_attack < self.CNT_LOG:
                            out += drone_hit

        if cnt_attack >= self.CNT_LOG:
            out += " ......... ....... ....\n"

        if round(self.hp) <= 0:
            out += self.died_hero_mob()

        self.km = 0
        return out

    def died_hero_mob(self) -> None:
        out = f"{self.log_hit(text_hero_dead)}\n"
        if self.zone == 1 or self.zone == 2:
            out += f"потеряно: 🕳 {round(self.coins * 0.5)}"
            self.coins *= 0.5
        else:
            if self.km >= 30:
                out += f"потеряно: 🕳 {round(self.coins * 0.25)}"
                self.coins = round(self.coins * 0.75)
        self.died_hero()
        return out

    def died_hero(self) -> None:
        self.km = 0
        self.died += 1
        self.hp = 1
        self.zone = 0
        self.mob_fight = None
        self.danges = []

    def log_hit(self, texts_list) -> str:
        return texts_list[random.randint(0, len(texts_list) - 1)]

    def attack_pvp_wmobs(self, hero: object) -> str:
        out = ""
        if self.is_first_hit(luck=hero.get_luck(True), use_perk=True):
            out += self.attack_player_with_mobs(hero)
        else:
            out += hero.attack_player_with_mobs(self)

        if hero.km !=0 and self.km != 0:
            out += self.attack_player(hero)

        return out

    def attack_player_with_mobs(self, hero: object) -> str:
        out = ""
        j = i = 0
        if self.mobs and hero.mobs:
            while i < len(self.mobs):
                out += self.mobs[i].attack_mob(hero.mobs[j])
                if hero.mobs[j].hp <= 0:
                    j += 1
                    if j >= len(hero.mobs):
                        break
                else:
                    i += 1

        while self.mobs and i < len(self.mobs) and hero.hp >= 0:
            out += hero.attack_mob_pvp(self.mobs[i])
            i += 1
        while hero.mobs and j < len(hero.mobs) and self.hp >= 0:
            out += self.attack_mob_pvp(hero.mobs[j])
            j += 1

        self.mobs = None
        hero.mobs = None
        return out

    @staticmethod
    def fight_heroes(hero1: object, hero2: object, cnt_attack: int) -> str:
        out = ""
        if hero1.get_miss(hero2.get_dexterity(True)):
            if cnt_attack < hero1.CNT_LOG:
                out += f"❤️ {round(hero1.hp)} {hero1.get_name()} 🌀{hero1.log_hit(text_hero_mis)}\n"
        else:
            drone_hit = ""
            drone_hit_block = ""
            drone_dmg = 0
            if hero1.drone:
                drone_dmg, drone_hit = hero1.drone.get_attack(hero2, hero1.perks)
            if drone_hit != "":
                out += drone_hit
                hero2.hp -= drone_dmg
                if hero2.hp <= 0:
                    out += f"{hero2.get_name()} повержен\n"
                    return out

            dmg = hero1.get_attack(True) - hero2.arm_clc

            if hero2.drone:
                drone_hit_block = hero2.drone.get_hit(dmg, hero2.perks)
                if hero2.drone.hp <= 0:
                    hero2.drone = None

            if drone_hit_block == "":
                dmg = 1 if dmg < 0 else dmg
                if cnt_attack < hero1.CNT_LOG:
                    out += f"❤️ {round(hero1.hp)} {hero1.get_name()} {hero1.log_hit(text_hit)} 💥{round(dmg)}\n"

                hero2.hp -= dmg
                hero2.get_hit_armor()
                if hero2.perks[5] != '0' and hero2.hp < hero2.max_hp:
                    coef = perk_luck_list[int(hero2.perks[5]) - 1] #2
                    if random.randint(0, 100) < coef*20:
                        hero2.hp += hero2.max_hp*0.3
                        out += f"❤️ {round(hero2.hp)} {hero2.get_name()} сработал навык счастливчик ❤️ +{hero2.max_hp*0.3} \n"

                if hero2.hp <= 0:
                    if cnt_attack > hero1.CNT_LOG:
                        out += " ......... ....... ....\n"
                    out += f"{hero2.get_name()} повержен\n"
                    return out
            else:
                out += drone_hit_block
        return out

    def attack_player(self, hero: object) -> str:
        out = "\n"
        self.arm_clc = self.calc_armor(True)
        hero.arm_clc = hero.calc_armor(True)
        cnt_attack = 0
        is_first = False
        if self.is_first_hit(luck=hero.get_luck(True), use_perk=True):
            is_first = True

        while round(self.hp) > 0:
            cnt_attack += 1
            if is_first:
                is_first = False
                out += Hero.fight_heroes(self, hero, cnt_attack)
            else:
                is_first = True
                out += Hero.fight_heroes(hero, self, cnt_attack)
            if hero.hp <= 0 or self.hp <= 0:
                break

        if cnt_attack > self.CNT_LOG:
            out += " ......... ....... ....\n"

        if round(self.hp) <= 0:
            out += f"{self.get_name()} {self.log_hit(text_hero_dead)}\n"
            hero.kl_pl += 1
        return out

    def from_db(self, hero_db: HeroDB) -> None:
        self.base_id = hero_db.id
        self.name = hero_db.name
        self.id = hero_db.user_id
        self.band_id = hero_db.band_id
        self.band_name = hero_db.band_name
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
        self.dzen = hero_db.dzen
        self.perks = hero_db.perks

    def to_db(self) -> HeroDB:
        return HeroDB(name=self.name, user_id=self.id,
                      hp=self.hp, max_hp=self.max_hp,
                      force=self.force, dexterity=self.dexterity,
                      charisma=self.charisma, luck=self.luck,
                      accuracy=self.accuracy, materials=self.materials,
                      coins=self.coins, hungry=self.hungry, km=self.km, mob="",
                      all_km=self.all_km, modul=self.modul, zone=self.zone, dzen=self.dzen,
                      band_id=self.band_id, band_name=self.band_name, perks=self.perks)
