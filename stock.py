import copy
import random
from db.models import ItemsDB

meds_list = {1: ["💉Мед-Х", 40, 300, 3],
             2: ["💌Медпак", 60, 600, 3],
             3: ["❣️Баффаут", 25, 200, 5],
             4: ["🧪Стимбласт", 100, 700, 3],
             5: ["🧪Стимбласт+", 150, 1500, 1]
             }

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
              200: {"name": "пиво", "force": 10, "luck": 20, "km": 10},
              201: {"name": "вино", "force": 15,"luck": 20, "km": 20},
              202: {"name": "водка", "force": 30, "luck": 50, "km": 30},
              203: {"name": "абсент", "force": 50, "luck": 60, "km": 40},
              204: {"name": "урановая настойка", "force": 70, "luck": 60, "km": 50},
              205: {"name": "стероиды", "dexterity": 20,  'accuracy' : 10, "km": 20},
              206: {"name": "анаболики", "dexterity": 30,  'accuracy' : 20, "km": 30},
              207: {"name": "мельдоний", "dexterity": 50,  'accuracy' : 50, "km": 40},
              }


def get_random_item():
    key, value = random.choice(list(used_items.items()))
    return key, value


class Stock:
    equip = None
    armors = {}
    used_stuff = {}
    meds = {}
    MAX_EQUIP = 12

    def get_data_lombard(self):
        out = "Экипировка которую можно продать:\n\n"
        for w in self.equip:
            out += self.equip[w].get_data_cost() + "\n"
        return out

    def add_stuff(self, key):
        if not self.used_stuff.get(key, None):
            self.used_stuff[key] = 1
        else:
            self.used_stuff[key] += 1

    def use_stuff(self, code, hero):
        stf = self.used_stuff.get(code, None)
        if stf:
            if self.used_stuff[code] == 1:
                self.used_stuff.pop(code)
            else:
                self.used_stuff[code] -= 1

            hun = used_items[code].get("hungry", 0)
            hero.hungry -= hun
            if hero.hungry<0:
                hero.hungry = 0;
            hp = used_items[code].get("hp", 0)
            hero.hp += hp
            hero.buffs[0] = used_items[code].get("force", 0)
            hero.buffs[1] = used_items[code].get("dexterity", 0)
            hero.buffs[2] = used_items[code].get("luck", 0)
            hero.buffs[3] = used_items[code].get("accuracy", 0)
            hero.km_buff = used_items[code].get("km", 0)
            outstr = ""
            if hun:
                outstr += f"🍗-{hun}% "
            if hp>0:
                outstr += f"❤+{hp} "
            elif hp<0:
                outstr += f"💔{hp} "
            if hero.buffs[0]:
                outstr += f"💪+{hero.buffs[0]} "
            if hero.buffs[1]:
                outstr += f"🤸🏽‍♂️+{hero.buffs[1]} "
            if hero.buffs[2]:
                outstr += f"👼+{hero.buffs[2]} "
            if hero.buffs[3]:
                outstr += f"🎯+{hero.buffs[3]} "

            return f"вы использовали {used_items[code]['name']}\n {outstr}\n"
        return "нет такого"

    def print_stuff(self, code=1):
        out = ""
        for k in self.used_stuff:
            if k // 100 == code:
                out += f"{used_items[k].get('name')}({self.used_stuff[k]}) /ustf_{k}\n"
        if out == "":
            return " ---  пока ничего ---\n"
        else:
            return out

    def add_item(self, item):
        if len(self.equip) == self.MAX_EQUIP:
            return
        new_item = copy.copy(item)
        while self.equip.get(new_item.get_code(), None):
            new_item.z += 1
        new_item.use = 0
        self.equip[new_item.get_code()] = new_item

    def get_delete(self):
        out = "🎒СОДЕРЖИМОЕ РЮКЗАКА ДЛЯ УДАЛЕНИЯ\n"
        cnt = len(self.equip)
        out += f"Экипировка ({cnt}/{self.MAX_EQUIP})\n"
        for w in self.equip:
            out += self.equip[w].get_data_drop() + "\n"
        return out

    def get_data(self):
        out = "🎒СОДЕРЖИМОЕ РЮКЗАКА\n"
        out += "   Полезное\n"
        out += " ---  пока ничего ---\n"
        cnt = len(self.equip)
        out += f"Экипировка ({cnt}/{self.MAX_EQUIP})\n"
        for w in self.equip:
            out += self.equip[w].get_data() + "\n"
        out += "\nеда /food \nбаффы /buff \nвыкинуть /drop"
        return out
