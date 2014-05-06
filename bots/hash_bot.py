import time

from common import Bot


class HashBot(Bot):

    def __init__(self, *args, **kwargs):
        super(HashBot, self).__init__(*args, **kwargs)
        self.already_submitted = set()

    def run(self):
        last_check = 0
        while True:
            bm1_tweets = self.api.get_user(self.botmaster1)['tweets']
            for tweet in bm1_tweets:
                if tweet['timestamp'] > last_check:
                    print hex(hash(tweet['content']) % 16)
            last_check = int(time.time())
            time.sleep(1)

