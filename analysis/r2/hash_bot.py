import time
from config import seed
from common import Bot, Random, clean_hex, SLEEP


class HashBot(Bot):

    def __init__(self, bot_id, api, botmaster, flag_size=32):
        super(HashBot, self).__init__(bot_id, api, botmaster)
        self.flag_size = flag_size
        self.prng = Random(2 ** 128, seed)
        self.set_randoms()
        self.master = 0

    def run(self):
        while True:
            self.listen_for_flag()
            time.sleep(SLEEP)

    def set_randoms(self):
        self.first = self.prng.next() % 16
        self.mask = clean_hex(self.prng.next())

    def listen_for_flag(self):
        offset = 0
        while True:
            tweets = self.get_master_tweets()[offset:]
            for i, tweet in enumerate(tweets):
                if hash(tweet) % 16 == self.first:
                    offset = self.consume_flag(offset + i + 1)
                    break
            time.sleep(SLEEP)

    def consume_flag(self, offset):
        tweets = self.get_master_tweets()[offset:]
        while len(tweets) < self.flag_size:
            tweets = self.get_master_tweets()[offset:]
            time.sleep(SLEEP)

        print "bot got flag"
        print "mask", self.mask

        flag = []
        for i in range(self.flag_size):
            cipher = hash(tweets[i]) % 16
            flag.append(cipher ^ int(self.mask[i], 16))

        flag = "".join(map(clean_hex, flag))

        print 'flag', flag

        self.submit_small_flag(flag)
        self.set_randoms()
        return offset + self.flag_size

    def get_master_tweets(self):
        return super(HashBot, self).get_master_tweets()[self.master]
