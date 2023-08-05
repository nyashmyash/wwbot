#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import random
import copy
from db.db_process import *
from hero import *
from db.base import *
from stock import Stock, used_items, get_random_food
from armor import Armor, armor_all
from weapon import Weapon, weapons_all
from mob import *
from menu import *
from drone import *
from collections import OrderedDict
from sethook import token
#from telegram.constants import ParseMode

from multiprocessing import Queue

queue_global = Queue()

all_data = {}

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, \
    MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# async def fixed_replay(update, text, reply_markup) -> None:
#     await update.message.reply_text(text, reply_markup)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!"
    )


async def get_hero(update):
    rslt = all_data.get(update.effective_user.id, None)
    if not rslt:
        db_hero_fetch = await get_hero_db(async_session, str(update.effective_user.id))

        hero = Hero()
        stock = Stock()
        hero.stock = stock
        hero.buffs = [0, 0, 0, 0]
        hero.danges = []
        stock.equip = OrderedDict()
        if not len(db_hero_fetch):

            hero.id = str(update.effective_user.id)
            hero.band_id = 0
            hero.name = update.effective_chat.first_name
            hero.weapon = copy.copy(weapons_all[0])
            hero.weapon.use = 1
            hero.armor = []
            hero.armor.append(copy.copy(armor_all[0][0]))
            hero.armor.append(copy.copy(armor_all[1][0]))
            hero.armor.append(copy.copy(armor_all[2][0]))
            hero.stock.used_stuff = {}
            hero.coins = 1000
            hero.perks = "000000"
            await add_hero_db(async_session, hero)
            h = await get_hero_db(async_session, str(update.effective_user.id))
            hero.base_id = h[0].id
            logger.info(update.effective_chat.first_name + f"  base_id {hero.base_id}")
            #await add_hero_armor_db(async_session, hero)
            #await add_hero_weapon_db(async_session, hero)

        else:
            hero_db = db_hero_fetch[0]
            db_hero_wp = await get_hero_weapon_db(async_session, hero_db)
            hero.from_db(hero_db)
            if hero.perks == '0':
                hero.perks ="000000"
            if hero.coins < 0:
                hero.coins = 1000
            if not hero.weapon:
                hero.weapon = copy.copy(weapons_all[0])
                hero.weapon.use = 1

            for iw in range(0, len(db_hero_wp)):
                if db_hero_wp[iw].use>1:
                    hero.drone = copy.copy(all_drones[db_hero_wp[iw].use-2])
                    hero.drone.from_db(db_hero_wp[iw])
                    continue

                dmg = int(db_hero_wp[iw].code.split('z')[0])
                z = int(db_hero_wp[iw].code.split('z')[1])
                wpn = None
                for i1 in range(0, len(weapons_all)):
                    if weapons_all[i1].dmg == dmg:
                        wpn = copy.copy(weapons_all[i1])
                        break
                wpn.from_db(db_hero_wp[iw])
                wpn.z = z
                if wpn.use:
                    hero.weapon = wpn
                else:
                    hero.stock.equip[wpn.get_code()] = wpn

            db_hero_ar = await get_hero_armor_db(async_session, hero_db)
            hero.armor = [None, None, None]
            if len(db_hero_ar):
                for irm in db_hero_ar:
                    arm_type = int(irm.code.split('t')[0])
                    arm_val = int(irm.code.split('t')[1].split('z')[0])
                    z = int(irm.code.split('t')[1].split('z')[1])
                    arm = None
                    for ia1 in range(0, len(armor_all[arm_type])):
                        if armor_all[arm_type][ia1].arm == arm_val:
                            arm = copy.copy(armor_all[arm_type][ia1])
                            break
                    arm.from_db(irm)
                    arm.z = z
                    if arm.use:
                        hero.armor[arm_type] = arm
                    else:
                        hero.stock.equip[arm.get_code()] = arm

            for i in range(0, 3):
                if not hero.armor[i]:
                    hero.armor[i] = copy.copy(armor_all[i][0])
                    hero.armor[i].use = 1

            db_hero_itms = await get_hero_items_db(async_session, hero_db)
            if len(db_hero_itms):
                for it in db_hero_itms:
                    if not hero.stock.used_stuff:
                        hero.stock.used_stuff = {}
                    hero.stock.used_stuff[it.index] = it.count
            else:
                if not hero.stock.used_stuff:
                    hero.stock.used_stuff = {}
        hero.ef_chat = update.effective_chat
        all_data[update.effective_user.id] = hero
        return hero
    else:
        return rslt


async def me_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    hero = await get_hero(update)
    #if hero.mob_fight:
    #    await update.message.reply_text(f"на вас напал моб {hero.mob_fight.get_name()}", reply_markup=menu_attack())
    await update.message.reply_text(hero.return_data(), reply_markup=menu_pip())

rad_zones = [15, 25, 34, 45, 55, 65, 75, 85]


async def menu_sel(update: Update, hero: Hero, data_:str) -> None:
    if hero.km == 0:
        await update.message.reply_text(data_)
        return
    if hero.in_dange <= 0:
        if hero.zone <= 1:
            await update.message.reply_text(data_, reply_markup=menu_go())
        else:
            await update.message.reply_text(data_, reply_markup=menu_go_dead())
    else:
        await update.message.reply_text(data_, reply_markup=menu_go_dange())


