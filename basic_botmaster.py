import sys
import time
import random
import requests
import botnet_utils as utils

from tweetnet import Tweetnet

def get_random_tweet(api):
    """
    returns random tweet from all tweets
    """
    tweet = api.get_realistic_tweet();
    return tweet;

def get_random_short_tweet(api, max_len):
    """
    returns random tweet of at most max_len length from all tweets
    """
    tweet = api.get_realistic_tweet();
    while (len(tweet['content']) > max_len):
        tweet = api.get_realistic_tweet();
    return tweet;

def tweet_flag_component(api, comp):
    random_content = get_random_short_tweet(api, 138)['content'].strip();
    tweet_content = random_content + utils.to_punctuation(comp) + ' ';
    api.tweet(user, tweet_content);

def tweet_flag(api, flag):
    # Signal beginning of flag
    random_content = get_random_short_tweet(api, 138)['content'];
    api.tweet(user, random_content + "  ");  
    # Tweet flag in chunks of base-4 digits
    for xy in flag['flag_id']:
        n = int(xy, 16);
        x = n // 4;
        y = n % 4;
        tweet_flag_component(api, x);
        time.sleep(1);
        tweet_flag_component(api, y);
        time.sleep(1);

if __name__ == "__main__":
    round_id = sys.argv[1]
    user = sys.argv[2]

    api = Tweetnet(round_id, role='admin')

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
            api.tweet(user, random_tweet['content'].strip());
        if flags:
            for flag in flags:
                tweet_flag(api, flag);
                time.sleep(10);
        time.sleep(3)
