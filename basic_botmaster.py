import sys
import time
import random
import requests
import botnet_utils as utils

from tweetnet import Tweetnet

TWEET_PERIOD = 1;
SLEEP_PERIOD = 1;

class TweetQueue:
    # NOTE: Tweet frequency is relative
    # to how often you call 'pop'.
    def __init__(self, user, api, tweet_period):
        self.user = user;
        self.api = api;
        self.tweet_period = tweet_period;
        self.queue = [];

    def push(self, content):
        self.queue.append(content);

    def pop(self):
        # Successful pop happens
        # with probability 1/tweet_period
        if (self.queue and (random.random() * self.tweet_period < 1)):
            content = self.queue.pop(0);
            self.api.tweet(self.user, content);
            return content;
        return False;



def get_random_tweet(api):
    """
    returns random tweet from all tweets
    """
    tweet = "hello hello";#api.get_realistic_tweet();
    return tweet;

def get_random_short_tweet(api, max_len):
    """
    returns random tweet of at most max_len length from all tweets
    """
    tweet = get_random_tweet(api);
    while (len(tweet) > max_len):
        tweet = get_random_tweet(api);
    return tweet;

def tweet_flag_component(api, queue, comp):
    random_content = get_random_short_tweet(api, 138).strip();
    tweet_content = random_content + utils.to_punctuation(comp) + ' ';
    queue.push(tweet_content);

def tweet_flag(api, queue, flag):
    # Signal beginning of flag
    random_content = get_random_short_tweet(api, 138);
    queue.push(random_content + "  ");  
    # Tweet flag in chunks of base-4 digits
    for xy in flag['flag_id']:
        n = int(xy, 16);
        x = n // 4;
        y = n % 4;
        tweet_flag_component(api, queue, x);
        tweet_flag_component(api, queue, y);

if __name__ == "__main__":
    round_id = sys.argv[1]
    user = sys.argv[2]

    api = Tweetnet(round_id, role='admin')
    queue = TweetQueue(user, api, TWEET_PERIOD);

    # Last check for flags
    last_check = 0
    already = set()

    while True:
        print "Checking for new flags...";
        flags = api.get_flags(since=last_check);
        last_check = int(time.time()) - 1;

        # Is it a 'sweetspot' for sending a tweet?
        # The 'sweetspot' is used by bot to 
        # determine validity of master.
        if utils.sweet_spot(last_check):
            random_tweet = get_random_tweet(api);
            api.tweet(user, random_tweet.strip());
        if flags:
            for flag in flags:
                tweet_flag(api, queue, flag);
        queue.pop();
        time.sleep(SLEEP_PERIOD)
