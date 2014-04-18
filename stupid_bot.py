import sys
import time

from tweetnet import Tweetnet

# Dumb example bot.

if __name__ == "__main__":
    round_id = sys.argv[1]
    bot_id = sys.argv[2]

    api = Tweetnet(round_id, role='bot')

    submitted = set()
    while True:
        wows = api.query_tweets('#wow')
        for tweet in wows:
            _, flag = tweet['content'].split(' ')
            if not flag in submitted:
                r = api.submit_small_flag(flag, bot_id)
                print r, flag
                submitted.add(flag)

        time.sleep(3)
