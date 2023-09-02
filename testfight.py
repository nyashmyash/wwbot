from hero import Hero
import copy
from armor import armor_all
from weapon import weapons_all
from drone import all_drones
from mob import *
from stock import Stock

x = 1500
hp = 1900
h1 = Hero()
h1.go_boss = 2
h1.km = 37
h1.buffs = [0, 0, 0, 0]
h1.debuffs = [0, 0, 0, 0]
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
h1.armor.append(copy.copy(armor_all[0][10]))
h1.armor.append(copy.copy(armor_all[1][10]))
h1.armor.append(copy.copy(armor_all[2][10]))
h1.stock = Stock()
h1.stock.used_stuff = {}
# увеличение брони в 2.1 раза
h1.drone = copy.copy(all_drones[3])
h1.drone.name = 'dr_111'
h1.perks = "000004"
h2 = copy.copy(h1)
h2.weapon = copy.copy(h1.weapon)
h2.perks = "004000"
h2.name = "222"
h2.armor = []
h2.armor.append(copy.copy(h1.armor[0]))
h2.armor.append(copy.copy(h1.armor[1]))
h2.armor.append(copy.copy(h1.armor[2]))
h1.dexterity = x
h2.force = x # увеличение силы в 1.5 раза?
h2.drone = copy.copy(all_drones[3])
h2.drone.name = 'dr_222'
f = s = 0
h2.stock = Stock()
h2.stock.used_stuff = {}
h3 = Hero()
h3 = copy.copy(h1)
h3.weapon = copy.copy(h1.weapon)
h3.weapon.use = 1
h3.name = "333"
h3.armor = []
h3.armor.append(copy.copy(h1.armor[0]))
h3.armor.append(copy.copy(h1.armor[1]))
h3.armor.append(copy.copy(h1.armor[2]))
h3.stock = Stock()
h3.stock.used_stuff = {}
# увеличение брони в 2.1 раза
h3.drone = copy.copy(all_drones[3])
h3.drone.name = 'dr_333'
h3.perks = "000004"
h4 = Hero()
h4 = copy.copy(h1)
h4.weapon = copy.copy(h1.weapon)
h4.weapon.use = 1
h4.name = "444"
h4.armor = []
h4.armor.append(copy.copy(h1.armor[0]))
h4.armor.append(copy.copy(h1.armor[1]))
h4.armor.append(copy.copy(h1.armor[2]))
h4.stock = Stock()
h4.stock.used_stuff = {}
# увеличение брони в 2.1 раза
h4.drone = copy.copy(all_drones[3])
h4.drone.name = 'dr_444'
h4.perks = "000004"

h5 = Hero()
h5 = copy.copy(h1)
h5.weapon = copy.copy(h1.weapon)
h5.weapon.use = 1
h5.name = "555"
h5.armor = []
h5.armor.append(copy.copy(h1.armor[0]))
h5.armor.append(copy.copy(h1.armor[1]))
h5.armor.append(copy.copy(h1.armor[2]))
h5.stock = Stock()
h5.stock.used_stuff = {}
# увеличение брони в 2.1 раза
h5.drone = copy.copy(all_drones[3])
h5.drone.name = 'dr_444'
h5.perks = "000004"

# list_boss[0].attack = 250
# print(h1.calc_armor())
# print(h1.calc_attack())
# heroes = [h1, h2, h3, h4, h5]
# Hero.attack_boss(heroes, list_boss[h1.go_boss-1], boss_id=h1.go_boss)
# print(h1.text_out_boss)
# print(h2.text_out_boss)
# print(h3.text_out_boss)
# print(h4.text_out_boss)
# print(h5.text_out_boss)
# for h in heroes:
#     print(f'{round(h.hp)}, {h.coins}, {len(h.stock.used_stuff)}')
# mob = list_mobs75_80[4]
# h1.weapon.mod = 403
#h1.armor[0].mod = 401

res = ""
#h1.armor[0].mod = h1.armor[1].mod = h1.armor[2].mod = 400
# print(h1.return_data())
#
# for i in range(0, len(list_dange80)-1):
#    if h1.hp > 1:
#        res += h1.attack_mob(list_dange80[i], True, True) +"\n"

#print(res)

# list_mob_dino_zone
# list_mk_zone
print(h1.get_force())
print(h1.calc_attack())
# l = {}
# died = 0
# for m in range(0, 10):
#     for k in range(0, len(list_mob_dino_zone)):
#         print(h1.attack_mob(list_mob_dino_zone[k]))
#         if not l.get(k, 0):
#             l[k] = 0
#         if h1.hp == 1:
#             died += 1
#         l[k] += round(h1.hp)
#         h1.hp = h1.max_hp
#
#
#
# print(l)
# print(died)

# for m in list_mob_dino_zone:
#     if h1.hp > 0:
#         print(h1.attack_mob(m))
    #h1.hp = h1.max_hp
# from rand import randint
# for i in range(0, 1000):
#     print(randint(0, 10))
# # print(round(h1.hp))
h1.perks = "000001"
h2.perks = "200000"
for i in range(0, 100):
    print(f"{h1.attack_pvp_wmobs(h2)}\n")
    #h1.attack_player(h2)
    if h1.hp > h2.hp:
        f += 1
    else:
        s += 1
    h1.hp = hp
    h2.hp = hp

print(f"win1 {f}\nwin2 {s}")

#f = list_mobs75_80[4]
#for i in range(0, 100):
#    print(f.log_hit_mob()+ "\n")
