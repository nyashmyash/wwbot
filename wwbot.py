#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position


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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!"
    )

#list_mob_clown_zone

async def get_hero(update):
    rslt = all_data.get(update.effective_user.id, None)
    if not rslt:
        db_hero_fetch = await get_hero_db(async_session, str(update.effective_user.id))

        hero = Hero()
        stock = Stock()
        hero.stock = stock
        hero.buffs = [0, 0, 0, 0]
        stock.equip = OrderedDict()
        if not len(db_hero_fetch):
            # for i in range(0, 5):
            #    stock.equip[weapons_all[i].get_code()] = copy.copy(weapons_all[i])
            # for i in range(0, 3):
            #    stock.equip[armor_all[i][6].get_code()] = copy.copy(armor_all[i][6])

            hero.id = str(update.effective_user.id)
            hero.chat_id = str(update.effective_chat.id)
            hero.name = update.effective_chat.first_name
            hero.weapon = copy.copy(weapons_all[0])
            hero.weapon.use = 1
            hero.armor = []
            hero.armor.append(copy.copy(armor_all[0][0]))
            hero.armor.append(copy.copy(armor_all[1][0]))
            hero.armor.append(copy.copy(armor_all[2][0]))
            hero.stock.used_stuff = {}
            hero.coins = 1000
            await add_hero_db(async_session, hero)
            await add_hero_armor_db(async_session, h)
            await add_hero_weapon_db(async_session, h)

        else:
            hero_db = db_hero_fetch[0]
            db_hero_wp = await get_hero_weapon_db(async_session, hero_db)
            hero.from_db(hero_db)
            hero.chat_id = str(update.effective_chat.id)
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

        all_data[update.effective_user.id] = [hero, update.effective_chat]
        return hero
    else:
        return rslt[0]


async def me_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    hero = await get_hero(update)
    if hero.mob_fight:
        await update.message.reply_text(f"на вас напал моб {hero.mob_fight.name}", reply_markup=menu_attack())
    else:
        await update.message.reply_text(hero.return_data(), reply_markup=menu_pip())

rad_zones = [15, 25, 34, 45, 55, 65, 75, 85]


