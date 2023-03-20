import random


class Mob:
    name = ''
    hp = 1
    attack = 1
    dexterity = 1
    luck = 1
    accuracy = 1
    coins = 20
    materials = 40

    def __init__(self, name, hp, attack, dexterity, luck, accuracy, coins):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.dexterity = dexterity
        self.luck = luck
        self.accuracy = accuracy
        self.coins = coins

    def calc_mob_coins(self, km):
        return (1 + km / 3) * self.coins * random.uniform(0.85, 1.15)

    def calc_mob_mat(self, km):
        return (1 + km / 3) * self.coins*1.5 * random.uniform(0.85, 1.15)

    def get_attack(self):
        return self.attack * random.uniform(0.85, 1.15)

    def get_miss(self, dex):  # dex шанс уворота для героя 0.1%
        if random.randint(0, 1000) < dex - self.accuracy:
            return True
        else:
            return False

    def is_first_hit(self, luck):
        if random.randint(0, 1000) - 500 < self.luck - luck:
            return True
        else:
            return False

    def get_hit(self, dmg, accur):  # удар героя по мобу
        if random.randint(0, 1000) < self.dexterity - accur:
            return "miss"
        else:
            self.hp = self.hp - dmg
            return "hit"


list_mobs1_5 = [
    Mob(name='🐶крысакот', hp=1, attack=2, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🐱мутамыш', hp=3, attack=2, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🐭мутант', hp=5, attack=2, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🐹мышка', hp=7, attack=2, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🐰толстый', hp=9, attack=2, dexterity=5, luck=5, accuracy=5, coins=20)
]

list_mobs5_10 = [
    Mob(name='🦊тварь', hp=11, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='🐼дилетант', hp=13, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='🪳солома', hp=15, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='🐊деловой', hp=17, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='🦕шышка', hp=19, attack=10, dexterity=10, luck=10, accuracy=10, coins=30)
]

list_mobs10_15 = [
    Mob(name='🐒сука', hp=21, attack=15, dexterity=15, luck=15, accuracy=15, coins=50),
    Mob(name='🐵зверокот', hp=23, attack=15, dexterity=15, luck=15, accuracy=15, coins=50),
    Mob(name='🦟зомби', hp=25, attack=15, dexterity=15, luck=15, accuracy=15, coins=50),
    Mob(name='🐝зорро', hp=27, attack=15, dexterity=15, luck=15, accuracy=15, coins=50),
    Mob(name='🐥злыдень', hp=29, attack=15, dexterity=15, luck=15, accuracy=15, coins=50)
]

list_mobs15_20 = [
    Mob(name='🐍торчек', hp=31, attack=20, dexterity=20, luck=20, accuracy=20, coins=60),
    Mob(name='🦇терран', hp=35, attack=20, dexterity=20, luck=20, accuracy=20, coins=60),
    Mob(name='🐛таракан', hp=36, attack=20, dexterity=20, luck=20, accuracy=20, coins=60),
    Mob(name='🐡монстр-наглец', hp=38, attack=20, dexterity=20, luck=20, accuracy=20, coins=60),
    Mob(name='🦂ежик', hp=39, attack=20, dexterity=20, luck=20, accuracy=20, coins=60)
]

list_mobs20_25 = [
    Mob(name='🦑соня', hp=51, attack=30, dexterity=20, luck=20, accuracy=20, coins=80),
    Mob(name='🪰дерево', hp=55, attack=30, dexterity=20, luck=20, accuracy=20, coins=80),
    Mob(name='🐬моб', hp=56, attack=30, dexterity=20, luck=20, accuracy=20, coins=80),
    Mob(name='🐜блин', hp=58, attack=30, dexterity=20, luck=20, accuracy=20, coins=80),
    Mob(name='🦛шиза', hp=59, attack=30, dexterity=20, luck=20, accuracy=20, coins=80)
]

