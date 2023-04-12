from hero import Hero
import copy
from armor import armor_all
from weapon import weapons_all
from drone import all_drones
from mob import *
from stock import Stock

h1 = Hero()
x = 1200
hp = 1500
h1.buffs = [0, 0, 0, 0]
h1.coins = 1000
h1.materials = 0
h1.hp = hp
h1.max_hp = hp
h1.force = x
h1.luck = x
h1.dexterity = x
h1.accuracy = x
h1.charisma = x
h1.weapon = copy.copy(weapons_all[19])
h1.weapon.use = 1
h1.id = 1
h1.band_id = 0
h1.name = "111"
h1.armor = []
h1.armor.append(copy.copy(armor_all[0][14]))
h1.armor.append(copy.copy(armor_all[1][14]))
h1.armor.append(copy.copy(armor_all[2][14]))
# увеличение брони в 2.1 раза
h1.drone = copy.copy(all_drones[3])
h1.drone.name = 'dr_111'
h2 = copy.copy(h1)
h1.perks = "000004"
h2.weapon = copy.copy(weapons_all[19])
h2.perks = "004000"
h2.name = "222"
h2.armor = []
h2.armor.append(copy.copy(armor_all[0][14]))
h2.armor.append(copy.copy(armor_all[1][14]))
h2.armor.append(copy.copy(armor_all[2][14]))
h1.dexterity = x
h2.force = x # увеличение силы в 1.5 раза?
h2.drone = copy.copy(all_drones[3])
h2.drone.name = 'dr_222'
h1.accuracy = x
h1.luck = x
f = s = 0
#h1.modul = 2111111
h1.stock = Stock()
h1.stock.used_stuff = {}
h1.km = 73
# mob = list_mobs75_80[4]
# res = h1.attack_mob(list_dange70[0]) +"\n"
# res += h1.attack_mob(list_dange70[1])+"\n"
# res += h1.attack_mob(list_dange70[2])+"\n"
# res += h1.attack_mob(list_dange70[3])+"\n"
# res += h1.attack_mob(list_dange70[4])+"\n"
#
#
# print(res)
# print(round(h1.hp))
for i in range(0, 200):
    #print(f"{h1.attack_player(h2)}\n")
    h1.attack_player(h2)
    if h2.hp <= 0:
        f += 1
    if h1.hp <= 0:
        s += 1
    h1.hp = hp
    h2.hp = hp
print(f"win1 {f}\n win2 {s}")