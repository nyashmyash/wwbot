# ресурсы для крафта
# коробки, кипарит k, иридий i * 2, диски d * 2.5, генератор g * 4, кварц c * 7
# титан t, осмий o, нитрин n
crafted_weapon = []
from db.models import ArmorDB


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
    use = 0
    type_stack = 0

    def __init__(self, name, arm, type, life=500, max_life=500, cost=0, mats=0, type_stack=0):
        self.name = name
        self.arm = arm
        self.life = life
        self.cost = cost
        self.mats = mats
        self.max_life = max_life
        self.type = type
        self.type_stack = type_stack

    def get_data(self):
        out = "▪️ {0} 🛡 {1} 🔧{2} % /eqa_{3}t{4}z{5}".format(self.name, self.arm,
                                                              round(100 * self.life / self.max_life), self.type,
                                                              self.arm,
                                                              self.z)
        return out

    def get_data_cost(self):
        out = "▪️ {0} 🛡 ️{1} 🔧{2} % 📦 {6} /sa_{3}t{4}z{5}".format(self.name, self.arm,
                                                                     round(100 * self.life / self.max_life), self.type,
                                                                     self.arm, self.z,
                                                                     self.calc_cost())
        return out

    def get_buy(self):
        out = "▪️ {0} 🛡 {1} 🕳{2} /ba_{3}t{1}".format(self.name, self.arm, self.calc_cost(), self.type)
        return out

    # def craft_cost(self):
    #    self.calc_cost()

    def calc_cost(self):
        if self.cost:
            return round(self.cost * self.life / self.max_life)
        else:
            return round(self.arm * 100 * self.life / self.max_life + self.arm * 200)

    def get_data_hero(self):
        out = "▪️ {0} 🛡 {1} 🔧{2} %".format(self.name, self.arm, round(100 * self.life / self.max_life))
        return out

    def get_code(self):
        return "{0}t{1}z{2}".format(self.type, self.arm, self.z)

    def to_db(self):
        return ArmorDB(code=self.get_code(), use=self.use, life=self.life, max_life=self.max_life)

    def from_db(self, armor_db):
        self.life = armor_db.life
        self.max_life = armor_db.max_life
        self.use = armor_db.use


# сила ловка удача меткость
stack_buff = [
    [0, 50, 50, 0],
    [30, 70, 50, 0],
    [50, 30, 50, 0],
    [70, 70, 100, 0],
    [100, 0, 100, 100],
    [150, 100, 150, 0]
]

armor_all = [[Armor("кепка", 1, 0, life=100, max_life=100),
              Armor("шапка", 2, 0, life=100, max_life=100),
              Armor("каска", 5, 0, life=100, max_life=100),
              Armor("шлем воителя", 7, 0, life=200, max_life=200),
              Armor("усиленная шапка", 10, 0, life=300, max_life=300),

              Armor("✳️титановый шлем", 15, 0, life=500, max_life=500, type_stack=1, cost=50000),
              # +50 ловки + 50 удачи
              Armor("💠адамантовый шлем", 25, 0, life=600, max_life=600, type_stack=2, cost=60000),
              # +70 ловки +30 силы + 50 удачи
              Armor("👹даэдрический шлем", 35, 0, life=600, max_life=600, type_stack=3, cost=80000),
              # +50 силы + 30 ловки + 50 удачи
              Armor("☯️мифический шлем", 50, 0, life=700, max_life=700, type_stack=4, cost=200000),
              # +70 ловки + 70 силы + 100 удачи
              Armor("🐲шлем дракона", 70, 0, life=1000, type_stack=5, max_life=1000),
              # +100 меткости +100 силы + 100 удачи
              Armor("☢️атомный шлем", 120, 0, life=2000, type_stack=6, max_life=2000)],
             # +150 силы +100 ловкости + 150 удачи

             [Armor("плащ", 1, 1, life=100, max_life=100),
              Armor("куртка", 2, 1, life=100, max_life=100),
              Armor("бронежилет", 5, 1, life=100, max_life=100),
              Armor("броня легкая", 10, 1, life=100, max_life=100),
              Armor("тяжелая броня", 20, 1, life=100, max_life=100),

              Armor("✳️титановая броня", 40, 1, life=500, max_life=500, type_stack=1, cost=70000),
              Armor("💠адамантовая броня", 50, 1, life=800, max_life=800, type_stack=2, cost=80000),
              Armor("👹даэдрическая броня", 65, 1, life=1000, max_life=1000, type_stack=3, cost=100000),
              Armor("☯️мифическая броня", 90, 1, life=1300, type_stack=4, max_life=1300),
              Armor("🐲броня дракона", 140, 1, life=2000, type_stack=5, max_life=2000),
              Armor("☢️атомная броня", 190, 1, life=3000, type_stack=6, max_life=3000), ],

             [Armor("руковицы", 1, 2, life=100, max_life=100),
              Armor("перчатки", 2, 2, life=100, max_life=100),
              Armor("браслет", 5, 2, life=100, max_life=100),
              Armor("железные перчатки", 8, 2, life=200, max_life=200),
              Armor("варежки уничтожения", 10, 2, life=300, max_life=300),

              Armor("✳️титановые перчатки", 15, 2, life=500, type_stack=1, max_life=500),
              Armor("💠адамантовые перчатки", 25, 2, life=500, type_stack=2, max_life=500),
              Armor("👹даэдрические перчатки", 40, 2, life=600, type_stack=3, max_life=600),
              Armor("☯️мифические перчатки", 60, 2, life=700, type_stack=4, max_life=700),
              Armor("🐲перчатки дракона", 90, 2, life=800, type_stack=5, max_life=800),
              Armor("☢️атомные перчатки", 120, 2, life=1000, type_stack=6, max_life=1000)]]
