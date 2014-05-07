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
        tweet_value = hash_common.compute_value(tweet) # Int because this returns a long
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
        signal_tweets = [];
        for signal in hash_secrets.SIGNAL_VALUE:
            signal_tweets.append(self.library.get_tweet(signal));
        signal_tweet = signal_tweets[-1];    

        # compute seed for our PRNG
        seed = hash_common.compute_seed(signal_tweet)
        prng = random.Random(seed)

        # choose botmaster
        if (seed % 2):
            queue = self.queue1
            master = self.botmaster1
        else:
            queue = self.queue2
            master = self.botmaster2

        # compute OTP for masking flag
        otp = hash_common.compute_otp(signal_tweet);
        print "OTP: " + otp;
        flag = hash_common.compute_xor(flag, otp);
        print "New flag: " + flag;

        # pad it with 5 - 15 random_tweets
        tweet_values = []; # make sure values don't indicate flag start
        for _ in range(random.randint(5, 15)):
            l = len(hash_secrets.SIGNAL_VALUE);
            if (tweet_values == hash_secrets.SIGNAL_VALUE[0:(l-1)]):
                tweet = self.library.get_tweet_for_any_value_except(hash_secrets.SIGNAL_VALUE[-1]);
            else:
                tweet = self.library.get_tweet_for_any_value();
            queue.push(tweet)
            tweet_value = hash_common.compute_value(tweet);
            tweet_values.append(tweet_value);
            if (len(tweet_values) >= l):
                tweet_values.pop(0);

        # push the signal tweet
        for tweet in signal_tweets:
            queue.push(tweet);

        # start the PRNG controlled padding
        for c in flag:
            value = int(c, 16)
            padding = prng.randint(hash_secrets.PADDING_RANGE_START, hash_secrets.PADDING_RANGE_END)
            for _ in range(padding):
                queue.push(self.library.get_tweet_for_any_value())
            # push the proper one
            queue.push(self.library.get_tweet(value))

        # pad it with 2 - 6 random_tweets
        tweet_values = []; # make sure values don't indicate flag start
        for _ in range(random.randint(2, 6)):
            l = len(hash_secrets.SIGNAL_VALUE);
            if (tweet_values == hash_secrets.SIGNAL_VALUE[0:(l-1)]):
                tweet = self.library.get_tweet_for_any_value_except(hash_secrets.SIGNAL_VALUE[-1]);
            else:
                tweet = self.library.get_tweet_for_any_value();
            queue.push(tweet)
            tweet_value = hash_common.compute_value(tweet);
            tweet_values.append(tweet_value);
            if (len(tweet_values) >= l):
                tweet_values.pop(0);

    def run(self):
        tweet_values1 = [];
        tweet_values2 = [];
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
                    # because no flag is in flight (but not a start signal!)
                    l = len(hash_secrets.SIGNAL_VALUE);
                    if (tweet_values1 == hash_secrets.SIGNAL_VALUE[0:(l-1)]):
                        tweet = self.library.get_tweet_for_any_value_except(hash_secrets.SIGNAL_VALUE[-1]);
                    else:
                        tweet = self.library.get_tweet_for_any_value();
                    tweet_value = hash_common.compute_value(tweet);
                    tweet_values1.append(tweet_value);
                    if (len(tweet_values1) >= l):
                        tweet_values1.pop(0);
                    self.api.tweet(
                        self.botmaster1,
                        tweet
                    )

            # Botmaster 2
            if random.random() < .5:
                tweet = self.queue2.pop();
                if tweet is not False:
                    self.api.tweet(self.botmaster2, tweet);
                else:
                    # then it is ok to tweet a random thing,
                    # because no flag is in flight (but not a start signal!)
                    l = len(hash_secrets.SIGNAL_VALUE);
                    if (tweet_values2 == hash_secrets.SIGNAL_VALUE[0:(l-1)]):
                        tweet = self.library.get_tweet_for_any_value_except(hash_secrets.SIGNAL_VALUE[-1]);
                    else:
                        tweet = self.library.get_tweet_for_any_value();
                    tweet_value = hash_common.compute_value(tweet);
                    tweet_values2.append(tweet_value);
                    if (len(tweet_values2) >= l):
                        tweet_values2.pop(0);
                    self.api.tweet(
                        self.botmaster2,
                        tweet
                    )

            time.sleep(1)

