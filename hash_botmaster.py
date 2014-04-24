"""
example of a stupid botmaster
"""
import sys
import time

from tweetnet import Tweetnet
from hashlib import md5

if __name__ == "__main__":
    round_id = sys.argv[1]
    user = sys.argv[2]

    api = Tweetnet(round_id, role='admin')

    last_check = 0
    already = set()

    while True:
        print "Checking for new flags..."
        flags = api.get_flags(since=last_check)
        last_check = int(time.time()) - 1
        if flags:
            for flag in flags:
                print "found one: %s" % flag['flag_id']
                print "tweeting '#wow %s'" % flag['flag_id']
                
            api.tweet(user, "#wow %s" % flag['flag_id'])
        time.sleep(3)
