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


def menu_rad():
    keyboard = [
        [
            InlineKeyboardButton("👣Идти дaльше"),
            InlineKeyboardButton("⛺️В лагерь"),
        ],
        [
            InlineKeyboardButton("🔎Осмотреться"),
            InlineKeyboardButton("👣☢Рад-️Пустошь")
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_dange():
    keyboard = [
        [
            InlineKeyboardButton("🔥Зайти в данж"),
            InlineKeyboardButton("👣Идти дaльше")
        ],
        [
            InlineKeyboardButton("🔎Осмотреться"),
            InlineKeyboardButton("⛺️В лагерь"),
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_rad_quit():
    keyboard = [
        [
            InlineKeyboardButton("☢Покинуть Рад-️Пустошь☢"),
            InlineKeyboardButton("👣Идти дaльше")
        ],
        [
            InlineKeyboardButton("🔎Осмотреться"),
            InlineKeyboardButton("⛺️В лагерь"),
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_lomb():
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

def menu_attack():
    keyboard = [
        [
            InlineKeyboardButton("⚔️Дать отпор"),
            InlineKeyboardButton("🏃Дать деру")
        ],
        [
            InlineKeyboardButton("🔎Осмотреться")
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_go():
    keyboard = [
        [
            InlineKeyboardButton("📟Пип-бой"),
            InlineKeyboardButton("🔎Осмотреться"),
        ],
        [
            InlineKeyboardButton("👣Идти дaльше"),
            InlineKeyboardButton("⛺️В лагерь")
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_pvp():
    keyboard = [
        [
            InlineKeyboardButton("🔪Напасть"),
            InlineKeyboardButton("🔎Осмотреться"),
        ],
        [
            InlineKeyboardButton("👣Идти дaльше"),
            InlineKeyboardButton("⛺️В лагерь")
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_pip():
    keyboard = [
        [
            InlineKeyboardButton("🎒Рюкзак"),
            InlineKeyboardButton("🔎Осмотреться"),
        ],
        [
            InlineKeyboardButton("⬅️Назад"),
            #InlineKeyboardButton("📙Дневник"),
            InlineKeyboardButton("🔝Топы")
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_camp():
    keyboard = [
        [
            InlineKeyboardButton("📟Пип-бой"),
            InlineKeyboardButton("💤Отдохнуть"),
        ],
        [

            InlineKeyboardButton("💰Ломбард"),
            #InlineKeyboardButton("👓Инженер"),
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

def menu_learn_x10():
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

def menu_learn():
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

