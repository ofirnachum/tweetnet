import random
import requests

BASE_URL = "http://tinyurl.com/api-create.php"


class BotBase(object):

    def __init__(self, api, max_size=5):
        self.api = api
        self.prng = Random(max_size)

    def get_short_flag_id(self, flag_id):
        return shorten_flag_id(flag_id)


class BotMaster(BotBase):

    def __init__(self, user, api):
        super(BotMaster, self).__init__(api)
        self.user = user

    def submit_flag(self, flag_id):
        raise NotImplementedError

    def should_tweet(self):
        return random.random() < 0.5


class Bot(BotBase):

    def __init__(self, bot_id, api):
        super(Bot, self).__init__(api)
        self.bot_id = bot_id

    def submit_small_flag(self, flag):
        return self.api.submit_small_flag(flag, self.bot_id)

    def get_master_tweets(self):
        return self.api.query_tweets("TODO")

    def consume_flag(self):
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
