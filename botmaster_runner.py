"""
1 character per tweet
"""
import sys

from tweetnet import Tweetnet
from bots import get_bot_type

if __name__ == "__main__":
    round_id = sys.argv[1]
    user = sys.argv[2]
    bot_type = sys.argv[3]

    try:
        api_type = sys.argv[4]
    except IndexError:
        api_type = 'default'
    api_obj = get_api_type(api_type)
    api = api_obj(round_id, role='bot')

    master_obj = get_bot_type(bot_type, is_master=True)
    master = master_obj(user, api)

    master.run()
