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
    CNT_LOG = 10

    def __init__(self, name: str, hp: int, attack: int, dexterity: int, luck: int, accuracy: int, coins: int):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.dexterity = dexterity
        self.luck = luck
        self.accuracy = accuracy
        self.coins = coins

    def calc_mob_coins(self, km: int) -> float:
        return (1 + km / 3) * self.coins * random.uniform(0.85, 1.15)

    def calc_mob_mat(self, km: int) -> float:
        return (1 + km / 3) * self.coins*1.5 * random.uniform(0.85, 1.15)

    def get_attack(self) -> float:
        return self.attack * random.uniform(0.85, 1.15)

    def get_miss(self, dex: int) -> bool:  # dex шанс уворота для героя 0.1%
        if random.randint(0, 1000) < dex - self.accuracy:
            return True
        else:
            return False

    def is_first_hit(self, luck: int) -> bool:
        if random.randint(0, 1000) - 500 < self.luck - luck:
            return True
        else:
            return False

    def attack_mob(self, mob: object) -> str:
        out = f"{self.name} vs {mob.name} ❤{mob.hp}\n"
        hp_mob = mob.hp
        cnt_attack = 0
        if mob.is_first_hit(luck=self.luck):
            if mob.get_miss(self.dexterity):
                out += f"🌀{mob.name} промахнулся\n"
            else:
                dmg = mob.get_attack()
                self.hp -= dmg
        while round(self.hp) > 0:
            cnt_attack += 1
            if self.get_miss(mob.dexterity):
                if cnt_attack < self.CNT_LOG:
                    out += f"{self.name} промахнулся\n"
            else:
                att = self.get_attack()
                hp_mob -= att
                if hp_mob <= 0:
                    if cnt_attack > self.CNT_LOG:
                        out += " ......... ....... ....\n"
                    out += f"{mob.name} повержен\n"
                    return out

            if mob.get_miss(self.dexterity):
                if cnt_attack < self.CNT_LOG:
                    out += f"{mob.name} промахнулся\n"
            else:
                dmg = mob.get_attack()
                if cnt_attack < self.CNT_LOG:
                    out += f"{mob.name} нанес {self.name} удар 💔-{round(dmg)}\n"
                self.hp -= dmg

        if cnt_attack > self.CNT_LOG:
            out += " ......... ....... ....\n"

        if round(self.hp) <= 0:
            out += f"{self.name} мертв :((\n"

        return out


list_dange10 = [
    Mob(name='😈кровосос', hp=5, attack=5, dexterity=50, luck=50, accuracy=10, coins=30),
    Mob(name='👩🏻‍🔧тянка-биполярка', hp=8, attack=10, dexterity=50, luck=50, accuracy=10, coins=30),
    Mob(name='🧔‍♂️санитар(с таблетками)', hp=10, attack=15, dexterity=50, luck=50, accuracy=10, coins=30),
    Mob(name='👨‍⚕доктор-марианетка(деменция)', hp=20, attack=20, dexterity=50, luck=50, accuracy=10, coins=30),
    Mob(name='👩‍⚕️медсестра-марионетка', hp=25, attack=25, dexterity=50, luck=50, accuracy=10, coins=30),
    None
]


