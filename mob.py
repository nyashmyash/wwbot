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


list_dange10 = [
    Mob(name='💊шиз-кровожадный', hp=5, attack=5, dexterity=50, luck=50, accuracy=10, coins=30),
    Mob(name='💉тянка-биполярка', hp=8, attack=10, dexterity=50, luck=50, accuracy=10, coins=30),
    Mob(name='🩸санитар(с таблетками)', hp=10, attack=15, dexterity=50, luck=50, accuracy=10, coins=30),
    Mob(name='🧬старушка(деменция)', hp=20, attack=20, dexterity=50, luck=50, accuracy=10, coins=30),
    Mob(name='🧫санитар(кровожадный)', hp=25, attack=25, dexterity=50, luck=50, accuracy=10, coins=30),
    None
]


list_dange20 = [
    Mob(name='🐜муравей с клыками', hp=30, attack=15, dexterity=50, luck=100, accuracy=50, coins=30),
    Mob(name='🐞божья коровка(кровожадная)', hp=35, attack=20, dexterity=50, luck=100, accuracy=50, coins=30),
    Mob(name='🐌улитка расчленитель', hp=40, attack=35, dexterity=50, luck=100, accuracy=50, coins=30),
    Mob(name='🦋бабочка(в крови)', hp=50, attack=40, dexterity=50, luck=100, accuracy=50, coins=30),
    Mob(name='🐛сороконожка(опасня с ножом)', hp=65, attack=55, dexterity=50, luck=100, accuracy=50, coins=30),
    None
]

list_dange30 = [
    Mob(name='👨‍🎓твой препод', hp=60, attack=70, dexterity=110, luck=110, accuracy=110, coins=30),
    Mob(name='👩‍🎤бывшая(кровожадная)', hp=80, attack=70, dexterity=110, luck=110, accuracy=110, coins=30),
    Mob(name='🧑‍🎤наркоман(ищет закладку)', hp=90, attack=90, dexterity=110, luck=110, accuracy=110, coins=30),
    Mob(name='👨‍🎤наркоман(нюхает)', hp=100, attack=100, dexterity=110, luck=110, accuracy=110, coins=30),
    Mob(name='💂‍♀шиз с кострюлей на голове', hp=120, attack=100, dexterity=110, luck=110, accuracy=110, coins=30),
    None
]

danges = {10: list_dange10, 20: list_dange20, 30: list_dange30}

list_mobs1_5 = [
    Mob(name='🐶крысакот(любопытный)', hp=1, attack=2, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🐱мутакот(голову тебе отожрет)', hp=3, attack=2, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🐭мутантская мышь убийца', hp=5, attack=2, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🐹хомяк(сожрет твои кишки)', hp=7, attack=2, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🐰толстый заяц(с твоей головой)', hp=9, attack=2, dexterity=5, luck=5, accuracy=5, coins=20)
]

list_mobs5_10 = [
    Mob(name='🦊я лав чина', hp=11, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='🐼панда в декрете', hp=13, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='🦭просто стас', hp=15, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='🌚скобка', hp=17, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='🍒пьяная вишня', hp=19, attack=10, dexterity=10, luck=10, accuracy=10, coins=30)
]

list_mobs10_15 = [
    Mob(name='🐒макака(с ножом)', hp=21, attack=15, dexterity=30, luck=15, accuracy=15, coins=50),
    Mob(name='🐵обезьяна(пьет кровь)', hp=23, attack=15, dexterity=30, luck=15, accuracy=15, coins=50),
    Mob(name='🐍киберзмей', hp=25, attack=15, dexterity=15, luck=30, accuracy=15, coins=50),
    Mob(name='🐝пчола(укуренная)', hp=27, attack=15, dexterity=30, luck=15, accuracy=15, coins=50),
    Mob(name='🦄гей(пидарас)', hp=29, attack=15, dexterity=30, luck=15, accuracy=15, coins=50)
]

