import time
import random
import thread
from common import BotMaster, Random, SLEEP, clean_hex
from collections import defaultdict
from config import seed


class HashBotMaster(BotMaster):
    tweet_table = defaultdict(list)  # this way, initializes empty lists
    CHAR_SIZE = 4  # how many bits of information per tweet?

    def __init__(self, psb, api):
        super(HashBotMaster, self).__init__(psb, api)
        self.prng = Random(2 ** 128, seed)
        self.set_randoms()
        self.user = self.botmaster1
        self.loser = self.botmaster2
        print "user", self.user, "loser", self.loser

    def run(self):
        flags = self.get_new_flags()
        thread.start_new_thread(self.run_dummy, ())
        while True:
            if len(flags):
                flag = flags.pop()
                self.submit_flag(flag)
            else:
                self.tweet_randomly()
                flags = self.get_new_flags()
            time.sleep(SLEEP)

    def run_dummy(self):
        while True:
            time.sleep(SLEEP)
            if self.should_tweet():
                self.api.tweet(self.loser, self.api.get_realistic_tweet())

    def set_randoms(self):
        print "master calling set_randoms"
        self.first = self.prng.next() % 16
        self.mask = self.prng.next()

    def tweet_randomly(self):
        if self.should_tweet():
            tweet = self.tweet_for_not_char(self.first)
            self.tweet(tweet)
        time.sleep(SLEEP)

    def submit_flag(self, flag_id):
        masked_flag = clean_hex(int(flag_id, 16) ^ self.mask)
        masked_flag = map(lambda i: int(i, 16), list(masked_flag))
        chars_to_send = [self.first] + masked_flag
        self.fill_table(chars_to_send)
        sent_char = 0
        while sent_char < len(chars_to_send):
            time.sleep(SLEEP)
            if self.should_tweet():
                tweet = self.tweet_for_char(chars_to_send[sent_char])
                self.tweet(tweet)
                sent_char += 1
        print "master sent flag"
        self.set_randoms()

    # Make sure the tweet_table has something for every character
    # we might use, but don't store too much
    def fill_table(self, chars_needed=None):
        # default to filling the dict with 2 of everything
        chars_needed = (chars_needed or range(16) * 2)[:]
        while len(chars_needed):
            tweet = self.api.get_realistic_tweet()
            val = hash(tweet) % 16

            # If the hashed value of the tweet matches one of our characters,
            # add it to the dictionary, and indicate that we no longer need =
            # clean_hex
            if val in chars_needed:
                # print "needed"
                chars_needed.remove(val)
                self.tweet_table[val].append(tweet)
            # else:
                # print "not needed", chars_needed, val

    # get tweet for ord(character)
    def tweet_for_char(self, char):
        if len(self.tweet_table[char]) == 0:
            self.fill_table()
        return self.tweet_table[char].pop()

    # get tweet for ord(any other character)
    def tweet_for_not_char(self, char):
        r = random.choice([i for i in range(16) if i != char])
        if len(self.tweet_table[r]) == 0:
            self.fill_table()
        return self.tweet_table[r].pop()
