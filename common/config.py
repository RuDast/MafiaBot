START_MESSAGE = ("<b>✨ Меню навигации ✨</b>\n"
         "<i>AYSSAU corp.</i>")

ROLES_MESSAGE = ("<b>🫂 Доступные роли</b>\n"
                 "role1\n"
                 "role2\n"
                 "...\n"
                 "roleN, N ∊ N")

RULES_MESSAGE = ("<i><u>📄 Правила игры <b>\"Мафия\"</b></u></i>\n"
         "📌<b>Цель игры</b>:\n"
         "•  🤵<b>Мирные житель</b> пытаются найти и казнить всех мафиози.\n"
         "•  🕵️‍♂️<b>Мафия</b> пытается устранить всех мирных жителей.\n\n"
         "📌<b>Этапы игры:</b>\n"
         "•  🌙<b>Ночь</b>: Бот тайно спрашивает мафию, кого убить. Комиссар может проверять одного игрока, а Доктор — лечить.\n"
         "•  🌞<b>День</b>: Бот сообщает, кто убит (если не спасён). Игроки обсуждают и голосуют, кого казнить.\n"
         "•   Игра повторяется, пока одна из сторон не победит.\n\n"
         "📌<b>Победа:</b>\n"
         "•  🤵<b>Мирные</b> выигрывают, если казнили всех мафиози.\n"
         "•  🕵️<b>Мафия</b> выигрывает, если её членов становится больше или столько же, сколько мирных.\n"
         "\n"
         "<i>Все действия выполняются через бота в чате и личных сообщениях.</i>")

ABOUT_MESSAGE = ("<b>🔞 О нас</b>\n"
                 "<i>AYSSAU corp.</i>")

GROUP_TO_LOG = "-1002379509893"
GROUP_TO_LOG_THREAD = 195

ANTIFLOOD_DELAY = 1

CIVILIANS = 'civilians'
MAFIA = 'mafia'
DETECTIVE = 'detective'
PUTANA = 'putana'
MANIAC = 'maniac'
DOCTOR = 'doctor'
roles = {
    5: {CIVILIANS: 3, MAFIA: 1, DETECTIVE:1},
    6: {CIVILIANS: 3, MAFIA: 1, DETECTIVE:1, PUTANA:1},
    7: {CIVILIANS: 3, MAFIA: 2, DETECTIVE:1, PUTANA:1},
    8: {CIVILIANS: 4, MAFIA: 2, DETECTIVE:1, PUTANA:1},
    9: {CIVILIANS: 4, MAFIA: 2, DETECTIVE:1, PUTANA:1, DOCTOR: 1},
    10: {CIVILIANS: 4, MAFIA: 2, DETECTIVE:1, PUTANA:1, DOCTOR: 1, MANIAC: 1},
    11: {CIVILIANS: 4, MAFIA: 3, DETECTIVE:1, PUTANA:1, DOCTOR: 1, MANIAC: 1},
}
def get_roles_list(count: int):
    role_list = []
    for key, val in roles[count].items():
        for i in range(val):
            role_list.append(key)
    return role_list
