#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position


import logging
import random
import copy
import asyncio
from hero import *
from db.base import *
from stock import Stock
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
        stock.equip = OrderedDict()
        if not len(db_hero_fetch):
            #for i in range(0, 5):
            #    stock.equip[weapons_all[i].get_code()] = copy.copy(weapons_all[i])
            #for i in range(0, 3):
            #    stock.equip[armor_all[i][6].get_code()] = copy.copy(armor_all[i][6])

            hero.id = str(update.effective_user.id)
            hero.name = update.effective_chat.first_name
            hero.weapon = copy.copy(weapons_all[0])
            hero.armor = []
            hero.armor.append(copy.copy(armor_all[0][0]))
            hero.armor.append(copy.copy(armor_all[1][0]))
            hero.armor.append(copy.copy(armor_all[2][0]))
            await add_hero_db(async_session, hero)
        else:
            hero_db = db_hero_fetch[0]
            hero.from_db(hero_db)
            hero.weapon = copy.copy(weapons_all[0])
            hero.weapon.z = 1
            hero.armor = []
            hero.armor.append(copy.copy(armor_all[0][0]))
            hero.armor.append(copy.copy(armor_all[1][0]))
            hero.armor.append(copy.copy(armor_all[2][0]))
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
    if hero.km == 0:
        if update.message.text == "💪Сила":
            if hero.coins >= hero.calc_cost(hero.force):
                hero.coins -= hero.calc_cost(hero.force)
                hero.force += 1
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())

        elif update.message.text == "🎯Меткость":
            if hero.coins >= hero.calc_cost(hero.accuracy):
                hero.coins -= hero.calc_cost(hero.accuracy)
                hero.accuracy += 1
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())

        elif update.message.text == "🤸🏽‍♂️Ловкость":
            if hero.coins >= hero.calc_cost(hero.dexterity):
                hero.coins -= hero.calc_cost(hero.dexterity)
                hero.dexterity += 1
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())

        elif update.message.text == "❤️Живучесть":
            if hero.coins >= hero.calc_cost(hero.max_hp):
                hero.coins -= hero.calc_cost(hero.max_hp)
                hero.max_hp += 1
                hero.hp += 1
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())
        elif update.message.text == "🗣Харизма":
            if hero.coins >= 10 * hero.charisma:
                hero.coins -= 10 * hero.charisma
                hero.charisma += 1
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())
        elif update.message.text == "👼Удача":
            if hero.coins >= hero.calc_cost(hero.luck):
                hero.coins -= hero.calc_cost(hero.luck)
                hero.luck += 1
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())
        elif update.message.text == "💤Отдохнуть" and hero.hp < hero.max_hp:
            if hero.coins < hero.max_hp:
                await update.message.reply_text(
                    "нужно {0} крышек, вы нищий и не можете отдохнуть\n".format(hero.max_hp), reply_markup=menu_camp())
            else:
                hero.hp = hero.max_hp
                hero.coins -= hero.max_hp
                await update.message.reply_text("вы отдохнули")
                await update.message.reply_text(hero.return_data(), reply_markup=menu_camp())
        elif update.message.text == "💰Ломбард":
            out = "📦×{0}\n".format(hero.materials)
            out += hero.stock.get_data_lombard()
            await update.message.reply_text(out, reply_markup=menu_lomb())
        elif update.message.text == "🏚Торгаш":
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
        elif update.message.text == "Продать все коробки":
            hero.coins += round(hero.materials/10)
            hero.materials = 0
            out = "📦×{0}\n".format(hero.materials)
            out += hero.stock.get_data_lombard()
            await update.message.reply_text(out, reply_markup=menu_lomb())
        elif update.message.text == "Продать 1/2 коробок":
            hero.coins += round(hero.materials / 20)
            hero.materials = round(hero.materials / 2)
            out = "📦×{0}\n".format(hero.materials)
            out += hero.stock.get_data_lombard()
            await update.message.reply_text(out, reply_markup=menu_lomb())
        elif update.message.text == "Продать 1/4 коробок":
            hero.coins += round(hero.materials / 40)
            hero.materials = round(hero.materials / 4)
            out = "📦×{0}\n".format(hero.materials)
            out += hero.stock.get_data_lombard()
            await update.message.reply_text(out, reply_markup=menu_lomb())
        elif update.message.text == "Продать 1/8 коробок":
            hero.coins += round(hero.materials / 80)
            hero.materials = round(hero.materials / 8)
            out = "📦×{0}\n".format(hero.materials)
            out += hero.stock.get_data_lombard()
            await update.message.reply_text(out, reply_markup=menu_lomb())
        elif update.message.text == "🎓Обучение":
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())

    if hero.in_dange <= 0:
        if update.message.text == "🔥Зайти в данж" and hero.km in [10, 20] and hero.in_dange == 0:
            hero.mob_fight = danges[hero.km][0]
            hero.in_dange = 1
            await update.message.reply_text("на вас напал моб {0}".format(hero.mob_fight.name),
                                            reply_markup=menu_go_dange())
        elif hero.mob_fight and update.message.text != "⚔️Дать отпор":
            await update.message.reply_text("на вас напал моб {0}".format(hero.mob_fight.name), reply_markup=menu_attack())
        elif not hero.mob_fight and update.message.text == "⛺️В лагерь":
            hero.km = 0
            await update.message.reply_text(hero.return_data(), reply_markup=menu_camp())
        elif update.message.text == "📟Пип-бой":
            await update.message.reply_text(hero.return_data(), reply_markup=menu_pip())
        elif update.message.text == "🔪Напасть":
            for h in all_data:
                hero_h = all_data[h][0]

                if update.effective_user.id != h and hero_h.km == hero.km:
                    chat = all_data[h][1]
                    out = hero.attack_player(hero_h)
                    hdr1 = "Сражение с {0}\n".format(hero.name)
                    hdr2 = "Сражение с {0}\n".format(hero_h.name)
                    if hero_h.hp <= 0:
                        hero_h.died_hero()
                        await update.message.reply_text(hdr2 + out + "Вы выиграли!!!", reply_markup=menu_go())
                        await chat.send_message(hdr1 + out + "Вы проиграли:((((", reply_markup=menu_camp())
                    if hero.hp <= 0:
                        hero.died_hero()
                        await update.message.reply_text(hdr2 + out + "Вы лузер!!!!", reply_markup=menu_camp())
                        await chat.send_message(hdr1 + out + "Вы выиграли!!!", reply_markup=menu_go())
                    break
        elif update.message.text == "👣Пустошь":
            hero.km += 1
            hero.all_km += 1
            header = hero.make_header()
            await update.message.reply_text(header + "вы отправились в пустошь", reply_markup=menu_go())
            if random.randint(0, 1):
                hero.select_mob()
                await update.message.reply_text("на вас напал моб {0}".format(hero.mob_fight.name),
                                                reply_markup=menu_attack())
        elif update.message.text == "⚔️Дать отпор":
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

        elif update.message.text == "👣Идти дaльше":
            hero.km += 1
            hero.all_km += 1
            header = hero.make_header()
            if hero.in_dange < 0:
                hero.in_dange = 0
            if random.randint(0, 1):
                hero.select_mob()
                await update.message.reply_text(header + "на вас напал моб {0}".format(hero.mob_fight.name),
                                                reply_markup=menu_attack())
            else:
                await update.message.reply_text(header + "вы в дороге", reply_markup=menu_go())
        elif update.message.text == "⬅️Назад":
            if hero.km == 0:
                await update.message.reply_text(hero.return_data(), reply_markup=menu_camp())
            else:
                await update.message.reply_text("вы в дороге", reply_markup=menu_go())
    else:
        if update.message.text == "👣Дальше":
            if hero.in_dange >= len(danges[hero.km]):
                hero.mob_fight = None
                hero.in_dange = -1
                if hero.km == 10:
                    if random.randint(0, 10) == 1:
                        hero.stock.equip[weapons_all[4].get_code()] = copy.copy(weapons_all[4])
                        await update.message.reply_text(hero.make_header()
                                                        + "вам выпало {0}".format(weapons_all[4].name), reply_markup=menu_go())
                    else:
                        await update.message.reply_text(hero.make_header()
                                                        + "вам выпало нихуя",
                                                        reply_markup=menu_go())
                if hero.km == 20:
                    if random.randint(0, 10) == 1:
                        hero.stock.equip[armor_all[0][5].get_code()] = copy.copy(armor_all[0][5])
                        await update.message.reply_text(hero.make_header()
                                                        + "вам выпало {0}".format(armor_all[0][5].name),
                                                        reply_markup=menu_go())
                    else:
                        await update.message.reply_text(hero.make_header()
                                                        + "вам выпало нихуя",
                                                        reply_markup=menu_go())

            else:
                mob = hero.mob_fight
                if mob:
                    res = hero.attack_mob(mob, True)
                    if hero.km != 0:
                        await update.message.reply_text(res)
                        await update.message.reply_text(hero.make_header() + "продолжаем идти", reply_markup=menu_go_dange())
                        hero.mob_fight = danges[hero.km][hero.in_dange]
                        hero.in_dange+=1
                    else:
                        hero.hp = 1
                        hero.mob_fight = None
                        hero.in_dange = 0
                        await update.message.reply_text(res)
                        await update.message.reply_text(hero.return_data(), reply_markup=menu_camp())

    if update.message.text == "🎒Рюкзак":
        if hero.in_dange <= 0:
            await update.message.reply_text(hero.stock.get_data(), reply_markup=menu_pip())
        else:
            await update.message.reply_text(hero.stock.get_data(), reply_markup=menu_go_dange())




    logger.info(update.effective_chat.first_name + "  " + update.message.text)

    if not hero.mob_fight and hero.km != 0 or update.message.text == "🔎Осмотреться":
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

    if hero.km in [10, 20] and not hero.mob_fight and hero.in_dange == 0:
        await update.message.reply_text("Перед вами вход в пещеру", reply_markup=menu_dange())

    #await upd_hero_db(async_session, hero)

