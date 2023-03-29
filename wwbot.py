#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position


import logging
import random
import copy
from db.db_process import *
from hero import *
from db.base import *
from stock import Stock, used_items
from armor import Armor, armor_all
from weapon import Weapon, weapons_all
from mob import *
from menu import *
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
            hero.name = update.effective_chat.first_name
            hero.weapon = copy.copy(weapons_all[0])
            hero.weapon.use = 1
            hero.armor = []
            hero.armor.append(copy.copy(armor_all[0][0]))
            hero.armor.append(copy.copy(armor_all[1][0]))
            hero.armor.append(copy.copy(armor_all[2][0]))
            await add_hero_db(async_session, hero)
            await add_hero_weapon_db(async_session, hero)
            await add_hero_armor_db(async_session, hero)
        else:
            hero_db = db_hero_fetch[0]
            db_hero_wp = await get_hero_weapon_db(async_session, hero_db)
            hero.from_db(hero_db)
            for iw in range(0, len(db_hero_wp)):
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

            db_hero_itms = await get_hero_items_db(async_session, hero_db)
            if len(db_hero_itms):
                for it in db_hero_itms:
                    hero.stock.used_stuff[it.index] = it.count

        all_data[update.effective_user.id] = [hero, update.effective_chat]
        return hero
    else:
        return rslt[0]


async def me_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    hero = await get_hero(update)
    if hero.mob_fight:
        await update.message.reply_text("на вас напал моб {0}".format(hero.mob_fight.name), reply_markup=menu_attack())
    else:
        await update.message.reply_text(hero.return_data(), reply_markup=menu_pip())


