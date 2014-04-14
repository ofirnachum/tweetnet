"""
runs a round (prototype)
"""
import sys
import random
import subprocess
import os

def main():
    usernames = ['tweetnet%02d' % i for i in range(10)]
    random.shuffle(usernames)

    round_id = sys.argv[1]
    print "Round: %s" % round_id

    subs = []

    try:
        for username in usernames:
            print "starting benign user %s" % username
            subs.append(subprocess.Popen(
                ["/usr/bin/env", "python","benign_tweeter.py", round_id, username],
            ))

        # launch our bots
        botscript = sys.argv[2]
        for i in range(10):
            print "starting bot %d" % i
            subs.append(subprocess.Popen(
                ["/usr/bin/env", "python", botscript, round_id, str(i)],
            ))

    except:
        for p in subs:
            p.terminate()
            p.wait()
        raise

    for p in subs:
        p.wait()



if __name__ == "__main__":
    main()