list_mobs15_20 = [
    Mob(name='🐍змея(подколодная)', hp=31, attack=20, dexterity=60, luck=20, accuracy=20, coins=60),
    Mob(name='🦇призрак ночи', hp=35, attack=20, dexterity=60, luck=20, accuracy=20, coins=60),
    Mob(name='🐛таракан(многоножечный)', hp=36, attack=20, dexterity=60, luck=20, accuracy=20, coins=60),
    Mob(name='🐡монстр-наглец(шарообразный)', hp=38, attack=20, dexterity=60, luck=20, accuracy=20, coins=60),
    Mob(name='🦨скунз(воняет)', hp=39, attack=20, dexterity=20, luck=60, accuracy=20, coins=60)
]

list_mobs20_25 = [
    Mob(name='🕷черная вдова', hp=51, attack=30, dexterity=100, luck=20, accuracy=20, coins=80),
    Mob(name='🐟пиранья(хочет крови)', hp=55, attack=30, dexterity=100, luck=20, accuracy=20, coins=80),
    Mob(name='🐬делфин-призрак', hp=56, attack=30, dexterity=100, luck=20, accuracy=20, coins=80),
    Mob(name='🐜муравей-уничтожиель', hp=58, attack=30, dexterity=100, luck=20, accuracy=20, coins=80),
    Mob(name='🦀краб(злой)', hp=59, attack=30, dexterity=20, luck=100, accuracy=20, coins=80)
]

list_mobs25_30 = [
    Mob(name='🐀мистическая крыса', hp=71, attack=50, dexterity=120, luck=20, accuracy=120, coins=100),
    Mob(name='🦫бобр(строит плотину)', hp=75, attack=50, dexterity=120, luck=20, accuracy=120, coins=100),
    Mob(name='🐲дракон(маленький)', hp=76, attack=50, dexterity=120, luck=20, accuracy=120, coins=100),
    Mob(name='🚬курильщик', hp=78, attack=50, dexterity=120, luck=20, accuracy=120, coins=100),
    Mob(name='🚬нарик(с косяком)', hp=79, attack=50, dexterity=120, luck=20, accuracy=120, coins=100)
]

list_mobs30_35 = [
    Mob(name='🐷свин(мутантский🥉)', hp=101, attack=70, dexterity=120, luck=200, accuracy=120, coins=120),
    Mob(name='🐸жаба киллер', hp=105, attack=70, dexterity=120, luck=200, accuracy=120, coins=120),
    Mob(name='🐊крокодил(не Гена🥉)', hp=106, attack=70, dexterity=120, luck=200, accuracy=120, coins=120),
    Mob(name='🐙осьминог(небольшой🥉)', hp=108, attack=70, dexterity=120, luck=200, accuracy=120, coins=120),
    Mob(name='🦞рак(клешни лезвия🥉)', hp=109, attack=70, dexterity=120, luck=200, accuracy=120, coins=120)
]

list_mobs35_40 = [
    Mob(name='🦐креведка(белорусская🥈)', hp=140, attack=100, dexterity=220, luck=220, accuracy=120, coins=150),
    Mob(name='🐻медвед(шлюха🥈)', hp=140, attack=100, dexterity=220, luck=220, accuracy=120, coins=150),
    Mob(name='🐺волк(не выступает в цирке🥈)', hp=140, attack=100, dexterity=220, luck=220, accuracy=120, coins=150),
    Mob(name='🦆утка', hp=145, attack=100, dexterity=220, luck=220, accuracy=120, coins=150),
    Mob(name='🦎чупакабра', hp=150, attack=100, dexterity=220, luck=220, accuracy=120, coins=150)
]

list_mobs40_45 = [
    Mob(name='🐲дракон(большой🥇)', hp=200, attack=150, dexterity=320, luck=320, accuracy=320, coins=160),
    Mob(name='🐺волк(выступает в цирке🥇)', hp=220, attack=150, dexterity=320, luck=320, accuracy=320, coins=160),
    Mob(name='🐻медвед(превед🥇)', hp=240, attack=150, dexterity=320, luck=320, accuracy=320, coins=160),
    Mob(name='🦂скорпион(ядовитый🥇)', hp=260, attack=150, dexterity=320, luck=320, accuracy=320, coins=160),
    Mob(name='🕵️сыщик(жрет пончики🥇)', hp=270, attack=150, dexterity=320, luck=320, accuracy=320, coins=160)
]