list_dange20 = [
    Mob(name='🐜ползающий', hp=30, attack=15, dexterity=50, luck=100, accuracy=50, coins=30),
    Mob(name='🐞парящее жало', hp=35, attack=20, dexterity=50, luck=100, accuracy=50, coins=30),
    Mob(name='🐌двуусый', hp=40, attack=35, dexterity=50, luck=100, accuracy=50, coins=30),
    Mob(name='🦋порхающий(в ночи)', hp=50, attack=40, dexterity=50, luck=100, accuracy=50, coins=30),
    Mob(name='🐛паразит(опасный с ножом)', hp=65, attack=55, dexterity=50, luck=100, accuracy=50, coins=30),
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

list_dange35 = [
    Mob(name='🦀хед-краб', hp=100, attack=100, dexterity=150, luck=150, accuracy=150, coins=30),
    Mob(name='🦑барнакл', hp=100, attack=120, dexterity=150, luck=150, accuracy=150, coins=30),
    Mob(name='🦖вортигонт', hp=130, attack=120, dexterity=150, luck=150, accuracy=150, coins=30),
    Mob(name='🦕пехотинец пришельцев', hp=150, attack=130, dexterity=150, luck=150, accuracy=150, coins=30),
    Mob(name='🐋гаргантюа(🌟)', hp=200, attack=150, dexterity=150, luck=150, accuracy=150, coins=30),
    None
]


list_dange40 = [
    Mob(name='🎖чертик', hp=200, attack=120, dexterity=210, luck=210, accuracy=210, coins=30),
    Mob(name='🎖демон', hp=250, attack=130, dexterity=210, luck=210, accuracy=210, coins=30),
    Mob(name='🌟огненный атронах', hp=260, attack=150, dexterity=210, luck=210, accuracy=210, coins=30),
    Mob(name='⚡️служитель бездны', hp=280, attack=170, dexterity=210, luck=210, accuracy=210, coins=30),
    Mob(name='️💥повелитель ада', hp=320, attack=200, dexterity=210, luck=210, accuracy=210, coins=30),
    None
]

list_dange50 = [
    Mob(name='🤡жалкий клоун', hp=250, attack=125, dexterity=320, luck=320, accuracy=320, coins=210),
    Mob(name='🎈оно', hp=300, attack=150, dexterity=330, luck=320, accuracy=320, coins=210),
    Mob(name='🤹🏻‍♀️жонглер костями', hp=320, attack=200, dexterity=320, luck=320, accuracy=320, coins=210),
    Mob(name='🎭кровавый арлекин', hp=400, attack=220, dexterity=320, luck=320, accuracy=320, coins=210),
    Mob(name='️🎪 ебучий цирк(будешь выступать)', hp=500, attack=250, dexterity=320, luck=320, accuracy=320, coins=210),
    None
]

list_dange60 = [
    Mob(name='🐙зерлинг', hp=400, attack=200, dexterity=410, luck=510, accuracy=510, coins=30),
    Mob(name='🦞гидралиск', hp=450, attack=250, dexterity=410, luck=510, accuracy=510, coins=30),
    Mob(name='🦐муталиск', hp=560, attack=300, dexterity=410, luck=510, accuracy=510, coins=30),
    Mob(name='🦀брудлорд', hp=580, attack=330, dexterity=410, luck=510, accuracy=510, coins=30),
    Mob(name='🦑ультралиск', hp=720, attack=450, dexterity=410, luck=510, accuracy=510, coins=30),
    None
]

list_dange70 = [
    Mob(name='🦂Заразитель (некроморф хитрец)', hp=1000, attack=350, dexterity=710, luck=510, accuracy=710, coins=30),
    Mob(name='🦎Сталкер (некроморф следит)', hp=1250, attack=400, dexterity=710, luck=510, accuracy=710, coins=30),
    Mob(name='🐍Расчленитель (некроморф режущий)', hp=1260, attack=500, dexterity=510, luck=510, accuracy=710, coins=30),
    Mob(name='🦖Охотник (некроморф тебя ищет)', hp=1480, attack=530, dexterity=710, luck=510, accuracy=710, coins=30),
    Mob(name='🐊Левиафан(некроморф босс)', hp=1520, attack=650, dexterity=710, luck=510, accuracy=710, coins=30),
    None
]

list_dange80 = [
    Mob(name='Потрошитель', hp=2510, attack=700, dexterity=820, luck=520, accuracy=1020, coins=400),
    Mob(name='Тервигон', hp=2710, attack=800, dexterity=820, luck=520, accuracy=1020, coins=400),
    Mob(name='Доминатрикс', hp=2810, attack=900, dexterity=820, luck=520, accuracy=1020, coins=400),
    Mob(name='Стражи тирана', hp=2910, attack=900, dexterity=820, luck=520, accuracy=1020, coins=400),
    Mob(name='Красный Ужас', hp=3010, attack=1000, dexterity=820, luck=520, accuracy=1020, coins=400),
    Mob(name='Повелитель роя', hp=3010, attack=1300, dexterity=820, luck=520, accuracy=1020, coins=400),
    None
]
danges = {10: list_dange10, 20: list_dange20,
          30: list_dange30, 35: list_dange35, 40: list_dange40,
          50: list_dange50, 60: list_dange60, 70: list_dange70, 80: list_dange80}

list_mobs1_5 = [
    Mob(name='🐶крысакот(любопытный)', hp=1, attack=2, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🐱кот(голову тебе отожрет)', hp=3, attack=2, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🐭мутантская мышь убийца', hp=5, attack=2, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🐹хомяк(сожрет твои кишки)', hp=7, attack=2, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🥚яйцо ксеноморфа', hp=9, attack=2, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🐷свинокрыс(злобно хрюкает)', hp=9, attack=3, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🐸жаба(смотрит и квакает)', hp=9, attack=3, dexterity=5, luck=5, accuracy=5, coins=30),
    Mob(name='🦐лицехват', hp=9, attack=3, dexterity=5, luck=5, accuracy=5, coins=30),
    Mob(name='🧟зомби(скучающий)', hp=9, attack=3, dexterity=5, luck=5, accuracy=5, coins=30),
    Mob(name='🧟‍♀️зомби(любопытный)', hp=9, attack=3, dexterity=5, luck=5, accuracy=5, coins=30),

]

list_mobs5_10 = [
    Mob(name='🐷свинокрыс(злобно хрюкает и смотрит)', hp=11, attack=10, dexterity=10, luck=10, accuracy=5, coins=30),
    Mob(name='🦊я лав чина', hp=11, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='🐼панда в декрете', hp=13, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='🦭просто стас', hp=15, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='🌚скобка', hp=17, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='Точа🍗 (травит токсичностью)', hp=17, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='🍒пьяная вишня', hp=19, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='❄️Снежка(дает бан⭐️)', hp=19, attack=12, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='⭐️Кирюха(кирюха⭐️)', hp=19, attack=13, dexterity=10, luck=100, accuracy=10, coins=30),
    Mob(name='😰METOKS(Бог нытья😰)', hp=19, attack=13, dexterity=10, luck=100, accuracy=10, coins=30),
    Mob(name='🐸жаба(злится)', hp=19, attack=13, dexterity=10, luck=100, accuracy=10, coins=40),

]

list_mobs10_15 = [
    Mob(name='🐷свинокрыс(сожрет тебя и твою маму)', hp=21, attack=15, dexterity=30, luck=15, accuracy=15, coins=50),
    Mob(name='🐒макака(с ножом)', hp=21, attack=15, dexterity=30, luck=15, accuracy=15, coins=50),
    Mob(name='🐵обезьяна(пьет кровь)', hp=23, attack=15, dexterity=30, luck=15, accuracy=15, coins=50),
    Mob(name='🐍киберзмей', hp=25, attack=15, dexterity=15, luck=30, accuracy=15, coins=50),
    Mob(name='🐝пчола(укуренная)', hp=27, attack=15, dexterity=30, luck=15, accuracy=15, coins=50),
    Mob(name='🦄гей(пидарас)', hp=29, attack=15, dexterity=30, luck=15, accuracy=15, coins=50),
    Mob(name='🪱грудолом', hp=29, attack=15, dexterity=30, luck=15, accuracy=15, coins=50),
    Mob(name='🐸жаба(мутант)', hp=29, attack=15, dexterity=30, luck=15, accuracy=15, coins=60)
]

list_mobs15_20 = [
    Mob(name='🐷свинокрыс(мутировавший)', hp=31, attack=20, dexterity=60, luck=20, accuracy=20, coins=60),
    Mob(name='🐍змея(железная)', hp=31, attack=20, dexterity=60, luck=20, accuracy=20, coins=60),
    Mob(name='🦇призрак ночи', hp=35, attack=20, dexterity=60, luck=20, accuracy=20, coins=60),
    Mob(name='🐛таракан(радиоактивный)', hp=36, attack=20, dexterity=60, luck=20, accuracy=20, coins=60),
    Mob(name='🐡монстр-наглец(со свинцом)', hp=38, attack=20, dexterity=60, luck=20, accuracy=20, coins=60),
    Mob(name='🦨скунз(воняет радиацией)', hp=39, attack=20, dexterity=20, luck=60, accuracy=20, coins=60),
    Mob(name='🐸жаба(кибернетическая)', hp=39, attack=20, dexterity=20, luck=60, accuracy=20, coins=80)
]

list_mobs20_25 = [
    Mob(name='🐷свинокрыс(демонический)', hp=51, attack=30, dexterity=100, luck=20, accuracy=20, coins=80),
    Mob(name='🕷черная вдова', hp=51, attack=30, dexterity=100, luck=20, accuracy=20, coins=80),
    Mob(name='🐟пиранья(хочет крови)', hp=55, attack=30, dexterity=100, luck=20, accuracy=20, coins=80),
    Mob(name='🐬сухопутный делфин-призрак', hp=56, attack=30, dexterity=100, luck=20, accuracy=20, coins=80),
    Mob(name='🐜муравей-робот', hp=58, attack=30, dexterity=100, luck=20, accuracy=20, coins=80),
    Mob(name='🦀гигантский краб(злой)', hp=59, attack=30, dexterity=20, luck=100, accuracy=20, coins=80),
    Mob(name='🐸жаба(демоничекая)', hp=59, attack=30, dexterity=20, luck=100, accuracy=20, coins=100)
]

list_mobs25_30 = [
    Mob(name='🐷свинокрыс(кибернетический)', hp=71, attack=50, dexterity=120, luck=120, accuracy=120, coins=100),
    Mob(name='🐀мистическая крыса', hp=71, attack=50, dexterity=120, luck=120, accuracy=120, coins=100),
    Mob(name='👽молодой ксеноморф', hp=75, attack=50, dexterity=120, luck=120, accuracy=120, coins=100),
    Mob(name='🐲дракон(маленький)', hp=76, attack=50, dexterity=120, luck=120, accuracy=120, coins=100),
    Mob(name='🚬курильщик', hp=78, attack=50, dexterity=120, luck=120, accuracy=120, coins=100),
    Mob(name='🚬нарик(с косяком)', hp=79, attack=50, dexterity=120, luck=120, accuracy=120, coins=100),
    Mob(name='🐸жаба(мифическая)', hp=79, attack=50, dexterity=120, luck=120, accuracy=120, coins=120)
]

list_mobs30_35 = [
    Mob(name='🐷свинокрыс(мифический🥉🥉🥉)', hp=101, attack=70, dexterity=120, luck=200, accuracy=120, coins=120),
    Mob(name='🐸жаба(киллер🥉)', hp=105, attack=70, dexterity=120, luck=200, accuracy=120, coins=120),
    Mob(name='🐊крокодил(не Гена🥉)', hp=106, attack=70, dexterity=120, luck=200, accuracy=120, coins=120),
    Mob(name='🐙осьминог(небольшой🥉)', hp=108, attack=70, dexterity=120, luck=200, accuracy=120, coins=120),
    Mob(name='🦞рак(клешни лезвия🥉)', hp=109, attack=70, dexterity=120, luck=200, accuracy=120, coins=120),
    Mob(name='🐸жаба(ядерная🥉)', hp=109, attack=70, dexterity=120, luck=200, accuracy=120, coins=140),
    Mob(name='👽ксеноморф(зрелый🥉)', hp=109, attack=70, dexterity=120, luck=200, accuracy=120, coins=120),
    Mob(name='🚬нарик(ищет закладку🥉)', hp=109, attack=70, dexterity=120, luck=200, accuracy=120, coins=120),
]

list_mobs35_40 = [
    Mob(name='🐷свинокрыс(радиоактивный🥈)', hp=140, attack=100, dexterity=220, luck=220, accuracy=120, coins=150),
    Mob(name='🦐креведка(белорусская🥈)', hp=140, attack=100, dexterity=220, luck=220, accuracy=120, coins=150),
    Mob(name='🐻медвед(шлюха🥈)', hp=140, attack=100, dexterity=220, luck=220, accuracy=120, coins=150),
    Mob(name='🐺волк(не выступает в цирке🥈)', hp=140, attack=100, dexterity=220, luck=220, accuracy=120, coins=150),
    Mob(name='🦆утка(кря-кря🥈)', hp=145, attack=100, dexterity=220, luck=220, accuracy=120, coins=150),
    Mob(name='🦎чупакабра(🥈)', hp=150, attack=100, dexterity=220, luck=220, accuracy=120, coins=150),
    Mob(name='🐸жаба(термоядерная🥈)', hp=150, attack=100, dexterity=220, luck=220, accuracy=120, coins=170)
]

list_mobs40_45 = [
    Mob(name='🐷свинокрыс(исполинский🥇)', hp=200, attack=150, dexterity=320, luck=320, accuracy=320, coins=160),
    Mob(name='🐲дракон(большой🥇)', hp=200, attack=150, dexterity=320, luck=320, accuracy=320, coins=160),
    Mob(name='🐺волк(выступает в цирке🥇)', hp=220, attack=150, dexterity=320, luck=320, accuracy=320, coins=160),
    Mob(name='🐻медвед(превед🥇)', hp=240, attack=150, dexterity=320, luck=320, accuracy=320, coins=160),
    Mob(name='🦂скорпион(ядовитый🥇)', hp=260, attack=150, dexterity=320, luck=320, accuracy=320, coins=160),
    Mob(name='🕵️сыщик(жрет пончики🥇)', hp=270, attack=150, dexterity=320, luck=320, accuracy=320, coins=160),
    Mob(name='🐸жаба(средовая🥇)', hp=270, attack=150, dexterity=320, luck=320, accuracy=320, coins=180)
]

list_mobs45_50 = [
    Mob(name='🐷свинокрыс(ты охуешь какой он🏵)', hp=340, attack=200, dexterity=320, luck=320, accuracy=320, coins=170),
    Mob(name='🧑🏿‍🏫айтишник(с геморроем🏵)', hp=340, attack=200, dexterity=320, luck=320, accuracy=320, coins=170),
    Mob(name='👶малыш(разорвет тебя🏵)', hp=320, attack=200, dexterity=320, luck=320, accuracy=320, coins=170),
    Mob(name='👮полиция(курит что-то🏵)', hp=341, attack=200, dexterity=320, luck=320, accuracy=320, coins=170),
    Mob(name='🕵️сыщик(ищет твой труп🏵)', hp=345, attack=200, dexterity=320, luck=320, accuracy=320, coins=170),
    Mob(name='👵🏿бабка(с аннигилятором🏵)', hp=360, attack=200, dexterity=320, luck=320, accuracy=320, coins=170),
    Mob(name='🐸жаба(легендарная🏵)', hp=360, attack=200, dexterity=320, luck=320, accuracy=320, coins=190)
]

list_mobs50_55 = [
    Mob(name='🐷свинокрыс(тварь дрожи и беги🏵🏵)', hp=410, attack=250, dexterity=420, luck=420, accuracy=420, coins=190),
    Mob(name='👶малыш(крадется за памперсом🏵🏵)', hp=410, attack=250, dexterity=420, luck=420, accuracy=420, coins=190),
    Mob(name='🧑‍✈️летчик-зомби', hp=425, attack=250, dexterity=420, luck=420, accuracy=420, coins=190),
    Mob(name='👩‍🚀космонавтка(хочет в космос🏵🏵)', hp=445, attack=250, dexterity=420, luck=420, accuracy=420, coins=190),
    Mob(name='👩‍🚒пожарный(разводит пожар🏵🏵)', hp=467, attack=250, dexterity=420, luck=420, accuracy=420, coins=190),
    Mob(name='🧓🏽бабка(у подъезда🏵🏵)', hp=490, attack=250, dexterity=420, luck=420, accuracy=420, coins=190),
    Mob(name='🐸жаба(из ада🏵🏵)', hp=490, attack=250, dexterity=420, luck=420, accuracy=420, coins=210)
]

list_mobs55_60 = [
    Mob(name='🐷свинокрыс(бегииии!!⭐️)', hp=610, attack=400, dexterity=520, luck=420, accuracy=520, coins=250),
    Mob(name='🧔‍♀️баба с бородой(пездец⭐️)', hp=610, attack=400, dexterity=520, luck=420, accuracy=520, coins=250),
    Mob(name='🧑‍🎤зеленый хер⭐️', hp=620, attack=400, dexterity=520, luck=420, accuracy=520, coins=250),
    Mob(name='💂‍♀️солдат королевы(думает о королеве⭐️)', hp=640, attack=400, dexterity=520, luck=420, accuracy=520, coins=250),
    Mob(name='👨‍🎓бакалавр(с шизой⭐️)', hp=665, attack=400, dexterity=520, luck=420, accuracy=520, coins=250),
    Mob(name='🧕моджахедка(с бомбой⭐️)', hp=670, attack=400, dexterity=520, luck=420, accuracy=520, coins=250),
    Mob(name='🐸жаба(шизоидная⭐️)', hp=670, attack=400, dexterity=520, luck=420, accuracy=520, coins=270)
]

list_mobs60_65 = [
    Mob(name='👩‍🍳повар(спрашивает у повара⭐️⭐️)', hp=810, attack=600, dexterity=520, luck=520, accuracy=620, coins=300),
    Mob(name='👨‍🌾писатель(напишет тебе хуй на голове⭐️⭐️)', hp=820, attack=600, dexterity=520, luck=520, accuracy=620, coins=300),
    Mob(name='🧙‍♀️маг(объелся мухоморов⭐️⭐️)', hp=840, attack=600, dexterity=520, luck=520, accuracy=620, coins=300),
    Mob(name='🧛‍♀️вампир(кровушки бы⭐️⭐️)', hp=865, attack=600, dexterity=520, luck=520, accuracy=620, coins=300),
    Mob(name='💁‍♀️твоя бывшая', hp=870, attack=600, dexterity=520, luck=520, accuracy=620, coins=300),
    Mob(name='🐸жаба(️твоя бывшая⭐️⭐️)', hp=870, attack=600, dexterity=520, luck=520, accuracy=620, coins=330)
]

list_mobs65_70 = [
    Mob(name='🐺волк(кибернетический🌟)', hp=1210, attack=700, dexterity=720, luck=520, accuracy=720, coins=320),
    Mob(name='🧓🏽бабка(терминатор🌟)', hp=1220, attack=700, dexterity=720, luck=520, accuracy=720, coins=320),
    Mob(name='🧑‍✈️летчик(истребителя🌟)', hp=1240, attack=700, dexterity=720, luck=520, accuracy=720, coins=320),
    Mob(name='👶малыш(из твоих кошмаров🌟)', hp=1265, attack=700, dexterity=720, luck=520, accuracy=720, coins=320),
    Mob(name='👮полиция(ест пончики🌟)', hp=1270, attack=700, dexterity=720, luck=520, accuracy=720, coins=320),
    Mob(name='🐸жаба(battletoad🌟)', hp=1270, attack=700, dexterity=720, luck=520, accuracy=720, coins=320)
]

list_mobs70_75 = [
    Mob(name='🐲дракон(механизированный🌟🌟)', hp=1510, attack=900, dexterity=720, luck=520, accuracy=720, coins=350),
    Mob(name='🦑кальмар(мистический🌟🌟)', hp=1520, attack=900, dexterity=720, luck=520, accuracy=720, coins=350),
    Mob(name='⚓якорь(проклятый🌟🌟)', hp=1540, attack=900, dexterity=720, luck=520, accuracy=720, coins=350),
    Mob(name='🪝крюк потрошителя', hp=1565, attack=900, dexterity=720, luck=520, accuracy=720, coins=350),
    Mob(name='🗿каменный голем(легендарный🌟🌟)', hp=1570, attack=900, dexterity=720, luck=520, accuracy=720, coins=350)
]

list_mobs75_80 = [
    Mob(name='моб75⚡️⚡️', hp=2510, attack=1000, dexterity=720, luck=720, accuracy=820, coins=370),
    Mob(name='моб76⚡⚡️️', hp=2520, attack=1000, dexterity=720, luck=720, accuracy=820, coins=370),
    Mob(name='моб77⚡⚡️️', hp=2540, attack=1000, dexterity=720, luck=720, accuracy=820, coins=370),
    Mob(name='моб78⚡⚡️️', hp=2565, attack=1000, dexterity=720, luck=720, accuracy=820, coins=370),
    Mob(name='моб79⚡️⚡️', hp=2570, attack=1000, dexterity=720, luck=720, accuracy=820, coins=370)
]

list_mobs80_85 = [
    Mob(name='моб80⚡️🌟⚡', hp=3010, attack=1200, dexterity=820, luck=720, accuracy=820, coins=400),
    Mob(name='моб81⚡️🌟⚡', hp=3020, attack=1200, dexterity=820, luck=720, accuracy=820, coins=400),
    Mob(name='моб82⚡️🌟⚡', hp=3040, attack=1200, dexterity=820, luck=720, accuracy=820, coins=400),
    Mob(name='моб83⚡️🌟⚡', hp=3065, attack=1200, dexterity=820, luck=720, accuracy=820, coins=400),
    Mob(name='моб84⚡️🌟⚡', hp=3070, attack=1200, dexterity=820, luck=720, accuracy=820, coins=400)
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