async def danges_fin_msg(update: Update, hero: Hero) -> None:
    hero.mob_fight = None
    hero.in_dange = -1
    mob = list_mobs[hero.km // 5][0]
    coins = round(mob.calc_mob_coins(hero.km))
    mats = round(mob.calc_mob_mat(hero.km))
    hero.coins += coins
    hero.materials += mats
    prize_money = f"получено 🕳 {coins} 📦 {mats}\n"

    if hero.km == 10:
        r = random.randint(0, 7)
        if r == 1:
            i = random.randint(4, 6)
            hero.stock.add_item(weapons_all[i])
            await update.message.reply_text(hero.make_header() + prize_money
                                            + f"вам выпало {weapons_all[i].get_name()}",
                                            reply_markup=menu_go())
        else:
            await update.message.reply_text(hero.make_header() + prize_money
                                            + "вам выпало нихуя",
                                            reply_markup=menu_go())

    if hero.km == 20:
        r = random.randint(0, 7)
        if r == 2:
            type = random.randint(0, 2)
            hero.stock.add_item(armor_all[type][5])
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + f"вам выпало {armor_all[type][5].get_name()}",
                                            reply_markup=menu_go())
        else:
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + "вам выпало нихуя",
                                            reply_markup=menu_go())
    if hero.km == 30:
        r = random.randint(0, 6)
        if r == 3:
            r = random.randint(7, 8)
            hero.stock.add_item(weapons_all[r])
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + f"вам выпало {weapons_all[r].get_name()}",
                                            reply_markup=menu_go())
        else:
            if random.randint(0, 15) == 1 and hero.moduls == '':
                hero.add_module()
                name = hero.get_str_modul()
                await update.message.reply_text(hero.make_header()+ prize_money
                                                + f"вам выпал модуль {name}",
                                                reply_markup=menu_go())
            else:
                await update.message.reply_text(hero.make_header()+ prize_money
                                                + "вам выпало нихуя",
                                                reply_markup=menu_go())

    if hero.km == 35:
        r = random.randint(0, 6)
        if r == 3:
            type = random.randint(0, 2)
            hero.stock.add_item(armor_all[type][6])
            w = armor_all[type][6]
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + f"вам выпало {w.get_name()}",
                                            reply_markup=menu_go())
        else:
            if random.randint(0, 15) == 1 and len(hero.moduls) == 1:
                hero.add_module()
                name = hero.get_str_modul()
                await update.message.reply_text(hero.make_header()+ prize_money
                                                + f"вам выпал модуль {name}",
                                                reply_markup=menu_go())
            else:
                await update.message.reply_text(hero.make_header()+ prize_money
                                                + "вам выпало нихуя",
                                                reply_markup=menu_go())

    if hero.km == 40:
        r = random.randint(0, 6)
        if r == 4:
            type = random.randint(0, 2)
            hero.stock.add_item(armor_all[type][7])
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + f"вам выпало {armor_all[type][7].get_name()}",
                                            reply_markup=menu_go())
        elif r == 5:
            w = weapons_all[10] if random.randint(0, 2) == 1 else weapons_all[9]
            hero.stock.add_item(w)
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + f"вам выпало {w.get_name()}",
                                            reply_markup=menu_go())
        else:
            if random.randint(0, 15) == 1 and len(hero.moduls) == 2:
                hero.add_module()
                name = hero.get_str_modul()
                await update.message.reply_text(hero.make_header()+ prize_money
                                                + f"вам выпал модуль {name}",
                                                reply_markup=menu_go())
            else:
                await update.message.reply_text(hero.make_header()+ prize_money
                                                + "вам выпало нихуя",
                                                reply_markup=menu_go())

    if hero.km == 50:
        r = random.randint(0, 7)
        if r == 4:
            type = random.randint(0, 2)
            hero.stock.add_item(armor_all[type][8])
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + f"вам выпало {armor_all[type][8].get_name()}",
                                            reply_markup=menu_go())
        elif r == 5:
            w = weapons_all[11 + random.randint(0, 2)]
            hero.stock.add_item(w)
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + f"вам выпало {w.get_name()}",
                                            reply_markup=menu_go())
        else:
            if random.randint(0, 15) == 1 and 2 <= len(hero.moduls) <= 5:
                hero.add_module()
                name = hero.get_str_modul()
                await update.message.reply_text(hero.make_header()+ prize_money
                                                + f"вам выпал модуль {name}",
                                                reply_markup=menu_go())
            else:
                await update.message.reply_text(hero.make_header()+ prize_money
                                                + "вам выпало нихуя",
                                                reply_markup=menu_go())

    if hero.km == 60:
        r = random.randint(0, 7)
        if r == 4:
            type = random.randint(0, 2)
            hero.stock.add_item(armor_all[type][9])
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + f"вам выпало {armor_all[type][9].get_name()}",
                                            reply_markup=menu_go())
        elif r == 5:
            w = weapons_all[13 + random.randint(0, 3)]
            hero.stock.add_item(w)
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + f"вам выпало {w.get_name()}",
                                            reply_markup=menu_go())
        else:
            if random.randint(0, 15) == 1 and len(hero.moduls) == 6:
                hero.add_module()
                name = hero.get_str_modul()
                await update.message.reply_text(hero.make_header()+ prize_money
                                                + f"вам выпал модуль {name}",
                                                reply_markup=menu_go())
            else:
                await update.message.reply_text(hero.make_header()+ prize_money
                                                + "вам выпало нихуя",
                                                reply_markup=menu_go())

    if hero.km == 70:
        r = random.randint(0, 8)
        if r == 4:
            type = random.randint(0, 2)
            hero.stock.add_item(armor_all[type][10])
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + f"вам выпало {armor_all[type][10].get_name()}",
                                            reply_markup=menu_go())
        elif r == 5:
            w = weapons_all[17 + random.randint(0, 2)]
            hero.stock.add_item(w)
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + f"вам выпало {w.get_name()}",
                                            reply_markup=menu_go())
        else:
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + "вам выпало нихуя",
                                            reply_markup=menu_go())
    if hero.km == 80:
        r = random.randint(0, 9)
        if r == 4:
            type = random.randint(0, 2)
            hero.stock.add_item(armor_all[type][11])
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + f"вам выпало {armor_all[type][11].get_name()}",
                                            reply_markup=menu_go())
        elif r == 5:
            w = weapons_all[20]
            hero.stock.add_item(w)
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + f"вам выпало {w.get_name()}",
                                            reply_markup=menu_go())
        else:
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + "вам выпало нихуя",
                                            reply_markup=menu_go())
    if hero.km == 90:
        r = random.randint(0, 7)
        if r == 4:
            type = random.randint(0, 2)
            hero.stock.add_item(armor_all[type][15])
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + f"вам выпало {armor_all[type][15].get_name()}",
                                            reply_markup=menu_go())
        elif r == 5:
            w = weapons_all[24]
            hero.stock.add_item(w)
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + f"вам выпало {w.get_name()}",
                                            reply_markup=menu_go())
        else:
            await update.message.reply_text(hero.make_header()+ prize_money
                                            + "вам выпало нихуя",
                                            reply_markup=menu_go())

async def msgs_in_camp(update: Update, msg_txt:str, hero: Hero) -> None:
    hero.zone = 0
    use_10x = 1
    i = 0
    if '*' in msg_txt:
        msg_txt = msg_txt.replace('*', '')
        use_10x = 10
    if msg_txt == "💪Сила":
        while i < use_10x:
            if hero.coins >= hero.calc_cost(hero.force) and hero.inc_force():
                hero.coins -= hero.calc_cost(hero.force)
                hero.force += 1
            else:
                break
            i += 1
        if use_10x == 1:
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())
        else:
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn_x10())

    elif msg_txt == "🎯Меткость":
        while i < use_10x:
            if hero.coins >= hero.calc_cost(hero.accuracy) and hero.inc_acc():
                hero.coins -= hero.calc_cost(hero.accuracy)
                hero.accuracy += 1
            else:
                break
            i += 1
        if use_10x == 1:
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())
        else:
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn_x10())

    elif msg_txt == "🤸🏽‍♂️Ловкость":
        while i < use_10x:
            if hero.coins >= hero.calc_cost(hero.dexterity) and hero.inc_dex():
                hero.coins -= hero.calc_cost(hero.dexterity)
                hero.dexterity += 1
            else:
                break
            i += 1
        if use_10x == 1:
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())
        else:
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn_x10())

    elif msg_txt == "❤️Живучесть":
        while i < use_10x:
            if hero.coins >= hero.calc_cost(hero.max_hp) and hero.inc_hp():
                hero.coins -= hero.calc_cost(hero.max_hp)
                hero.max_hp += 1
                hero.hp += 1
            else:
                break
            i += 1
        if use_10x == 1:
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())
        else:
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn_x10())
    elif msg_txt == "🗣Харизма":
        while i < use_10x:
            if hero.coins >= 10 * hero.charisma and hero.inc_char():
                hero.coins -= 10 * hero.charisma
                hero.charisma += 1
            else:
                break
            i += 1
        if use_10x == 1:
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())
        else:
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn_x10())
    elif msg_txt == "👼Удача":
        while i < use_10x:
            if hero.coins >= hero.calc_cost(hero.luck) and hero.inc_luck():
                hero.coins -= hero.calc_cost(hero.luck)
                hero.luck += 1
            else:
                break
            i += 1
        if use_10x == 1:
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())
        else:
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn_x10())
    elif msg_txt == "💤Отдохнуть":
        if hero.hp < hero.max_hp or hero.hungry > 0:
            if hero.coins < hero.max_hp:
                await update.message.reply_text(
                    f"нужно {hero.max_hp} крышек, вы нищий и не можете отдохнуть\n", reply_markup=menu_camp())
            else:
                hero.hp = hero.max_hp
                hero.hungry = 0
                hero.coins -= hero.max_hp
                await update.message.reply_text("вы отдохнули и поели")
                await update.message.reply_text(hero.return_data(), reply_markup=menu_camp())
        else:
            await update.message.reply_text("вы и так здоровы и сыты", reply_markup=menu_camp())

    elif msg_txt == "💰Ломбард":
        out = f"📦×{hero.materials}\n"
        out += hero.stock.get_data_lombard()
        await update.message.reply_text(out, reply_markup=menu_lomb())
    elif msg_txt == "👓Инженер":
        out = f"🕳×{hero.coins}\n\n"
        out += "вы можете купить дрона:\n\n"
        out += all_drones[0].get_buy_text()
        cnt_mod = len(hero.moduls)
        if cnt_mod:
            out += "\nвы можете активировать модуль:\n\n"
            for i in range(0, cnt_mod):
                out += f"{all_modules[i + 1][1]}  /module{i + 1}\n"
        else:
            out += "\nнет модулей"
        await update.message.reply_text(out, reply_markup=menu_pip())
    elif msg_txt == "🏚Торгаш":
        out = f"🕳×{hero.coins}\n"
        out += "вы можете купить:\n"
        for type in armor_all:
            i = 0
            for armor in type:
                if i < 5:
                    out += armor.get_buy() + "\n"
                i += 1
        for w in weapons_all:
            if w.dmg < 50:
                out += w.get_buy() + "\n"

        await update.message.reply_text(out, reply_markup=menu_pip())
    elif msg_txt == "Продать все коробки":
        hero.coins += round(hero.materials / 10)
        hero.materials = 0
        out = f"📦×{hero.materials}\n"
        out += hero.stock.get_data_lombard()
        await update.message.reply_text(out, reply_markup=menu_lomb())
    elif msg_txt == "Продать 1/2 коробок":
        hero.coins += round(hero.materials / 20)
        hero.materials -= round(hero.materials / 2)
        out = f"📦×{hero.materials}\n"
        out += hero.stock.get_data_lombard()
        await update.message.reply_text(out, reply_markup=menu_lomb())
    elif msg_txt == "Продать 1/4 коробок":
        hero.coins += round(hero.materials / 40)
        hero.materials -= round(hero.materials / 4)
        out = f"📦×{hero.materials}\n"
        out += hero.stock.get_data_lombard()
        await update.message.reply_text(out, reply_markup=menu_lomb())
    elif msg_txt == "Продать 1/8 коробок":
        hero.coins += round(hero.materials / 80)
        hero.materials -= round(hero.materials / 8)
        out = f"📦×{hero.materials}\n"
        out += hero.stock.get_data_lombard()
        await update.message.reply_text(out, reply_markup=menu_lomb())
    elif msg_txt == "🎓Обучение":
        await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())
    elif msg_txt == "x10 навыков":
        await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn_x10())