list_mobs25_30 = [
    Mob(name='дракон', hp=71, attack=50, dexterity=120, luck=20, accuracy=120, coins=100),
    Mob(name='бобр', hp=75, attack=50, dexterity=120, luck=20, accuracy=120, coins=100),
    Mob(name='пчела', hp=76, attack=50, dexterity=120, luck=20, accuracy=120, coins=100),
    Mob(name='тарелка', hp=78, attack=50, dexterity=120, luck=20, accuracy=120, coins=100),
    Mob(name='ножик', hp=79, attack=50, dexterity=120, luck=20, accuracy=120, coins=100)
]

list_mobs30_35 = [
    Mob(name='дурак', hp=101, attack=70, dexterity=120, luck=20, accuracy=120, coins=120),
    Mob(name='дрова', hp=105, attack=70, dexterity=120, luck=20, accuracy=120, coins=120),
    Mob(name='корова', hp=106, attack=70, dexterity=120, luck=20, accuracy=120, coins=120),
    Mob(name='масяня', hp=108, attack=70, dexterity=120, luck=20, accuracy=120, coins=120),
    Mob(name='касадор', hp=109, attack=70, dexterity=120, luck=20, accuracy=120, coins=120)
]

list_mobs35_40 = [
    Mob(name='карапуз', hp=140, attack=100, dexterity=220, luck=20, accuracy=120, coins=150),
    Mob(name='попрыгун', hp=140, attack=100, dexterity=220, luck=20, accuracy=120, coins=150),
    Mob(name='жаба', hp=140, attack=100, dexterity=220, luck=20, accuracy=120, coins=150),
    Mob(name='сорняк', hp=145, attack=100, dexterity=220, luck=20, accuracy=120, coins=150),
    Mob(name='чупакабра', hp=150, attack=100, dexterity=220, luck=20, accuracy=120, coins=150)
]

list_mobs40_45 = [
    Mob(name='моб40', hp=200, attack=150, dexterity=320, luck=20, accuracy=320, coins=160),
    Mob(name='моб41', hp=220, attack=150, dexterity=320, luck=20, accuracy=320, coins=160),
    Mob(name='моб42', hp=240, attack=150, dexterity=320, luck=20, accuracy=320, coins=160),
    Mob(name='моб43', hp=260, attack=150, dexterity=320, luck=20, accuracy=320, coins=160),
    Mob(name='моб44', hp=270, attack=150, dexterity=320, luck=20, accuracy=320, coins=160)
]

list_mobs45_50 = [
    Mob(name='моб45', hp=340, attack=200, dexterity=320, luck=20, accuracy=320, coins=170),
    Mob(name='моб46', hp=320, attack=200, dexterity=320, luck=20, accuracy=320, coins=170),
    Mob(name='моб47', hp=341, attack=200, dexterity=320, luck=20, accuracy=320, coins=170),
    Mob(name='моб48', hp=345, attack=200, dexterity=320, luck=20, accuracy=320, coins=170),
    Mob(name='моб49', hp=360, attack=200, dexterity=320, luck=20, accuracy=320, coins=170)
]

list_mobs50_55 = [
    Mob(name='моб50', hp=410, attack=250, dexterity=420, luck=20, accuracy=420, coins=190),
    Mob(name='моб51', hp=425, attack=250, dexterity=420, luck=20, accuracy=420, coins=190),
    Mob(name='моб52', hp=445, attack=250, dexterity=420, luck=20, accuracy=420, coins=190),
    Mob(name='моб53', hp=467, attack=250, dexterity=420, luck=20, accuracy=420, coins=190),
    Mob(name='моб54', hp=490, attack=250, dexterity=420, luck=20, accuracy=420, coins=190)
]

list_mobs55_60 = [
    Mob(name='моб55', hp=510, attack=400, dexterity=520, luck=20, accuracy=520, coins=250),
    Mob(name='моб56', hp=520, attack=400, dexterity=520, luck=20, accuracy=520, coins=250),
    Mob(name='моб57', hp=540, attack=400, dexterity=520, luck=20, accuracy=520, coins=250),
    Mob(name='моб58', hp=565, attack=400, dexterity=520, luck=20, accuracy=520, coins=250),
    Mob(name='моб59', hp=570, attack=400, dexterity=520, luck=20, accuracy=520, coins=250)
]

