#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position


import logging
import random
import copy
from hero import Hero
from stock import Stock
from weapon import *
from mob import *
from menu import *

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


def get_hero(update):
    rslt = all_data.get(update.effective_user.id, None)
    if not rslt:
        hero = Hero()
        stock = Stock()
        for i in range(0, 5):
            stock.weapons[str(weapons_all[i].dmg)+ "z0"] = weapons_all[i]
        hero.stock = stock
        hero.id = update.effective_user.id
        hero.name = Hero.generate_name()
        hero.weapon = copy.copy(weapons_all[0])
        hero.weapon.z = 1
        all_data[update.effective_user.id] = [hero, update.effective_chat]
        return hero
    else:
        return rslt[0]


async def me_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    hero = get_hero(update)
    if hero.mob_fight:
        await update.message.reply_text("на вас напал моб {0}".format(hero.mob_fight.name), reply_markup=menu_attack())
    else:
        await update.message.reply_text(hero.return_data(), reply_markup=menu_pip())


async def text_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    hero = get_hero(update)

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
                hero.coins -= hero.calc_cost(hero.force)
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
                await update.message.reply_text("нужно {0} крышек, вы нищий и не можете отдохнуть\n".format(hero.max_hp), reply_markup=menu_camp())
            else:
                hero.hp = hero.max_hp
                hero.coins -= hero.max_hp
                await update.message.reply_text("вы отдохнули")
                await update.message.reply_text(hero.return_data(), reply_markup=menu_camp())

    if hero.mob_fight and update.message.text != "⚔️Дать отпор":
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
        header = hero.make_header()
        await update.message.reply_text(header + "вы отправились в пустошь", reply_markup=menu_go())
        if random.randint(0, 1):
            hero.select_mob()
            await update.message.reply_text("на вас напал моб {0}".format(hero.mob_fight.name), reply_markup=menu_attack())
    elif update.message.text == "⚔️Дать отпор":
        mob = hero.mob_fight
        if mob:
            hero.km += 1
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
        header = hero.make_header()
        if random.randint(0, 1):
            hero.select_mob()
            await update.message.reply_text(header + "на вас напал моб{0}".format(hero.mob_fight.name), reply_markup=menu_attack())
        else:
            await update.message.reply_text(header + "вы в дороге", reply_markup=menu_go())
    elif update.message.text == "⬅️Назад":
        if hero.km == 0:
            await update.message.reply_text(hero.return_data(), reply_markup=menu_camp())
        else:
            await update.message.reply_text("вы в дороге", reply_markup=menu_go())
    elif update.message.text == "🎓Обучение":
        if hero.km == 0:
            await update.message.reply_text(hero.learn_data(), reply_markup=menu_learn())
        else:
            await update.message.reply_text("вы в дороге", reply_markup=menu_go())
    elif update.message.text == "🎒Рюкзак":
        await update.message.reply_text(hero.stock.get_data(), reply_markup=menu_pip())
    else:
        logger.info(str(update.effective_user.id) + "  " + update.message.text)

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


async def comm_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(str(update.effective_user.id) + "  " + update.message.text)
    hero = get_hero(update)
    if update.message.text == "/cheat1":
        hero.luck = 1500
        hero.dexterity = 2000
    elif update.message.text == "/mystock":
        await update.message.reply_text(hero.stock.get_data(), reply_markup=menu_pip())
    elif "/eqw_" in update.message.text:
        w = update.message.text.replace("/eqw_", "")
        wp = hero.stock.weapons.get(w, None)
        if wp:
            hero.stock.weapons["{0}z{1}".format(hero.weapon.dmg, hero.weapon.z)] = copy.copy(hero.weapon)
            hero.weapon = hero.stock.weapons.pop(w)
            await update.message.reply_text(hero.return_data(), reply_markup=menu_pip())


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
