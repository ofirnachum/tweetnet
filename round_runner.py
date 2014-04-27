"""
runs a round (prototype)
"""
import random
import subprocess

from tweetnet import Tweetnet

PY_PATH = "/usr/bin/env"
BOT_RUNNER = "bot_runner.py"


def main(round_id, bot_type,
         num_bots=10, num_tweeters=10):
    print "Round: %s" % round_id

    usernames = ['tweetnet%02d' % i for i in range(num_tweeters)]
    random.shuffle(usernames)

    api = Tweetnet(round_id, 'admin')
    for user in usernames:
        api.create_user(user)

    botmaster = usernames.pop()

    print "Botmaster: %s" % botmaster

    subs = []

    try:
        for username in usernames:
            print "Starting benign user %s" % username
            subs.append(subprocess.Popen(
                get_popen_args(get_beign_args(round_id,
                                              username))
            ))

        # launch our bots

        for i in range(num_bots):
            print "Starting bot %d" % i
            subs.append(subprocess.Popen(
                get_popen_args(get_bot_args(round_id,
                                            i,
                                            bot_type,
                                            botmaster)),
            ))

        # launch botmaster
        print "starting botmaster with handle %s" % botmaster
        subs.append(subprocess.Popen(
            get_popen_args(get_master_args(round_id,
                                           botmaster,
                    bot_type))
        ))

    except:
        for p in subs:
            p.terminate()
            p.wait()
        raise

    for p in subs:
        p.wait()


def get_beign_args(round_id, username):
    return get_popen_args(*[round_id, username, "benign"])


def get_bot_args(round_id, i, bot_type, botmaster):
    return get_popen_args(*[round_id, str(i), bot_type, "bot"])


def get_master_args(round_id, username, bot_type):
    return get_popen_args(*[round_id, username, bot_type, "master"])


def get_popen_args(*args):
    base_args = [PY_PATH, "python", BOT_RUNNER]
    base_args.extend(args)
    return base_args


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--round_id", help="set the round_id")
    parser.add_argument("-b", "--bot_type",
                        help="set the type of bot/master pair")
    args = parser.parse_args()
    main(args.round_id, args.bot_type)
