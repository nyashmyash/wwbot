import random
from rand import randint

text_mob_mis = ["тварь смешно упала",
                "монстр подавился злобой",
                "монстрятина промахнулась",
                "существо подскользнулось",
                "тварь врезалась в дерево",
                "глупая тварь не попадает"]

name_mob = [["тварь", 0], ["монстр", 1], ["мразь", 0], ["чудовище", 2],
            ["противник", 1], ["нечисть", 0], ["мразота", 0], ["сволота", 0], ["существо", 2]]

type_att_custma = ["сделала хитрый маневр и напала", "сбила с ног", "брызнула слизью", "откусила палец", "вгрызлась в плоть", "схватила за шею", "неожиданно подкралась и ударила"]
type_att_custmb = ["сделал хитрый маневр и напал", "сбил с ног", "брызнул слизью", "откусил палец", "вгрызся в плоть", "схватил за шею", "неожиданно подкрался и ударил"]
type_att_custmc = ["сделало хитрый маневр и напало", "сбило с ног", "брызнуло слизью", "откусило палец", "вгрызлось в плоть", "схватило за шею", "неожиданно подкралось и ударило"]

type_moba = ["мерзкая", "злая", "противная", "тупая", "злобная", "вонючая", "сумасшедшая", "зверская"]
type_mobb = ["мерзкий", "злой", "противный", "тупой", "мощный", "хитрый", "зверский"]
type_mobc = ["мерзкое", "злое", "противное", "тупое", "страшное", "злобное", "дебильное"]

type_mob = {0: type_moba, 1: type_mobb, 2: type_mobc}

type_atta = ["ебнула", "врезала", "хуйнула", "переебала", "ударила", "жахнула"]
type_attb = ["ебнул", "врезал", "хуйнул", "переебал", "ударил", "жахнул"]
type_attc = ["ебнуло", "врезало", "хуйнуло", "переебало", "ударило", "жахнуло"]

type_att = {0: type_atta, 1: type_attb, 2: type_attc}

type_custm = {0: type_att_custma, 1: type_att_custmb, 2: type_att_custmc}

type_att_str = ["сильно", "резко", "неожиданно", "мощно", "с разворота",
                "дерзко", "изворотливо", "хитро", "жестко", "метко", "больно"]

type_att_hero = ["по яйцам", "по голове", "в ебальник",
                 "в лицо", "по шее", "в грудь", "в живот", "в печень"]


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
    km = 0
    enfect = False
    cnt_miss = 0

    def __init__(self, name: str, hp: int, attack: int, dexterity: int, luck: int, accuracy: int, coins: int, km: int = 0):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.dexterity = dexterity
        self.luck = luck
        self.accuracy = accuracy
        self.coins = coins
        self.km = km

    def get_name(self) -> str:
        return self.name

    def calc_mob_coins(self, km: int) -> float:
        return (1 + km / 3) * self.coins * random.uniform(0.85, 1.15)

    def calc_mob_mat(self, km: int) -> float:
        return (1 + km / 3) * self.coins * 1.5 * random.uniform(0.85, 1.15)

    def get_attack(self) -> float:
        return self.attack * random.uniform(0.85, 1.15)

    def get_miss(self, dex: int) -> bool:  # dex шанс уворота для героя 0.1%
        # k = 1.7 if dex / self.accuracy >= 1.7 else dex / self.accuracy
        # return randint(0, 1000) < 500 * k
        if self.cnt_miss > 0:
            self.cnt_miss = 0
            return False
        r = randint(0, 500)
        k = 4 if dex / self.accuracy >= 4 else dex / self.accuracy
        #print(f'{r} < {10 * k} mob {self.name}')
        if k <= 0.5 and r < 100 * k:
            self.cnt_miss += 1
        return r < 100 * k


    def is_first_hit(self, luck: int) -> bool:
        if randint(0, 1000) - 500 < self.luck - luck:
            return True
        else:
            return False

    def log_hit_mob(self, min_log: bool = False) -> str:
        if min_log:
            return ""
        mob = name_mob[randint(0, len(name_mob) - 1)]
        name = mob[0]
        type = mob[1]
        if randint(0, 10) == 1:
            out = f"{self.log_hit(type_mob[type])} {name} {self.log_hit(type_custm[type])}"
            return out

        fuck_mob = self.log_hit(type_mob[type]) + " " if randint(0, 5) > 2 else ""
        out = fuck_mob + f"{name} "
        type_attack = self.log_hit(type_att_str) + " " if randint(0, 5) > 2 else ""

        out += f"{self.log_hit(type_att[type])} {type_attack}{self.log_hit(type_att_hero)}"

        return out

    def log_hit(self, texts_list, min_log: bool = False) -> str:
        if min_log:
            return ""
        return texts_list[randint(0, len(texts_list) - 1)]

    def attack_mob(self, mob: object, min_log: bool = False) -> str:
        out = f"❤{round(self.hp)} {self.name} vs {mob.name} ❤{round(mob.hp)}\n"
        cnt_attack = self.CNT_LOG
        is_first = True
        if self.is_first_hit(luck=mob.luck):
            is_first = False

        while round(self.hp) > 0:
            cnt_attack += 1
            if is_first:
                is_first = False
                if mob.get_miss(self.dexterity):
                    if cnt_attack < self.CNT_LOG:
                        out += f"❤️ {round(mob.hp)} {mob.name} 🌀{self.log_hit(text_mob_mis, min_log)}\n"
                else:
                    dmg = mob.get_attack()
                    if cnt_attack < self.CNT_LOG:
                        out += f"❤️ {round(mob.hp)} {mob.name} {self.log_hit_mob(min_log)} {self.name} 💔-{round(dmg)}\n"
                    self.hp -= dmg

            else:
                is_first = True
                if self.get_miss(mob.dexterity):
                    if cnt_attack < self.CNT_LOG:
                        out += f"❤️ {round(self.hp)} {self.name} 🌀{self.log_hit(text_mob_mis, min_log)}\n"
                else:
                    att = self.get_attack()
                    mob.hp -= att
                    if cnt_attack < self.CNT_LOG:
                        out += f"❤️ {round(self.hp)} {self.name} {self.log_hit_mob(min_log)} {mob.name} 💔-{round(att)}\n"
                    if mob.hp <= 0:
                        if cnt_attack >= self.CNT_LOG:
                            out += " ......... ....... ....\n"
                        out += f"{mob.name} повержен\n"
                        return out

        if round(self.hp) <= 0:
            out += f"{self.name} мертв : ((\n"

        return out


list_dange10 = [
    Mob(name='😈кровосос', hp=5, attack=5, dexterity=50, luck=50, accuracy=10, coins=30),
    Mob(name='👩🏻‍🔧тянка-биполярка', hp=8, attack=10, dexterity=50, luck=50, accuracy=10, coins=30),
    Mob(name='🧔‍♂️санитар (с таблетками)', hp=10, attack=15, dexterity=50, luck=50, accuracy=10, coins=30),
    Mob(name='👨‍⚕доктор-марианетка (деменция)', hp=20, attack=20, dexterity=50, luck=50, accuracy=10, coins=30),
    Mob(name='👩‍⚕️медсестра-марионетка', hp=25, attack=25, dexterity=50, luck=50, accuracy=10, coins=30),
    None
]

list_dange20 = [
    Mob(name='🐜ползающий', hp=30, attack=15, dexterity=50, luck=100, accuracy=50, coins=30),
    Mob(name='🐞парящее жало', hp=35, attack=20, dexterity=50, luck=100, accuracy=50, coins=30),
    Mob(name='🐌двуусый', hp=40, attack=35, dexterity=50, luck=100, accuracy=50, coins=30),
    Mob(name='🦋порхающий (в ночи)', hp=50, attack=40, dexterity=50, luck=100, accuracy=50, coins=30),
    Mob(name='🐛паразит (опасный с ножом)', hp=65, attack=55, dexterity=50, luck=100, accuracy=50, coins=30),
    None
]

