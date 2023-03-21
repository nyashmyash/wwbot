class Armor:
    name = ""
    arm = 0
    life = 0
    max_life = 0
    cost = 0
    mats = 0
    z = 0
    upgrade_lvl = 0
    type = 0  # 0 head 1 body 2 foot

    def __init__(self, name, arm, type, life=1000, max_life=1000, cost=0, mats=0):
        self.name = name
        self.arm = arm
        self.life = life
        self.cost = cost
        self.mats = mats
        self.max_life = max_life
        self.type = type

    def get_data(self):
        out = "▪️ {0} 🛡 {1} 🔧{2} % /eqa_{5}t{3}z{4}".format(self.name, self.arm,
                                                              round(100 * self.life / self.max_life), self.arm,
                                                              self.z, self.type)
        return out

    def get_data_hero(self):
        out = "▪️ {0} 🛡 {1} 🔧{2} %".format(self.name, self.arm, round(100 * self.life / self.max_life))
        return out

    def get_code(self):
        return "{0}t{1}z{2}".format(self.type, self.arm, self.z)


armor_all = [Armor("кепка", 1, 0),
             Armor("шапка", 2, 0),
             Armor("каска", 5, 0),
             Armor("титановый шлем", 10, 0),
             Armor("даэдрический шлем", 35, 0),  # 4
             Armor("мифический шлем", 50, 0),
             Armor("шлем дракона", 70, 0),
             Armor("плащ", 1, 1),
             Armor("куртка", 2, 1),
             Armor("бронежилет", 5, 1),
             Armor("броня легкая", 10, 1),
             Armor("тяжелая броня", 20, 1),
             Armor("титановая броня", 40, 1),  # 12
             Armor("мифическая броня", 70, 1),
             Armor("броня дракона", 100, 1),
             Armor("ядерная броня", 150, 1),
             Armor("руковицы", 1, 2),
             Armor("перчатки", 2, 2),
             Armor("браслет", 5, 2),
             Armor("железные перчатки", 8, 2),
             Armor("варежки", 9, 2),
             Armor("титановые перчатки", 10, 2),  # 21
             Armor("мифические перчатки", 30, 2),
             Armor("перчатки из кожи дракона", 30, 2),
             Armor("атомные перчатки", 50, 2)]