async def comm_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(update.effective_chat.first_name + "  " + update.message.text)
    hero = await get_hero(update)
    if "/initbase" == update.message.text:
        await init_models()
    if "/savebase" == update.message.text:
        for k in all_data:
            h = all_data[k][0]
            await upd_hero_db(async_session, h)
            await add_hero_weapon_db(async_session, h, h.weapon, use=1)

    elif "/cheat" in update.message.text:
        x = int(update.message.text.replace("/cheat", ""))
        hero.hp = x*2
        hero.max_hp = x*2
        hero.force = x
        hero.luck = x
        hero.dexterity = x
        hero.accuracy = x
        hero.charisma = x
        l = len(weapons_all) - 1
        for i in range(0, 5):
            hero.stock.equip[weapons_all[l - i].get_code()] = copy.copy(weapons_all[l - i])
        for i in range(0, 3):
            l = len(armor_all[i])-1
            hero.stock.equip[armor_all[i][l].get_code()] = copy.copy(armor_all[i][l])
    elif update.message.text == "/mystock":
        await update.message.reply_text(hero.stock.get_data(), reply_markup=menu_pip())
    elif "/eqw_" in update.message.text: #проверка кол-ва силы
        w = update.message.text.replace("/eqw_", "")
        wp = hero.stock.equip.get(w, None)
        if wp:
            if hero.weapon:
                hero.stock.equip[hero.weapon.get_code()] = copy.copy(hero.weapon)
            hero.weapon = hero.stock.equip.pop(w)
            await update.message.reply_text(hero.return_data(), reply_markup=menu_pip())
    elif "/eqa_" in update.message.text:
        a = update.message.text.replace("/eqa_", "")
        ap = hero.stock.equip.get(a, None)
        if ap:
            i = int(a[0])
            if hero.armor[i]:
                hero.stock.equip[hero.armor[i].get_code()] = copy.copy(hero.armor[i])
            hero.armor[i] = hero.stock.equip.pop(a)
            await update.message.reply_text(hero.return_data(), reply_markup=menu_pip())
    elif "/sw_" in update.message.text and hero.km == 0:
        w = update.message.text.replace("/sw_", "")
        wp = hero.stock.equip.get(w, None)
        if wp:
            w = hero.stock.equip.pop(w)
            hero.materials += w.calc_cost()
            out = "📦×{0}\n".format(hero.materials)
            out += hero.stock.get_data_lombard()
            await update.message.reply_text(out, reply_markup=menu_lomb())
    elif "/sa_" in update.message.text and hero.km == 0:
        a = update.message.text.replace("/sa_", "")
        ap = hero.stock.equip.get(a, None)
        if ap:
            a = hero.stock.equip.pop(a)
            hero.materials += a.calc_cost()
            out = "📦×{0}\n".format(hero.materials)
            out += hero.stock.get_data_lombard()
            await update.message.reply_text(out, reply_markup=menu_lomb())
    elif "/bw_" in update.message.text and hero.km == 0:
        if len(hero.stock.equip) >= hero.stock.MAX_EQUIP:
            await update.message.reply_text("рюкзак полон", reply_markup=menu_pip())
        else:
            weapon_dmg = update.message.text.replace("/bw_", "")
            buy_weapon = None
            z = 0
            for item_key in hero.stock.equip:
                if isinstance(hero.stock.equip[item_key], Weapon) and str(hero.stock.equip[item_key].dmg) == weapon_dmg:
                    hero.stock.equip[item_key].z = z
                    buy_weapon = hero.stock.equip[item_key]
                    z += 1

            if not buy_weapon:
                for weapon in weapons_all:
                    if str(weapon.dmg) == weapon_dmg:
                        buy_weapon = weapon
                        break

            if buy_weapon:
                buy_weapon = copy.copy(buy_weapon)
                buy_weapon.life = buy_weapon.max_life
                cost = buy_weapon.calc_cost()
                buy_weapon.z = z
                if cost <= hero.coins:
                    hero.stock.equip[buy_weapon.get_code()] = buy_weapon
                    hero.coins -= cost
                    await update.message.reply_text("вы купили {0}".format(buy_weapon.name), reply_markup=menu_pip())
                else:
                    await update.message.reply_text("не хватило денег для покупки", reply_markup=menu_pip())
    elif "/ba_" in update.message.text and hero.km == 0:
        if len(hero.stock.equip) >= hero.stock.MAX_EQUIP:
            await update.message.reply_text("рюкзак полон", reply_markup=menu_pip())
        else:
            buy_arm_code = update.message.text.replace("/ba_", "").split('t')
            buy_arm_type = buy_arm_code[0]
            buy_arm_val = buy_arm_code[1]
            buy_arm = None
            z = 0
            for item in hero.stock.equip:
                if isinstance(hero.stock.equip[item], Armor) \
                        and str(hero.stock.equip[item].arm) == buy_arm_val\
                        and str(hero.stock.equip[item].type) == buy_arm_type:
                    hero.stock.equip[item].z = z
                    buy_arm = hero.stock.equip[item]
                    z += 1

            if not buy_arm:
                if buy_arm_type in ['0', '1', '2']:
                    for ar in armor_all[int(buy_arm_type)]:
                        if str(ar.arm) == buy_arm_val:
                            buy_arm = ar
                            break
            if buy_arm:
                buy_arm = copy.copy(buy_arm)
                buy_arm.life = buy_arm.max_life
                cost = buy_arm.calc_cost()
                buy_arm.z = z
                if cost <= hero.coins:
                    hero.stock.equip[buy_arm.get_code()] = buy_arm
                    hero.coins -= cost
                    await update.message.reply_text("вы купили {0}".format(buy_arm.name), reply_markup=menu_pip())
                else:
                    await update.message.reply_text("не хватило денег для покупки", reply_markup=menu_pip())
    #await upd_hero_db(async_session, hero)


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
