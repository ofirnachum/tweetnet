import time

from common import Bot


class SingleCharBot(Bot):

    def __init__(self, flag_size=32):
        self.flag_size = 32

    def consume_flag(self):
        rand_num = self.prng.next()
        count = rand_num
        flag = ""
        while len(flag) < self.flag_size:
            tweets = self.get_master_tweets()
            for tweet in tweets:
                if count != 0:
                    count -= 1
                    time.sleep(3)
                    continue  # ignore tweets
                flag += self.extract_char(rand_num, tweet)
                rand_num = self.prng.next()
                count = rand_num

        self.submit_small_flag(flag)

    def extract_char(self, rand_num, tweet):
        content = tweet['content']
        index = rand_num % len(content)
        return content[index]

class HashBot(Bot):

    def __init__(self, flag_size=32):
        self.flag_size = 32

    def consume_flag(self):
        rand_num = self.prng.next()
        count = rand_num
        flag = ""
        while len(flag) < self.flag_size:
            tweets = self.get_master_tweets()
            for tweet in tweets:
                if count != 0:
                    count -= 1
                    time.sleep(3)
                    continue  # ignore tweets
                flag += hex(hash(tweet) % 16)
                rand_num = self.prng.next()
                count = rand_num

        self.submit_small_flag(flag)
