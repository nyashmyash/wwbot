import copy
import random
#from hero import Hero

# сила ловка удача меткость харизма hp голод


used_items = {100: {"name": "сырое мясо", "hungry": 30, "hp": 2},
              101: {"name": "жареная курица", "hungry": 25, "hp": 3},
              102: {"name": "картошка", "hungry": 20, "hp": 1},
              103: {"name": "радиоактивная картошка", "hungry": 15},
              104: {"name": "мутантский салат", "hungry": 15, "hp": -3},
              105: {"name": "жаренное мясо", "hungry": 35, "hp": 5},
              106: {"name": "гнилое мясо", "hungry": 25, "hp": -2},
              107: {"name": "вонючая жижа", "hungry": 30, "hp": -5},
              108: {"name": "хомячок", "hungry": 15, "hp": -1},
              109: {"name": "крыса", "hungry": 10, "hp": -2},
              110: {"name": "аптечка", "hp": 10, "hungry": 10},
              111: {"name": "большая аптечка", "hp": 30, "hungry": 10},
              112: {"name": "консервы", "hp": 10, "hungry": 35},
              113: {"name": "гнилые фрукты", "hp": -3, "hungry": 35},
              114: {"name": "вяленое мясо", "hungry": 40},
              200: {"name": "пиво", "force": 10, "luck": 20, "km": 10},
              201: {"name": "вино", "force": 15, "luck": 20, "km": 20},
              202: {"name": "водка", "force": 30, "luck": 50, "km": 30},
              203: {"name": "абсент", "force": 50, "luck": 60, "km": 40},
              204: {"name": "урановая настойка", "force": 70, "luck": 60, "km": 50},
              205: {"name": "стероиды", "dexterity": 50, "accuracy": 50, "km": 20},
              206: {"name": "психонавт", "dexterity": 100, "accuracy": 100, "km": 30},
              207: {"name": "мельдоний", "dexterity": 150, "accuracy": 150, "km": 40},
              208: {"name": "прививка", "km_protect": 15},
              209: {"name": "антибиотик", "km_protect": 25},
              300: {"name": "💉Мед-Х", "hp": 50},
              301: {"name": "💌Медпак", "hp": 80},
              302: {"name": "🧪Стимбласт", "hp": 120, "km_heal": 3},
              303: {"name": "🧪Стимбласт+", "hp": 150, "km_heal": 5},
              400: {"name": "☢️модификатор ядерный тип А", "damage": 50, "armor": 55, "dexterity": -100,
                    "accuracy": -100},
              401: {"name": "⚛️модификатор тритиевый", "damage": 70, "armor": 75, "dexterity": -150, "accuracy": -150},
              402: {"name": "☢️модификатор ядерный тип Б", "damage": 75, "armor": 85, "dexterity": -170,
                    "accuracy": -150},
              403: {"name": "👽модификатор тирранид", "damage": 100, "armor": 110, "dexterity": -200, "accuracy": -200},
              404: {"name": "☠️модификатор проклятый", "damage": 110, "armor": 120, "dexterity": -100, "luck": -250, "accuracy": -250},
              405: {"name": "🤸🏽‍♂️модификатор ловкости", "damage": -40, "armor": -40, "dexterity": 200},
              406: {"name": "🎯модификатор точности", "damage": -40, "armor": -40, "accuracy": 200},
              407: {"name": "️🤪модификатор глупец", "damage": -60, "armor": -60, "dexterity": 150, "accuracy": 150},
              500: {"name": "Сбрасыватель перков"},
              }

#"force", "dexterity", "luck", "accuracy", "armory", "damage"
def get_random_item(med: bool = False) -> (int, dict):
    if not med:
        if random.randint(0, 1):
            return get_random_food()
        else:
            return get_random_buff()
    else:
        med = random.randint(300, 303)
        return med, used_items[med]


def get_random_buff() -> (int, dict):
    buff = random.randint(200, 209)
    return buff, used_items[buff]


def get_random_food() -> (int, dict):
    food = random.randint(100, 114)
    return food, used_items[food]


