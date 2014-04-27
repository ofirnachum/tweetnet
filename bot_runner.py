import sys

from tweetnet import get_api_type
from bots import get_bot_type

if __name__ == "__main__":
    round_id = sys.argv[1]
    bot_id = sys.argv[2]
    bot_type = sys.argv[3]
    botmaster = sys.argv[4]

    try:
        api_type = sys.argv[5]
    except IndexError:
        api_type = 'default'
    api_obj = get_api_type(api_type)
    api = api_obj(round_id, role='bot')

    bot_obj = get_bot_type(bot_type)
    bot = bot_obj(bot_id, api, botmaster)

    bot.run()