async def text_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    hero = await get_hero(update)
    msg_txt = update.message.text
    if hero.km != 0:
        if hero.weapon.life < 5:
            await update.message.reply_text("⭐️⚡️Внимание, оружие {0} скоро сломается!⭐️⚡️".format(hero.weapon.name))
        for ar in hero.armor:
            if ar and ar.life < 5:
                await update.message.reply_text("⭐️⚡️Внимание, броня {0} скоро сломается!⭐️⚡️".format(ar.name))

    if hero.km == 0:
        use_10x = 1
        i = 0
        if '*' in msg_txt:
            msg_txt = msg_txt.replace('*', '')
            use_10x = 10
        if msg_txt == "💪Сила":
            while i < use_10x:
                if hero.coins >= hero.calc_cost(hero.force):
                    hero.coins -= hero.calc_cost(hero.force)
                    hero.force += 1
                i += 1
            if use_10x == 1:
                await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())
            else:
                await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn_x10())

        elif msg_txt == "🎯Меткость":
            while i < use_10x:
                if hero.coins >= hero.calc_cost(hero.accuracy):
                    hero.coins -= hero.calc_cost(hero.accuracy)
                    hero.accuracy += 1
                i += 1
            if use_10x == 1:
                await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())
            else:
                await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn_x10())

        elif msg_txt == "🤸🏽‍♂️Ловкость":
            while i < use_10x:
                if hero.coins >= hero.calc_cost(hero.dexterity):
                    hero.coins -= hero.calc_cost(hero.dexterity)
                    hero.dexterity += 1
                i += 1
            if use_10x == 1:
                await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())
            else:
                await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn_x10())

        elif msg_txt == "❤️Живучесть":
            while i < use_10x:
                if hero.coins >= hero.calc_cost(hero.max_hp):
                    hero.coins -= hero.calc_cost(hero.max_hp)
                    hero.max_hp += 1
                    hero.hp += 1
                i += 1
            if use_10x == 1:
                await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())
            else:
                await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn_x10())
        elif msg_txt == "🗣Харизма":
            while i < use_10x:
                if hero.coins >= 10 * hero.charisma:
                    hero.coins -= 10 * hero.charisma
                    hero.charisma += 1
                i += 1
            if use_10x == 1:
                await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())
            else:
                await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn_x10())
        elif msg_txt == "👼Удача":
            while i < use_10x:
                if hero.coins >= hero.calc_cost(hero.luck):
                    hero.coins -= hero.calc_cost(hero.luck)
                    hero.luck += 1
                i += 1
            if use_10x == 1:
                await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())
            else:
                await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn_x10())
        elif msg_txt == "💤Отдохнуть" and hero.hp < hero.max_hp:
            if hero.coins < hero.max_hp:
                await update.message.reply_text(
                    "нужно {0} крышек, вы нищий и не можете отдохнуть\n".format(hero.max_hp), reply_markup=menu_camp())
            else:
                hero.hp = hero.max_hp
                hero.hungry = 0
                hero.coins -= hero.max_hp
                await update.message.reply_text("вы отдохнули")
                await update.message.reply_text(hero.return_data(), reply_markup=menu_camp())
        elif msg_txt == "💰Ломбард":
            out = "📦×{0}\n".format(hero.materials)
            out += hero.stock.get_data_lombard()
            await update.message.reply_text(out, reply_markup=menu_lomb())
        elif msg_txt == "🏚Торгаш":
            out = "🕳×{0}\n".format(hero.coins)
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
            out = "📦×{0}\n".format(hero.materials)
            out += hero.stock.get_data_lombard()
            await update.message.reply_text(out, reply_markup=menu_lomb())
        elif msg_txt == "Продать 1/2 коробок":
            hero.coins += round(hero.materials / 20)
            hero.materials = round(hero.materials / 2)
            out = "📦×{0}\n".format(hero.materials)
            out += hero.stock.get_data_lombard()
            await update.message.reply_text(out, reply_markup=menu_lomb())
        elif msg_txt == "Продать 1/4 коробок":
            hero.coins += round(hero.materials / 40)
            hero.materials = round(hero.materials / 4)
            out = "📦×{0}\n".format(hero.materials)
            out += hero.stock.get_data_lombard()
            await update.message.reply_text(out, reply_markup=menu_lomb())
        elif msg_txt == "Продать 1/8 коробок":
            hero.coins += round(hero.materials / 80)
            hero.materials = round(hero.materials / 8)
            out = "📦×{0}\n".format(hero.materials)
            out += hero.stock.get_data_lombard()
            await update.message.reply_text(out, reply_markup=menu_lomb())
        elif msg_txt == "🎓Обучение":
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())
        elif msg_txt == "x10 навыков":
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn_x10())

    if hero.in_dange <= 0:
        if msg_txt == "🔥Зайти в данж" and hero.km in danges.keys() and hero.in_dange == 0:
            hero.mob_fight = danges[hero.km][0]
            hero.in_dange = 1
            await update.message.reply_text("на вас напал моб {0}".format(hero.mob_fight.name),
                                            reply_markup=menu_go_dange())
        elif hero.mob_fight and msg_txt != "⚔️Дать отпор":
            await update.message.reply_text("на вас напал моб {0}".format(hero.mob_fight.name),
                                            reply_markup=menu_attack())
        elif not hero.mob_fight and msg_txt == "⛺️В лагерь":
            hero.km = 0
            await update.message.reply_text(hero.return_data(), reply_markup=menu_camp())
        elif msg_txt == "📟Пип-бой":
            await update.message.reply_text(hero.return_data(), reply_markup=menu_pip())
        elif msg_txt == "🔪Напасть":
            for h in all_data:
                hero_h = all_data[h][0]

                if update.effective_user.id != h and hero_h.km == hero.km and hero_h.in_dange <= 0:
                    chat = all_data[h][1]
                    out = hero.attack_player(hero_h)
                    hdr1 = "Сражение с {0}\n".format(hero.name)
                    hdr2 = "Сражение с {0}\n".format(hero_h.name)
                    if hero_h.hp <= 0:
                        hero_h.died_hero()  # -10%
                        hero_h.coins -= round(hero_h.coins * 0.1)
                        hero.coins += round(hero_h.coins * 0.09)
                        await update.message.reply_text(hdr2 + out +
                                                        "Вы выиграли!!!\n получено: 🕳 {0}".format(
                                                            round(hero_h.coins * 0.09)),
                                                        reply_markup=menu_go())
                        await chat.send_message(hdr1 + out +
                                                "Вы проиграли:((((\n потеряно: 🕳 {0}".format(
                                                    round(hero_h.coins * 0.1)),
                                                reply_markup=menu_camp())
                    if hero.hp <= 0:
                        hero.died_hero()
                        hero.coins -= round(hero.coins * 0.1)
                        hero_h.coins += round(hero.coins * 0.09)
                        await update.message.reply_text(hdr2 + out +
                                                        "Вы лузер!!!!\n потеряно: 🕳 {0}".format(
                                                            round(hero.coins * 0.1)),
                                                        reply_markup=menu_camp())
                        await chat.send_message(
                            hdr1 + out + "Вы выиграли!!!\n получено: 🕳 {0}".format(round(hero.coins * 0.09)),
                            reply_markup=menu_go())
                    break
        elif msg_txt == "👣Пустошь":
            hero.go()
            header = hero.make_header()
            await update.message.reply_text(header + "вы отправились в пустошь", reply_markup=menu_go())
            if random.randint(0, 1):
                hero.select_mob()
                await update.message.reply_text("на вас напал моб {0}".format(hero.mob_fight.name),
                                                reply_markup=menu_attack())
        elif msg_txt == "⚔️Дать отпор":
            mob = hero.mob_fight
            if mob:
                res = hero.attack_mob(mob)
                hero.mob_fight = None
                if hero.km != 0:
                    await update.message.reply_text(res)
                    await update.message.reply_text(hero.make_header() + "вы в дороге", reply_markup=menu_go())
                else:
                    hero.hp = 1
                    await update.message.reply_text(res)
                    await update.message.reply_text(hero.return_data(), reply_markup=menu_camp())
            else:
                await update.message.reply_text(hero.return_data(), reply_markup=menu_pip())



        elif msg_txt == "👣Идти дaльше":
            hero.go()
            if hero.hungry <= 98:
                hero.hungry += 2
            else:
                hero.hp -= round(hero.max_hp / 5)
            if hero.hp > 0:
                if hero.hungry > 96:
                    await update.message.reply_text("⭐️⚡вы голодны, скоро начнете умирать⭐️⚡")
                header = hero.make_header()
                if hero.in_dange < 0:
                    hero.in_dange = 0
                if random.randint(0, 1):
                    hero.select_mob()
                    await update.message.reply_text(header + "на вас напал моб {0}".format(hero.mob_fight.name),
                                                    reply_markup=menu_attack())
                else:
                    await update.message.reply_text(header + "вы в дороге", reply_markup=menu_go())
            else:
                hero.hp = 1
                hero.km = 0
                await update.message.reply_text("⭐️⚡ты сдох от голода((((⭐️⚡", reply_markup=menu_camp())

        elif msg_txt == "⬅️Назад":
            if hero.km == 0:
                await update.message.reply_text(hero.return_data(), reply_markup=menu_camp())
            else:
                await update.message.reply_text("вы в дороге", reply_markup=menu_go())
    else:
        if msg_txt == "👣Дальше":
            if hero.in_dange >= len(danges[hero.km]):
                hero.mob_fight = None
                hero.in_dange = -1
                if hero.km == 10:
                    r = random.randint(0, 10)
                    logger.info(update.effective_chat.first_name + " dange {0}km {1}".format(hero.km, r))
                    if r == 1:
                        hero.stock.add_item(weapons_all[4])
                        await update.message.reply_text(hero.make_header()
                                                        + "вам выпало {0}".format(weapons_all[4].name),
                                                        reply_markup=menu_go())
                    else:
                        await update.message.reply_text(hero.make_header()
                                                        + "вам выпало нихуя",
                                                        reply_markup=menu_go())
                if hero.km == 20:
                    r = random.randint(0, 7)
                    logger.info(update.effective_chat.first_name + " dange {0}km {1}".format(hero.km, r))
                    if r == 2:
                        type = random.randint(0, 2)
                        hero.stock.add_item(armor_all[type][5])
                        await update.message.reply_text(hero.make_header()
                                                        + "вам выпало {0}".format(armor_all[type][5].name),
                                                        reply_markup=menu_go())
                    else:
                        await update.message.reply_text(hero.make_header()
                                                        + "вам выпало нихуя",
                                                        reply_markup=menu_go())
                if hero.km == 30:
                    r = random.randint(0, 6)
                    logger.info(update.effective_chat.first_name + " dange {0}km {1}".format(hero.km, r))
                    if r == 3:
                        name_w = ""
                        r = random.randint(0, 2)
                        if r in [0, 1]:
                            hero.stock.add_item(weapons_all[5])
                            name_w = weapons_all[5].name
                        else:
                            hero.stock.add_item(weapons_all[6])
                            name_w = weapons_all[6].name

                        await update.message.reply_text(hero.make_header()
                                                        + "вам выпало {0}".format(name_w),
                                                        reply_markup=menu_go())
                    else:
                        await update.message.reply_text(hero.make_header()
                                                        + "вам выпало нихуя",
                                                        reply_markup=menu_go())

                if hero.km == 35:
                    r = random.randint(0, 6)
                    logger.info(update.effective_chat.first_name + " dange {0}km {1}".format(hero.km, r))
                    if r == 3:
                        type = random.randint(0, 2)
                        hero.stock.add_item(armor_all[type][6])
                        name_w = armor_all[type][6].name
                        await update.message.reply_text(hero.make_header()
                                                        + "вам выпало {0}".format(name_w),
                                                        reply_markup=menu_go())
                    else:
                        await update.message.reply_text(hero.make_header()
                                                        + "вам выпало нихуя",
                                                        reply_markup=menu_go())

                if hero.km == 40:
                    r = random.randint(0, 6)
                    logger.info(update.effective_chat.first_name + " dange {0}km {1}".format(hero.km, r))
                    if r == 4:
                        type = random.randint(0, 2)
                        hero.stock.add_item(armor_all[type][7])
                        await update.message.reply_text(hero.make_header()
                                                        + "вам выпало {0}".format(armor_all[type][7].name),
                                                        reply_markup=menu_go())
                    else:
                        await update.message.reply_text(hero.make_header()
                                                        + "вам выпало нихуя",
                                                        reply_markup=menu_go())
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

    logger.info(update.effective_chat.first_name + "  {0}  {1}km".format(msg_txt, hero.km))

    if hero.in_dange == 0:
        if not hero.mob_fight and hero.km != 0 or msg_txt == "🔎Осмотреться":
            out = ""
            for h in all_data:
                hero_h = all_data[h][0]
                if update.effective_user.id != h and hero_h.km == hero.km:
                    out += "{0}\n".format(hero_h.name)

            if out != "":
                out = "возле вас игроки:\n" + out
                if hero.km != 0:
                    await update.message.reply_text(out, reply_markup=menu_pvp())
                else:
                    await update.message.reply_text(out, reply_markup=menu_camp())

    if hero.km in danges.keys() and not hero.mob_fight and hero.in_dange == 0:
        await update.message.reply_text("Перед вами вход в пещеру", reply_markup=menu_dange())

    # await upd_hero_db(async_session, hero)


