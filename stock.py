meds_list = {1: ['💉Мед-Х', 40, 300, 3],
             2: ['💌Медпак', 60, 600, 3],
             3: ['❣️Баффаут', 25, 200, 5],
             4: ['🧪Стимбласт', 100, 700, 3],
             5: ['🧪Стимбласт+', 150, 1500, 1]
             }


class Stock:
    equip = None
    armors = {}
    stuff = {}
    meds = {}

    def get_data(self):
        out = "🎒СОДЕРЖИМОЕ РЮКЗАКА\n"
        out += "   Полезное\n"
        out += " ---  пока ничего ---\n"
        cnt = len(self.equip)
        out += "Экипировка ({0}/12)\n".format(cnt)
        for w in self.equip:
            out += self.equip[w].get_data() + "\n"
        return out
