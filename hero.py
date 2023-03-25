from string import ascii_lowercase
from random import sample
from mob import *
import random
import copy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from db.models import HeroDB, WeaponDB


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

    def calc_armor(self):
        ret = 0
        for i in range(0, 3):
            if self.armor[i]:
                ret += self.armor[i].arm
        return ret

    def return_data(self):
        data = """
        👤{0} 
        ├ ❤ {1}/{2}  🍗{14} | ⚔️{15} | 🛡 {16} 
        ├ 👣{17}
        ├ 💪{3} | 🤸🏽‍♂️{4} | 🗣{5} 
        ├ 👼{6} | 🎯{7}
        ├ 🗡{8}
        ├ 🪖{9}
        | 🧥{10}
        | 🧤{11}
        ├ 📦{12}
        └ 🕳{13} 👣👣{18}"""
        weapon = None
        if self.weapon:
            weapon = self.weapon.get_data_hero()
        else:
            weapon = "нет оружия"

        armor = self.calc_armor()
        return data.format(self.name, round(self.hp), self.max_hp,
                           self.force, self.dexterity, self.charisma,
                           self.luck, self.accuracy, weapon, self.arm_str(self.armor[0]),
                           self.arm_str(self.armor[1]), self.arm_str(self.armor[2]), self.materials,
                           self.coins, self.hungry, self.calc_attack(),
                           armor, self.km, self.all_km)

    @staticmethod
    def generate_name():
        return "hero.." + "".join(sample(ascii_lowercase, 5))

    def arm_str(self, arm):
        if arm:
            return arm.get_data_hero()
        else:
            return "нет брони"

    def calc_attack(self):
        if self.weapon:
            if self.force < 50:
                return (self.weapon.dmg + self.force)
            else:
                return (round(50 + self.weapon.dmg * pow(1.03, self.force / 50)))
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
            self.weapon.life -= 1
            return self.calc_attack() * random.uniform(0.85, 1.15)
        else:
            self.weapon = None
            return 1

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
        if k >= len(list_mobs):
            k = len(list_mobs) - 1
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

    def attack_mob(self, mob: Mob, is_dange = False):
        out = "Сражение с {0} ❤{1}\n".format(mob.name, mob.hp)
        armor = self.calc_armor()
        hp_mob = mob.hp
        cnt_attack = 0
        if mob.is_first_hit(luck=self.luck):
            if mob.get_miss(self.dexterity):
                out += "моб промахнулся\n"
            else:
                dmg = mob.get_attack() - armor
                if dmg < 0:
                    dmg = 1
                    # out += "урон заблокирован\n"

                out += "{0} нанес тебе удар 💔-{1}\n".format(mob.name, round(dmg))
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
                    out += "👤Ты ударил 💥{0}\n".format(round(att))
                hp_mob -= att
                if hp_mob <= 0:
                    if cnt_attack > self.CNT_LOG:
                        out += " ......... ....... ....\n"
                    out += "{0} повержен\n".format(mob.name)
                    coins = round(mob.calc_mob_coins(self.km))
                    mats = round(mob.calc_mob_mat(self.km))
                    if not is_dange:
                        self.coins += coins
                        self.materials += mats
                        out += "получено 🕳 {0} 📦 {1}\n".format(coins, mats)
                    return out

            if mob.get_miss(self.dexterity):
                if cnt_attack < self.CNT_LOG:
                    out += "моб промахнулся\n"
            else:
                dmg = mob.get_attack() - armor
                if dmg < 0:
                    dmg = 1
                    # out += "урон заблокирован\n"
                if cnt_attack < self.CNT_LOG:
                    out += "{0} нанес тебе удар 💔-{1}\n".format(mob.name, round(dmg))
                self.hp -= dmg
                self.get_hit_armor()

        if cnt_attack > self.CNT_LOG:
            out += " ......... ....... ....\n"

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
        armor = self.calc_armor()
        armor_hero = hero.calc_armor()
        cnt_attack = 0
        if hero.is_first_hit(luck=self.luck):
            if hero.get_miss(self.dexterity):
                out += "{0} ❤️ {1} промахнулся\n".format(hero.name, round(hero.hp))
            else:
                dmg = hero.get_attack() - armor
                if dmg < 0:
                    dmg = 1
                    # out += "{0} ❤️ {1}  урон {2} заблокирован\n".format(hero.name, round(hero.hp), round(dmg))

                out += "{0} ❤️ {1} нанес {3} удар 💔-{2}\n".format(hero.name, round(hero.hp), round(dmg), self.name)
                self.hp -= dmg
                self.get_hit_armor()

        while round(self.hp) > 0:
            cnt_attack += 1
            if self.get_miss(hero.dexterity):
                if cnt_attack < self.CNT_LOG:
                    out += "❤️ {0} {1} промахнулся\n".format(round(self.hp), self.name)
            else:
                dmg = self.get_attack() - armor_hero
                if dmg < 0:
                    dmg = 1
                    # out += "❤️ {0} урон {1} заблокировал враг\n".format(round(self.hp), round(dmg))

                if cnt_attack < self.CNT_LOG:
                    out += "❤️ {0} {2} ударил 💥{1}\n".format(round(self.hp), round(dmg), self.name)
                hero.hp -= dmg
                hero.get_hit_armor()
                if hero.hp <= 0:
                    if cnt_attack > self.CNT_LOG:
                        out += " ......... ....... ....\n"
                    out += "{0} повержен\n".format(hero.name)
                    return out

            if hero.get_miss(self.dexterity):
                if cnt_attack < self.CNT_LOG:
                    out += "{0} ❤️ {1} промахнулся\n".format(hero.name, round(hero.hp))
            else:
                dmg = hero.get_attack() - armor
                if dmg < 0:
                    dmg = 1
                    # out += "{0} ❤️ {1} урон {2} заблокирован\n".format(hero.name, round(hero.hp), round(dmg))

                if cnt_attack < self.CNT_LOG:
                    out += "{0} ❤️ {1} нанес {3} удар 💔-{2}\n".format(hero.name, round(hero.hp), round(dmg), self.name)
                self.hp -= dmg
                self.get_hit_armor()

        if cnt_attack > self.CNT_LOG:
            out += " ......... ....... ....\n"

        if round(self.hp) <= 0:
            out += "{0} помер :((((((\n".format(self.name)
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

    def to_db(self):
        return HeroDB(name=self.name, user_id=self.id,
                      hp=self.hp, max_hp=self.max_hp,
                      force=self.force, dexterity=self.dexterity,
                      charisma=self.charisma, luck=self.luck,
                      accuracy=self.accuracy, materials=self.materials,
                      coins=self.coins, hungry=self.hungry, km=self.km, mob="")