async def text_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    hero = await get_hero(update)
    msg_txt = update.message.text
    out = ""
    pvp = False
    pvp_end = False
    if hero.band_name == "введите имя банды":
        if len(msg_txt) < 5:
            await update.message.reply_text(f"название банды должно быть больше 5 символов - {msg_txt}", reply_markup=menu_go())
        else:
            await update.message.reply_text(f"вы создали банду с именем {msg_txt}", reply_markup=menu_go())
            hero.band_name = msg_txt
        return None
    if hero.km != 0:
        if hero.weapon and hero.weapon.life < 5:
            await update.message.reply_text(f"⭐️⚡️Внимание, оружие {hero.weapon.get_name()} скоро сломается!⭐️⚡️")
        for ar in hero.armor:
            if ar and ar.life < 3:
                await update.message.reply_text(f"⭐️⚡️Внимание, броня {ar.get_name()} скоро сломается!⭐️⚡️")

    if hero.km == 0:
        await msgs_in_camp(update, msg_txt, hero)

    if msg_txt == "📟Пип-бой":
        await update.message.reply_text(hero.return_data(), reply_markup=menu_pip())
        return

    if hero.in_dange <= 0:
        if hero.zone >= 1:
            if msg_txt == "🔪Напасть" and hero.km != 0:
                fight = False
                for h in all_data:
                    hero_h = all_data[h]
                    if update.effective_user.id != h and hero_h.km == hero.km and hero_h.in_dange <= 0 and hero.zone == hero_h.zone:
                        chat = all_data[h].ef_chat
                        fight = True
                        out = hero.attack_pvp_wmobs(hero_h, hero.min_log)

                        hdr1 = f"Сражение с {hero.get_name()}\n\n"
                        hdr2 = f"Сражение с {hero_h.get_name()}\n\n"
                        if hero_h.hp < hero.hp:
                            hero_h.died_hero()  # -10%
                            hero_h.coins -= round(hero_h.coins * (0.25 + hero.get_module(6) / 100))
                            hero.coins += round(hero_h.coins * (0.23 + hero.get_module(6) / 100))
                            await chat.send_message(hdr1 + out +
                                                    f"Вы проиграли:((((\n потеряно: 🕳 {round(hero_h.coins * 0.25)}",
                                                    reply_markup=menu_camp())
                            await update.message.reply_text(hdr2 + out +f"Вы выиграли!!!\n получено: 🕳 {round(hero_h.coins * 0.23)}")
                            pvp_end = True
                        else:
                            hero.died_hero()
                            hero.coins -= round(hero.coins * (0.25 + hero_h.get_module(6) / 100))
                            hero_h.coins += round(hero.coins * (0.23 + hero_h.get_module(6) / 100))
                            await update.message.reply_text(hdr2 + out +
                                                            f"Вы лузер!!!!\n потеряно: 🕳 {round(hero.coins * 0.25)}",
                                                            reply_markup=menu_camp())
                            await chat.send_message(
                                hdr1 + out + f"Вы выиграли!!!\n получено: 🕳 {round(hero.coins * 0.23)}")
                        out = ""

                        break
                if not fight:
                    await update.message.reply_text("противник ушел")
        if hero.zone == 1:
            if msg_txt == "👣️☠️Пустошь смерти☠️" and hero.km == 20:
                hero.zone = 2
                hero.go()
                header = hero.make_header()
                hero.select_mob()
                if hero.mob_fight:
                    await update.message.reply_text(
                        header + "вы отправились в пустошь смерти, вернуться в лагерь нельзя")
                    # await update.message.reply_text(f"на вас напал моб {hero.mob_fight.name}",
                    #                                 reply_markup=menu_attack())
                else:
                    await update.message.reply_text(
                        header + "вы отправились в пустошь смерти, вернуться в лагерь нельзя",
                        reply_markup=menu_go_dead())

            if msg_txt == "👣️🎪 Зайти в блядский цирк🎪 ️" and hero.km == 33:
                hero.zone = 3
                hero.go()
                header = hero.make_header()
                hero.select_mob()
                if hero.mob_fight:
                    await update.message.reply_text(
                        header + "вы отправились в блядский цирк, вернуться в лагерь нельзя")
                else:
                    await update.message.reply_text(
                        header + "вы отправились в блядский цирк, вернуться в лагерь нельзя",
                        reply_markup=menu_go_dead())

            if msg_txt == "🔪️painkiller🔪️" and hero.km == 47:
                hero.zone = 4
                hero.go()
                header = hero.make_header()
                hero.select_mob()
                if hero.mob_fight:
                    await update.message.reply_text(
                        header + "вы отправились в 🔪️painkiller🔪️ зону, вернуться в лагерь нельзя")
                else:
                    await update.message.reply_text(
                        header + "вы отправились в 🔪️painkiller🔪️ зону, вернуться в лагерь нельзя",
                        reply_markup=menu_go_dead())

            if msg_txt == "👣️Парк динозавров" and hero.km == 66:
                hero.zone = 6
                hero.go()
                header = hero.make_header()
                hero.select_mob()
                if hero.mob_fight:
                    await update.message.reply_text(
                        header + "вы отправились в пустошь где динозавры, вернуться в лагерь нельзя")
                    # await update.message.reply_text(f"на вас напал моб {hero.mob_fight.name}",
                    #                                 reply_markup=menu_attack())
                else:
                    await update.message.reply_text(
                        header + "вы отправились в пустошь где динозавры, вернуться в лагерь нельзя",
                        reply_markup=menu_go_dead())


        if hero.zone == 2:
            if msg_txt == "👣️👹Смертельная арена👹" and hero.km == 30:
                hero.zone = 5
                hero.go()
                header = hero.make_header()
                hero.select_mob()
                if hero.mob_fight:
                    await update.message.reply_text(
                        header + "вы отправились на смертельную арену, вернуться в лагерь нельзя")
                else:
                    await update.message.reply_text(
                        header + "вы отправились на смертельную арену, вернуться в лагерь нельзя",
                        reply_markup=menu_go_dead())

        if msg_txt == "🔥Зайти в данж" and hero.km in danges.keys() and hero.in_dange == 0:
            if hero.km in hero.danges:
                await update.message.reply_text("вы уже были в данже, идите в лагерь")
                return
            hero.mob_fight = danges[hero.km][0]
            hero.in_dange = 1
            header = hero.make_header()
            await update.message.reply_text(header + f"на вас напал моб {hero.mob_fight.get_name()}",
                                            reply_markup=menu_go_dange())
        elif hero.mob_fight and msg_txt != "⚔️Дать отпор" and msg_txt != "🏃Дать деру":
            header = hero.make_header()
            await update.message.reply_text(header + f"на вас напал моб {hero.mob_fight.get_name()}",
                                            reply_markup=menu_attack())
        elif not hero.mob_fight and msg_txt == "⛺️В лагерь":
            if hero.zone >= 2:
                await update.message.reply_text("☠☠в лагерь нельзя☠☠", reply_markup=menu_go_dead())
            else:
                if hero.get_module(7):
                    if hero.hp > hero.max_hp:
                        hero.hp = hero.max_hp
                hero.km = 0
                hero.danges = []
                hero.necro_lvl = 1

                text_camp = "Приветствую в лагере!\nПомощь по игре /help \nЧат по игре: https://t.me/+l1OjhV7mzwc1MGIy\n" \
                            "Наверное никто не задумывался насчет того, кто такие свинокрысы, а свинокрыс - это выдуманный персонаж из русской народной сказки. Это существо с объедками, которое было создано для того, чтобы пугать детей и заставлять их быть послушными. В некоторых версиях сказки свинокрыс описывается как полу-свинья, полу-крыса, которая может ходить на задних лапах и даже разговаривать на человеческом языке. В сказках обычно говорится, что свинокрыс живет в печи, в подвале или на чердаке и тайно прислушивается к разговорам или делает что-то плохое."
                await update.message.reply_text(text_camp, reply_markup=menu_camp())

        elif msg_txt == "👣Пустошь" and hero.zone == 0:
            hero.go()
            header = hero.make_header()
            hero.select_mob()
            if hero.mob_fight:
                await update.message.reply_text(header + "вы отправились в пустошь")
                await update.message.reply_text(f"на вас напал моб {hero.mob_fight.get_name()}",
                                                reply_markup=menu_attack())
            else:
                await update.message.reply_text(header + "вы отправились в пустошь", reply_markup=menu_go())

        elif msg_txt == "👣☢Рад-️Пустошь":
            if hero.km in rad_zones and hero.zone<=1 or hero.km == 0:
                hero.zone = 1
                hero.go()
                header = hero.make_header()
                hero.select_mob()
                if hero.mob_fight:
                    await update.message.reply_text(header + "вы отправились в радиоактивную пустошь")
                    await update.message.reply_text(f"на вас напал моб {hero.mob_fight.get_name()}",
                                                    reply_markup=menu_attack())
                else:
                    await update.message.reply_text(header + "вы отправились в радиоактивную пустошь",
                                                    reply_markup=menu_go())

        elif msg_txt == "☢Покинуть Рад-️Пустошь☢" and hero.zone == 1:
            if hero.km in rad_zones:
                hero.zone = 0
                hero.go()
                header = hero.make_header()
                hero.select_mob()
                if hero.mob_fight:
                    await update.message.reply_text(header + "вы покинули радиоактивную пустошь")
                    await update.message.reply_text(f"на вас напал моб {hero.mob_fight.get_name()}",
                                                    reply_markup=menu_attack())
                else:
                    await update.message.reply_text(header + "вы покинули радиоактивную пустошь",
                                                    reply_markup=menu_go())

        elif msg_txt == "️☠Покинуть пустошь смерти☠" and hero.zone == 2:
            hero.zone = 1
            hero.go()
            header = hero.make_header()
            hero.select_mob()
            if hero.mob_fight:
                await update.message.reply_text(header + "вы покинули пустошь смерти")
                await update.message.reply_text(f"на вас напал моб {hero.mob_fight.get_name()}",
                                                reply_markup=menu_attack())
            else:
                await update.message.reply_text(header + "вы покинули пустошь смерти",
                                                reply_markup=menu_go())
        elif msg_txt == "⚔️Дать отпор":
            mob = hero.mob_fight
            if mob:
                res = hero.attack_mob(mob, False, hero.min_log)
                hero.mob_fight = None
                if hero.km != 0:
                    if mob.enfect and not hero.km_protect:
                        out_eff = ""
                        if hero.buffs[0] < 0:
                            out_eff = f"cила {hero.buffs[0]}\n"
                        if hero.buffs[1] < 0:
                            out_eff += f"ловкость {hero.buffs[1]}\n"
                        if hero.buffs[2] < 0:
                            out_eff += f"удача {hero.buffs[2]}\n"
                        if hero.buffs[3] < 0:
                            out_eff += f"точность {hero.buffs[3]}\n"

                        await update.message.reply_text(f"Внимание! Вы заражены:{out_eff}\nПейте баффы: /buff")
                    await menu_sel(update, hero, hero.make_header() + res)
                else:
                    hero.hp = 1
                    await update.message.reply_text(res)
                    await update.message.reply_text(hero.return_data(), reply_markup=menu_camp())
            else:
                await update.message.reply_text(hero.return_data(), reply_markup=menu_pip())
        elif msg_txt == "🏃Дать деру":
            if hero.mob_fight:
                k = hero.dexterity - hero.mob_fight.dexterity
                lost = round(hero.mob_fight.calc_mob_coins(hero.km) * 2)
                if hero.coins > lost:
                    hero.coins -= lost

                if k > random.randint(0, 1000):
                    if hero.coins < 0:
                        hero.coins = 0

                    await update.message.reply_text(hero.make_header() +
                                                    f"побег успешен, но вы потеряли 🕳 {lost}\n",
                                                    reply_markup=menu_go())
                else:
                    dmg = round(hero.mob_fight.get_attack())
                    hero.hp -= dmg
                    if round(hero.hp) <= 0:
                        hero.died_hero()
                        await update.message.reply_text(
                            f"побег не успешен, ты помер\:\(, вы потеряли 🕳 {lost}",
                            reply_markup=menu_camp())
                    else:
                        await menu_sel(update, hero, hero.make_header() +
                                                         f"побег не успешен\(, вы потеряли 💔 {dmg} 🕳 {lost}")

                hero.mob_fight = None

        elif msg_txt == "👣Идти к лагерю":
            if hero.zone > 1:
                await update.message.reply_text("Нельзя идти тут назад!")
                return
            if hero.km <= 1:
                hero.km = 0
                await update.message.reply_text(hero.return_data(), reply_markup=menu_camp())
                return
            hero.go(True)

            if hero.hungry < 100:
                if not hero.zone:
                    hero.hungry += 2
                else:
                    hero.hungry += 3
            else:
                hero.hp -= round(hero.max_hp / 5)
            if hero.hungry > 100:
                hero.hungry = 100
            if hero.hp > 0:
                if hero.hungry > 96:
                    await update.message.reply_text("⭐️⚡вы голодны, скоро начнете умирать⭐️\n/food ⚡")
                header = hero.make_header()
                if random.randint(0, 10) > 8:
                    hero.mob_fight = copy.copy(list_boss[0])
                    hero.mob_fight.name = "💀Теневой некромонстр ⚡️🌟⚡"
                    hero.mob_fight.attack = hero.max_hp*hero.necro_lvl
                    hero.mob_fight.luck = hero.luck/1.5
                    hero.mob_fight.dexterity = hero.dexterity/1.5
                    hero.mob_fight.accuracy = 5000
                    hero.mob_fight.hp = round(hero.max_hp*1.5*hero.necro_lvl)
                    hero.necro_lvl += 0.2
                else:
                    hero.select_mob()
                if hero.mob_fight:
                    await update.message.reply_text(header + f"на вас напал моб {hero.mob_fight.get_name()}",
                                                    reply_markup=menu_attack())
                else:
                    text_go = text_mess_go[random.randint(0, len(text_mess_go)-1)]
                    await update.message.reply_text(header + text_go, reply_markup=menu_go())
            else:
                out = hero.died_hero_mob()
                await update.message.reply_text("⭐️⚡ты сдох от голода((((⭐️⚡\n" + out, reply_markup=menu_camp())

        elif msg_txt == "👣Идти дальше":
            if hero.km == 45 and hero.zone == 5:
                hero.zone = 1
                await update.message.reply_text("Вы покинули арену! Поздравляем!")

            if hero.km == 44 and hero.zone == 3:
                hero.zone = 1
                await update.message.reply_text("Вы покинули блядский цирк")

            if hero.km == 79 and hero.zone == 6:
                hero.zone = 0
                await update.message.reply_text("Вы покинули зону динозавров")

            if hero.km == 59 and hero.zone == 4:
                hero.zone = 1
                await update.message.reply_text("Вы покинули painkiller zone")
            hero.go()
            if hero.hungry < 100:
                if not hero.zone:
                    hero.hungry += 2
                else:
                    hero.hungry += 3
            else:
                hero.hp -= round(hero.max_hp / 5)
            if hero.hungry >100:
                hero.hungry = 100
            if hero.hp > 0:
                if hero.hungry > 96:
                    await update.message.reply_text("⭐️⚡вы голодны, скоро начнете умирать⭐️\n/food ⚡")
                header = hero.make_header()
                if hero.in_dange < 0:
                    hero.in_dange = 0

                hero.select_mob()
                if hero.mob_fight:
                    await update.message.reply_text(header + f"на вас напал моб {hero.mob_fight.get_name()}",
                                                    reply_markup=menu_attack())
                else:
                    text_go = text_mess_go[random.randint(0, len(text_mess_go)-1)]
                    if hero.zone in [1, 2] and random.randint(0, 15) == 4:
                        rkey, ritem = get_random_food()
                        text_go += f"\nбонус зоны:\n{ritem['name']} /ustf_{rkey}\n"
                        hero.stock.add_stuff(rkey)
                    if hero.zone <= 1:
                        await update.message.reply_text(header + text_go, reply_markup=menu_go())
                    elif hero.zone >= 2:
                        await update.message.reply_text(header + text_go, reply_markup=menu_go_dead())

            else:
                out = hero.died_hero_mob()
                await update.message.reply_text("⭐️⚡ты сдох от голода((((⭐️⚡\n" + out, reply_markup=menu_camp())

    else:
        if msg_txt == "👣Дальше":
            if hero.in_dange >= len(danges[hero.km]):
                await danges_fin_msg(update, hero)
                hero.hungry += 2
                hero.danges.append(hero.km)
            else:
                mob = hero.mob_fight
                if mob:
                    res = hero.attack_mob(mob, True, hero.min_log)
                    if hero.km != 0:
                        await update.message.reply_text(res)
                        await update.message.reply_text(hero.make_header() + "продолжаем идти",
                                                        reply_markup=menu_go_dange())
                        hero.mob_fight = danges[hero.km][hero.in_dange]
                        hero.in_dange += 1
                    else:
                        hero.hp = 1
                        hero.mob_fight = None
                        hero.in_dange = 0
                        await update.message.reply_text(res)
                        await update.message.reply_text(hero.return_data(), reply_markup=menu_camp())

    if msg_txt == "⬅️Назад":
        if hero.km == 0:
            await update.message.reply_text(hero.return_data(), reply_markup=menu_camp())
            return
        else:
            await menu_sel(update, hero, "Вы в дороге, идите дальше")

    if msg_txt == "🎒Рюкзак":
        if hero.in_dange <= 0:
            await update.message.reply_text(hero.stock.get_data(), reply_markup=menu_pip())
        else:
            await update.message.reply_text(hero.stock.get_data(), reply_markup=menu_go_dange())
        return
    elif msg_txt == "🔝Топы":
        data = "/topkm  - топ игроков по километрам\n/topcoins" + \
               " - топ игроков по монетам\n/tophp - топ игроков" + \
               "по hp\n/topbm - топ игроков по сумме характеристик"
        await update.message.reply_text(data, reply_markup=menu_pip())
        return

    logger.info(update.effective_chat.first_name + f"  {msg_txt}  {hero.km}km")
    if not hero.mob_fight:
        if hero.in_dange == 0:
            if hero.km != 0 or msg_txt == "🔎Осмотреться":
            #if hero.km != 0:
                out = ""
                for h in all_data:
                    hero_h = all_data[h]
                    if update.effective_user.id != h and hero_h.km == hero.km and hero.zone == hero_h.zone:
                        zone = "☢" if hero_h.zone == 1 else ""
                        if hero.km!=27:
                            out += f"{zone}{hero_h.get_name()}\n"
                        else:
                            out += f"{hero_h.get_name()}  /add_band{hero_h.all_km}\n"

                if out != "":
                    pvp = True
                    out = "возле вас игроки:\n" + out
                    if hero.km != 0:
                        if hero.zone >= 1:
                            if hero.km==27:
                                await update.message.reply_text(out, reply_markup=menu_go())
                                return
                        if hero.zone == 0:
                            pvp = False
                        await update.message.reply_text(out, reply_markup=menu_go(pvp))
                    else:
                        await update.message.reply_text(out, reply_markup=menu_camp())
                        return
                else:
                    pvp = False



        if hero.km in danges.keys() and hero.in_dange == 0 and hero.zone == 0:
            await update.message.reply_text("Перед вами вход в пещеру", reply_markup=menu_dange())
            return

        if hero.zone == 2:
            if hero.km == 30:
                await update.message.reply_text("Можно зайти на смертельную арену 👹👹", reply_markup=menu_mk(pvp))
                return

        if hero.zone == 1:
            if hero.km == 30:
                await update.message.reply_text(f"Можно изучить дзен, всего заполнено 🕳{hero.get_in_dzen()}\nПоместить крышки в дзен /dzen", reply_markup=menu_go(pvp))
                return

            if hero.km == 20:
                await update.message.reply_text("Можно войти в пустошь смерти", reply_markup=menu_dead(pvp))
                return

            if hero.km == 33:
                await update.message.reply_text("Можно войти в пустошь где жизнь это цирк🤡🤡🤡", reply_markup=menu_clown(pvp))
                return

            if hero.km == 47:
                await update.message.reply_text("Можно войти в пустошь painkiller🔪", reply_markup=menu_painkiller(pvp))
                return

            if hero.km == 66:
                await update.message.reply_text("Можно войти в пустошь динозавров", reply_markup=menu_dino(pvp))
                return

            if hero.km == 31 or hero.km == 16:
                await update.message.reply_text("Можно записаться на босса, если у вас больше 100 брони она будет "
                                                "приведена к 100, если больше 400 хп "
                                                "броня приравнивается к 0. Всего игроков 5. удачи))))\n/goboss",
                                                reply_markup=menu_go(pvp))
                return

        if hero.km == 27 and hero.zone <= 1:
            await update.message.reply_text("Здесь можно создать банду.\nС помощью команды /make_band \nСтоить это будет 30000 крышек\nКоманда для выхода из банды /leave_band", reply_markup=menu_go())
            return

        if hero.km == 52:
            await update.message.reply_text("Можно отдохнуть /deeprest", reply_markup=menu_go(pvp))
            return

        if hero.km in [34, 44, 54, 64, 74] and hero.zone == 2:
            await update.message.reply_text("Можно выйти из пустоши смерти", reply_markup=menu_dead_quit(pvp))
            return

        if hero.km in rad_zones and hero.zone <= 1:
            if hero.zone == 1:
                await update.message.reply_text("Можно выйти из радиоактивной пустоши", reply_markup=menu_rad_quit(pvp))
            else:
                await update.message.reply_text("Можно войти в радиактивную пустошь", reply_markup=menu_rad(pvp))
            return

        if pvp_end and out == "":
            await update.message.reply_text("вы в пустоши", reply_markup=menu_go())



