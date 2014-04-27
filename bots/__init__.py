from stupid_bot import StupidBot
from stupid_botmaster import StupidBotMaster

from benign_tweeter import BenignTweeter

TYPES = {
    'stupid': (StupidBot, StupidBotMaster),
}


def get_bot_type(flag, run_type):
    if run_type == 'benign':
        return BenignTweeter

    bot, master = TYPES[flag]
    if run_type == 'master':
        return master
    else:
        return bot

