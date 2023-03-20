from telegram import InlineKeyboardButton, ReplyKeyboardMarkup


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
            InlineKeyboardButton("📙Дневник")
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_camp():
    keyboard = [
        [
            InlineKeyboardButton("📟Пип-бой"),
            InlineKeyboardButton("💤Отдохнуть"),
            #InlineKeyboardButton("💰Ломбард"),
        ],
        [
            InlineKeyboardButton("👣Пустошь"),
            InlineKeyboardButton("🎓Обучение")
        ],
        #[
            #InlineKeyboardButton("👓Инженер"),
            #InlineKeyboardButton("🏚Торгаш")
        #]
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
            InlineKeyboardButton("⬅️Назад")
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup