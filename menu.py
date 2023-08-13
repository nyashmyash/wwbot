from telegram import InlineKeyboardButton, ReplyKeyboardMarkup


def menu_go_dange():
    keyboard = [
        [
            InlineKeyboardButton("👣Дальше"),
        ],
        [
            InlineKeyboardButton("🎒Рюкзак"),
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_rad(add_fight: bool = False) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("👣☢Рад-️Пустошь"),
            InlineKeyboardButton("👣Идти дальше"),

        ],
        [
            InlineKeyboardButton("👣Идти к лагерю"),
            InlineKeyboardButton("⛺️В лагерь"),
            InlineKeyboardButton("📟Пип-бой"),
        ]
    ]
    if add_fight:
        keyboard[0].insert(0, InlineKeyboardButton("🔪Напасть"))
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_clown(add_fight: bool = False) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("👣️🎪 Зайти в блядский цирк🎪 ️"),
            InlineKeyboardButton("👣Идти дальше"),
        ],
        [
            InlineKeyboardButton("👣Идти к лагерю"),
            InlineKeyboardButton("⛺️В лагерь"),
            InlineKeyboardButton("📟Пип-бой"),
        ]
    ]
    if add_fight:
        keyboard[0].insert(0, InlineKeyboardButton("🔪Напасть"))

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_painkiller(add_fight: bool = False) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🔪️painkiller🔪️"),
            InlineKeyboardButton("👣Идти дальше"),
        ],
        [
            InlineKeyboardButton("👣Идти к лагерю"),
            InlineKeyboardButton("⛺️В лагерь"),
            InlineKeyboardButton("📟Пип-бой"),
        ]
    ]
    if add_fight:
        keyboard[0].insert(0, InlineKeyboardButton("🔪Напасть"))

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_dead(add_fight: bool = False) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("👣️☠️Пустошь смерти☠️"),
            InlineKeyboardButton("👣Идти дальше"),
        ],
        [
            InlineKeyboardButton("👣Идти к лагерю"),
            InlineKeyboardButton("⛺️В лагерь"),
            InlineKeyboardButton("📟Пип-бой"),
        ]
    ]
    if add_fight:
        keyboard[0].insert(0, InlineKeyboardButton("🔪Напасть"))
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_mk(add_fight: bool = False) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("👣️👹Смертельная арена👹"),
            InlineKeyboardButton("👣Идти дальше"),
        ],
        [
            InlineKeyboardButton("📟Пип-бой"),
        ]
    ]
    if add_fight:
        keyboard[0].insert(0, InlineKeyboardButton("🔪Напасть"))
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_necro(add_fight: bool = False) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("👣️💀Зона некронов"),
            InlineKeyboardButton("👣Идти дальше"),
        ],
        [
            InlineKeyboardButton("📟Пип-бой"),
        ]
    ]
    if add_fight:
        keyboard[0].insert(0, InlineKeyboardButton("🔪Напасть"))
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_necro_quit(add_fight: bool = False) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("️💀Покинуть пустошь некронов💀"),
            InlineKeyboardButton("👣Идти дальше")
        ],
        [
            InlineKeyboardButton("📟Пип-бой"),
        ]
    ]
    if add_fight:
        keyboard[0].insert(0, InlineKeyboardButton("🔪Напасть"))

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_dino(add_fight: bool = False) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("👣️Парк динозавров"),
            InlineKeyboardButton("👣Идти дальше"),
        ],
        [
            InlineKeyboardButton("👣Идти к лагерю"),
            InlineKeyboardButton("⛺️В лагерь"),
            InlineKeyboardButton("📟Пип-бой"),
        ]
    ]
    if add_fight:
        keyboard[0].insert(0, InlineKeyboardButton("🔪Напасть"))
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup

