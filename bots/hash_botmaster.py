"""
example of a stupid botmaster
"""
import random
import time

from common import BotMaster

import hash_secrets
import hash_common

class TweetQueue:
    # NOTE: Tweet frequency is relative
    # to how often you call 'pop'.
    def __init__(self, user, api, tweet_period=2):
        self.user = user;
        self.api = api;
        self.tweet_period = tweet_period;
        self.queue = [];

    def push(self, content):
        self.queue.append(content);

    def pop(self):
        # Successful pop happens
        # with probability 1/tweet_period
        if (self.queue):
            content = self.queue.pop(0);
            return content;
        return False;


class TweetLibrary(object):

    def __init__(self, api):
        """
        provides access to random tweets, indexed by their hex value
        """
        self.library = {}
        for i in range(0x0, 0xf + 1):
            self.library[i] = [] # append to add, pop() to remove (stack)

        self.api = api

    def _get_tweet_from_api(self):
        """
        gets some realistic tweet and stores it in the right library slot
        """
        tweet = self.api.get_realistic_tweet();
        tweet_value = int(hash_common.md5int(tweet) % 16) # Int because this returns a long
        self.library[tweet_value].append(tweet)

    def _checkout_tweet(self, value):
        """
        returns a tweet with the given value, or returns none
        if there isn't one
        """
        if self.library[value]:
            return self.library[value].pop()
        else:
            return None

    def get_tweet(self, value):
        """
        promises to return a tweet with the given value
        """
        while True:
            t = self._checkout_tweet(value)
            if t is not None:
                return t
            # Otherwise, try and get one
            self._get_tweet_from_api()

    def get_tweet_for_any_value_except(self, bad_value):
        # pick one
        value = None
        while value is None:
            value = random.randint(0x0, 0xf)
            if value == bad_value:
                value = None

        # ok, so we have a value!
        return self.get_tweet(value)

    def get_tweet_for_any_value(self):
        value = random.randint(0x0, 0xf)
        return self.get_tweet(value)

class HashBotMaster(BotMaster):
    def __init__(self, *args, **kwargs):
        super(HashBotMaster, self).__init__(*args, **kwargs);
        self.queue1 = TweetQueue(self.botmaster1, self.api);
        self.queue2 = TweetQueue(self.botmaster2, self.api);

        self.library = TweetLibrary(self.api)

    def tweet_flag(self, flag):
        # TODO: decide whether to send it from botmaster 1 or botmaster 2
        queue = self.queue1
        master = self.botmaster1

        signal_tweet = self.library.get_tweet(hash_secrets.SIGNAL_VALUE)

        # compute seed for our PRNG
        seed = hash_common.compute_seed(signal_tweet)
        prng = random.Random(seed)

        # pad it with 5 - 15 random_tweets
        for _ in range(random.randint(5, 15)):
            queue.push(self.library.get_tweet_for_any_value_except(hash_secrets.SIGNAL_VALUE))

        # push the signal tweet
        queue.push(signal_tweet)

        # start the PRNG controlled padding
        # TODO: THE FLAG IS SENT IN THE CLEAR>>>> NOT OK
        for c in flag:
            value = int(c, 16)
            padding = prng.randint(hash_secrets.PADDING_RANGE_START, hash_secrets.PADDING_RANGE_END)
            for _ in range(padding):
                queue.push(self.library.get_tweet_for_any_value())
            # push the proper one
            queue.push(self.library.get_tweet(value))

        # pad it with 2 - 6 random_tweets
        for _ in range(random.randint(2, 6)):
            queue.push(self.library.get_tweet_for_any_value_except(hash_secrets.SIGNAL_VALUE))

    def run(self):
        while True:
            flags = self.get_new_flags()
            if flags:
                for flag in flags:
                    print "got new flag: %s" % flag
                    self.tweet_flag(flag);

            # Let's tweet with probability .5, for each person

            # Botmaster 1
            if random.random() < .5:
                tweet = self.queue1.pop();
                if tweet is not False:
                    self.api.tweet(self.botmaster1, tweet);
                else:
                    # then it is ok to tweet a random thing,
                    # because no flag is in flight (but not a 0xF!)
                    self.api.tweet(
                        self.botmaster1,
                        self.library.get_tweet_for_any_value_except(hash_secrets.SIGNAL_VALUE),
                    )

            # Botmaster 2
            if random.random() < .5:
                tweet = self.queue2.pop();
                if tweet is not False:
                    self.api.tweet(self.botmaster2, tweet);
                else:
                    # then it is ok to tweet a random thing,
                    # because no flag is in flight (but not a 0xF!)
                    self.api.tweet(
                        self.botmaster2,
                        self.library.get_tweet_for_any_value_except(hash_secrets.SIGNAL_VALUE),
                    )

            time.sleep(1)