list_dange30 = [
    Mob(name='🐕цербер', hp=60, attack=70, dexterity=110, luck=110, accuracy=110, coins=30),
    Mob(name='💀чистильщик', hp=80, attack=70, dexterity=110, luck=110, accuracy=110, coins=30),
    Mob(name='🔪бензопильщик', hp=90, attack=90, dexterity=110, luck=110, accuracy=110, coins=30),
    Mob(name='🏍мама Бейкер', hp=100, attack=100, dexterity=110, luck=110, accuracy=110, coins=30),
    Mob(name='🧌немезис', hp=120, attack=100, dexterity=110, luck=110, accuracy=110, coins=30),
    None
]

list_dange35 = [
    Mob(name='🦀хед-краб', hp=100, attack=100, dexterity=150, luck=150, accuracy=150, coins=30),
    Mob(name='🦑барнакл', hp=100, attack=120, dexterity=150, luck=150, accuracy=150, coins=30),
    Mob(name='🦖вортигонт', hp=130, attack=120, dexterity=150, luck=150, accuracy=150, coins=30),
    Mob(name='🦕пехотинец пришельцев', hp=150, attack=130, dexterity=150, luck=150, accuracy=150, coins=30),
    Mob(name='🐋гаргантюа (🌟)', hp=200, attack=150, dexterity=150, luck=150, accuracy=150, coins=30),
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
    Mob(name='👨🏻‍🏭Сайфер', hp=250, attack=125, dexterity=320, luck=320, accuracy=320, coins=210),
    Mob(name='🤵🏻Агент Смит', hp=300, attack=150, dexterity=330, luck=320, accuracy=320, coins=210),
    Mob(name='🦹🏿‍♂️Морфеус', hp=320, attack=200, dexterity=320, luck=320, accuracy=320, coins=210),
    Mob(name='🦹‍♀️Тринити', hp=400, attack=220, dexterity=320, luck=320, accuracy=320, coins=210),
    Mob(name='🦹🏻️Нео', hp=500, attack=250, dexterity=320, luck=320, accuracy=320, coins=210),
    None
]

list_dange60 = [
    Mob(name='🐙зерлинг', hp=400, attack=200, dexterity=410, luck=510, accuracy=710, coins=30),
    Mob(name='🦞гидралиск', hp=450, attack=250, dexterity=410, luck=510, accuracy=710, coins=30),
    Mob(name='🦐муталиск', hp=560, attack=300, dexterity=410, luck=510, accuracy=710, coins=30),
    Mob(name='🦀брудлорд', hp=580, attack=330, dexterity=410, luck=510, accuracy=710, coins=30),
    Mob(name='🦑ультралиск', hp=720, attack=450, dexterity=410, luck=510, accuracy=710, coins=30),
    None
]

list_dange70 = [
    Mob(name='🦂Заразитель (некроморф хитрец)', hp=1000, attack=350, dexterity=810, luck=710, accuracy=910, coins=30),
    Mob(name='🦎Сталкер (некроморф следит)', hp=1250, attack=400, dexterity=810, luck=710, accuracy=910, coins=30),
    Mob(name='🐍Расчленитель (некроморф режущий)', hp=1260, attack=500, dexterity=810, luck=710, accuracy=910,
        coins=30),
    Mob(name='🦖Охотник (некроморф тебя ищет)', hp=1480, attack=530, dexterity=810, luck=710, accuracy=910, coins=30),
    Mob(name='🐊Левиафан (некроморф босс)', hp=1520, attack=650, dexterity=810, luck=710, accuracy=910, coins=30),
    None
]

list_dange80 = [
    Mob(name='🐍Потрошитель ⚡️⚡️', hp=2010, attack=700, dexterity=1220, luck=1020, accuracy=1320, coins=400),
    Mob(name='🦀Тервигон ⚡️⚡️', hp=2210, attack=800, dexterity=1220, luck=1020, accuracy=1320, coins=400),
    Mob(name='🦖Доминатрикс ⚡️⚡️', hp=2510, attack=900, dexterity=1220, luck=1020, accuracy=1320, coins=400),
    Mob(name='🛡Стражи тирана ⚡️⚡️', hp=2610, attack=900, dexterity=1220, luck=1020, accuracy=1320, coins=400),
    Mob(name='🦐Красный Ужас ⚡️⚡️', hp=3010, attack=1000, dexterity=1220, luck=1020, accuracy=1320, coins=400),
    Mob(name='👿Повелитель роя ⚡️⚡️', hp=3010, attack=1300, dexterity=1220, luck=1020, accuracy=1320, coins=400),
    None
]

list_dange90 = [
    Mob(name='Арес (Марс 🌟💢🌟)', hp=4010, attack=1500, dexterity=1620, luck=1620, accuracy=1620, coins=400),
    Mob(name='Посейдон (Нептун 🌟💢🌟)', hp=4210, attack=1600, dexterity=1620, luck=1620, accuracy=1620, coins=400),
    Mob(name='Гефест (Вулкан 🌟💢🌟)️', hp=4510, attack=1700, dexterity=1620, luck=1620, accuracy=1620, coins=400),
    Mob(name='Аполлон 🌟💢🌟', hp=4610, attack=1900, dexterity=1620, luck=1620, accuracy=1620, coins=400),
    Mob(name='Гермес (Меркурий 🌟💢🌟)️', hp=5010, attack=2000, dexterity=1620, luck=1620, accuracy=1620, coins=400),
    Mob(name='Зевс (Юпитер 🌟💢🌟)️', hp=5010, attack=2300, dexterity=1620, luck=1620, accuracy=1620, coins=400),
    None
    ]


danges = {10: list_dange10, 20: list_dange20,
          30: list_dange30, 35: list_dange35, 40: list_dange40,
          50: list_dange50, 60: list_dange60, 70: list_dange70, 80: list_dange80, 90: list_dange90}


list_mk_zone = [
    Mob(name="🧙‍♀️Кунг лао (шапкой закидает🌟🌟)", hp=1710, attack=600, dexterity=720, luck=1020, accuracy=1020, coins=450),
    Mob(name="⚡️Рейден (получи шок🌟🌟)", hp=1710, attack=600, dexterity=720, luck=1020, accuracy=1020, coins=450),
    Mob(name='👊Лю Кэнг (переебет тебе в щи🌟🌟)', hp=1810, attack=600, dexterity=720, luck=1020, accuracy=1020, coins=450),
    Mob(name='❄️Саб-Зиро (отморозит тебе все🌟🌟)', hp=1910, attack=700, dexterity=720, luck=1020, accuracy=1020, coins=450),
    Mob(name='🦂Скорпион (ядовитое🌟🌟)', hp=1910, attack=700, dexterity=720, luck=1020, accuracy=1020, coins=450),
    Mob(name='🦾Джакс (🌟🌟)', hp=1910, attack=700, dexterity=720, luck=1020, accuracy=1020, coins=450),
    Mob(name='🦚Китана (о веер прикольно🌟🌟)', hp=2010, attack=800, dexterity=720, luck=1020, accuracy=1020, coins=450),
    Mob(name='🥷Джейд (сучка тебя уничтожит🌟🌟)', hp=2010, attack=800, dexterity=720, luck=1020, accuracy=1020, coins=450),
    Mob(name='🥷Нубсайбот (🌟🌟)', hp=2010, attack=800, dexterity=720, luck=1020, accuracy=1020,
        coins=450),
    Mob(name='🔪Барака (острые когти🌟🌟)', hp=2110, attack=900, dexterity=1020, luck=1020, accuracy=1020, coins=450),
    Mob(name='💪Горо (много рук🌟🌟)', hp=2110, attack=900, dexterity=1020, luck=1020, accuracy=1020, coins=450),
    Mob(name='👹Шао-Кан (твоя смертушка 🌟🌟)', hp=2210, attack=1000, dexterity=1020, luck=1020, accuracy=1020, coins=450),
]


