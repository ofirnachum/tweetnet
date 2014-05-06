from stupid_bot import StupidBot
from stupid_botmaster import StupidBotMaster
from hash_bot import HashBot
from hash_botmaster import HashBotMaster


from benign_tweeter import BenignTweeter

TYPES = {
    'stupid': (StupidBot, StupidBotMaster),
    'hash'	: (HashBot, HashBotMaster)
}


def get_bot_type(flag, run_type):
    if run_type == 'benign':
        return BenignTweeter

    bot, master = TYPES[flag]
    if run_type == 'master':
        return master
    else:
        return bot