list_mobs60_65 = [
    Mob(name='моб60', hp=710, attack=500, dexterity=520, luck=20, accuracy=620, coins=300),
    Mob(name='моб61', hp=720, attack=500, dexterity=520, luck=20, accuracy=620, coins=300),
    Mob(name='моб62', hp=740, attack=500, dexterity=520, luck=20, accuracy=620, coins=300),
    Mob(name='моб63', hp=765, attack=500, dexterity=520, luck=20, accuracy=620, coins=300),
    Mob(name='моб64', hp=770, attack=500, dexterity=520, luck=20, accuracy=620, coins=300)
]

list_mobs65_70 = [
    Mob(name='моб65', hp=1010, attack=700, dexterity=720, luck=20, accuracy=720, coins=320),
    Mob(name='моб66', hp=1020, attack=700, dexterity=720, luck=20, accuracy=720, coins=320),
    Mob(name='моб67', hp=1040, attack=700, dexterity=720, luck=20, accuracy=720, coins=320),
    Mob(name='моб68', hp=1065, attack=700, dexterity=720, luck=20, accuracy=720, coins=320),
    Mob(name='моб69', hp=1070, attack=700, dexterity=720, luck=20, accuracy=720, coins=320)
]

list_mobs70_75 = [
    Mob(name='моб70', hp=1510, attack=900, dexterity=720, luck=20, accuracy=720, coins=350),
    Mob(name='моб71', hp=1520, attack=900, dexterity=720, luck=20, accuracy=720, coins=350),
    Mob(name='моб72', hp=1540, attack=900, dexterity=720, luck=20, accuracy=720, coins=350),
    Mob(name='моб73', hp=1565, attack=900, dexterity=720, luck=20, accuracy=720, coins=350),
    Mob(name='моб74', hp=1570, attack=900, dexterity=720, luck=20, accuracy=720, coins=350)
]

list_mobs75_80 = [
    Mob(name='моб75', hp=2510, attack=1000, dexterity=720, luck=20, accuracy=820, coins=370),
    Mob(name='моб76', hp=2520, attack=1000, dexterity=720, luck=20, accuracy=820, coins=370),
    Mob(name='моб77', hp=2540, attack=1000, dexterity=720, luck=20, accuracy=820, coins=370),
    Mob(name='моб78', hp=2565, attack=1000, dexterity=720, luck=20, accuracy=820, coins=370),
    Mob(name='моб79', hp=2570, attack=1000, dexterity=720, luck=20, accuracy=820, coins=370)
]

list_mobs80_85 = [
    Mob(name='моб80', hp=3010, attack=1200, dexterity=820, luck=20, accuracy=1020, coins=400),
    Mob(name='моб81', hp=3020, attack=1200, dexterity=820, luck=20, accuracy=1020, coins=400),
    Mob(name='моб82', hp=3040, attack=1200, dexterity=820, luck=20, accuracy=1020, coins=400),
    Mob(name='моб83', hp=3065, attack=1200, dexterity=820, luck=20, accuracy=1020, coins=400),
    Mob(name='моб84', hp=3070, attack=1200, dexterity=820, luck=20, accuracy=1020, coins=400)
]

list_mobs85_90 = [
    Mob(name='моб85', hp=3510, attack=1400, dexterity=820, luck=20, accuracy=1220, coins=450),
    Mob(name='моб86', hp=3520, attack=1400, dexterity=820, luck=20, accuracy=1220, coins=450),
    Mob(name='моб87', hp=3540, attack=1400, dexterity=820, luck=20, accuracy=1220, coins=450),
    Mob(name='моб88', hp=3565, attack=1400, dexterity=820, luck=20, accuracy=1220, coins=450),
    Mob(name='моб89', hp=3570, attack=1400, dexterity=820, luck=20, accuracy=1220, coins=450)
]

list_mobs = [list_mobs1_5, list_mobs5_10,
             list_mobs10_15, list_mobs15_20,
             list_mobs20_25, list_mobs25_30,
             list_mobs30_35, list_mobs35_40,
             list_mobs40_45, list_mobs45_50,
             list_mobs50_55, list_mobs55_60,
             list_mobs60_65, list_mobs65_70,
             list_mobs70_75, list_mobs75_80,
             list_mobs80_85, list_mobs85_90
             ]
