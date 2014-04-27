import sys
import time
import operator
import requests
import botnet_utils as utils

from tweetnet import Tweetnet

# tweet has content, timestamp, username

flag_components = [];
flag_length = 32;

if __name__ == "__main__":
    round_id = sys.argv[1]
    bot_id = sys.argv[2]
    start_time = time.time();

    api = Tweetnet(round_id, role='bot')

    submitted = set()

    # Most recent timestamp of check for flags
    last_check = start_time;
    last_master = None
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
            else:
                users[tweet['username']] -= 1

        if (len(users)): 
            # Predicted master is one with most 
            # 'sweetspot' tweets
            master = max(users.iteritems(), key=operator.itemgetter(1))[0];
            if master != last_master:
                last_check = start_time
                flag_components = []
            last_master = master
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
                        # Content is flag-relevant iff ' ' is at end
                        if (content[-1] == ' '):
                            # Flag component found in 2nd to last char (punctuation)
                            component = utils.from_punctuation(content[-2]);
                            flag_components.append((tweet['timestamp'], component));
                            print "got flag component! %d, %s" % (component, ''.join([str(f[1]) for f in flag_components]))
                    if (tweet['timestamp'] > new_last_check):
                        new_last_check = tweet['timestamp'];
                # Update last check time
                last_check = new_last_check;
        # Do we have entire flag?
        if (len(flag_components) > 2*flag_length):
            flag_components.sort();
            print [y for (x,y) in flag_components];
            # Check correct beginning of flag
            if (flag_components[0][1] != -1):
                print "CORRUPTED FLAG! START = " + str(flag_components[0][1]);
                print flag_components;
                flag_components = [];
                continue;
            flag_components.pop(0);
            flag_b4 = [];
            # Go through flag components to reconstruct flag
            while (flag_components and (flag_components[0][1] != -1)):
                flag_b4.append(flag_components[0][1]);
                flag_components.pop(0);

            if len(flag_b4) != 2*flag_length:
                print "CORRUPTED FLAG! LENGTH = " + str(len(flag_b4));
                print flag_components;
                flag_components = [];
                continue;
            flag_b16 = [];
            flag = "";
            for i in xrange(flag_length):
                print "FLAGCOMP: " + str(flag_b4[2*i]) + str(flag_b4[2*i+1])
                flag_b16.append(4*flag_b4[2*i] + flag_b4[2*i+1]);
                flag += str(hex(flag_b16[-1]))[-1];
            print "FOUND FLAG: " + flag;
            if not flag in submitted:
                r = api.submit_small_flag(flag, bot_id);
                print r, flag;
                submitted.add(flag);
        time.sleep(1)
