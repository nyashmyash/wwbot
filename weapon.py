from db.models import WeaponDB


class Weapon:
    name = ""
    dmg = 0
    life = 0
    max_life = 0
    cost = 0
    mats = 0
    z = 0
    upgrade_lvl = 0
    use = 0

    def __init__(self, name, dmg, life=500, max_life=500, cost=0, mats=0):
        self.name = name
        self.dmg = dmg
        self.life = life
        self.cost = cost
        self.mats = mats
        self.max_life = max_life

    def get_data_drop(self) -> str:
        return self.get_data("drw_")

    def get_data(self, code="eqw_") -> str:
        out = f"▪️ {self.get_name()} ⚡️{self.dmg} 🔧{round(100 * self.life / self.max_life)} % /{code}{self.dmg}z{self.z}"
        return out

    def get_data_cost(self) -> str:
        out = f"▪️ {self.get_name()} ⚡️{self.dmg} 🔧{round(100 * self.life / self.max_life)} % 📦 {self.calc_cost()} /sw_{self.dmg}z{self.z}"

        return out

    def get_buy(self) -> str:
        out = f"▪️ {self.get_name()} ⚡️{self.dmg} 🕳{self.calc_cost()} /bw_{self.dmg}"
        return out

    def calc_cost(self) -> int:
        if not self.cost:
            return round(self.dmg * 100 * self.life / self.max_life + self.dmg * 200)
        else:
            return round(self.cost * self.life / self.max_life)

    def get_data_hero(self) -> str:
        out = f"▪️ {self.get_name()} ⚡️{self.dmg} 🔧{round(100 * self.life / self.max_life)} %"
        return out

    def get_name(self) -> str:
        return self.name

    def get_code(self) -> str:
        return f"{self.dmg}z{self.z}"

    def to_db(self) -> WeaponDB:
        return WeaponDB(code=self.get_code(), use=self.use, life=self.life, max_life=self.max_life)

    def from_db(self, weapon_db) -> None:
        self.life = weapon_db.life
        self.max_life = weapon_db.max_life
        self.use = weapon_db.use
        self.z = int(weapon_db.code.split('z')[1])
        self.dmg = int(weapon_db.code.split('z')[0])


weapons_all = [Weapon("бита", 1, cost=100),  # титановый арбалет, лазерный лук, секира плазмы
               Weapon("🗡меч", 5, cost=1000),
               Weapon("🔫пистолет", 10, cost=5000),
               Weapon("🔫⚡️автомат", 20, cost=15000),
               Weapon("🏹арбалет", 30, cost=25000),
               Weapon("снайперская винтовка", 40, cost=45000),
               Weapon("💥лазер", 50, cost=70000),
               Weapon("⚡️️электрошок", 75, life=700, max_life=700, cost=80000),
               Weapon("🚀ракетница", 100, life=900, max_life=900, cost=100000),
               Weapon("♻️рандомган", 120, life=1000, max_life=1000, cost=120000),  # 9
               Weapon("☄️рельса", 180, life=1200, max_life=1200, cost=130000),
               Weapon("❇️потрошитель", 240, life=1200, max_life=1200, cost=140000),
               Weapon("🧨гранатомет", 300, life=1500, max_life=1500, cost=160000),
               Weapon("♨️святое пламя", 350, life=1500, max_life=1500, cost=170000),  # 13
               Weapon("🔮плюмбус", 400, life=1500, max_life=1500, cost=180000),
               Weapon("💠дезинтегратор", 500, life=1500, max_life=1500, cost=190000),
               Weapon("🦠черная вдова", 550, life=1500, max_life=1500),  # 16
               Weapon("🔆ядерный уничтожитель", 600, life=2000, max_life=2000),
               Weapon("🌪лазерное торнадо", 650, life=2000, max_life=2000),
               Weapon("🌀черная дыра", 700, life=2000, max_life=2000), #19
               Weapon("🌀пушка тиранид", 850, life=2000, max_life=2000),
               Weapon("🔪коса смерти", 666, life=1000, max_life=1000),
               Weapon("🪓клоунский молоток", 456, life=1000, max_life=1000),
               Weapon("Посох Шао-Кана", 770, life=1000, max_life=1000),
               ]
