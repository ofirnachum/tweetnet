import random
import requests

class BotMaster(object):

    def __init__(self, user, api):
        self.user = user
        self.api = api

        self._last_flag_check = 0

    def should_tweet(self):
        # TODO: replace
        # with optional tweet queue?
        # way to replicate benign
        return random.random() < 0.5

    def get_new_flags(self):
        flags = api.get_flags(since=self._last_flag_check)
        self._last_flag_check = int(time.time()) - 1
        return [f['flag_id'] for f in flags]

    def run(self):
        raise NotImplementedError


class Bot(object):

    def __init__(self, bot_id, api, botmaster):
        self.bot_id = bot_id
        self.api = api
        self.botmaster = botmaster

    def submit_small_flag(self, flag):
        return self.api.submit_small_flag(flag, self.bot_id)

    def get_master_tweets(self):
        # TODO: do we really want the bot knowing
        # who the master is right away?
        tweets = self.api.get_user(self.botmaster)['tweets']
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


def get_bot_type(flag, is_master=False):
    bot, master = bots.TYPES[flag]
    if is_master:
        return master
    return bot
