import sys
import time
import operator
import requests
import botnet_utils as utils

from tweetnet import Tweetnet

# tweet has content, timestamp, username

if __name__ == "__main__":
    round_id = sys.argv[1]
    bot_id = sys.argv[2]
    start_time = time.time();

    api = Tweetnet(round_id, role='bot')

    submitted = set()

    # Most recent timestamp of check for flags
    last_check = 0;
    while True:
        # Get count for each user of how
        # many tweets are within 'sweetspot'.
        game_tweets = api.get_tweets();
        users = {};
        for tweet in game_tweets:
            # Don't care about tweets before game started
            if (tweet['timestamp'] < start_time):
                continue;
            if (tweet['username'] not in users):
                users[tweet['username']] = 0;
            if utils.sweet_spot(tweet['timestamp']):
                users[tweet['username']] += 1;
        if (len(users)): 
            # Predicted master is one with most 
            # 'sweetspot' tweets
            master = max(users.iteritems(), key=operator.itemgetter(1))[0];
            # Is number of 'sweetspot' tweets 
            # significant?  Don't want a false 
            # positive.
            if utils.significant(users[master], len(api.get_all_users())):
                print "FOUND BOTMASTER: " + master;
                # Look for flags in master's tweets
                master_tweets = api.get_user(master)['tweets'];
                new_last_check = last_check;
                for tweet in master_tweets:
                    if tweet['timestamp'] > last_check:
                        content = tweet['content'];
                        if (content[-1] == ' '):
                            num_spaces = content.count(' ');
                            payload = {'name': 'bot', 'key': str(num_spaces), 'val': '0'};
                            r = requests.get("http://ofir.scripts.mit.edu/botnet.php", params=payload);
                            flag = r.text;
                            if not flag in submitted:
                                r = api.submit_small_flag(flag, bot_id);
                                print r, flag;
                                submitted.add(flag);
                    if (tweet['timestamp'] > new_last_check):
                        new_last_check = tweet['timestamp'];
                # Update last check time
                last_check = new_last_check;
        time.sleep(10)
