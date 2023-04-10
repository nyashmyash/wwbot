from hero import Hero
import copy
from armor import armor_all
from weapon import weapons_all
from drone import all_drones

h = Hero()
x = 1000
h.buffs = [0, 0, 0, 0]
h.coins = 1000
h.materials = 0
h.hp = x
h.max_hp = x
h.force = x
h.luck = x
h.dexterity = x
h.accuracy = x
h.charisma = x
h.weapon = copy.copy(weapons_all[19])
h.weapon.use = 1
h.id = 1
h.band_id = 0
h.name = "qqq"
h.armor = []
h.armor.append(copy.copy(armor_all[0][10]))
h.armor.append(copy.copy(armor_all[1][10]))
h.armor.append(copy.copy(armor_all[2][10]))
h.armor[0].arm *= 1
h.armor[1].arm *= 1
h.armor[2].arm *= 1
# увеличение брони в 2.1 раза
h.drone = copy.copy(all_drones[3])
h.drone.name = 'dr_qqq'
hw = copy.copy(h)
hw.perks = "000040"
hw.name = "aaa"
hw.armor = []
hw.armor.append(copy.copy(armor_all[0][10]))
hw.armor.append(copy.copy(armor_all[1][10]))
hw.armor.append(copy.copy(armor_all[2][10]))
h.dexterity = 1000
hw.force = 1000 # увеличение силы в 1.5 раза?
hw.drone = copy.copy(all_drones[3])
hw.drone.name = 'dr_aaa'
h.accuracy = 1000
h.luck = 1000
f = s = 0
for i in range(0, 1000):
    #print(f"{hw.attack_player(h)}\n")
    hw.attack_player(h)
    if hw.hp <= 0:
        f += 1
    if h.hp <= 0:
        s += 1
    h.hp = x
    hw.hp = x
print(f"win1 {f}\n win2 {s}")