list_mob_clown_zone = [
    Mob(name='🤡жалкий клоун', hp=550, attack=325, dexterity=620, luck=320, accuracy=320, coins=210),
    Mob(name='🐺волк в цирке (выступает)', hp=550, attack=325, dexterity=620, luck=320, accuracy=320, coins=210),
    Mob(name='🤹🏿мим (хуим)', hp=550, attack=325, dexterity=620, luck=320, accuracy=320, coins=210),
    Mob(name='🎈оно', hp=500, attack=400, dexterity=630, luck=320, accuracy=320, coins=210),
    Mob(name='🤹🏻‍♀️жонглер костями', hp=520, attack=450, dexterity=620, luck=320, accuracy=320, coins=210),
    Mob(name='🎭кровавый арлекин', hp=500, attack=450, dexterity=620, luck=320, accuracy=320, coins=210),
    Mob(name='️🎪 ебучий цирк (будешь выступать)', hp=700, attack=500, dexterity=620, luck=320, accuracy=320,
        coins=210),
    Mob(name='🥲Пьеро (ищет Мальвину⭐️)', hp=1000, attack=490, dexterity=620, luck=320, accuracy=320, coins=210),
    Mob(name='️🙍🏼‍♀️Мальвина⭐️ (нахуй Пьеро)', hp=1200, attack=500, dexterity=620, luck=320, accuracy=320, coins=210),
    Mob(name='🎅🏻️Карабас-барабас (отпиздит тебя плеткой⭐️⭐️)', hp=1500, attack=600, dexterity=720, luck=320,
        accuracy=320, coins=210),
    Mob(name='🃏Джокер (ехидно смеется⭐️⭐️)', hp=1600, attack=650, dexterity=720, luck=320,
        accuracy=320, coins=210),
    Mob(name='🤥Буратино! (закапывает монетки и тебя🌟)', hp=1700, attack=750, dexterity=720, luck=320,
        accuracy=320, coins=210),

]

list_mob_painkiller_zone = [
    Mob(name='🏍Адский байкер 🏵🏵', hp=750, attack=425, dexterity=620, luck=320, accuracy=620, coins=350),
    Mob(name='😷Прокаженный 🏵🏵', hp=750, attack=425, dexterity=620, luck=320, accuracy=620, coins=350),
    Mob(name='👩‍🦽Ампутант 🏵🏵', hp=750, attack=425, dexterity=620, luck=320, accuracy=620, coins=350),
    Mob(name='🐶Анубис 🏵🏵', hp=900, attack=480, dexterity=630, luck=320, accuracy=620, coins=350),
    Mob(name='🦾Биомеханоид ⭐️', hp=900, attack=480, dexterity=620, luck=320, accuracy=620, coins=350),
    Mob(name='😇Ангел ада ⭐️', hp=1000, attack=550, dexterity=620, luck=320, accuracy=620,
        coins=350),
    Mob(name='🏴‍☠️Пират ⭐️', hp=1000, attack=550, dexterity=620, luck=320, accuracy=620,
        coins=410),
    Mob(name='🤯Пожиратель мозгов ⭐️⭐️', hp=1300, attack=590, dexterity=620, luck=320, accuracy=620, coins=410),
    Mob(name='🧑‍🦽Безногий урод ⭐️⭐️', hp=1300, attack=590, dexterity=620, luck=320, accuracy=620, coins=410),
    Mob(name='🧛Архивампир ⭐️⭐️', hp=1500, attack=600, dexterity=620, luck=320, accuracy=620, coins=410),
    Mob(name='😈Черный демон ⭐️⭐️' , hp=1500, attack=680, dexterity=620, luck=320,
        accuracy=620, coins=410),
    Mob(name='💀Череп ⭐️⭐️', hp=1500, attack=680, dexterity=620, luck=320,
        accuracy=620, coins=410),
    Mob(name='🔪Палач 🌟', hp=1600, attack=325, dexterity=680, luck=320, accuracy=620, coins=410),
    Mob(name='🐙Щупальцевый монстр 🌟', hp=1600, attack=680, dexterity=620, luck=320,
        accuracy=620, coins=410),
    Mob(name='🤪Безумный культист 🌟', hp=1700, attack=680, dexterity=620, luck=320,
        accuracy=620, coins=510),
    Mob(name='👹Панцирный демон 🌟', hp=1700, attack=680, dexterity=620, luck=320,
        accuracy=620, coins=510),
    Mob(name='👺Магмовый демон 🌟', hp=1800, attack=750, dexterity=620, luck=320,
        accuracy=620, coins=510),
    Mob(name='🧛Колоссальный вампир 🌟🌟', hp=2000, attack=850, dexterity=620, luck=320,
        accuracy=620, coins=510)

]

list_mob_dino_zone = [
    Mob(name='🦤Птеродактиль ⭐️', hp=750, attack=1000, dexterity=10000, luck=2000, accuracy=500, coins=350),
    Mob(name='🦖Диплодок ⭐️⭐️', hp=2000, attack=1000, dexterity=500, luck=1000, accuracy=10000, coins=360),
    Mob(name='🦖Ахиллобатор ⭐️⭐️', hp=1000, attack=1000, dexterity=1000, luck=1500, accuracy=10000, coins=360),
    Mob(name='🐊Стегозавр ⭐️⭐️', hp=1500, attack=1000, dexterity=500, luck=2000, accuracy=1000, coins=370),
    Mob(name='🦖Спинозавр 🌟', hp=2000, attack=1500, dexterity=500, luck=500, accuracy=500, coins=370),
    Mob(name='🦖Мегалозавр 🌟', hp=2500, attack=1500, dexterity=1500, luck=1000, accuracy=1500, coins=370),
    Mob(name='🦖Гуанлонг 🌟', hp=2200, attack=1500, dexterity=1200, luck=1200, accuracy=1500, coins=370),
    Mob(name='🦖Карнотавр 🌟🌟', hp=2000, attack=1500, dexterity=1500, luck=1500, accuracy=1000, coins=380),
    Mob(name='🦖Археоцератопс 🌟🌟', hp=1500, attack=1500, dexterity=1500, luck=1000, accuracy=1500, coins=380),
    Mob(name='🦖Трицератопс 🌟🌟', hp=1800, attack=2000, dexterity=1200, luck=1200, accuracy=1200, coins=380),
    Mob(name='🦕Бронтозавр 🌟🌟', hp=2000, attack=2000, dexterity=500, luck=1000, accuracy=1000, coins=390),
    Mob(name='🦖Тираннозавр 🌟🌟', hp=3000, attack=2000, dexterity=500, luck=1000, accuracy=1000, coins=390),
]


