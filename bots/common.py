import random
import requests
import time

class BotMaster(object):

    def __init__(self, pipe_separated_botmasters, api):
        self.botmaster1, self.botmaster2 = pipe_separated_botmasters.split('|')
        self.user = self.botmaster1 # backwards compat
        self.api = api

        self._last_flag_check = 0

    def should_tweet(self):
        # TODO: replace
        # with optional tweet queue?
        # way to replicate benign
        return random.random() < 0.5

    def get_new_flags(self):
        flags = self.api.get_flags(since=self._last_flag_check)
        self._last_flag_check = int(time.time())
        return [f['flag_id'] for f in flags]

    def run(self):
        raise NotImplementedError


class Bot(object):

    def __init__(self, bot_id, api, pipe_separated_botmasters):
        self.bot_id = bot_id
        self.api = api
        self.botmaster1, self.botmaster2 = pipe_separated_botmasters.split('|')
        self.botmaster = self.botmaster1

    def submit_small_flag(self, flag):
        return self.api.submit_small_flag(flag, self.bot_id)

    def get_master_tweets(self):
        return self.get_user_tweets(self.botmaster)

    def get_user_tweets(self, username):
        tweets = self.api.get_user(username)['tweets']
        return [tweet['content'] for tweet in tweets]

    def run(self):
        raise NotImplementedError


class Random(object):

    def __init__(self, max_size):
        self.prng = random.Random(0)
        self.max_size = max_size

    def next(self):
        return int(self.prng.random() * self.max_size)


def shorten_flag_id(url):

    r = requests.get(BASE_URL, params={
        'url': url,
    })
    return r.text.split("/")[-1]
