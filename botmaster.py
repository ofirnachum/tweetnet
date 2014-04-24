from common import BotMaster
from collections import defaultdict
import time


class SingleCharBotMaster(BotMaster):

    def submit_flag(self, flag_id):
        sent_char = 0
        rand_num = self.prng.next()
        count = rand_num
        while sent_char < len(flag_id):
            time.sleep(1)
            if not self.should_tweet():
                continue

            tweet = self.api.get_realistic_tweet()
            if count != 0:
                count -= 1
            else:
                rand_num = self.prng.next()
                count = rand_num
                tweet = self.insert_char(rand_num,
                                         flag_id[sent_char], tweet)
                print "Master::: char: %s, el: %s, tweeting: %s" %\
                    (flag_id[sent_char], sent_char, tweet)
                sent_char += 1

            self.api.tweet(self.user, tweet)

    def insert_char(self, rand_num, char, tweet):
        content = list(tweet)
        index = rand_num % len(content)
        content[index] = char  # replace w/char
        return content


class HashBotMaster(BotMaster):
    tweet_table = defaultdict(list)  # this way, initializes empty lists
    CHAR_SIZE = 4  # how many bits of information per tweet?

    def submit_flag(self, flag_id):
        sent_char = 0
        self.fill_table()
        rand = self.prng.next()

        while sent_char < len(flag_id):
            time.sleep(1)
            if not self.should_tweet():
                continue

            if rand == 0:
                # When we reach 0, find a random realtext tweet
                # which hashes to the value we want, and send it
                tweet = self.tweet_for_char(ord(flag_id[sent_char]))
                self.api.tweet(self.user, tweet)

                sent_char += 4 / self.CHAR_SIZE
                rand = self.prng.next()
            else:
                # Otherwise, tweet something random and decrement counter
                self.api.tweet(self.user, self.api.get_realistic_tweet())
                rand -= 1

    # Make sure the tweet_table has something for every character
    # we might use, but don't store too much
    def fill_table(self):
        while len(self.tweet_table) < 2 ** self.CHAR_SIZE:
            tweet = self.api.get_realistic_tweet()
            val = hash(tweet) % 2 ** self.CHAR_SIZE

            # Only store it if we have fewer than len(message) tweets.
            if len(self.tweet_table[val]) < 128 / self.CHAR_SIZE:
                self.tweet_table[val].add(tweet)

    # get tweet for ord(character)
    def tweet_for_char(self, char):
        if len(self.tweet_table[char]) == 0:
            self.fill_table()
        return self.tweet_table[char].pop()