list_mobs1_5 = [
    Mob(name='🐶крысакот (любопытный)', hp=1, attack=2, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🐱кот (голову тебе отожрет)', hp=3, attack=2, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🐭мутантская мышь убийца', hp=5, attack=2, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🐹хомяк (сожрет твои кишки)', hp=7, attack=2, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🥚яйцо ксеноморфа', hp=9, attack=2, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🐷свинокрыс (злобно хрюкает)', hp=9, attack=3, dexterity=5, luck=5, accuracy=5, coins=20),
    Mob(name='🐸жаба (смотрит и квакает)', hp=9, attack=3, dexterity=5, luck=5, accuracy=5, coins=30),
    Mob(name='🦐лицехват', hp=9, attack=3, dexterity=5, luck=5, accuracy=5, coins=30),
    Mob(name='🧟зомби (скучающий)', hp=9, attack=3, dexterity=5, luck=5, accuracy=5, coins=30),
    Mob(name='🧟‍♀️зомби (любопытный)', hp=9, attack=3, dexterity=5, luck=5, accuracy=5, coins=30),
    Mob(name='🤖робот-убийца', hp=10, attack=3, dexterity=5, luck=5, accuracy=5, coins=30),
    Mob(name='️🤖робот-помощник', hp=10, attack=3, dexterity=5, luck=5, accuracy=5, coins=30),
    Mob(name='️🤖андроид-калека', hp=10, attack=3, dexterity=5, luck=5, accuracy=5, coins=30),
    Mob(name='👯‍♀️блекджек и шлюхи', hp=10, attack=3, dexterity=5, luck=5, accuracy=5, coins=30)
]

list_mobs5_10 = [
    Mob(name='🐷свинокрыс (злобно хрюкает и смотрит)', hp=11, attack=10, dexterity=10, luck=10, accuracy=5, coins=30),
    Mob(name='🦊я лав чина', hp=11, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='🐼панда в декрете', hp=13, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='🦭🦭🦭просто стас🦭🦭🦭', hp=15, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='🌚скобка', hp=17, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='Точа🍗 (травит токсичностью)', hp=17, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='🍒пьяная вишня🍒', hp=19, attack=10, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='❄️Снежка (дает бан⭐️)', hp=19, attack=12, dexterity=10, luck=10, accuracy=10, coins=30),
    Mob(name='⭐️Кирюха (кирюха⭐️)', hp=19, attack=13, dexterity=10, luck=100, accuracy=10, coins=30),
    Mob(name='😰METOKS (Бог нытья😰)', hp=19, attack=13, dexterity=10, luck=100, accuracy=10, coins=30),
    Mob(name='🐸жаба (злится)', hp=19, attack=13, dexterity=10, luck=100, accuracy=10, coins=40),
    Mob(name='☃️☃️☃️𝚃𝙷𝙴𝙻𝚄𝙸𝙳𝙴𝙽☃️☃️☃️ (46 dzen >:)', hp=19, attack=13, dexterity=10, luck=100, accuracy=10,
        coins=30),
    Mob(name='👩🏻‍🦰Собчак (любит конь)', hp=19, attack=13, dexterity=10, luck=100, accuracy=10,
            coins=30),
    Mob(name='🤡Нэвэльный (блэд)', hp=19, attack=13, dexterity=10, luck=100, accuracy=10,
            coins=30),
    Mob(name='🧔‍♂️Джигурда (выебет и коня)', hp=19, attack=13, dexterity=10, luck=100, accuracy=10,
            coins=30),
    Mob(name='👱🏻‍♂️Кличко (смотрит в завтрашний день)', hp=19, attack=13, dexterity=10, luck=100, accuracy=10,
            coins=30),
    Mob(name='🫃Вилса-ком (купи айфон)', hp=19, attack=13, dexterity=10, luck=100, accuracy=10,
            coins=30),
    Mob(name='👯‍♀преферанс и барышни', hp=19, attack=13, dexterity=10, luck=100, accuracy=10,
            coins=30),

]

list_mobs10_15 = [
    Mob(name='🐷свинокрыс (сожрет тебя и твою маму)', hp=21, attack=15, dexterity=30, luck=15, accuracy=15, coins=50),
    Mob(name='🐒макака (с ножом)', hp=21, attack=15, dexterity=30, luck=15, accuracy=15, coins=50),
    Mob(name='🐵обезьяна (пьет кровь)', hp=23, attack=15, dexterity=30, luck=15, accuracy=15, coins=50),
    Mob(name='🐍киберзмей', hp=25, attack=15, dexterity=15, luck=30, accuracy=15, coins=50),
    Mob(name='🐝пчола (укуренная)', hp=27, attack=15, dexterity=30, luck=15, accuracy=15, coins=50),
    Mob(name='🦄гей (пидарас)', hp=29, attack=15, dexterity=30, luck=15, accuracy=15, coins=50),
    Mob(name='🪱грудолом', hp=29, attack=15, dexterity=30, luck=15, accuracy=15, coins=50),
    Mob(name='🐸жаба (мутант)', hp=29, attack=15, dexterity=30, luck=15, accuracy=15, coins=60),
    Mob(name='🐟ЯЯЯЯЯЯЗЬ (!!!!)', hp=29, attack=15, dexterity=30, luck=15, accuracy=15, coins=70),
    Mob(name='🐘зеленый слоник (на покушой)', hp=29, attack=15, dexterity=30, luck=15, accuracy=15, coins=70),
    Mob(name='🍊заводной апельсин (ультранасилие)', hp=29, attack=15, dexterity=30, luck=15, accuracy=15, coins=70),
    Mob(name='🍞кот-хлеб', hp=29, attack=15, dexterity=30, luck=15, accuracy=15, coins=70),
    Mob(name='👠барби (с Гослингом)', hp=29, attack=15, dexterity=30, luck=15, accuracy=15, coins=70),
    Mob(name='⏰будильник (звонит твоим шлюхам)', hp=29, attack=15, dexterity=30, luck=15, accuracy=15, coins=70),
    Mob(name='👯‍♀покер и куртизанки', hp=29, attack=15, dexterity=30, luck=15, accuracy=15, coins=70),
]

list_mobs15_20 = [
    Mob(name='🐷свинокрыс (мутировавший)', hp=31, attack=20, dexterity=60, luck=20, accuracy=20, coins=60),
    Mob(name='🐍змея (железная)', hp=31, attack=20, dexterity=60, luck=20, accuracy=20, coins=60),
    Mob(name='🦇призрак ночи', hp=35, attack=20, dexterity=60, luck=20, accuracy=20, coins=60),
    Mob(name='🐛таракан (радиоактивный)', hp=36, attack=20, dexterity=60, luck=20, accuracy=20, coins=60),
    Mob(name='🐡монстр-наглец (со свинцом)', hp=38, attack=20, dexterity=60, luck=20, accuracy=20, coins=60),
    Mob(name='🦨скунз (воняет радиацией)', hp=39, attack=20, dexterity=20, luck=60, accuracy=20, coins=60),
    Mob(name='🐸жаба (кибернетическая)', hp=39, attack=20, dexterity=20, luck=60, accuracy=20, coins=80),
    Mob(name='🐟ЯЯЯЯЯЯЗЬ (!!!!!!!!!!!)', hp=40, attack=24, dexterity=30, luck=25, accuracy=25, coins=70),
    Mob(name='🐘зеленый слоник (уже покушал)', hp=40, attack=25, dexterity=30, luck=15, accuracy=15, coins=70),
    Mob(name='🍊заводной апельсин (ультраненависть)', hp=40, attack=25, dexterity=30, luck=15, accuracy=15, coins=70),
    Mob(name='🍞кот-хлеб (подгоревший)', hp=40, attack=24, dexterity=30, luck=15, accuracy=15, coins=70),
    Mob(name='⏰будильник (обзвонил шлюх)', hp=40, attack=25, dexterity=30, luck=15, accuracy=15, coins=70),
    Mob(name='👯‍♀нарды и гурии', hp=40, attack=25, dexterity=30, luck=15, accuracy=15, coins=70),
]

list_mobs20_25 = [
    Mob(name='🐷свинокрыс (демонический)', hp=51, attack=30, dexterity=100, luck=20, accuracy=20, coins=80),
    Mob(name='🕷черная вдова', hp=51, attack=30, dexterity=100, luck=20, accuracy=20, coins=80),
    Mob(name='🐟пиранья (хочет крови)', hp=55, attack=30, dexterity=100, luck=20, accuracy=20, coins=80),
    Mob(name='🐬сухопутный делфин-призрак', hp=56, attack=30, dexterity=100, luck=20, accuracy=20, coins=80),
    Mob(name='🐜муравей-робот', hp=58, attack=30, dexterity=100, luck=20, accuracy=20, coins=80),
    Mob(name='🦀гигантский краб (злой)', hp=59, attack=30, dexterity=20, luck=100, accuracy=20, coins=80),
    Mob(name='🐸жаба (демоничекая)', hp=59, attack=30, dexterity=20, luck=100, accuracy=20, coins=100),
    Mob(name='💀терминатор т-70 (прототип)', hp=59, attack=30, dexterity=20, luck=100, accuracy=20, coins=100),
    Mob(name='🕺упячка (чо, чо попячся)', hp=59, attack=30, dexterity=20, luck=100, accuracy=20, coins=100),
    Mob(name='🦈бейбишарк (только попробуй загуглить)', hp=59, attack=30, dexterity=20, luck=100, accuracy=20, coins=100),
    Mob(name='🕊это голубь?', hp=59, attack=30, dexterity=20, luck=100, accuracy=20, coins=100),
    Mob(name='💷Фрай (заткнись и возьми мои деньги)', hp=59, attack=30, dexterity=20, luck=100, accuracy=20, coins=100),
    Mob(name='🦛Муми-тролль (зарежу ножом)', hp=59, attack=30, dexterity=20, luck=100, accuracy=20, coins=100),
    Mob(name='👯‍♀шахматы и библиотекарши', hp=59, attack=30, dexterity=20, luck=100, accuracy=20, coins=100),
    Mob(name='🦭ждун (ждет)', hp=59, attack=30, dexterity=20, luck=100, accuracy=20, coins=100),
]

list_mobs25_30 = [
    Mob(name='🐷свинокрыс (кибернетический)', hp=71, attack=50, dexterity=120, luck=120, accuracy=120, coins=100),
    Mob(name='🐀мистическая крыса', hp=71, attack=50, dexterity=120, luck=120, accuracy=120, coins=100),
    Mob(name='👽молодой ксеноморф', hp=75, attack=50, dexterity=120, luck=120, accuracy=120, coins=100),
    Mob(name='🐲дракон (маленький)', hp=76, attack=50, dexterity=120, luck=120, accuracy=120, coins=100),
    Mob(name='🚬курильщик', hp=78, attack=50, dexterity=120, luck=120, accuracy=120, coins=100),
    Mob(name='🚬нарик (с косяком)', hp=79, attack=50, dexterity=120, luck=120, accuracy=120, coins=100),
    Mob(name='🐸жаба (мифическая)', hp=100, attack=70, dexterity=120, luck=120, accuracy=120, coins=120),
    Mob(name='💀терминатор T-800 (ищет Сарру Конор)', hp=90, attack=60, dexterity=120, luck=120, accuracy=120, coins=120),
    Mob(name='👮🏻‍♀️терминатор T-1000 (превратился в пол)', hp=90, attack=60, dexterity=120, luck=120, accuracy=120, coins=120),
    Mob(name='👯‍♀тротил и шахидки', hp=90, attack=60, dexterity=120, luck=120, accuracy=120, coins=120),
]

list_mobs30_35 = [
    Mob(name='🐷свинокрыс (мифический🥉🥉🥉)', hp=101, attack=70, dexterity=120, luck=200, accuracy=120, coins=120),
    Mob(name='🐸жаба (киллер🥉)', hp=105, attack=70, dexterity=120, luck=200, accuracy=120, coins=120),
    Mob(name='🐊крокодил (не Гена🥉)', hp=106, attack=70, dexterity=120, luck=200, accuracy=120, coins=120),
    Mob(name='🐙осьминог (небольшой🥉)', hp=108, attack=70, dexterity=120, luck=200, accuracy=120, coins=120),
    Mob(name='🦞рак (клешни лезвия🥉)', hp=109, attack=70, dexterity=120, luck=200, accuracy=120, coins=120),
    Mob(name='🐸жаба (ядерная🥉)', hp=130, attack=90, dexterity=120, luck=200, accuracy=120, coins=150),
    Mob(name='👽ксеноморф (зрелый🥉)', hp=109, attack=70, dexterity=120, luck=200, accuracy=120, coins=120),
    Mob(name='🚬нарик (ищет закладку🥉)', hp=109, attack=70, dexterity=120, luck=200, accuracy=120, coins=120),
    Mob(name='👩🏼‍⚖️ терминатор T-3000', hp=120, attack=80, dexterity=120, luck=220, accuracy=210, coins=140),
    Mob(name='🦹🏽терминатор T-5000', hp=120, attack=80, dexterity=120, luck=220, accuracy=220, coins=140),
    Mob(name='🌕🌝🌕чебурашка (чебурашнулся🥉)', hp=126, attack=90, dexterity=120, luck=200, accuracy=120, coins=150),
    Mob(name='🧙‍♀️шапакляк (не бабка🥉)', hp=126, attack=90, dexterity=120, luck=200, accuracy=120, coins=150),
    Mob(name='💩мистер гавняшка (хеппи shitter year!!🥉)', hp=126, attack=90, dexterity=120, luck=200, accuracy=120, coins=150),
    Mob(name='🧻полотенчик (пыхнем?🥉)', hp=126, attack=90, dexterity=120, luck=200, accuracy=120, coins=150),
    Mob(name='👯‍♀игрища и блудницы', hp=126, attack=90, dexterity=120, luck=200, accuracy=120, coins=150),
]

list_mobs35_40 = [
    Mob(name='🐷свинокрыс (радиоактивный🥈)', hp=140, attack=100, dexterity=220, luck=220, accuracy=120, coins=150),
    Mob(name='🦐креведка (белорусская🥈)', hp=140, attack=100, dexterity=220, luck=220, accuracy=120, coins=150),
    Mob(name='🐻медвед (шлюха🥈)', hp=140, attack=100, dexterity=220, luck=220, accuracy=120, coins=150),
    Mob(name='🐺волк (не выступает в цирке🥈)', hp=140, attack=100, dexterity=220, luck=220, accuracy=120, coins=150),
    Mob(name='🦆утка (кря-кря🥈)', hp=145, attack=100, dexterity=220, luck=220, accuracy=120, coins=150),
    Mob(name='🦎чупакабра (🥈)', hp=150, attack=100, dexterity=220, luck=220, accuracy=120, coins=150),
    Mob(name='🐸жаба (термоядерная🥈)', hp=190, attack=140, dexterity=220, luck=220, accuracy=120, coins=180),
    Mob(name='💀терминатор Rev-9', hp=170, attack=120, dexterity=220, luck=220, accuracy=220, coins=180),
    Mob(name='💃инстасамка (сядет на лицо🥈)', hp=180, attack=130, dexterity=220, luck=220, accuracy=220, coins=180),
    Mob(name='🐟альфа-сомец', hp=180, attack=130, dexterity=220, luck=220, accuracy=220, coins=180),
    Mob(name='🧽Спанч Боб (квадратные штаны🥈)', hp=180, attack=130, dexterity=220, luck=220, accuracy=220, coins=180),
    Mob(name='🐖свiня (в джакузi)', hp=180, attack=130, dexterity=220, luck=220, accuracy=220, coins=180),
]

list_mobs40_45 = [
    Mob(name='🐷свинокрыс (исполинский🥇)', hp=200, attack=150, dexterity=320, luck=320, accuracy=320, coins=160),
    Mob(name='🐲дракон (большой🥇)', hp=200, attack=150, dexterity=320, luck=320, accuracy=320, coins=160),
    Mob(name='🐺волк (выступает в цирке🥇)', hp=220, attack=150, dexterity=320, luck=320, accuracy=320, coins=160),
    Mob(name='🐻медвед (превед🥇)', hp=240, attack=150, dexterity=320, luck=320, accuracy=320, coins=160),
    Mob(name='🦂скорпион (ядовитый🥇)', hp=260, attack=150, dexterity=320, luck=320, accuracy=320, coins=160),
    Mob(name='🕵️сыщик (жрет пончики🥇)', hp=270, attack=150, dexterity=320, luck=320, accuracy=320, coins=160),
    Mob(name='🐸жаба (средовая🥇)', hp=300, attack=180, dexterity=320, luck=320, accuracy=320, coins=190),
    Mob(name='🐁мыш (закралась🥇)', hp=270, attack=150, dexterity=320, luck=320, accuracy=320, coins=180),
    Mob(name='😡ЪУЪ (СЪУКА🥇)', hp=280, attack=150, dexterity=320, luck=320, accuracy=320, coins=180),
    Mob(name='🐄польская корова (коксу пенч грам??🥇)', hp=290, attack=160, dexterity=320, luck=320, accuracy=320, coins=180),
    Mob(name='🦎рептилоид (правительство🥇)', hp=290, attack=160, dexterity=320, luck=320, accuracy=320, coins=180),
    Mob(name='🎓шапочка из фольги (от заговора🥇)', hp=290, attack=170, dexterity=320, luck=320, accuracy=320, coins=180),

]

list_mobs45_50 = [
    Mob(name='🐷свинокрыс (ты охуешь какой он🏵)', hp=340, attack=200, dexterity=320, luck=320, accuracy=320, coins=170),
    Mob(name='🧑🏿‍🏫айтишник (с геморроем🏵)', hp=340, attack=200, dexterity=320, luck=320, accuracy=320, coins=170),
    Mob(name='👶малыш (разорвет тебя🏵)', hp=320, attack=200, dexterity=320, luck=320, accuracy=320, coins=170),
    Mob(name='👮полиция (курит что-то🏵)', hp=341, attack=200, dexterity=320, luck=320, accuracy=320, coins=170),
    Mob(name='🕵️сыщик (ищет твой труп🏵)', hp=345, attack=200, dexterity=320, luck=320, accuracy=320, coins=170),
    Mob(name='👵🏿бабка (с аннигилятором🏵)', hp=360, attack=200, dexterity=320, luck=320, accuracy=320, coins=170),
    Mob(name='👨‍🦳дед (с аннигилятором🏵)', hp=370, attack=210, dexterity=320, luck=320, accuracy=320, coins=170),
    Mob(name='🐸жаба (легендарная🏵)', hp=380, attack=220, dexterity=320, luck=320, accuracy=320, coins=210),
    Mob(name='🐴конь БоДжек(нюхает герыч🏵)', hp=370, attack=210, dexterity=330, luck=320, accuracy=330, coins=200),
    Mob(name='🧑🏼‍🔬Джесси (готовит кристаллы🏵)', hp=370, attack=210, dexterity=330, luck=320, accuracy=330, coins=200),
    Mob(name='👴Хайзенберг (самое время варить🏵)', hp=370, attack=210, dexterity=330, luck=320, accuracy=330, coins=200),
    Mob(name='👦🏻Картман (не жирный, а кость широкая🏵)', hp=370, attack=210, dexterity=330, luck=320, accuracy=330, coins=200),
    Mob(name='👺Gazizov (где донаты??🏵)', hp=370, attack=210, dexterity=330, luck=320, accuracy=330, coins=200),
    Mob(name='👌Панасенков (всех переиграл🏵)', hp=370, attack=210, dexterity=330, luck=320, accuracy=330, coins=200),
]

list_mobs50_55 = [
    Mob(name='🐷свинокрыс (тварь дрожи и беги🏵🏵)', hp=410, attack=250, dexterity=420, luck=420, accuracy=420,
        coins=190),
    Mob(name='👶малыш (крадется за памперсом🏵🏵)', hp=410, attack=250, dexterity=420, luck=420, accuracy=420,
        coins=190),
    Mob(name='🧑‍✈️летчик-зомби', hp=425, attack=250, dexterity=420, luck=420, accuracy=420, coins=190),
    Mob(name='👩‍🚀космонавтка (хочет в космос🏵🏵)', hp=445, attack=250, dexterity=420, luck=420, accuracy=420,
        coins=190),
    Mob(name='👩‍🚒пожарный (разводит пожар🏵🏵)', hp=467, attack=250, dexterity=420, luck=420, accuracy=420,
        coins=190),
    Mob(name='🧓🏽бабка (у подъезда🏵🏵)', hp=490, attack=250, dexterity=420, luck=420, accuracy=420, coins=190),
    Mob(name='🐸жаба (из ада🏵🏵)', hp=510, attack=260, dexterity=450, luck=450, accuracy=470, coins=230),
    Mob(name='😈Джек-потрошитель (в твоих снах🏵🏵)', hp=450, attack=250, dexterity=450, luck=400, accuracy=400, coins=210),
    Mob(name='👻Нечто (что это🏵🏵)', hp=450, attack=220, dexterity=400, luck=450, accuracy=400, coins=210),
    Mob(name='🦇Джиперс-криперс (ждет тебя🏵🏵)', hp=490, attack=250, dexterity=420, luck=420, accuracy=420, coins=210),
    Mob(name='🧌Хищник (за тобой охотится🏵🏵)', hp=490, attack=260, dexterity=400, luck=420, accuracy=450, coins=210),
    Mob(name='👽Чужой (матка 🏵🏵)', hp=500, attack=260, dexterity=420, luck=420, accuracy=420, coins=220),
    Mob(name='☠️Особь (голодная 🏵🏵)', hp=490, attack=240, dexterity=400, luck=470, accuracy=470, coins=210),
    Mob(name='👾Крикун (прячется в песке 🏵🏵)', hp=500, attack=200, dexterity=450, luck=420, accuracy=470, coins=220),
]

list_mobs55_60 = [
    Mob(name='🐷свинокрыс (бегииии!!⭐️)', hp=610, attack=400, dexterity=520, luck=520, accuracy=520, coins=250),
    Mob(name='🧔‍♀️баба с бородой (пездец⭐️)', hp=610, attack=400, dexterity=520, luck=520, accuracy=520, coins=250),
    Mob(name='🧑‍🎤зеленый хер⭐️', hp=620, attack=400, dexterity=520, luck=420, accuracy=520, coins=250),
    Mob(name='💂‍♀️солдат королевы (думает о королеве⭐️)', hp=640, attack=400, dexterity=520, luck=520, accuracy=520,
        coins=250),
    Mob(name='👨‍🎓бакалавр (с шизой⭐️)', hp=665, attack=400, dexterity=520, luck=520, accuracy=520, coins=250),
    Mob(name='🧕моджахедка (с бомбой⭐️)', hp=670, attack=400, dexterity=520, luck=520, accuracy=520, coins=250),
    Mob(name='🐸жаба (шизоидная⭐️)', hp=790, attack=420, dexterity=520, luck=520, accuracy=520, coins=290),
    Mob(name='🐻вонни (т прнс?⭐️)', hp=720, attack=420, dexterity=520, luck=520, accuracy=520, coins=280),
    Mob(name='🐷потачок (нт⭐️)', hp=720, attack=420, dexterity=520, luck=520, accuracy=520, coins=280),
    Mob(name='🦆долан (с уважением⭐️)', hp=770, attack=420, dexterity=520, luck=520, accuracy=520, coins=280),
]

list_mobs60_65 = [
    Mob(name='👩‍🍳повар (спрашивает у повара⭐️⭐️)', hp=810, attack=600, dexterity=620, luck=520, accuracy=620,
        coins=300),
    Mob(name='👨‍🌾писатель (напишет тебе хуй на голове⭐️⭐️)', hp=820, attack=600, dexterity=620, luck=620,
        accuracy=620, coins=300),
    Mob(name='🧙‍♀️маг (объелся мухоморов⭐️⭐️)', hp=840, attack=600, dexterity=620, luck=620, accuracy=620, coins=300),
    Mob(name='🧛‍♀️вампир (кровушки бы⭐️⭐️)', hp=865, attack=600, dexterity=620, luck=620, accuracy=620, coins=300),
    Mob(name='💁‍♀️твоя бывшая', hp=870, attack=600, dexterity=620, luck=620, accuracy=620, coins=300),
    Mob(name='🐸жаба (️твоя бывшая⭐️⭐️)', hp=900, attack=700, dexterity=720, luck=720, accuracy=720, coins=350),
    Mob(name='🐇кролик Роджер  (подставленный ️⭐️⭐️)', hp=870, attack=600, dexterity=620, luck=620, accuracy=620, coins=330),
    Mob(name='🐺вервольф (кибернетический ️⭐️⭐️)', hp=870, attack=600, dexterity=620, luck=620, accuracy=620, coins=330),
    Mob(name='🦊лиса (и ее грязная норка ️⭐️⭐️)', hp=870, attack=650, dexterity=620, luck=620, accuracy=620, coins=330),
    Mob(name='🐿белка (и ее очень большое дупло ️⭐️⭐️)', hp=870, attack=650, dexterity=620, luck=620, accuracy=620, coins=330),
    Mob(name='🐦дятел (долбит шишки ️⭐️⭐️)', hp=870, attack=650, dexterity=620, luck=620, accuracy=620,
        coins=330),
    Mob(name='🌚колобок-негр (️от дедушки ушел⭐️⭐️)', hp=900, attack=650, dexterity=720, luck=720, accuracy=720, coins=340),
    Mob(name='🌝колобок (️от бабушки ушел⭐️⭐️)', hp=900, attack=700, dexterity=720, luck=720, accuracy=720, coins=340),
    Mob(name='💜Тинки-Винки (️телепузик любопытный⭐️⭐️)', hp=950, attack=600, dexterity=820, luck=820, accuracy=720,
        coins=350),
    Mob(name='💚Дипси (️телепузик игривый⭐️⭐️)', hp=850, attack=650, dexterity=720, luck=720, accuracy=720, coins=350),
    Mob(name='🧡Ляля (️телепузик смешной⭐️⭐️)', hp=750, attack=700, dexterity=820, luck=720, accuracy=820,
        coins=350),
    Mob(name='❤️По (️телепузик меткий⭐️⭐️)', hp=800, attack=650, dexterity=820, luck=820, accuracy=1220, coins=350),
]

list_mobs65_70 = [
    Mob(name='🐺волк (кибернетический🌟)', hp=1200, attack=700, dexterity=720, luck=720, accuracy=720, coins=320),
    Mob(name='🧓🏽бабка (терминатор🌟)', hp=1200, attack=700, dexterity=720, luck=720, accuracy=720, coins=320),
    Mob(name='🧑‍✈️летчик (истребителя🌟)', hp=1250, attack=700, dexterity=720, luck=720, accuracy=720, coins=320),
    Mob(name='👶малыш (из твоих кошмаров🌟)', hp=1250, attack=650, dexterity=720, luck=720, accuracy=720, coins=320),
    Mob(name='👮полиция (ест пончики🌟)', hp=1270, attack=650, dexterity=720, luck=720, accuracy=720, coins=320),
    Mob(name='🕴Хан Соло (возит контрабанду🌟)', hp=1300, attack=750, dexterity=720, luck=720, accuracy=720, coins=320),
    Mob(name='🤖R2-D2 (пип-пип🌟)', hp=1250, attack=750, dexterity=720, luck=720, accuracy=720, coins=350),
    Mob(name='🧙🏻‍♂️Оби-Ван Кеноби (присматривает за Люком🌟)', hp=1300, attack=750, dexterity=720, luck=520, accuracy=720, coins=350),
    Mob(name='🦍Чубакка (долго не мылся🌟)', hp=1250, attack=750, dexterity=720, luck=720, accuracy=720, coins=350),
    Mob(name='🤖C-3PO(консультирует в этикете🌟)', hp=1250, attack=750, dexterity=720, luck=720, accuracy=720, coins=350),
    Mob(name='🧑🏿‍🏫ABOBO (boss🌟)', hp=1200, attack=650, dexterity=720, luck=720, accuracy=720, coins=320),
    Mob(name='🦔BIG BLACK (boss🌟)', hp=1250, attack=650, dexterity=720, luck=720, accuracy=720, coins=320),
    Mob(name='👨‍🎤ROPER (boss🌟)', hp=1300, attack=600, dexterity=800, luck=720, accuracy=720, coins=320),
    Mob(name='💀SHADOW BOSS (boss🌟)', hp=1350, attack=700, dexterity=800, luck=720, accuracy=720, coins=320),
    Mob(name='🤖ROBO MANUS (boss🌟)', hp=1370, attack=700, dexterity=800, luck=720, accuracy=720, coins=320),
    Mob(name='👸THE DARK QUEEN (boss🌟)', hp=1370, attack=700, dexterity=800, luck=720, accuracy=720, coins=320),
    Mob(name='🐸Rash (battletoad🌟)', hp=1400, attack=650, dexterity=620, luck=720, accuracy=720, coins=320),
    Mob(name='🐸Zitz (battletoad🌟)', hp=1350, attack=700, dexterity=700, luck=720, accuracy=720, coins=320),
    Mob(name='🐸Pimple (battletoad🌟)', hp=1300, attack=750, dexterity=720, luck=720, accuracy=720, coins=320),
]

list_mobs70_75 = [
    Mob(name='🐲дракон (механизированный🌟🌟)', hp=1500, attack=900, dexterity=720, luck=520, accuracy=1020, coins=350),
    Mob(name='🦑кальмар (мистический🌟🌟)', hp=1520, attack=900, dexterity=720, luck=520, accuracy=1020, coins=350),
    Mob(name='⚓якорь (проклятый🌟🌟)', hp=1540, attack=900, dexterity=720, luck=520, accuracy=1020, coins=350),
    Mob(name='🪝крюк потрошителя', hp=1565, attack=900, dexterity=720, luck=520, accuracy=1020, coins=350),
    Mob(name='🗿каменный голем (легендарный🌟🌟)', hp=1600, attack=900, dexterity=720, luck=520, accuracy=1020,
        coins=350),
    Mob(name='🦹🏿‍♂️Дарт Вейдер (переходи на темную сторону🌟🌟)', hp=1600, attack=900, dexterity=820, luck=720, accuracy=1020,
            coins=400),
    Mob(name='🧑🏼‍💼Люк Скайуокер (махает световым мечом🌟🌟)', hp=1600, attack=900, dexterity=820, luck=720, accuracy=1020,
            coins=400),
    Mob(name='👰🏼‍♀️Лея Органа (убьет сексуальностью🌟🌟)', hp=1600, attack=900, dexterity=820, luck=720, accuracy=1020,
            coins=400),
    Mob(name='🐢Йода (леветирует и ебашит🌟🌟)', hp=1600, attack=900, dexterity=820, luck=720, accuracy=1020,
            coins=400),
    Mob(name='👶Голлум (моя прелесть🌟🌟)', hp=1400, attack=1000, dexterity=920, luck=820, accuracy=1220,
                coins=400),
    Mob(name='🤴Арагорн (король 🌟🌟)', hp=1800, attack=800, dexterity=1020, luck=720, accuracy=1020,
                coins=400),
    Mob(name='🧙Гэндальф (ты не пройдешь 🌟🌟)', hp=1300, attack=1100, dexterity=1020, luck=1020, accuracy=1220,
                coins=400),
    Mob(name='👦🏻Фродо (несет кольцо 🌟🌟)', hp=1500, attack=900, dexterity=1020, luck=1020, accuracy=1020,
        coins=400),
    Mob(name='🦹🏿‍♂️Саурон (смерть всем 🌟🌟)', hp=1600, attack=1000, dexterity=720, luck=720, accuracy=720,
        coins=400),
]

list_mobs75_80 = [
    Mob(name='🧞Джин (ужасающий⚡️⚡ )️', hp=2010, attack=900, dexterity=1020, luck=720, accuracy=1020, coins=370),
    Mob(name='🧜🏿‍♀️Русалка (Нетфликс⚡⚡ )️️', hp=2150, attack=1000, dexterity=820, luck=720, accuracy=1020, coins=370),
    Mob(name='🧚🏻‍♀️Фея (твоих кошмарных снов⚡⚡ )️️', hp=2200, attack=1100, dexterity=1020, luck=720, accuracy=1020, coins=370),
    Mob(name='🧜🏾‍♂️Тритон (Бог⚡⚡ )️️', hp=2200, attack=1100, dexterity=1020, luck=720, accuracy=1020, coins=370),
    Mob(name='🧜🏻Тритон (кибертрон⚡️⚡️ )', hp=2300, attack=1200, dexterity=1020, luck=720, accuracy=1020, coins=370),
    Mob(name='🔳Разум (кибернетический⚡️⚡️ )', hp=2300, attack=1200, dexterity=1020, luck=720, accuracy=1020, coins=370),
    Mob(name='🧞‍♂️Джин (колоссальный⚡️⚡️ )', hp=2300, attack=1200, dexterity=1020, luck=720, accuracy=1020, coins=370),
    Mob(name='🧞‍♀Джин (фантастический⚡️⚡️ )', hp=2500, attack=1200, dexterity=1020, luck=720, accuracy=1020, coins=370),
    Mob(name='🧞‍♀Джин (сила⚡️⚡️ )', hp=2200, attack=1250, dexterity=1020, luck=1020, accuracy=1020, coins=370),
    Mob(name='🧞Джин (гуль⚡️⚡️ )', hp=2200, attack=1100, dexterity=1420, luck=1020, accuracy=1220, coins=370),
    Mob(name='🧞‍♀Джин (ифрит⚡️⚡️ )', hp=2400, attack=1100, dexterity=1220, luck=1020, accuracy=1020, coins=370),
    Mob(name='🧞Джин (марид⚡️⚡️ )', hp=2000, attack=1100, dexterity=1420, luck=1420, accuracy=1420, coins=370),
    Mob(name='🐉Змей горыныч (дышит огнем⚡️⚡️ )', hp=2000, attack=1000, dexterity=1820, luck=1420, accuracy=1420, coins=370),
    Mob(name='💀Кощей Бессмертный  (смерть в игле⚡️⚡️ )', hp=2500, attack=1300, dexterity=1120, luck=1120, accuracy=1020, coins=370),

]

list_mobs80_85 = [
    Mob(name='Угх Зан III ⚡⚡(️🌟)', hp=2600, attack=1300, dexterity=1220, luck=720, accuracy=1320, coins=400),
    Mob(name='Биотанк ⚡️⚡(️🌟)', hp=2700, attack=1300, dexterity=1220, luck=720, accuracy=1320, coins=400),
    Mob(name='Арахноид (взрослый) ⚡️⚡(️🌟)', hp=2750, attack=1400, dexterity=1220, luck=720, accuracy=1320, coins=400),
    Mob(name='Алудранский Рептилоид ⚡️⚡(️🌟️🌟)', hp=2900, attack=1400, dexterity=1220, luck=720, accuracy=1320, coins=400),
    Mob(name='Кукулькан, Бог Ветра ⚡️⚡(️🌟️🌟)', hp=3000, attack=1500, dexterity=1220, luck=720, accuracy=1320, coins=400),
    Mob(name='Личинка-Экзотех ⚡️⚡(️🌟️🌟️🌟)', hp=3300, attack=1500, dexterity=1220, luck=720, accuracy=1320, coins=400),
    Mob(name='Мордехай Заклинатель ⚡️⚡(️🌟️🌟️🌟)', hp=3300, attack=1500, dexterity=1220, luck=720, accuracy=1320, coins=400),
    Mob(name='Болотный прыгун ⚡️⚡(️🌟️🌟️🌟)', hp=3000, attack=1200, dexterity=1820, luck=1000, accuracy=1320, coins=400),

]

list_mobs85_90 = [
    Mob(name='Вергилий 💢(🌟)', hp=3200, attack=1600, dexterity=1520, luck=1020, accuracy=1420, coins=450),
    Mob(name='Атеон 💢(🌟)', hp=3200, attack=1600, dexterity=1520, luck=1020, accuracy=1420, coins=450),
    Mob(name='Galamoth 💢(🌟🌟)', hp=3300, attack=1650, dexterity=1320, luck=1620, accuracy=1420, coins=450),
    Mob(name='Лавовый Голем 💢(🌟🌟)', hp=3450, attack=1700, dexterity=1320, luck=1120, accuracy=1420, coins=450),
    Mob(name='Дымный Рыцарь 💢(🌟🌟)', hp=3400, attack=1750, dexterity=1320, luck=1220, accuracy=1420, coins=450),
    Mob(name='Рам-Бог 💢(🌟🌟)', hp=3450, attack=1700, dexterity=1320, luck=920, accuracy=1420, coins=450),
    Mob(name='Крепость Ментала 💢(🌟🌟🌟)', hp=3600, attack=1800, dexterity=1320, luck=920, accuracy=1420, coins=450),
    Mob(name='Рахлум 💢(🌟🌟🌟)', hp=3600, attack=1800, dexterity=1420, luck=1220, accuracy=1520, coins=450),
    Mob(name='Мундус 💢(🌟🌟🌟)', hp=3600, attack=1800, dexterity=1420, luck=1220, accuracy=1420, coins=450),

]

list_mobs90_95 = [
    Mob(name='Амфисбена 🎇(🌟)', hp=4000, attack=1700, dexterity=1420, luck=1520, accuracy=1520, coins=550),
    Mob(name='Горгона 🎇(🌟)', hp=4000, attack=1700, dexterity=1400, luck=1520, accuracy=1520, coins=550),
    Mob(name='Дракайн 🎇(🌟)', hp=4000, attack=1700, dexterity=1420, luck=1520, accuracy=1520, coins=550),
    Mob(name='Пегас 🎇(🌟🌟)', hp=4300, attack=1800, dexterity=1420, luck=1520, accuracy=1520, coins=550),
    Mob(name='Титан 🎇(🌟🌟)', hp=4300, attack=1800, dexterity=1420, luck=1520, accuracy=1520, coins=550),
    Mob(name='Кербер 🎇(🌟🌟)', hp=4300, attack=1800, dexterity=1420, luck=1520, accuracy=1520, coins=550),
    Mob(name='Минотавр 🎇(🌟🌟🌟)', hp=4500, attack=1900, dexterity=1400, luck=1520, accuracy=1520, coins=550),
    Mob(name='Грифон 🎇(🌟🌟🌟)', hp=4500, attack=1900, dexterity=1420, luck=1520, accuracy=1520, coins=550),
    Mob(name='Гидра Лернейская 🎇(🌟🌟🌟)', hp=4500, attack=1900, dexterity=1420, luck=1520, accuracy=1520, coins=550),
    Mob(name='Гарпии 🎇(🌟🌟🌟)', hp=4500, attack=1900, dexterity=1420, luck=1520, accuracy=1520, coins=550)
]

list_mobs95_100 = [
    Mob(name='Лосяш 🔮(🌟)', hp=4500, attack=2000, dexterity=1520, luck=1620, accuracy=1720, coins=600),
    Mob(name='Пин 🔮(🌟)', hp=4500, attack=2100, dexterity=1500, luck=1620, accuracy=1720, coins=600),
    Mob(name='Бараш 🔮(🌟🌟)', hp=5000, attack=2200, dexterity=1520, luck=1620, accuracy=1720, coins=600),
    Mob(name='Крош 🔮(🌟🌟)', hp=5000, attack=2200, dexterity=1520, luck=1620, accuracy=1720, coins=600),
    Mob(name='Нюша 🔮(🌟🌟)', hp=5000, attack=2200, dexterity=1500, luck=1620, accuracy=1720, coins=600),
    Mob(name='Копатыч 🔮(🌟🌟)', hp=5000, attack=2300, dexterity=1520, luck=1620, accuracy=1720, coins=600),
    Mob(name='Совунья 🔮(🌟🌟🌟)', hp=5500, attack=2400, dexterity=1520, luck=1620, accuracy=1720, coins=600),
    Mob(name='Кар-Карыч 🔮(🌟🌟🌟)', hp=5500, attack=2400, dexterity=1520, luck=1620, accuracy=1720, coins=600),
    Mob(name='Жулик 🔮(🌟🌟🌟)', hp=5500, attack=2400, dexterity=1520, luck=1720, accuracy=1820, coins=600),
    Mob(name='Подболотник 🔮(🌟🌟🌟)', hp=5500, attack=2400, dexterity=1500, luck=1720, accuracy=1820, coins=600),
]

list_mobs100_105 = [
    Mob(name='Фиксик Шпулик 🔩(🌟)', hp=5500, attack=2600, dexterity=1920, luck=1920, accuracy=1820, coins=650),
    Mob(name='Фиксик Ватрушка 🔩(🌟)', hp=5500, attack=2700, dexterity=1900, luck=1920, accuracy=1820, coins=650),
    Mob(name='Фиксик Кусачка 🔩(🌟🌟)', hp=6000, attack=2700, dexterity=1920, luck=1920, accuracy=1820, coins=650),
    Mob(name='Фиксик Кнопка 🔩(🌟🌟)', hp=6000, attack=2700, dexterity=1920, luck=1920, accuracy=1820, coins=650),
    Mob(name='Фиксик Шурупчик 🔩(🌟🌟🌟)', hp=6500, attack=2800, dexterity=1920, luck=1920, accuracy=1720, coins=650),
    Mob(name='Фиксик Болтик 🔩(🌟🌟🌟)', hp=6500, attack=2800, dexterity=1920, luck=1920, accuracy=1720, coins=650)
]

list_boss = [
    Mob(name='💀Некрогигант ⚡️🌟⚡', hp=3500, attack=200, dexterity=50, luck=120, accuracy=1000, coins=400, km=31),
    Mob(name='Мрачный жнец ⚡️🌟⚡', hp=3000, attack=170, dexterity=50, luck=120, accuracy=1000, coins=400, km=16),
]

list_mobs = [list_mobs1_5, list_mobs5_10,
             list_mobs10_15, list_mobs15_20,
             list_mobs20_25, list_mobs25_30,
             list_mobs30_35, list_mobs35_40,
             list_mobs40_45, list_mobs45_50,
             list_mobs50_55, list_mobs55_60,
             list_mobs60_65, list_mobs65_70,
             list_mobs70_75, list_mobs75_80,
             list_mobs80_85, list_mobs85_90, list_mobs90_95, list_mobs95_100, list_mobs100_105
             ]
