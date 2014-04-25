import time

from common import Bot


class SingleCharBot(Bot):

    def __init__(self, bot_id, api, botmaster, flag_size=32):
        super(SingleCharBot, self).__init__(bot_id, api, botmaster)
        self.flag_size = flag_size

    def consume_flag(self):
        oldIndex = 0
        while True:
            nums = [self.prng.next() for x in range(self.flag_size)]
            num_tweets = sum(nums) + self.flag_size - 1
            tweets = self.get_master_tweets()[oldIndex:]
            while len(tweets) < num_tweets:
                time.sleep(10)
                print "Bot::: waiting. found %d tweets, need %d tweets" % (len(tweets), num_tweets)
                tweets = self.get_master_tweets()[oldIndex:]

            flag = ""
            count = -1
            for num in nums:
                count += num + 1
                tweet = tweets[count]
                flag += self.extract_char(num, tweet)
                print "Bot::: flag %s" % flag
            # time.sleep(60)
            oldIndex += count + 1
            self.submit_small_flag(flag)

    def extract_char(self, rand_num, tweet):
        index = rand_num % len(tweet)
        char = tweet[index]
        print "Bot::: char: %s, index: %s, tweet: %s" % (char, index, tweet)
        return char


class HashBot(Bot):

    def __init__(self, bot_id, api, botmaster, flag_size=32):
        super(HashBot, self).__init__(bot_id, api, botmaster)
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
