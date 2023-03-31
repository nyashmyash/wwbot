class Drone():
    hp = 100
    max_hp = 100
    name = ""
    dmg = 10
    chanse = 20
    cost = 100000
    buffs = None
    coeff = 10

    def __init__(self, hp, name, dmg, chanse, cost, buffs, coeff):
        self.hp = hp
        self.max_hp = hp
        self.name = name
        self.dmg = dmg
        self.chanse = chanse
        self.cost = cost
        self.buffs = buffs
        self.coeff = coeff

    def hit_drone(self, armor, dmg):
        hit_dmg = armor - dmg > 0 if armor - dmg else 0
        self.hp -= round(hit_dmg/self.coeff)


all_drones = [Drone(100, "drone1", 10, 15, 100000, [0, 0, 0, 10], 10),
             Drone(150, "drone2", 10, 15, 200000, [0, 20, 0, 10], 12),
             Drone(250, "drone3", 10, 15, 400000, [0, 20, 40, 40], 14),
             Drone(400, "drone4", 10, 15, 800000, [0, 40, 40, 40]), 15]