list_mobs45_50 = [
    Mob(name='🧑🏿‍🏫айтишник(с геморроем🏵)', hp=340, attack=200, dexterity=320, luck=320, accuracy=320, coins=170),
    Mob(name='👶малыш(разорвет тебя🏵)', hp=320, attack=200, dexterity=320, luck=320, accuracy=320, coins=170),
    Mob(name='👮полиция(курит что-то🏵)', hp=341, attack=200, dexterity=320, luck=320, accuracy=320, coins=170),
    Mob(name='🕵️сыщик(ищет твой труп🏵)', hp=345, attack=200, dexterity=320, luck=320, accuracy=320, coins=170),
    Mob(name='👵🏿бабка(с аннигилятором🏵)', hp=360, attack=200, dexterity=320, luck=320, accuracy=320, coins=170)
]

list_mobs50_55 = [
    Mob(name='👶малыш(крадется за памперсом🏵🏵)', hp=410, attack=250, dexterity=420, luck=420, accuracy=420, coins=190),
    Mob(name='🧑‍✈️летчик-зомби', hp=425, attack=250, dexterity=420, luck=420, accuracy=420, coins=190),
    Mob(name='👩‍🚀космонавтка(хочет в космос🏵🏵)', hp=445, attack=250, dexterity=420, luck=420, accuracy=420, coins=190),
    Mob(name='👩‍🚒пожарный(разводит пожар🏵🏵)', hp=467, attack=250, dexterity=420, luck=420, accuracy=420, coins=190),
    Mob(name='🧓🏽бабка(у подъезда🏵🏵)', hp=490, attack=250, dexterity=420, luck=420, accuracy=420, coins=190)
]

list_mobs55_60 = [
    Mob(name='🧔‍♀️баба с бородой(пездец⭐️)', hp=510, attack=400, dexterity=520, luck=420, accuracy=520, coins=250),
    Mob(name='🧑‍🎤зеленый хер⭐️', hp=520, attack=400, dexterity=520, luck=420, accuracy=520, coins=250),
    Mob(name='💂‍♀️солдат королевы(думает о королеве⭐️)', hp=540, attack=400, dexterity=520, luck=420, accuracy=520, coins=250),
    Mob(name='👨‍🎓бакалавр(с шизой⭐️)', hp=565, attack=400, dexterity=520, luck=420, accuracy=520, coins=250),
    Mob(name='🧕моджахедка(с бомбой⭐️)', hp=570, attack=400, dexterity=520, luck=420, accuracy=520, coins=250)
]

list_mobs60_65 = [
    Mob(name='👩‍🍳повар(спрашивает у повара⭐️⭐️)', hp=710, attack=500, dexterity=520, luck=520, accuracy=620, coins=300),
    Mob(name='👨‍🌾писатель(напишет тебе хуй на голове⭐️⭐️)', hp=720, attack=500, dexterity=520, luck=520, accuracy=620, coins=300),
    Mob(name='🧙‍♀️маг(объелся мухоморов⭐️⭐️)', hp=740, attack=500, dexterity=520, luck=520, accuracy=620, coins=300),
    Mob(name='🧛‍♀️вампир(кровушки бы⭐️⭐️)', hp=765, attack=500, dexterity=520, luck=520, accuracy=620, coins=300),
    Mob(name='💁‍♀️твоя бывшая', hp=770, attack=500, dexterity=520, luck=520, accuracy=620, coins=300)
]

list_mobs65_70 = [
    Mob(name='🐺волк(кибернетический🌟)', hp=1010, attack=700, dexterity=720, luck=520, accuracy=720, coins=320),
    Mob(name='🧓🏽бабка(терминатор🌟)', hp=1020, attack=700, dexterity=720, luck=520, accuracy=720, coins=320),
    Mob(name='🧑‍✈️летчик(истребителя🌟)', hp=1040, attack=700, dexterity=720, luck=520, accuracy=720, coins=320),
    Mob(name='👶малыш(из твоих кошмаров🌟)', hp=1065, attack=700, dexterity=720, luck=520, accuracy=720, coins=320),
    Mob(name='👮полиция(ест пончики🌟)', hp=1070, attack=700, dexterity=720, luck=520, accuracy=720, coins=320)
]

