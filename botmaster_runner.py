"""
1 character per tweet
"""
import sys
import time

from tweetnet import Tweetnet
from bots.common import get_bot_type

if __name__ == "__main__":
    round_id = sys.argv[1]
    user = sys.argv[2]
    bot_type = sys.argv[3]
    api = Tweetnet(round_id, role='admin')

    master_obj = get_bot_type(bot_type, is_master=True)
    master = master_obj(user, api)

    master.run()