async def comm_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg_txt = update.message.text
    logger.info(update.effective_chat.first_name + "  " + msg_txt)
    hero = await get_hero(update)
    data = ""
    if "/initbase" == msg_txt:
        await create_table_db(async_session)
    elif "/savebase" == msg_txt:
        for k in all_data:
            h = all_data[k][0]
            await upd_hero_db(async_session, h)
            await delete_hero_weapon_db(async_session, h)
            await add_hero_weapon_db(async_session, h)
            await delete_hero_armor_db(async_session, h)
            await add_hero_armor_db(async_session, h)
            await delete_hero_items_db(async_session, h)
            await add_hero_items_db(async_session, h)

    elif "/tophp" in msg_txt:
        def sortf(e):
            return e.max_hp
        all = await get_hero_db(async_session)
        all.sort(key = sortf)
        for h in all:
            data += "{0} || {1}\n".format(h.name, h.max_hp)

    elif "/topkm" in msg_txt:
        def sortf(e):
            return e.all_km
        all = await get_hero_db(async_session)
        all.sort(key=sortf)
        for h in all:
            data += "{0} || {1}\n".format(h.name, h.all_km)

    elif "/topcoins" in msg_txt:
        def sortf(e):
            return e.coins
        all = await get_hero_db(async_session)
        all.sort(key=sortf)
        for h in all:
            data += "{0} || {1}\n".format(h.name, h.coins)

    elif "/topbm" in msg_txt:
        def sortf(e):
            return e.max_hp + e.force + e.accuracy + e.luck + e.dexterity + e.charisma
        all = await get_hero_db(async_session)
        all.sort(key=sortf)
        for h in all:
            data += "{0} || {1}\n".format(h.name, h.max_hp + h.force + h.accuracy + h.luck + h.dexterity + h.charisma)

    elif "/cheatgg" in msg_txt:
        x = int(msg_txt.replace("/cheatgg", ""))
        hero.hp = x
        hero.max_hp = x
        hero.force = x
        hero.luck = x
        hero.dexterity = x
        hero.accuracy = x
        hero.charisma = x
        # for i in range(4, 6):
        #    hero.stock.equip[weapons_all[i].get_code()] = copy.copy(weapons_all[i])
        # for i in range(0, 3):
        #    hero.stock.equip[armor_all[i][5].get_code()] = copy.copy(armor_all[i][5])
    elif msg_txt == "/mystock":
        data = hero.stock.get_data()
    elif msg_txt == "/food":
        data = hero.stock.print_stuff(1)
    elif msg_txt == "/buff":
        data = hero.stock.print_stuff(2)
    elif "/ustf_" in msg_txt:
        code = int(msg_txt.replace("/ustf_", ""))
        data = hero.stock.use_stuff(code, hero)

    elif "/eqw_" in msg_txt:  # проверка кол-ва силы
        w = msg_txt.replace("/eqw_", "")
        wp = hero.stock.equip.get(w, None)
        if wp:
            weapon = hero.stock.equip.pop(w)
            if hero.weapon:
                code = hero.weapon.get_code()
                hero.weapon.use = 0
                hero.stock.equip[code] = copy.copy(hero.weapon)
            hero.weapon = copy.copy(weapon)
            hero.weapon.use = 1
            data = hero.stock.get_data()

    elif "/eqa_" in msg_txt:
        a = msg_txt.replace("/eqa_", "")
        ap = hero.stock.equip.get(a, None)
        if ap:
            i = int(a.split('t')[0])
            arm = hero.stock.equip.pop(a)
            if hero.armor[i]:
                code = hero.armor[i].get_code()
                hero.armor[i].use = 0
                hero.stock.equip[code] = copy.copy(hero.armor[i])

            hero.armor[i] = copy.copy(arm)
            hero.armor[i].use = 1
            data = hero.stock.get_data()

    elif "/sw_" in msg_txt and hero.km == 0:
        w = msg_txt.replace("/sw_", "")
        wp = hero.stock.equip.get(w, None)
        if wp:
            w = hero.stock.equip.pop(w)
            hero.materials += w.calc_cost()
            out = "📦×{0}\n".format(hero.materials)
            out += hero.stock.get_data_lombard()
            await update.message.reply_text(out, reply_markup=menu_lomb())
    elif "/sa_" in msg_txt and hero.km == 0:
        a = msg_txt.replace("/sa_", "")
        ap = hero.stock.equip.get(a, None)
        if ap:
            a = hero.stock.equip.pop(a)
            hero.materials += a.calc_cost()
            out = "📦×{0}\n".format(hero.materials)
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
                    data = "вы купили {0}".format(buy_weapon.name)
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
                    data = "вы купили {0}".format(buy_arm.name)
                else:
                    data = "не хватило денег для покупки"
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
