from hero import Hero
import copy
from armor import armor_all
from weapon import weapons_all
from drone import all_drones
from mob import *
from stock import Stock
from collections import OrderedDict

h = Hero()
s = """👤лягушка 🏵14
        ├ 🤟жабья братва   /band       умения /perks
        ├ ❤️ 2154/2154  🍗21% | ⚔️2548 | 🛡 500 
        ├ 👣8   /min_log /summ_stats
        ├ 💪1958+220 | 🤸🏽‍♂️1850+150 | 🗣1900 
        ├ 👼1850+120 | 🎯1889+120
        ├ 📥модуль хп
        ├ нет дрона
        ├ 🗡▪️ 🔱Тризуб тираннозавра ⚡️770 🔧69 %
        ├ 🪖▪️ ☣️шлем тиранид 🛡 140 🔧33 %
        ├ 🧥▪️ ☣️броня тиранид 🛡 220 🔧99 %
        ├ 🧤▪️ ☣️перчатки тиранид 🛡 140 🔧99 %
        ├ 📦1387935
        └ 🕳4600 👣👣92221 dzen🕳49912"""
hh = Hero()
hh.parse_data(s)
print(hh.__dict__)
print(hh.weapon.__dict__)
print(hh.armor[0].__dict__)
print(hh.armor[1].__dict__)
print(hh.armor[2].__dict__)


s1 = """сырое мясо(37) /ustf_100
жареная курица(10) /ustf_101
картошка(26) /ustf_102
мутантский салат(2) /ustf_104
жаренное мясо(1) /ustf_105
гнилое мясо(3) /ustf_106
вонючая жижа(9) /ustf_107
хомячок(7) /ustf_108
крыса(13) /ustf_109
аптечка(63) /ustf_110
большая аптечка(50) /ustf_111
консервы(29) /ustf_112
гнилые фрукты(11) /ustf_113
вяленое мясо(21) /ustf_114"""

s2 = """☢️модификатор ядерный тип А(5) 🛡55|⚔️50 🎯-100 🤸🏽‍♂️-100  /ustf_400
⚛️модификатор тритиевый(5) 🛡75|⚔️70 🎯-150 🤸🏽‍♂️-150  /ustf_401
☢️модификатор ядерный тип Б(5) 🛡85|⚔️75 🎯-150 🤸🏽‍♂️-170  /ustf_402
👽модификатор тирранид(1) 🛡110|⚔️100 🎯-200 🤸🏽‍♂️-200  /ustf_403
☠️модификатор проклятый(2) 🛡120|⚔️110 🎯-250 🤸🏽‍♂️-100 👼-250 /ustf_404
🤸🏽‍♂️модификатор ловкости(2) 🛡-40|⚔️-40  🤸🏽‍♂️200  /ustf_405
🎯модификатор точности(1) 🛡-40|⚔️-40 🎯200   /ustf_406
️🤪модификатор глупец(7) 🛡-60|⚔️-60 🎯150 🤸🏽‍♂️150  /ustf_407"""

s3 = """пиво(93) /ustf_200
вино(89) /ustf_201
водка(73) /ustf_202
абсент(74) /ustf_203
урановая настойка(84) /ustf_204
стероиды(68) /ustf_205
психонавт(65) /ustf_206
мельдоний(41) /ustf_207
прививка(13) /ustf_208
антибиотик(11) /ustf_209
некро-вакцина(3) /ustf_210"""


s4 = """🎒СОДЕРЖИМОЕ РЮКЗАКА
   Полезное
💉Мед-Х(46) /ustf_300
💌Медпак(43) /ustf_301
🧪Стимбласт(21) /ustf_302
🧪Стимбласт+(22) /ustf_303
/mods модификаторы
Сбрасыватель перков(5) /ustf_500
Экипировка   11/12
▪️ ☣️броня тиранид 🛡 220 🔧100 % /eqa_1t220z0
▪️ ☣️броня тиранид* 🛡 220+120 🔧40 % /eqa_1t220z2
▪️ ☣️шлем тиранид 🛡 140 🔧100 % /eqa_0t140z1
▪️ ☣️️перчатки тиранид 🛡 140 🔧100 % /eqa_2t140z2
▪️ ☣️️перчатки тиранид* 🛡 140+85 🔧28 % /eqa_2t140z1
▪️ ✴️пушка тиранид ⚡️750 🔧100 % /eqw_750z2
▪️ ✴️пушка тиранид ⚡️750 🔧100 % /eqw_750z3
▪️ ✴️пушка тиранид ⚡️750 🔧86 % /eqw_750z4
▪️ ✴️пушка тиранид* ⚡️750+75 🔧45 % /eqw_750z1
▪️ 🔱Тиранно-доспех 🛡 240 🔧100 % /eqa_1t240z0
▪️ 🔱Тиранно-шлем 🛡 150 🔧100 % /eqa_0t150z0

еда /food 
баффы /buff 
выкинуть /drop
мобы в команде /mobs
убрать мобов /clr_mobs"""
hh.stock = Stock()
hh.stock.used_stuff = {}
hh.stock.equip = OrderedDict()
hh.parse_stuff(s1)
hh.parse_stuff(s2)
hh.parse_stuff(s3)
hh.parse_stock(s4)
hh.buffs = [0, 0, 0, 0]
hh.danges = []
print(hh.stock.equip)
print(len(hh.stock.equip))
print(hh.stock.used_stuff)