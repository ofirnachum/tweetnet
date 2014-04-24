"""
runs a round (prototype)
"""
import sys
import random
import subprocess

from tweetnet import Tweetnet


def main(botmaster_type, bot_type):
    usernames = ['tweetnet%02d' % i for i in range(10)]
    random.shuffle(usernames)

    round_id = sys.argv[1]
    print "Round: %s" % round_id

    api = Tweetnet(round_id, 'admin')
    for user in usernames:
        api.create_user(user)

    botmaster = usernames.pop()

    print "Botmaster: %s" % botmaster

    subs = []

    try:
        for username in usernames:
            print "starting benign user %s" % username
            subs.append(subprocess.Popen(
                ["/usr/bin/env", "python",
                    "benign_tweeter.py", round_id, username, bot_type],
            ))

        # launch our bots
        botscript = sys.argv[2]
        for i in range(10):
            print "starting bot %d" % i
            subs.append(subprocess.Popen(
                ["/usr/bin/env", "python", botscript, round_id, str(i)],
            ))

        # launch botmaster
        botmasterscript = sys.argv[3]
        print "starting botmaster with handle %s" % botmaster
        subs.append(subprocess.Popen(
            ["/usr/bin/env", "python", botmasterscript,
                round_id, botmaster, botmaster_type]
        ))

    except:
        for p in subs:
            p.terminate()
            p.wait()
        raise

    for p in subs:
        p.wait()


if __name__ == "__main__":
    botmaster_type = sys.argv[1]
    bot_type = sys.argv[2]
    main(botmaster_type, bot_type)
