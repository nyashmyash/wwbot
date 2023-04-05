import random
from db.models import WeaponDB


class Drone():
    index = 0
    hp = 100
    max_hp = 100
    name = ""
    dmg = 10
    chanse = 20
    cost = 100000
    buffs = None
    coeff = 10

    def __init__(self, index, hp, name, dmg, chanse, cost, buffs, coeff):
        self.index = index
        self.hp = hp
        self.max_hp = hp
        self.name = name
        self.dmg = dmg
        self.chanse = chanse
        self.cost = cost
        self.buffs = buffs
        self.coeff = coeff

    def get_hit(self, armor, dmg):
        if self.hp > 0 and self.chanse > random.randint(0, 100):
            hit = round(dmg / self.coeff) // 10
            self.hp -= hit
            if self.hp > 0:
                return f"🛰{self.name} заблокировал урон 🛡{hit}\n"
            else:
                return f"🛰{self.name} ебнулся 🛡{hit} и умер(((\n"
        return ""

    def get_attack(self, enemy):
        if self.chanse > random.randint(0, 100):
            dmg = round(self.dmg * random.uniform(0.85, 1.15))
            return dmg, f"🛰{self.name} атаковал 💥{dmg} врага {enemy.name}\n"
        return 0, ""

    def get_buy_text(self):
        return self.get_drone_text() + f"/buy_dr_{self.index}, 🕳 {self.cost}\n"

    def get_drone_text(self):
        return f"🛰{self.name}\n💥 {self.dmg}\n🛡 {self.hp}/{self.max_hp}\n👼 {self.chanse} \n"

    def get_drone_text_line(self):
        return f"🛰{self.name} 💥 {self.dmg} 🛡 {self.hp}/{self.max_hp}👼 {self.chanse}"


    def to_db(self):
        return WeaponDB(code=self.name, use=self.index+1, life=self.hp, max_life=self.max_hp)

    def from_db(self, weapon_db):
        self.hp = weapon_db.life
        self.max_hp = weapon_db.max_life
        self.index = weapon_db.use-1
        self.name = weapon_db.code


all_drones = [Drone(1, 100, "drone1", 10, 15, 200000, [0, 0, 0, 10], 15),
              Drone(2, 150, "drone2", 10, 15, 500000, [0, 20, 0, 10], 20),
              Drone(3, 250, "drone3", 10, 15, 1000000, [0, 20, 40, 40], 25),
              Drone(4, 400, "drone4", 10, 15, 1500000, [0, 40, 40, 40], 35)]
