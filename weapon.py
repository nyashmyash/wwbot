class Weapon:
    name = ""
    dmg = 0
    life = 0
    max_life = 0
    cost = 0
    mats = 0
    z = 0
    upgrade_lvl = 0

    def __init__(self, name, dmg, life=1000, max_life=1000, cost=0, mats=0):
        self.name = name
        self.dmg = dmg
        self.life = life
        self.cost = cost
        self.mats = mats
        self.max_life = max_life

    def get_data(self):
        out = "▪️ {0} ⚡️{1} 🔧{2} % /eqw_{3}z{4}".format(self.name, self.dmg,
                                                         round(100 * self.life / self.max_life), self.dmg, self.z)
        return out

    def get_data_hero(self):
        out = "▪️ {0} ⚡️{1} 🔧{2} %".format(self.name, self.dmg, round(100 * self.life / self.max_life))
        return out

    def get_code(self):
        return "{0}z{1}".format(self.dmg, self.z)


weapons_all = [Weapon("бита", 1), #титановый арбалет, лазерный лук, секира плазмы
               Weapon("🗡меч", 5),
               Weapon("🔫пистолет", 10),
               Weapon("🔫⚡️автомат", 20),
               Weapon("💥лазер", 50),
               Weapon("⚡️ракетница", 100),
               Weapon("♻️рандомган", 120),
               Weapon("☄️рельса", 180),
               Weapon("❇️потрошитель", 240),
               Weapon("🧨гранатомет", 300),
               Weapon("♨️святое пламя", 350),
               Weapon("🔮плюмбус", 400),
               Weapon("💠дезинтегратор", 500),
               Weapon("🦠черная вдова", 550),
               Weapon("🔆ядерный уничтожитель", 600),
               Weapon("🌪лазерное торнадо", 650),
               Weapon("🌀черная дыра", 700)]
