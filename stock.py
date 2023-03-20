from collections import OrderedDict

meds_list = {1: ['💉Мед-Х', 40, 300, 3],
             2: ['💌Медпак', 60, 600, 3],
             3: ['❣️Баффаут', 25, 200, 5],
             4: ['🧪Стимбласт', 100, 700, 3],
             5: ['🧪Стимбласт+', 150, 1500, 1]
             }


class Stock:
    weapons = OrderedDict()
    armors = {}
    stuff = {}
    meds = {}

    def get_data(self):
        out = "🎒СОДЕРЖИМОЕ РЮКЗАКА\n"
        out += "   Полезное\n"
        out += " ---  пока ничего ---\n"
        cnt = len(self.weapons) + len(self.armors)
        out += "Экипировка ({0}/12)\n".format(cnt)
        for w in self.weapons:
            out += self.weapons[w].get_data()
        return out