def menu_dange(add_fight: bool = False) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🔥Зайти в данж"),
            InlineKeyboardButton("👣Идти дальше")
        ],
        [
            InlineKeyboardButton("👣Идти к лагерю"),
            InlineKeyboardButton("⛺️В лагерь"),
            InlineKeyboardButton("📟Пип-бой")
        ]
    ]
    if add_fight:
        keyboard[0].insert(0, InlineKeyboardButton("🔪Напасть"))

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_rad_quit(add_fight: bool = False) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("☢Покинуть Рад-️Пустошь☢"),
            InlineKeyboardButton("👣Идти дальше")
        ],
        [
            InlineKeyboardButton("👣Идти к лагерю"),
            InlineKeyboardButton("⛺️В лагерь"),
            InlineKeyboardButton("📟Пип-бой"),
        ]
    ]
    if add_fight:
        keyboard[0].insert(0, InlineKeyboardButton("🔪Напасть"))

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_dead_quit(add_fight: bool = False) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("️☠Покинуть пустошь смерти☠"),
            InlineKeyboardButton("👣Идти дальше")
        ],
        [
            InlineKeyboardButton("📟Пип-бой"),
        ]
    ]
    if add_fight:
        keyboard[0].insert(0, InlineKeyboardButton("🔪Напасть"))

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_lomb() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("Продать все коробки"),
            InlineKeyboardButton("Продать 1/2 коробок")
        ],
        [
            InlineKeyboardButton("Продать 1/4 коробок"),
            InlineKeyboardButton("Продать 1/8 коробок"),
            InlineKeyboardButton("⬅️Назад"),
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_attack() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🏃Дать деру"),
            InlineKeyboardButton("⚔️Дать отпор")

        ],
        [
            InlineKeyboardButton("📟Пип-бой")
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_go(add_fight: bool = False) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("📟Пип-бой"),
            InlineKeyboardButton("👣Идти дальше"),
        ],
        [
            #InlineKeyboardButton("🔎Осмотреться"),
            InlineKeyboardButton("👣Идти к лагерю"),
            InlineKeyboardButton("⛺️В лагерь")
        ]
    ]
    if add_fight:
        keyboard[0].insert(0, InlineKeyboardButton("🔪Напасть"))

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_go_dead() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("📟Пип-бой"),
            InlineKeyboardButton("👣Идти дальше"),
        ],
        [
            InlineKeyboardButton("🔎Осмотреться"),
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_pvp() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🔪Напасть"),
            InlineKeyboardButton("👣Идти дальше"),
        ],
        [
            InlineKeyboardButton("📟Пип-бой"),
            InlineKeyboardButton("👣Идти к лагерю"),
            InlineKeyboardButton("⛺️В лагерь"),
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_pip() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🎒Рюкзак"),
            InlineKeyboardButton("🔎Осмотреться"),
        ],
        [
            InlineKeyboardButton("⬅️Назад"),
            # InlineKeyboardButton("📙Дневник"),
            InlineKeyboardButton("🔝Топы")
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_camp() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("📟Пип-бой"),
            InlineKeyboardButton("💤Отдохнуть"),
        ],
        [

            InlineKeyboardButton("💰Ломбард"),
            InlineKeyboardButton("👓Инженер"),
            InlineKeyboardButton("🎓Обучение")
        ],
        [
            InlineKeyboardButton("🏚Торгаш"),
            InlineKeyboardButton("👣Пустошь"),
            InlineKeyboardButton("👣☢Рад-️Пустошь"),
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_learn_x10() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("💪Сила*"),
            InlineKeyboardButton("🎯Меткость*"),
            InlineKeyboardButton("🤸🏽‍♂️Ловкость*"),
        ],
        [
            InlineKeyboardButton("❤️Живучесть*"),
            InlineKeyboardButton("🗣Харизма*"),
            InlineKeyboardButton("👼Удача*"),
        ],
        [
            InlineKeyboardButton("⬅️Назад"),
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_learn() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("💪Сила"),
            InlineKeyboardButton("🎯Меткость"),
            InlineKeyboardButton("🤸🏽‍♂️Ловкость"),
        ],
        [
            InlineKeyboardButton("❤️Живучесть"),
            InlineKeyboardButton("🗣Харизма"),
            InlineKeyboardButton("👼Удача"),
        ],
        [
            InlineKeyboardButton("⬅️Назад"),
            InlineKeyboardButton("x10 навыков")
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup
