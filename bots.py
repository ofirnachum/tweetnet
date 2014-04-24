import time

from common import Bot


class SingleCharBot(Bot):

    def __init__(self, bot_id, api, flag_size=32):
        super(SingleCharBot, self).__init__(bot_id, api)
        self.flag_size = flag_size

    def consume_flag(self):
        rand_num = self.prng.next()
        count = rand_num
        flag = ""
        while len(flag) < self.flag_size:
            tweets = self.get_master_tweets()
            for tweet in tweets:
                if count != 0:
                    count -= 1
                    time.sleep(1)
                    continue  # ignore tweets
                flag += self.extract_char(rand_num, tweet)
                print "Bot::: flag: %s" % flag
                rand_num = self.prng.next()
                count = rand_num

        self.submit_small_flag(flag)

    def extract_char(self, rand_num, tweet):
        content = tweet['content']
        index = rand_num % len(content)
        return "".join(content[index])


class HashBot(Bot):

    def __init__(self, bot_id, api, flag_size=32):
        super(HashBot, self).__init__(bot_id, api)
        self.flag_size = flag_size

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
