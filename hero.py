from string import ascii_lowercase
from random import sample
from mob import *
import random
import copy


class Hero:
    id = 0
    name = ""
    hp = 100
    max_hp = 100 # здоровье 1500
    force = 100  # cила 1300
    dexterity = 100  # ловкость 1200
    charisma = 100  # харизма 1200
    luck = 100  # удача 1200
    accuracy = 100  # меткость 1200
    weapon = None
    armor = [10, 15, 10]
    materials = 0
    coins = 0
    # attack = 1
    hungry = 0
    km = 0
    kl_pl = 0
    kl_mb = 0
    died = 0
    mob_fight = None
    stock = None

    def return_data(self):
        data = """
        👤{0}
        ├ ❤ {1}/{2}  🍗{14} | ⚔️{15} | 🛡 {16} 
        ├ 👣{17}
        ├ 💪{3} | 🤸🏽‍♂️{4} | 🗣{5} 
        ├ 👼{6} | 🎯{7}
        ├ 🗡{8}        ├ 🪖🥾🧥{9}|{10}|{11}
        ├ 📦{12}
        └ 🕳{13}"""
        return data.format(self.name, round(self.hp), self.max_hp,
                           self.force, self.dexterity, self.charisma,
                           self.luck, self.accuracy, self.weapon.get_data(), self.armor[0],
                           self.armor[1], self.armor[2], self.materials,
                           self.coins, self.hungry, self.calc_attack(),
                           self.armor[0] + self.armor[1] + self.armor[2], self.km)

    @staticmethod
    def generate_name():
        return "hero.." + "".join(sample(ascii_lowercase, 5))

    def calc_attack(self):
        if self.weapon.life > 0:
            self.weapon.life -= 1
            if self.force < 50:
                return (self.weapon.dmg + self.force)
            else:
                return (round(50 + self.weapon.dmg * pow(1.03, self.force / 50)))
        else:
            return 1

    def get_attack(self):
        return self.calc_attack() * random.uniform(0.85, 1.15)

    def get_miss(self, dex):  # dex шанс уворота для героя 0.1%
        if random.randint(0, 1000) < dex - self.accuracy:
            return True
        else:
            return False

    def calc_cost(self, val):
        out = 13 * val - 3 * self.charisma
        if out < 10:
            return 10
        else:
            return round(13 * val - 3 * self.charisma);

    def select_mob(self):
        k = self.km // 5
        list_m = list_mobs[k]
        i = random.randint(0, len(list_m) - 1)
        self.mob_fight = copy.copy(list_m[i])

    def learn_data(self):
        out = "🕳Крышки: {0}\n".format(self.coins)
        out += "💪Сила({0}): 🕳{1}\n".format(self.force, self.calc_cost(self.force))
        out += "🎯Меткость({0}): 🕳{1}\n".format(self.accuracy, self.calc_cost(self.accuracy))
        out += "🤸🏽‍♂️Ловкость({0}): 🕳{1}\n".format(self.dexterity, self.calc_cost(self.dexterity))
        out += "❤️Живучесть({0}): 🕳{1}\n".format(self.max_hp, self.calc_cost(self.max_hp))
        out += "🗣Харизма({0}): 🕳{1}\n".format(self.charisma, 10 * self.charisma)
        out += "👼Удача({0}): 🕳{1}\n\n".format(self.luck, self.calc_cost(self.luck))
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
        if random.randint(0, 1000) - 500 < self.luck - luck:
            return True
        else:
            return False

    def make_header(self):
        return "❤️ {0}\{1} 🍗{2}  👣{3}\n".format(round(self.hp), self.max_hp, self.hungry, self.km)

    def attack_mob(self, mob: Mob):
        out = "Сражение с {0} ❤{1}\n".format(mob.name, mob.hp)
        armor = self.armor[0] + self.armor[1] + self.armor[2]
        hp_mob = mob.hp
        if mob.is_first_hit(luck=self.luck):
            if mob.get_miss(self.dexterity):
                out += "моб промахнулся\n"
            else:
                dmg = mob.get_attack() - armor
                if dmg < 0:
                    out += "урон заблокирован\n"
                else:
                    out += "{0} нанес тебе удар 💔-{1}\n".format(mob.name, round(dmg))
                    self.hp -= dmg

        while round(self.hp) > 0:
            if self.get_miss(mob.dexterity):
                out += "👤Ты промахнулся\n"
            else:
                att = self.get_attack()
                out += "👤Ты ударил 💥{0}\n".format(round(att))
                hp_mob -= att
                if hp_mob <= 0:
                    out += "{0} повержен\n".format(mob.name)
                    coins = round(mob.calc_mob_coins(self.km))
                    mats = round(mob.calc_mob_mat(self.km))
                    self.coins += coins
                    self.materials += mats
                    out += "получено 🕳 {0} 📦 {1}\n".format(coins, mats)
                    return out

            if mob.get_miss(self.dexterity):
                out += "моб промахнулся\n"
            else:
                dmg = mob.get_attack() - armor
                if dmg < 0:
                    out += "урон заблокирован\n"
                else:
                    out += "{0} нанес тебе удар 💔-{1}\n".format(mob.name, round(dmg))
                    self.hp -= dmg

        if round(self.hp) <= 0:
            out += "ты помер :((((((\n"
            self.hp = self.max_hp

        self.km = 0
        return out

    def died_hero(self):
        self.km = 0
        self.died += 1
        self.hp = 1

    def attack_player(self, hero):
        out = ""
        armor = self.armor[0] + self.armor[1] + self.armor[2]
        armor_hero = hero.armor[0] + hero.armor[1] + hero.armor[2]
        if hero.is_first_hit(luck=self.luck):
            if hero.get_miss(self.dexterity):
                out += "{0} ❤️ {1} промахнулся\n".format(hero.name, round(hero.hp))
            else:
                dmg = hero.get_attack() - armor
                if dmg < 0:
                    out += "{0} ❤️ {1}  урон {2} заблокирован\n".format(hero.name, round(hero.hp), round(dmg))
                else:
                    out += "{0} ❤️ {1} нанес {3} удар 💔-{2}\n".format(hero.name, round(hero.hp), round(dmg), self.name)
                    self.hp -= dmg

        while round(self.hp) > 0:
            if self.get_miss(hero.dexterity):
                out += "❤️ {0} {1} промахнулся\n".format(round(self.hp), self.name)
            else:
                dmg = self.get_attack() - armor_hero
                if dmg < 0:
                    out += "❤️ {0} урон {1} заблокировал враг\n".format(round(self.hp), round(dmg))
                else:
                    out += "❤️ {0} {2} ударил 💥{1}\n".format(round(self.hp), round(dmg), self.name)
                    hero.hp -= dmg
                    if hero.hp <= 0:
                        out += "{0} повержен\n".format(hero.name)
                        return out

            if hero.get_miss(self.dexterity):
                out += "{0} ❤️ {1} промахнулся\n".format(hero.name, round(hero.hp))
            else:
                dmg = hero.get_attack() - armor
                if dmg < 0:
                    out += "{0} ❤️ {1} урон {2} заблокирован\n".format(hero.name, round(hero.hp), round(dmg))
                else:
                    out += "{0} ❤️ {1} нанес {3} удар 💔-{2}\n".format(hero.name, round(hero.hp), round(dmg), self.name)
                    self.hp -= dmg

        if round(self.hp) <= 0:
            out += "{0} помер :((((((\n".format(self.name)
            hero.kl_pl += 1
        return out
