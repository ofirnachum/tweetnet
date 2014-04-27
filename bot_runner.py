import sys
import time

from tweetnet import Tweetnet
from bots import SingleCharBot, HashBot

TYPES = {
    'SingleCharBot': SingleCharBot,
    'HashBot': HashBot,
}

if __name__ == "__main__":
    round_id = sys.argv[1]
    bot_id = sys.argv[2]
    bot_type = sys.argv[3]
    botmaster = sys.argv[4]

    api = Tweetnet(round_id, role='bot')
    bot = TYPES[bot_type](bot_id, api, botmaster)

    bot.run()
