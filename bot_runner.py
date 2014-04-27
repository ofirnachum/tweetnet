import sys
import time

from tweetnet import Tweetnet
from bots.common import get_bot_type

if __name__ == "__main__":
    round_id = sys.argv[1]
    bot_id = sys.argv[2]
    bot_type = sys.argv[3]
    botmaster = sys.argv[4]

    api = Tweetnet(round_id, role='bot')
    bot_obj = get_bot_type(bot_type)
    bot = bot_obj(bot_id, api, botmaster)

    bot.run()