async def menu_sel(update: Update, hero: Hero, data_:str) -> None:
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
    if hero.km == 10:
        r = random.randint(0, 7)
        logger.info(update.effective_chat.first_name + f" dange {hero.km}km {r}")
        if r == 1:
            i = random.randint(4, 6)
            hero.stock.add_item(weapons_all[i])
            await update.message.reply_text(hero.make_header()
                                            + f"вам выпало {weapons_all[i].name}",
                                            reply_markup=menu_go())
        else:
            await update.message.reply_text(hero.make_header()
                                            + "вам выпало нихуя",
                                            reply_markup=menu_go())

    if hero.km == 20:
        r = random.randint(0, 7)
        logger.info(update.effective_chat.first_name + f" dange {hero.km}km {r}")
        if r == 2:
            type = random.randint(0, 2)
            hero.stock.add_item(armor_all[type][5])
            await update.message.reply_text(hero.make_header()
                                            + f"вам выпало {armor_all[type][5].name}",
                                            reply_markup=menu_go())
        else:
            await update.message.reply_text(hero.make_header()
                                            + "вам выпало нихуя",
                                            reply_markup=menu_go())
    if hero.km == 30:
        r = random.randint(0, 6)
        logger.info(update.effective_chat.first_name + f" dange {hero.km}km {r}")
        if r == 3:
            r = random.randint(7, 8)
            hero.stock.add_item(weapons_all[r])
            await update.message.reply_text(hero.make_header()
                                            + f"вам выпало {weapons_all[r].name}",
                                            reply_markup=menu_go())
        else:
            if random.randint(0, 15) == 1 and hero.modul == 0:
                hero.add_module()
                name = hero.get_str_modul()
                await update.message.reply_text(hero.make_header()
                                                + f"вам выпал модуль {name}",
                                                reply_markup=menu_go())
            else:
                await update.message.reply_text(hero.make_header()
                                                + "вам выпало нихуя",
                                                reply_markup=menu_go())

    if hero.km == 35:
        r = random.randint(0, 6)
        logger.info(update.effective_chat.first_name + f" dange {hero.km}km {r}")
        if r == 3:
            type = random.randint(0, 2)
            hero.stock.add_item(armor_all[type][6])
            w = armor_all[type][6]
            await update.message.reply_text(hero.make_header()
                                            + f"вам выпало {w.name}",
                                            reply_markup=menu_go())
        else:
            if random.randint(0, 15) == 1 and hero.modul == 2:
                hero.add_module()
                name = hero.get_str_modul()
                await update.message.reply_text(hero.make_header()
                                                + f"вам выпал модуль {name}",
                                                reply_markup=menu_go())
            else:
                await update.message.reply_text(hero.make_header()
                                                + "вам выпало нихуя",
                                                reply_markup=menu_go())

    if hero.km == 40:
        r = random.randint(0, 6)
        logger.info(update.effective_chat.first_name + f" dange {hero.km}km {r}")
        if r == 4:
            type = random.randint(0, 2)
            hero.stock.add_item(armor_all[type][7])
            await update.message.reply_text(hero.make_header()
                                            + f"вам выпало {armor_all[type][7].name}",
                                            reply_markup=menu_go())
        elif r == 5:
            w = weapons_all[10] if random.randint(0, 2) == 1 else weapons_all[9]
            hero.stock.add_item(w)
            await update.message.reply_text(hero.make_header()
                                            + f"вам выпало {w.name}",
                                            reply_markup=menu_go())
        else:
            if random.randint(0, 15) == 1 and hero.modul in [21, 12]:
                hero.add_module()
                name = hero.get_str_modul()
                await update.message.reply_text(hero.make_header()
                                                + f"вам выпал модуль {name}",
                                                reply_markup=menu_go())
            else:
                await update.message.reply_text(hero.make_header()
                                                + "вам выпало нихуя",
                                                reply_markup=menu_go())

    if hero.km == 50:
        r = random.randint(0, 7)
        logger.info(update.effective_chat.first_name + f" dange {hero.km}km {r}")
        if r == 4:
            type = random.randint(0, 2)
            hero.stock.add_item(armor_all[type][8])
            await update.message.reply_text(hero.make_header()
                                            + f"вам выпало {armor_all[type][8].name}",
                                            reply_markup=menu_go())
        elif r == 5:
            w = weapons_all[11 + random.randint(0, 2)]
            hero.stock.add_item(w)
            await update.message.reply_text(hero.make_header()
                                            + f"вам выпало {w.name}",
                                            reply_markup=menu_go())
        else:
            if random.randint(0, 15) == 1 and 100 < hero.modul < 100000:
                hero.add_module()
                name = hero.get_str_modul()
                await update.message.reply_text(hero.make_header()
                                                + f"вам выпал модуль {name}",
                                                reply_markup=menu_go())
            else:
                await update.message.reply_text(hero.make_header()
                                                + "вам выпало нихуя",
                                                reply_markup=menu_go())

    if hero.km == 60:
        r = random.randint(0, 7)
        logger.info(update.effective_chat.first_name + f" dange {hero.km}km {r}")
        if r == 4:
            type = random.randint(0, 2)
            hero.stock.add_item(armor_all[type][9])
            await update.message.reply_text(hero.make_header()
                                            + f"вам выпало {armor_all[type][9].name}",
                                            reply_markup=menu_go())
        elif r == 5:
            w = weapons_all[13 + random.randint(0, 3)]
            hero.stock.add_item(w)
            await update.message.reply_text(hero.make_header()
                                            + f"вам выпало {w.name}",
                                            reply_markup=menu_go())
        else:
            await update.message.reply_text(hero.make_header()
                                            + "вам выпало нихуя",
                                            reply_markup=menu_go())

    if hero.km == 70:
        r = random.randint(0, 8)
        logger.info(update.effective_chat.first_name + f" dange {hero.km}km {r}")
        if r == 4:
            type = random.randint(0, 2)
            hero.stock.add_item(armor_all[type][10])
            await update.message.reply_text(hero.make_header()
                                            + f"вам выпало {armor_all[type][10].name}",
                                            reply_markup=menu_go())
        elif r == 5:
            w = weapons_all[17 + random.randint(0, 2)]
            hero.stock.add_item(w)
            await update.message.reply_text(hero.make_header()
                                            + f"вам выпало {w.name}",
                                            reply_markup=menu_go())
        else:
            await update.message.reply_text(hero.make_header()
                                            + "вам выпало нихуя",
                                            reply_markup=menu_go())
    if hero.km == 80:
        r = random.randint(0, 9)
        logger.info(update.effective_chat.first_name + f" dange {hero.km}km {r}")
        if r == 4:
            type = random.randint(0, 2)
            hero.stock.add_item(armor_all[type][11])
            await update.message.reply_text(hero.make_header()
                                            + f"вам выпало {armor_all[type][10].name}",
                                            reply_markup=menu_go())
        elif r == 5:
            w = weapons_all[20]
            hero.stock.add_item(w)
            await update.message.reply_text(hero.make_header()
                                            + f"вам выпало {w.name}",
                                            reply_markup=menu_go())
        else:
            await update.message.reply_text(hero.make_header()
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
        cnt_mod = len(str(hero.modul)) if hero.modul else 0
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
        hero.materials = round(hero.materials / 2)
        out = f"📦×{hero.materials}\n"
        out += hero.stock.get_data_lombard()
        await update.message.reply_text(out, reply_markup=menu_lomb())
    elif msg_txt == "Продать 1/4 коробок":
        hero.coins += round(hero.materials / 40)
        hero.materials = round(hero.materials / 4)
        out = f"📦×{hero.materials}\n"
        out += hero.stock.get_data_lombard()
        await update.message.reply_text(out, reply_markup=menu_lomb())
    elif msg_txt == "Продать 1/8 коробок":
        hero.coins += round(hero.materials / 80)
        hero.materials = round(hero.materials / 8)
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
    if hero.km != 0:
        if hero.weapon and hero.weapon.life < 5:
            await update.message.reply_text(f"⭐️⚡️Внимание, оружие {hero.weapon.name} скоро сломается!⭐️⚡️")
        for ar in hero.armor:
            if ar and ar.life < 3:
                await update.message.reply_text(f"⭐️⚡️Внимание, броня {ar.name} скоро сломается!⭐️⚡️")

    if hero.km == 0:
        await msgs_in_camp(update, msg_txt, hero)

    if hero.in_dange <= 0:
        if msg_txt == "🔥Зайти в данж" and hero.km in danges.keys() and hero.in_dange == 0:
            hero.mob_fight = danges[hero.km][0]
            hero.in_dange = 1
            await update.message.reply_text(f"на вас напал моб {hero.mob_fight.name}",
                                            reply_markup=menu_go_dange())
        elif hero.mob_fight and msg_txt != "⚔️Дать отпор" and msg_txt != "🏃Дать деру":
            await update.message.reply_text(f"на вас напал моб {hero.mob_fight.name}",
                                            reply_markup=menu_attack())
        elif not hero.mob_fight and msg_txt == "⛺️В лагерь":
            if hero.zone ==2 or hero.zone == 3:
                await update.message.reply_text("☠☠в лагерь нельзя☠☠", reply_markup=menu_go_dead())
            else:
                hero.km = 0
                await update.message.reply_text(hero.return_data(), reply_markup=menu_camp())
        elif msg_txt == "📟Пип-бой":
            await update.message.reply_text(hero.return_data(), reply_markup=menu_pip())
        elif msg_txt == "🔪Напасть" and hero.km != 0:
            if hero.zone == 0:
                await update.message.reply_text("можете напасть только в рад-зоне")
            else:
                fight = False
                not_zone = False
                if hero.zone == 1:
                    for h in all_data:
                        hero_h = all_data[h][0]
                        if update.effective_user.id != h and hero_h.km == hero.km and hero_h.in_dange <= 0 and hero.zone == hero_h.zone:
                            chat = all_data[h][1]
                            fight = True
                            out = hero.attack_pvp_wmobs(hero_h)

                            hdr1 = f"Сражение с {hero.name}\n"
                            hdr2 = f"Сражение с {hero_h.name}\n"
                            if hero_h.hp <= 0:
                                hero_h.died_hero()  # -10%
                                hero_h.coins -= round(hero_h.coins * (0.1 + hero.get_module(6) / 100))
                                hero.coins += round(hero_h.coins * (0.09 + hero.get_module(6) / 100))
                                await update.message.reply_text(hdr2 + out +
                                                                f"Вы выиграли!!!\n получено: 🕳 {round(hero_h.coins * 0.09)}",
                                                                reply_markup=menu_go())
                                await chat.send_message(hdr1 + out +
                                                        f"Вы проиграли:((((\n потеряно: 🕳 {round(hero_h.coins * 0.1)}",
                                                        reply_markup=menu_camp())
                            if hero.hp <= 0:
                                hero.died_hero()
                                hero.coins -= round(hero.coins * (0.1 + hero_h.get_module(6) / 100))
                                hero_h.coins += round(hero.coins * (0.09 + hero_h.get_module(6) / 100))
                                await update.message.reply_text(hdr2 + out +
                                                                f"Вы лузер!!!!\n потеряно: 🕳 {round(hero.coins * 0.1)}",
                                                                reply_markup=menu_camp())
                                await chat.send_message(
                                    hdr1 + out + f"Вы выиграли!!!\n получено: 🕳 {round(hero.coins * 0.09)}",
                                    reply_markup=menu_go())
                            break
                    if not fight:
                        await update.message.reply_text("противник ушел")
                else:
                    await update.message.reply_text("нельзя нападать в обычной пустоши")

        elif msg_txt == "👣Пустошь" and hero.zone == 0:
            hero.go()
            header = hero.make_header()

            hero.select_mob()
            if hero.mob_fight:
                await update.message.reply_text(header + "вы отправились в пустошь")
                await update.message.reply_text(f"на вас напал моб {hero.mob_fight.name}",
                                                reply_markup=menu_attack())
            else:
                await update.message.reply_text(header + "вы отправились в пустошь", reply_markup=menu_go())
        elif msg_txt == "👣️☠️Пустошь смерти☠️":
            if hero.km == 20 and hero.zone == 1:
                hero.zone = 2
                hero.go()
                header = hero.make_header()
                hero.select_mob()
                if hero.mob_fight:
                    await update.message.reply_text(header + "вы отправились в пустошь смерти, вернуться в лагерь нельзя")
                    await update.message.reply_text(f"на вас напал моб {hero.mob_fight.name}",
                                                    reply_markup=menu_attack())
                else:
                    await update.message.reply_text(header + "вы отправились в пустошь смерти, вернуться в лагерь нельзя",
                                                    reply_markup=menu_go_dead())
        elif msg_txt == "👣️🎪 Зайти в блядский цирк🎪 ️":
            if hero.km == 33 and hero.zone == 1:
                hero.zone = 3
                hero.go()
                header = hero.make_header()
                hero.select_mob()
                if hero.mob_fight:
                    await update.message.reply_text(header + "вы отправились в блядский цирк, вернуться в лагерь нельзя")
                    await update.message.reply_text(f"на вас напал моб {hero.mob_fight.name}",
                                                    reply_markup=menu_attack())
                else:
                    await update.message.reply_text(header + "вы отправились в блядский цирк, вернуться в лагерь нельзя",
                                                    reply_markup=menu_go_dead())
        elif msg_txt == "👣☢Рад-️Пустошь":
            if hero.km in rad_zones or hero.km == 0:
                hero.zone = 1
                hero.go()
                header = hero.make_header()
                hero.select_mob()
                if hero.mob_fight:
                    await update.message.reply_text(header + "вы отправились в радиоактивную пустошь")
                    await update.message.reply_text(f"на вас напал моб {hero.mob_fight.name}",
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
                    await update.message.reply_text(f"на вас напал моб {hero.mob_fight.name}",
                                                    reply_markup=menu_attack())
                else:
                    await update.message.reply_text(header + "вы покинули радиоактивную пустошь",
                                                    reply_markup=menu_go())

        elif msg_txt == "⚔️Дать отпор":
            mob = hero.mob_fight
            if mob:
                res = hero.attack_mob(mob)
                hero.mob_fight = None
                if hero.km != 0:
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
                            f"побег не успешен, ты помер:(((((, вы потеряли 🕳 {lost}",
                            reply_markup=menu_camp())
                    else:
                        await menu_sel(update, hero, hero.make_header() +
                                                         f"побег не успешен(((, вы потеряли 💔 {dmg} 🕳 {lost}")

                hero.mob_fight = None

        elif msg_txt == "👣Идти дaльше":
            if hero.km == 34 and hero.zone == 2:
                hero.zone = 1
                await update.message.reply_text("Вы вышли из пустоши смерти")
            if hero.km == 44 and hero.zone == 3:
                hero.zone = 1
                await update.message.reply_text("Вы покинули блядский цирк")
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
                    await update.message.reply_text(header + f"на вас напал моб {hero.mob_fight.name}",
                                                    reply_markup=menu_attack())
                else:
                    text_go = text_mess_go[random.randint(0, len(text_mess_go)-1)]
                    if hero.zone in [1, 2] and random.randint(0, 15) == 4:
                        rkey, ritem = get_random_food()
                        text_go += f"\n✅✅вам выпал {ritem['name']} /ustf_{rkey}✅✅\n"
                        hero.stock.add_stuff(rkey)
                    if hero.zone <= 1:
                        await update.message.reply_text(header + text_go, reply_markup=menu_go())
                    elif hero.zone == 2 or hero.zone == 3:
                        await update.message.reply_text(header + text_go, reply_markup=menu_go_dead())

            else:
                hero.hp = 1
                hero.km = 0
                await update.message.reply_text("⭐️⚡ты сдох от голода((((⭐️⚡", reply_markup=menu_camp())

        elif msg_txt == "⬅️Назад":
            if hero.km == 0:
                await update.message.reply_text(hero.return_data(), reply_markup=menu_camp())
            else:
                await menu_sel(update, hero, "Вы в дороге, идите дальше.")
                #await update.message.reply_text("Вы в дороге, идите дальше.", reply_markup=menu_go())
    else:
        if msg_txt == "👣Дальше":
            if hero.in_dange >= len(danges[hero.km]):
                await danges_fin_msg(update, hero)
                hero.hungry += 2
            else:
                mob = hero.mob_fight
                if mob:
                    res = hero.attack_mob(mob, True)
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

    if msg_txt == "🎒Рюкзак":
        if hero.in_dange <= 0:
            await update.message.reply_text(hero.stock.get_data(), reply_markup=menu_pip())
        else:
            await update.message.reply_text(hero.stock.get_data(), reply_markup=menu_go_dange())
    elif msg_txt == "🔝Топы":
        data = "/topkm  - топ игроков по километрам\n/topcoins" + \
               " - топ игроков по монетам\n/tophp - топ игроков" + \
               "по hp\n/topbm - топ игроков по сумме характеристик"
        await update.message.reply_text(data, reply_markup=menu_pip())

    logger.info(update.effective_chat.first_name + f"  {msg_txt}  {hero.km}km")

    if hero.in_dange == 0:
        if not hero.mob_fight and hero.km != 0 or msg_txt == "🔎Осмотреться":
            out = ""
            for h in all_data:
                hero_h = all_data[h][0]
                if update.effective_user.id != h and hero_h.km == hero.km and hero.zone == hero_h.zone:
                    zone = "☢" if hero_h.zone == 1 else ""
                    out += f"{zone}{hero_h.name}\n"

            if out != "":
                out = "возле вас игроки:\n" + out
                if hero.km != 0:
                    if hero.zone >= 1:
                        await update.message.reply_text(out, reply_markup=menu_pvp())
                    elif hero.zone == 0:
                        await update.message.reply_text(out, reply_markup=menu_go())
                else:
                    await update.message.reply_text(out, reply_markup=menu_camp())

    if hero.km in danges.keys() and not hero.mob_fight and hero.in_dange == 0 and hero.zone == 0:
        await update.message.reply_text("Перед вами вход в пещеру", reply_markup=menu_dange())

    if hero.km == 30 and not hero.mob_fight and hero.zone == 1:
        await update.message.reply_text(f"Можно изучить дзен, всего заполнено 🕳{hero.get_in_dzen()}\nПоместить крышки в дзен /dzen", reply_markup=menu_go())

    if hero.km == 20 and hero.zone == 1 and not hero.mob_fight:
        await update.message.reply_text("Можно войти в пустошь смерти", reply_markup=menu_dead())

    if hero.km == 33 and hero.zone == 1 and not hero.mob_fight:
        await update.message.reply_text("Можно войти в пустошь где жизнь это цирк🤡🤡🤡", reply_markup=menu_clown())

    if hero.km in rad_zones and not hero.mob_fight and hero.zone in [0, 1]:
        if hero.zone == 1:
            await update.message.reply_text("Можно выйти из радиоактивной пустоши", reply_markup=menu_rad_quit())
        else:
            await update.message.reply_text("Можно войти в радиактивную пустошь", reply_markup=menu_rad())

    # await upd_hero_db(async_session, hero)


async def comm_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg_txt = update.message.text
    logger.info(update.effective_chat.first_name + "  " + msg_txt)
    hero = await get_hero(update)
    data = ""
    if "/savebase" == msg_txt:
        for k in all_data:
            h = all_data[k][0]
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
    elif "/tophp" in msg_txt:
        def sortf(e):
            return e.max_hp

        all = await get_hero_db(async_session)
        all.sort(reverse=True, key=sortf)
        p = k = 0
        for h in all:
            if h.id == hero.base_id:
                p = k
            if 5 > k or k > len(all) - 5:
                data += f"{k+1}. {h.name} || {h.max_hp}\n"
            if k == 5:
                data += "------------\n"
            k += 1
        data += f"\n{p+1}. {hero.name} || {hero.max_hp}\n"

    elif "/topkm" in msg_txt:
        def sortf(e):
            return e.all_km

        all = await get_hero_db(async_session)
        all.sort(reverse=True, key=sortf)
        p = k = 0
        for h in all:
            if h.id == hero.base_id:
                p = k
            if 5 > k or k > len(all) - 5:
                data += f"{k+1}. {h.name} || {h.all_km}\n"
            if k == 5:
                data += "------------\n"
            k += 1
        data += f"\n{p+1}. {hero.name} || {hero.all_km}\n"


    elif "/topcoins" in msg_txt:
        def sortf(e):
            return e.coins
        all = await get_hero_db(async_session)
        all.sort(reverse=True, key=sortf)
        p = k = 0
        for h in all:
            if h.id == hero.base_id:
                p = k
            if 5 > k or k > len(all) - 5:
                data += f"{k+1}. {h.name} || {h.coins}\n"
            if k == 5:
                data += "------------\n"
            k += 1
        data += f"\n{p+1}. {hero.name} || {hero.coins}\n"

    elif "/topbm" in msg_txt:
        def sortf(e):
            return e.max_hp + e.force + e.accuracy + e.luck + e.dexterity + e.charisma
        all = await get_hero_db(async_session)
        all.sort(reverse=True, key=sortf)
        p = k = 0
        for h in all:
            if h.id == hero.base_id:
                p = k
            if 5 > k or k > len(all) - 5:
                data += f"{k+1}. {h.name} || {h.max_hp + h.force + h.accuracy + h.luck + h.dexterity + h.charisma}\n"
            if k == 5:
                data += "------------\n"
            k += 1
        data += f"\n{p+1}. {hero.name} || {hero.max_hp + hero.force + hero.accuracy + hero.luck + hero.dexterity + hero.charisma}\n"

    # elif "/cheatw" in msg_txt:
    #    hero.stock.equip[armor_all[0][6].get_code()] = copy.copy(armor_all[0][6])
    #elif "/gokm" in msg_txt:
    #    x = int(msg_txt.replace("/gokm", ""))
    #    hero.km = x
    # elif "/msgall" in msg_txt:
    #     msg = msg_txt.replace("/msgall", "")
    #     for h in all_data:
    #         hero_h = all_data[h][0]
    #         if hero_h.id != hero.id:
    #             chat = all_data[h][1]
    #             chat.send_message(msg)
    elif "/cheatgg" in msg_txt:
        x = int(msg_txt.replace("/cheatgg", ""))
        # for i in range(0, 3):
        #    hero.stock.add_item(armor_all[i][7])
        # hero.stock.add_item(weapons_all[10])
        hero.coins = 1000
        hero.materials = 0
        hero.hp = x
        hero.max_hp = x
        hero.force = x
        hero.luck = x
        hero.dexterity = x
        hero.accuracy = x
        hero.charisma = x
    elif msg_txt == "/mystock":
        data = hero.stock.get_data()
    elif msg_txt == "/food":
        data = hero.stock.print_stuff(1)
    elif msg_txt == "/buff":
        data = hero.stock.print_stuff(2)
    elif "/ustf_" in msg_txt:
        code = int(msg_txt.replace("/ustf_", ""))
        data_ = hero.stock.use_stuff(code, hero)
        await menu_sel(update, hero, data_)

    elif "/drop" == msg_txt:
        data = hero.stock.get_delete()

    elif "/drw_" in msg_txt or "/dra_" in msg_txt:
        i = msg_txt.replace("/drw_", "").replace("/dra_", "")
        if hero.stock.equip.get(i, None):
            data = f"вы уверены что хотите удалить?{hero.stock.equip.get(i).name}\n"
            i_new = msg_txt.replace("/drw_", "/drww_").replace("/dra_", "/draa_")
            data += i_new
        else:
            data = "ошибка удаления\n"
    elif "/drww_" in msg_txt or "/draa_" in msg_txt:
        i = msg_txt.replace("/drww_", "").replace("/draa_", "")
        i_del = hero.stock.equip.pop(i)
        data = f"удалено {i_del.name}"
    elif "/eqw_" in msg_txt:
        w = msg_txt.replace("/eqw_", "")
        wp = hero.stock.equip.get(w, None)
        data_ = "ошибка"
        if wp:
            weapon = hero.stock.equip.pop(w)
            if hero.weapon:
                hero.stock.add_item(hero.weapon)
            hero.weapon = copy.copy(weapon)
            hero.weapon.use = 1
            data_ = hero.stock.get_data()
        await menu_sel(update, hero, data_)
    elif "/eqa_" in msg_txt:
        a = msg_txt.replace("/eqa_", "")
        ap = hero.stock.equip.get(a, None)
        data_ = "ошибка"
        if ap:
            i = int(a.split('t')[0])
            arm = hero.stock.equip.pop(a)
            if hero.armor[i]:
                hero.stock.add_item(hero.armor[i])

            hero.armor[i] = copy.copy(arm)
            hero.armor[i].use = 1
            data_ = hero.stock.get_data()
        await menu_sel(update, hero, data_)

    elif "/sw_" in msg_txt and hero.km == 0:
        w = msg_txt.replace("/sw_", "")
        wp = hero.stock.equip.get(w, None)
        if wp:
            w = hero.stock.equip.pop(w)
            hero.materials += w.calc_cost()
            out = f"📦×{hero.materials}\n"
            out += hero.stock.get_data_lombard()
            await update.message.reply_text(out, reply_markup=menu_lomb())
    elif "/sa_" in msg_txt and hero.km == 0:
        a = msg_txt.replace("/sa_", "")
        ap = hero.stock.equip.get(a, None)
        if ap:
            a = hero.stock.equip.pop(a)
            hero.materials += a.calc_cost()
            out = f"📦×{hero.materials}\n"
            out += hero.stock.get_data_lombard()
            await update.message.reply_text(out, reply_markup=menu_lomb())
    elif "/bw_" in msg_txt and hero.km == 0:
        if len(hero.stock.equip) >= hero.stock.MAX_EQUIP:
            data = "рюкзак полон"
        else:
            weapon_dmg = msg_txt.replace("/bw_", "")
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
                    data = f"вы купили {buy_weapon.name}"
                else:
                    data = "не хватило денег для покупки"
    elif "/ba_" in msg_txt and hero.km == 0:
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
                    data = f"вы купили {buy_arm.name}"
                else:
                    data = "не хватило денег для покупки"
    elif "/module" in msg_txt and hero.km == 0:
        i_mod = msg_txt.replace("/module", "")
        if i_mod in list('123456'):
            data = hero.activate_module(int(i_mod))
    elif "/buy_dr_1" == msg_txt and hero.km == 0:
        if hero.coins > 200000:
            hero.drone = copy.copy(all_drones[0])
            hero.coins -= 200000
            data = "вы купили дрона!"
        else:
            data = "не хватает крышек((("
    elif "/dzen" == msg_txt and hero.km == 30 and hero.zone == 1:
        data = f"Вы отправили 🕳{hero.coins} в дзен\n"
        hero.dzen += hero.coins
        hero.coins = 0
        data += f"Набрано 🕳{hero.get_in_dzen()} из 🕳{hero.get_coins_to_dzen()}\n"
    elif "/mobs" == msg_txt:
        if hero.mobs:
            data = "Мобы в команде:\n"
            for m in hero.mobs:
                data+= f"{m.name}\n"

    if data != "":
        if hero.in_dange <= 0:
            await update.message.reply_text(data, reply_markup=menu_pip())
        else:
            await update.message.reply_text(data, reply_markup=menu_go_dange())


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6292699351:AAFvNZB5A11o0unUoBSmteO9K4JY6hnmC54").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("me", me_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_msg))
    application.add_handler(MessageHandler(filters.COMMAND, comm_msg))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