async def boss_fight(boss_id: int = 0) -> None:
    if not boss_id:
        return
    list_heroes = []
    for h in all_data:
        hero_h = all_data[h]
        if hero_h.go_boss == boss_id:
            list_heroes.append(hero_h)
    Hero.attack_boss(list_heroes, list_boss[boss_id-1], boss_id=boss_id)

    str_heroes = "\n"
    for i in range(0, len(list_heroes)):
        if list_heroes[i].hp <= 0:
            str_heroes += f"💀{list_heroes[i].name}\n"
        else:
            str_heroes += f"🏆{list_heroes[i].name}\n"

    for i in range(0, len(list_heroes)):
        if list_heroes[i].hp <= 0:
            list_heroes[i].died_hero()
            await list_heroes[i].ef_chat.send_message(list_heroes[i].text_out_boss + str_heroes,
                                                      reply_markup=menu_camp())
        else:
            await list_heroes[i].ef_chat.send_message(list_heroes[i].text_out_boss + str_heroes)


async def comm_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg_txt = update.message.text
    logger.info(update.effective_chat.first_name + "  " + msg_txt)
    hero = await get_hero(update)
    data = ""
    if "/savebase" == msg_txt:
        for k in all_data:
            h = all_data[k]
            await upd_hero_db(async_session, h)
            await delete_hero_weapon_db(async_session, h)
            await delete_hero_armor_db(async_session, h)
            await add_hero_armor_db(async_session, h)
            await add_hero_weapon_db(async_session, h)
            await update_hero_items(async_session, h)
            #await upd_indexes(async_session, h)
    #elif "/initbase" == msg_txt:
    #    await create_table_db(async_session)
    elif "/updindex" == msg_txt:
        await upd_indexes(async_session)
    elif msg_txt.startswith("/tophp"):
        def sortf(e):
            return e.max_hp

        all = await get_hero_db(async_session)
        all.sort(reverse=True, key=sortf)
        p = k = 0
        for h in all:
            if h.id == hero.base_id:
                p = k
            if 5 > k or k >= len(all) - 5:
                data += f"{k+1}. {h.max_hp} || {h.get_name()}\n"
            if k == 5:
                data += "------------\n"
            k += 1
        data += f"\n{p+1}. {hero.max_hp} || {hero.get_name()}\n"

    elif msg_txt.startswith("/topkm"):
        def sortf(e):
            return e.all_km

        all = await get_hero_db(async_session)
        all.sort(reverse=True, key=sortf)
        p = k = 0
        for h in all:
            if h.id == hero.base_id:
                p = k
            if 5 > k or k >= len(all) - 5:
                data += f"{k+1}. {h.all_km} || {h.get_name()}\n"
            if k == 5:
                data += "------------\n"
            k += 1
        data += f"\n{p+1}. {hero.all_km} || {hero.get_name()}\n"


    elif msg_txt.startswith("/topcoins"):
        def sortf(e):
            return e.coins
        all = await get_hero_db(async_session)
        all.sort(reverse=True, key=sortf)
        p = k = 0
        for h in all:
            if h.id == hero.base_id:
                p = k
            if 5 > k or k >= len(all) - 5:
                data += f"{k+1}. {h.coins} || {h.get_name()} \n"
            if k == 5:
                data += "------------\n"
            k += 1
        data += f"\n{p+1}. {hero.coins} || {hero.get_name()}\n"

    elif msg_txt.startswith("/topbm"):
        def sortf(e):
            return e.max_hp + e.force + e.accuracy + e.luck + e.dexterity + e.charisma
        all = await get_hero_db(async_session)
        all.sort(reverse=True, key=sortf)
        p = k = 0
        for h in all:
            if h.id == hero.base_id:
                p = k
            if 5 > k or k >= len(all) - 5:
                data += f"{k+1} {h.max_hp + h.force + h.accuracy + h.luck + h.dexterity + h.charisma} || {h.get_name()}\n"
            if k == 5:
                data += "\n"
            k += 1
        data += f"\n{p+1} {hero.max_hp + hero.force + hero.accuracy + hero.luck + hero.dexterity + hero.charisma} || {hero.get_name()}\n"

    # elif "/cheatw" in msg_txt:
    #    hero.stock.equip[armor_all[0][6].get_code()] = copy.copy(armor_all[0][6])
    #elif "/gokm" in msg_txt:
    #    x = int(msg_txt.replace("/gokm", ""))
    #    hero.km = x
    elif msg_txt.startswith("/name_drone"):
        if len(msg_txt.replace("/name_drone", "")) > 100:
            return
        if hero.drone:
            hero.drone.name = msg_txt.replace("/name_drone", "")
    elif "/online" == msg_txt:
        for h in all_data:
            hero_h = all_data[h]
            if hero_h.id != hero.id:
                data += f"{hero_h.get_name()} {hero_h.km}\n"
    elif "/band" == msg_txt:
        if hero.band_name:
            all = await get_hero_db(async_session)
            data = f"вы в банде {hero.band_name}:\n"
            for h in all:
                if h.id != hero.base_id and hero.band_name == h.band_name:
                    data += f"{h.name}\n"

    elif msg_txt.startswith("/msgall"):
        msg = msg_txt.replace("/msgall", "")
        for h in all_data:
            hero_h = all_data[h]
            if hero_h.id != hero.id:
                chat = all_data[h].ef_chat
                await chat.send_message(msg)
    # elif "/cheatgg" in msg_txt:
    #     x = int(msg_txt.replace("/cheatgg", ""))
    #     hero.coins = 1000
    #     hero.materials = 0
    #     hero.hp = x
    #     hero.max_hp = x
    #     hero.force = x
    #     hero.luck = x
    #     hero.dexterity = x
    #     hero.accuracy = x
    #     hero.charisma = x

    elif msg_txt == "/mystock":
        data = hero.stock.get_data()
    elif msg_txt == "/help":
        data = "Немного информации по пустоши.\n\nПро обычную пустошь.\nВ игре есть основная пустошь, где нельзя нападать на игроков. Если умрешь до 30 км, то не теряешь крышек. Если умираешь после 30км включительно, то теряешь 25%. Коробки не теряются. С мобов выпадает еда и баффы. Баффы используются для повышения характеристик и снимания заражения. Заражение снимает 1/2 рандомной характеристики. Еда понятно для снижения голода. На 52км можно обнулить голод.Данжи доступны только из основной пустоши. Дроны не выпадают, но можно купить у инженера. Можно идти назад, но с шансом 25% нападет монстр. Мобы каждые 5км становятся сильнее. \n\nПро рад пустошь.\nСмерть в этой зоне -50%, как и в других зонах, кроме первой. Мобы в 2 раза сильнее чем в обычной. Вход в рад в лагере. А также входы и выходы на 15км, 25км, 34км, 45км, 55км, 65км. После 30км в рад выпадают стимбласты и другие сильные аптечки. Повышенный шанс выпадения баффов и еды. Выпадает второй дрон, если нет. На 20км можно зайти в смертельную зону. На 33км вход в зону блядского цирка, на 47км вход в painkiller зону. В ней есть на 30км место для пополнения дзена, на 16км и 31км можно записаться на босса. Мобы каждые 5км становятся сильнее. \n\nПро зону смерти.\nВход на 20км в зону. Выходы 34км, 44км, 54км. Раньше выйти из зоны возвратившись в лагерь нельзя. Там самые сильные мобы. Там выпадают аптечки, дрон как в рад, с небольшим шансом  выпадает броня и оружие с мобов. Есть вход в арену смерти на 30км. Мобы каждые 5км становятся сильнее. Выпадают модифиакторы на оружие и броню.\n\nПро зону клоунов.\nВход на 33км. Выпадает такой же дрон как в рад. Также выпадает уникальная броня и оружие. Выходишь дойдя до конца зоны на 44км. Особые мобы разной силы рандомно по всему промежутку зоны.\n\nПро painkiller зону.\nВход на 47км из рад пустоши. Выход на 59км. В зоне обитают особые мобы и рандомно распределены по пустоши. Увеличенный шанс выпадения аптечек. Выпадает особый дрон, который сильнее чем в рад. Выпадают модифиакторы на оружие и броню.\n\nПро arena зону.\nВход на 30км из пустоши смерти. Там очень сильные мобы и с каждым км сильнее. Из самого сильного моба выбивается оружие и броня. Выпадают аптечки и остальное. Также там можно найти самого сильного дрона. Выход в рад зону на 46 км. Также выпадают модифиакторы на оружие и броню.\n\nПро модификаторы.\nЕсть которые увеличивают хакрактеристики оружия или брони, но снижают характеристики героя. А есть которые снижают характеристики оружия и брони, но увеличивают навыки героя.\n\nПро модули.\nМодули выпадают в данжах. 30км - 1 модуль, 35км- 1 модуль, 40км- 1 модуль, 50км- 3 модуля, 60км - 1 модуль. Акивируется сразу. Но можно поменять у инженера. \n\nПро банды.\nМожно создать свою банду на 27км. Забирать к себе в банду может любой. Надо чтобы вы были в одной пустоши.\n\nПро перки.\nЕсть 6 перков. Действуют в пвп и с дронами. Нужны такие значения для взятия 1-4 перков - 250, 550, 850, 1150. Очки характеристик 1250 тратятся на перк. Сила кратно увеличивает силу, ловкость соответственно увеличивает ловкость, удача дает шанс на регенерацию 30%, харизма увеличивает шансы вступления в битву дрона, меткость увеличивает разброс урона, живучесть увеличивает броню."
    elif msg_txt == "/mods":
        data = hero.stock.get_mods()
    elif msg_txt == "/food":
        data = hero.stock.print_stuff(1)
    elif msg_txt == "/buff":
        data = hero.stock.print_stuff(2)
    elif msg_txt == "/boss":
        cnt_boss = 0
        for h in all_data:
            hero_h = all_data[h]
            if hero.go_boss and hero_h.go_boss == hero.go_boss:
                cnt_boss += 1
        if cnt_boss:
            await update.message.reply_text(f"записано на босса {list_boss[hero.go_boss-1].name} {cnt_boss}")
        else:
            await update.message.reply_text(f"никого нет на босса")

    # elif "/additm" in msg_txt:
    #     msg = msg_txt.replace("/additm", "")
    #     items = msg.split("u")
    #     user = items[0]
    #     item = items[1]
    #     for h in all_data:
    #         if h == user:
    #             hero_h = all_data[h]
    #             if item.startswith("w"):
    #                 dmg = item.replace("w", "")
    #                 for weapon in weapons_all:
    #                     if str(weapon.dmg) == dmg:
    #                         hero_h.stock.add_item(weapon)
    #             if item.startswith("a"):
    #                 arm = item.replace("a", "")
    #                 arm = arm.split('t')
    #                 for armor in armor_all[arm[0]]:
    #                     if str(armor.arm) == arm[1]:
    #                         hero_h.stock.add_item(armor)

    elif msg_txt.startswith("/set_name "):
        name = msg_txt.replace("/set_name ", "")
        hero.name = name

    elif msg_txt == "/startboss":
        if hero.go_boss:
            await boss_fight(hero.go_boss)
        else:
            await update.message.reply_text(f"никого нет на босса")

    elif msg_txt == "/goboss" and (hero.km == 31 or hero.km == 16) and hero.zone == 1:
        if not hero.go_boss:
            if hero.km == 16:
                hero.go_boss = 2
            if hero.km == 31:
                hero.go_boss = 1
            cnt_boss = 0
            for h in all_data:
                hero_h = all_data[h]
                if hero_h.go_boss == hero.go_boss:
                    cnt_boss += 1
            if cnt_boss == 5:
                await boss_fight(hero.go_boss)
            else:
                await update.message.reply_text("вы записались на босса")
        else:
            await update.message.reply_text("уже записаны на босса")


    elif "/ustf_" in msg_txt:
        code = msg_txt.replace("/ustf_", "")
        if len(code) > 100:
            return
        data_ = hero.stock.use_stuff(int(code), hero)
        await update.message.reply_text(data_)
        #await menu_sel(update, hero, data_)

    elif "/drop" == msg_txt:
        data = hero.stock.get_delete()

    elif msg_txt.startswith("/drw_") or msg_txt.startswith("/dra_"):
        i = msg_txt.replace("/drw_", "").replace("/dra_", "")
        if len(i) > 100:
            return
        if hero.stock.equip.get(i, None):
            data = f"вы уверены что хотите удалить?{hero.stock.equip.get(i).get_name()}\n"
            i_new = msg_txt.replace("/drw_", "/drww_").replace("/dra_", "/draa_")
            data += i_new
        else:
            data = "ошибка удаления\n"
    elif msg_txt.startswith("/drww_") or msg_txt.startswith("/draa_"):
        i = msg_txt.replace("/drww_", "").replace("/draa_", "")
        if len(i) > 100:
            return
        i_del = hero.stock.equip.pop(i)
        data = f"удалено {i_del.get_name()}"
    elif msg_txt.startswith("/eqw_"):
        w = msg_txt.replace("/eqw_", "")
        if len(w) > 100:
            return
        wp = hero.stock.equip.get(w, None)
        data_ = "ошибка"
        if wp:
            weapon = hero.stock.equip.pop(w)
            if hero.weapon:
                hero.stock.add_item(hero.weapon)
            hero.weapon = copy.copy(weapon)
            hero.weapon.use = 1
            #data_ = hero.stock.get_data()
            data_ = "экипировано: " + hero.weapon.get_name()
        await menu_sel(update, hero, data_)
    elif msg_txt.startswith("/eqa_"):
        a = msg_txt.replace("/eqa_", "")
        if len(a) > 100:
            return
        ap = hero.stock.equip.get(a, None)
        data_ = "ошибка"
        if ap:
            i = int(a.split('t')[0])
            arm = hero.stock.equip.pop(a)
            if hero.armor[i]:
                hero.stock.add_item(hero.armor[i])

            hero.armor[i] = copy.copy(arm)
            hero.armor[i].use = 1
            data_ = "экипировано: " + hero.armor[i].get_name()
            #data_ = hero.stock.get_data()
        await menu_sel(update, hero, data_)

    elif msg_txt.startswith("/sw_") and hero.km == 0:
        w = msg_txt.replace("/sw_", "")
        if len(w) > 100:
            return
        wp = hero.stock.equip.get(w, None)
        if wp:
            w = hero.stock.equip.pop(w)
            hero.materials += w.calc_cost()
            out = f"📦×{hero.materials}\n"
            out += hero.stock.get_data_lombard()
            await update.message.reply_text(out, reply_markup=menu_lomb())
    elif msg_txt.startswith("/sa_") and hero.km == 0:
        a = msg_txt.replace("/sa_", "")
        if len(a) > 100:
            return
        ap = hero.stock.equip.get(a, None)
        if ap:
            a = hero.stock.equip.pop(a)
            hero.materials += a.calc_cost()
            out = f"📦×{hero.materials}\n"
            out += hero.stock.get_data_lombard()
            await update.message.reply_text(out, reply_markup=menu_lomb())
    elif msg_txt.startswith("/givecoin") and hero.km == 0:
        #id = "48"
        a = msg_txt.replace("/givecoin", "")
        id = a.split("id")[0]
        coins = a.split("id")[1]
        for h in all_data:
            hero_h = all_data[h]
            if hero_h.base_id == int(id):
                hero_h.coins = int(coins)
                break

    elif msg_txt.startswith("/bw_") and hero.km == 0:
        if len(hero.stock.equip) >= hero.stock.MAX_EQUIP:
            data = "рюкзак полон"
        else:
            weapon_dmg = msg_txt.replace("/bw_", "")
            if len(weapon_dmg) > 100:
                return
            buy_weapon = None
            for weapon in weapons_all:
                if str(weapon.dmg) == weapon_dmg:
                    buy_weapon = weapon
                    break

            if buy_weapon:
                cost = buy_weapon.calc_cost()
                if cost <= hero.coins:
                    hero.stock.add_item(buy_weapon)
                    hero.coins -= cost
                    data = f"вы купили {buy_weapon.get_name()}"
                else:
                    data = "не хватило денег для покупки"
    elif msg_txt.startswith("/ba_") and hero.km == 0:
        if len(hero.stock.equip) >= hero.stock.MAX_EQUIP:
            data = "рюкзак полон"
        else:
            buy_arm_code = msg_txt.replace("/ba_", "").split('t')
            buy_arm_type = buy_arm_code[0]
            buy_arm_val = buy_arm_code[1]
            buy_arm = None
            if buy_arm_type in ['0', '1', '2']:
                for ar in armor_all[int(buy_arm_type)]:
                    if str(ar.arm) == buy_arm_val:
                        buy_arm = ar
                        break
            if buy_arm:
                cost = buy_arm.calc_cost()
                if cost <= hero.coins:
                    hero.stock.add_item(buy_arm)
                    hero.coins -= cost
                    data = f"вы купили {buy_arm.get_name()}"
                else:
                    data = "не хватило денег для покупки"
    elif msg_txt.startswith("/module") and hero.km == 0:
        i_mod = msg_txt.replace("/module", "")
        try:
            if 0 <= int(i_mod) <= 7:
                data = hero.activate_module(int(i_mod))
        except Exception as e:
            pass
    elif "/buy_dr_1" == msg_txt and hero.km == 0:
        if hero.coins > 200000:
            hero.drone = copy.copy(all_drones[0])
            hero.coins -= 200000
            data = "вы купили дрона!"
        else:
            data = "не хватает крышек((("
    elif "/dzen" == msg_txt and hero.km == 30 and hero.zone == 1:
        data = f"Вы отправили 🕳{round(hero.coins)} в дзен\n"
        hero.dzen += hero.coins
        hero.coins = 0
        data += f"Набрано 🕳{hero.get_in_dzen()} из 🕳{hero.get_coins_to_dzen()}\n"
    elif "/make_band" == msg_txt and hero.km == 27 and hero.zone <= 1:
        if hero.coins >= 30000:
            hero.band_name = "введите имя банды"
            data = "введите имя банды"
            hero.coins -= 30000
        else:
            data = "не хватает крышек((("
    elif msg_txt == "/leave_band" and hero.km == 27 and hero.zone <= 1:
        if hero.band_name and hero.band_name != "":
            hero.band_name = ""
            data = f"вы покинули банду {hero.band_name}(((!!"
            await upd_hero_db(async_session, hero)
        else:
            data = f"вы не в банде!!"
    elif msg_txt.startswith("/add_band") and hero.km == 27 and hero.zone <= 1:
        iduser = int(msg_txt.replace("/add_band", ""))
        for h in all_data:
            hero_h = all_data[h]
            if hero_h.all_km == iduser and (hero_h.band_name == None or hero_h.band_name == ""):
                hero_h.band_name = hero.band_name
                data = f"вы взяли игрока {hero_h.get_name()} в банду {hero.band_name}!!"
                await upd_hero_db(async_session, hero_h)
                break

    elif hero.km == 52 and "/deeprest" == msg_txt:
        hero.hungry = 0
        await menu_sel(update, hero, "вы покушали")

    elif "/mobs" == msg_txt:
        if hero.mobs:
            data = "Мобы в команде:\n"
            for m in hero.mobs:
                data += f"{m.get_name()}\n"
    elif "/clr_mobs" == msg_txt:
        if hero.mobs:
            hero.mobs = []
            data = "вы выкинули мобов"
    #elif "/perksx" == msg_txt and hero.id == 1:
    #    hero.perks = '0' * 6
    elif "/min_log" == msg_txt:
        hero.min_log = not hero.min_log
    elif "/perks" == msg_txt:
        data = hero.return_perks()
    elif "/perk_" in msg_txt and hero.free_perks():
        if msg_txt == "/perk_force":
            data = hero.inc_perk(0)
        if msg_txt == "/perk_arm":
            data = hero.inc_perk(1)
        if msg_txt == "/perk_dex":
            data = hero.inc_perk(2)
        if msg_txt == "/perk_accur":
            data = hero.inc_perk(3)
        if msg_txt == "/perk_char":
            data = hero.inc_perk(4)
        if msg_txt == "/perk_luck":
            data = hero.inc_perk(5)

    elif msg_txt.startswith("/mod_"):
        a = msg_txt.replace("/mod_", "")
        ap = hero.stock.equip.get(a.split('m')[0], None)
        data_ = "ошибка"
        if ap and not ap.mod:
            code = int(a.split('m')[1])
            ap.mod = code
            if hero.accuracy < 300 or hero.luck < 300 or hero.dexterity < 300 :
                await update.message.reply_text("повысьте характеристики точности, ловкости и удачи до 300")
                return
            data_ = f"{ap.name} улучшено"
            stf = hero.stock.used_stuff.get(code, None)
            if stf:
                if hero.stock.used_stuff[code] == 1:
                    hero.stock.used_stuff.pop(code)
                else:
                    hero.stock.used_stuff[code] -= 1

        await menu_sel(update, hero, data_)
    #await update.message.reply_markdown_v2(text=data)
    if data != "":
        if hero.in_dange <= 0:
            #await update.message.reply_markdown_v2(data, reply_markup=menu_pip())
            await update.message.reply_text(data, reply_markup=menu_pip())
        else:
            #await update.message.reply_markdown_v2(data, reply_markup=menu_go_dange())
            await update.message.reply_text(data, reply_markup=menu_pip())


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("me", me_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_msg))
    application.add_handler(MessageHandler(filters.COMMAND, comm_msg))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
