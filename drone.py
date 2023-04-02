import random


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
            hit_dmg = armor - dmg > 0 if armor - dmg else 0
            hit = round(hit_dmg / self.coeff)
            self.hp -= hit
            if self.hp > 0:
                return f"🛰{self.name} заблокировал урон 🛡{hit}\n"
            else:
                return f"🛰{self.name} ебнулся 🛡{hit} и умер(((\n"
        return ""

    def get_attack(self, enemy):
        if self.chanse > random.randint(0, 100):
            dmg = round(self.dmg * random.uniform(0.85, 1.15))
            enemy.hp -= dmg
            return f"🛰{self.name} атаковал 💥{dmg} врага {enemy.name}\n"
        return ""


all_drones = [Drone(1, 100, "drone1", 10, 15, 100000, [0, 0, 0, 10], 10),
              Drone(2, 150, "drone2", 10, 15, 200000, [0, 20, 0, 10], 12),
              Drone(3, 250, "drone3", 10, 15, 400000, [0, 20, 40, 40], 14),
              Drone(4, 400, "drone4", 10, 15, 800000, [0, 40, 40, 40], 15)]