list_mobs70_75 = [
    Mob(name='🐲дракон(механизированный🌟🌟)', hp=1510, attack=900, dexterity=720, luck=520, accuracy=720, coins=350),
    Mob(name='🦑кальмар(мистический🌟🌟)', hp=1520, attack=900, dexterity=720, luck=520, accuracy=720, coins=350),
    Mob(name='⚓якорь(проклятый🌟🌟)', hp=1540, attack=900, dexterity=720, luck=520, accuracy=720, coins=350),
    Mob(name='🪝крюк потрошителя', hp=1565, attack=900, dexterity=720, luck=520, accuracy=720, coins=350),
    Mob(name='🗿каменный голем(легендарный🌟🌟)', hp=1570, attack=900, dexterity=720, luck=520, accuracy=720, coins=350)
]

list_mobs75_80 = [
    Mob(name='моб75⚡️⚡️', hp=2510, attack=1000, dexterity=720, luck=20, accuracy=820, coins=370),
    Mob(name='моб76⚡⚡️️', hp=2520, attack=1000, dexterity=720, luck=20, accuracy=820, coins=370),
    Mob(name='моб77⚡⚡️️', hp=2540, attack=1000, dexterity=720, luck=20, accuracy=820, coins=370),
    Mob(name='моб78⚡⚡️️', hp=2565, attack=1000, dexterity=720, luck=20, accuracy=820, coins=370),
    Mob(name='моб79⚡️⚡️', hp=2570, attack=1000, dexterity=720, luck=20, accuracy=820, coins=370)
]

list_mobs80_85 = [
    Mob(name='моб80⚡️🌟⚡', hp=3010, attack=1200, dexterity=820, luck=20, accuracy=1020, coins=400),
    Mob(name='моб81⚡️🌟⚡', hp=3020, attack=1200, dexterity=820, luck=20, accuracy=1020, coins=400),
    Mob(name='моб82⚡️🌟⚡', hp=3040, attack=1200, dexterity=820, luck=20, accuracy=1020, coins=400),
    Mob(name='моб83⚡️🌟⚡', hp=3065, attack=1200, dexterity=820, luck=20, accuracy=1020, coins=400),
    Mob(name='моб84⚡️🌟⚡', hp=3070, attack=1200, dexterity=820, luck=20, accuracy=1020, coins=400)
]

list_mobs85_90 = [
    Mob(name='моб85', hp=3510, attack=1400, dexterity=820, luck=20, accuracy=1220, coins=450),
    Mob(name='моб86', hp=3520, attack=1400, dexterity=820, luck=20, accuracy=1220, coins=450),
    Mob(name='моб87', hp=3540, attack=1400, dexterity=820, luck=20, accuracy=1220, coins=450),
    Mob(name='моб88', hp=3565, attack=1400, dexterity=820, luck=20, accuracy=1220, coins=450),
    Mob(name='моб89', hp=3570, attack=1400, dexterity=820, luck=20, accuracy=1220, coins=450)
]

list_mobs90 = [
    Mob(name='моб90', hp=4510, attack=1600, dexterity=1020, luck=20, accuracy=1320, coins=650),
    Mob(name='моб91', hp=4520, attack=1600, dexterity=1020, luck=20, accuracy=1320, coins=650),
    Mob(name='моб92', hp=4540, attack=1600, dexterity=1020, luck=20, accuracy=1320, coins=650),
    Mob(name='моб93', hp=4565, attack=1600, dexterity=1020, luck=20, accuracy=1320, coins=650),
    Mob(name='моб94', hp=4570, attack=1600, dexterity=1020, luck=20, accuracy=1320, coins=650)
]

list_mobs = [list_mobs1_5, list_mobs5_10,
             list_mobs10_15, list_mobs15_20,
             list_mobs20_25, list_mobs25_30,
             list_mobs30_35, list_mobs35_40,
             list_mobs40_45, list_mobs45_50,
             list_mobs50_55, list_mobs55_60,
             list_mobs60_65, list_mobs65_70,
             list_mobs70_75, list_mobs75_80,
             list_mobs80_85, list_mobs85_90, list_mobs90
             ]
