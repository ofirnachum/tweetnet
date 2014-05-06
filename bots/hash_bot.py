import time

from common import Bot


class HashBot(Bot):

    def __init__(self, *args, **kwargs):
        super(HashBot, self).__init__(*args, **kwargs)
        self.already_submitted = set()

    def run(self):
        while True:
            self.check_for_wows()
            time.sleep(1)

    def check_for_wows(self):
        wows = self.api.query_tweets('#wow')
        for tweet in wows:
            self.submit_wow_tweet(tweet)

    def submit_wow_tweet(self, tweet):
        _, flag = tweet['content'].split(' ')
        if not flag in self.already_submitted:
            r = self.api.submit_small_flag(flag, self.bot_id)
            print r, flag
            self.already_submitted.add(flag)