async def get_hero_db(async_session: async_sessionmaker[AsyncSession], user_id):
    async with async_session() as session:
        result = await session.execute(select(HeroDB).where(HeroDB.user_id == user_id))
        return result.scalars().all()


async def add_hero_db(async_session: async_sessionmaker[AsyncSession], hero: Hero):
    async with async_session() as session:
        async with session.begin():
            session.add(hero.to_db())


async def add_hero_weapon_db(async_session: async_sessionmaker[AsyncSession], hero: Hero, weapon, use=0):
    async with async_session() as session:
        async with session.begin():
            if not hero.base_id:
                result = await session.execute(select(HeroDB).where(HeroDB.user_id == hero.id))
                hero_db = result.scalars().one()
                hero.base_id = hero_db.id
            wdb = weapon.to_db()
            wdb.user = hero.base_id
            wdb.use = use
            session.add(wdb)


async def upd_hero_weapon_db(async_session: async_sessionmaker[AsyncSession], hero: Hero, code="", life=0, use=0):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(WeaponDB).where(WeaponDB.user == hero.base_id and WeaponDB.code == code))
            res = result.scalars().one()
            res.life = life
            res.use = use
            await session.commit()


async def upd_hero_db(async_session: async_sessionmaker[AsyncSession], hero: Hero):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(HeroDB).where(HeroDB.user_id == hero.id))
            res = result.scalars().one()
            res.copy_val(hero.to_db())
            await session.commit()