class Stock:
    equip = None
    used_stuff = None
    MAX_EQUIP = 12

    def get_data_lombard(self) -> str:
        out = "Экипировка которую можно продать:\n\n"
        equip_list = []
        for w in self.equip:
            equip_list.append(self.equip[w].get_data_cost())
        for ws in sorted(equip_list):
            out += ws + "\n"
        return out

    def add_stuff(self, key: int) -> None:
        if not self.used_stuff.get(key, None):
            self.used_stuff[key] = 1
        else:
            self.used_stuff[key] += 1

    def use_stuff(self, code: int, hero: object) -> str:
        if code // 100 == 4:
            stf = self.used_stuff.get(code, None)
            if stf:
                out = "Выбери элемент для улучшения:\n"
                equip_list = []
                for w in self.equip:
                    equip_list.append(self.equip[w].get_data_mod(code))
                for ws in sorted(equip_list):
                    out += ws + "\n"
                return out
            return
        if code == 500:
            hero.perks = '0' * 6
            if self.used_stuff[code] == 1:
                self.used_stuff.pop(code)
            else:
                self.used_stuff[code] -= 1
            return "навыки сброшены"
        stf = self.used_stuff.get(code, None)
        if stf:
            if self.used_stuff[code] == 1:
                self.used_stuff.pop(code)
            else:
                self.used_stuff[code] -= 1

            hun = used_items[code].get("hungry", 0)
            hero.hungry -= hun
            if hero.hungry < 0:
                hero.hungry = 0;
            hp = used_items[code].get("hp", 0)
            hero.hp += hp
            force = dex = luck = accur = 0
            if code // 100 == 2:
                for i in range(0, len(hero.buffs)):
                    hero.buffs[i] = 0
                force = used_items[code].get("force", 0)
                dex = used_items[code].get("dexterity", 0)
                luck = used_items[code].get("luck", 0)
                accur = used_items[code].get("accuracy", 0)
                hero.km_buff = used_items[code].get("km", 0)
                hero.km_protect = used_items[code].get("km_protect", 0)


            if code // 100 == 3:
                hero.km_heal = used_items[code].get("km_heal", 0)
            outstr = ""
            if hun:
                outstr += f"🍗-{hun}% (🍗{round(hero.hungry)}%)"
            if hp > 0:
                outstr += f"❤+{hp} ({round(hero.hp)}) "
            elif hp < 0:
                outstr += f"💔{hp} "
            if force:
                outstr += f"💪+{force} "
                hero.buffs[0] = force
            if dex:
                outstr += f"🤸🏽‍♂️+{dex} "
                hero.buffs[1] = dex
            if luck:
                outstr += f"👼+{luck} "
                hero.buffs[2] = luck
            if accur:
                outstr += f"🎯+{accur} "
                hero.buffs[3] = accur

            return f"вы использовали {used_items[code]['name']}\n {outstr}\n"
        return "нет такого"

    def print_stuff(self, code: int = 1) -> str:
        out = ""
        for k in sorted(self.used_stuff):
            if k // 100 == code and self.used_stuff[k]:
                if code == 4:
                    luck = used_items[k].get('luck', 0)
                    arm = used_items[k].get('armor')
                    dmg = used_items[k].get('damage')
                    dex = used_items[k].get('dexterity')
                    acc = used_items[k].get('accuracy')
                    luck = f"👼{luck}" if luck else ""
                    dex = f"🤸🏽‍♂️{dex}" if dex else ""
                    acc = f"🎯{acc}" if acc else ""
                    out += f"{used_items[k].get('name')}({self.used_stuff[k]}) 🛡{arm}|⚔️{dmg} {acc} {dex} {luck} /ustf_{k}\n"
                else:
                    out += f"{used_items[k].get('name')}({self.used_stuff[k]}) /ustf_{k}\n"

        if out == "":
            return " пока ничего \n"
        else:
            return out

    def add_item(self, item: object) -> None:
        if len(self.equip) == self.MAX_EQUIP:
            return
        new_item = copy.copy(item)
        while self.equip.get(new_item.get_code(), None):
            new_item.z += 1
        new_item.use = 0
        self.equip[new_item.get_code()] = new_item

    def get_delete(self) -> str:
        out = "🎒СОДЕРЖИМОЕ РЮКЗАКА ДЛЯ УДАЛЕНИЯ\n"
        cnt = len(self.equip)
        out += f"Экипировка ({cnt}/{self.MAX_EQUIP})\n"
        for w in self.equip:
            out += self.equip[w].get_data_drop() + "\n"
        return out

    def get_data(self) -> str:
        out = "🎒СОДЕРЖИМОЕ РЮКЗАКА\n"
        out += "   Полезное\n"
        out += self.print_stuff(3)
        out += self.print_stuff(5)
        out += "/mods модификаторы\n"
        cnt = len(self.equip)
        out += f"Экипировка ({cnt}/{self.MAX_EQUIP})\n"
        equip_list = []
        for w in self.equip:
            equip_list.append(self.equip[w].get_data())
        for ws in sorted(equip_list):
            out += ws + "\n"
        out += "\nеда /food \nбаффы /buff \nвыкинуть /drop\nмобы в команде /mobs\nубрать мобов /clr_mobs"
        return out

    def get_mods(self) -> str:
        return self.print_stuff(4)