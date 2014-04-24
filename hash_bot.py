import sys
import time

from tweetnet import Tweetnet
from hashlib import md5

# Bot that gathers data from tweet hashes.

CHARS_PER_TWEET = 4

if __name__ == "__main__":
    round_id = sys.argv[1]
    bot_id = sys.argv[2]

    api = Tweetnet(round_id, role='bot')

    submitted = set()
    while True:
        tweets = api.
        for tweet in wows:
            _, flag = tweet['content'].split(' ')
            if not flag in submitted:
                r = api.submit_small_flag(flag, bot_id)
                print r, flag
                submitted.add(flag)

        time.sleep(3)

def hash(tweet):
    m = md5()
    m.update(tweet)
    return m.hexdigest()[-4:]
