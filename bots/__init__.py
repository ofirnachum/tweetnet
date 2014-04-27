from stupid_bot import StupidBot
from stupid_botmaster import StupidBotMaster

TYPES = {
    'stupid': (StupidBot, StupidBotMaster),
}


def get_bot_type(flag, is_master=False):
    bot, master = TYPES[flag]
    if is_master:
        return master
    return bot
