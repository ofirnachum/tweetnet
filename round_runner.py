"""
runs a round (prototype)
"""
import random
import subprocess

from tweetnet import Tweetnet

PY_PATH = "/usr/bin/env"
BOT_RUNNER = "bot_runner.py"

def main(round_id, bot_type,
         num_bots=10, num_tweeters=20, dev=False):
    print "Round: %s" % round_id

    usernames = ['tweetnet%02d' % i for i in range(num_tweeters)]
    random.shuffle(usernames)

    api = Tweetnet(round_id, 'admin')
    for user in usernames:
        api.create_user(user)

    botmaster_bonnie = usernames.pop()
    botmaster_clyde = usernames.pop()
    pipe_separated_botmasters = botmaster_bonnie + '|' + botmaster_clyde

    print "Botmasters: %s" % pipe_separated_botmasters

    subs = []

    try:
        for username in usernames:
            print "Starting benign user %s" % username
            subs.append(subprocess.Popen(
                get_beign_args(round_id,
                               username,
                               dev)
            ))

        # launch our bots

        for i in range(num_bots):
            print "Starting bot %d" % i
            subs.append(subprocess.Popen(
                get_bot_args(round_id,
                             i,
                             bot_type,
                             pipe_separated_botmasters,
                             dev),
            ))

        # launch botmaster
        print "starting botmaster with handles %s" % pipe_separated_botmasters
        subs.append(subprocess.Popen(
            get_master_args(round_id,
                            pipe_separated_botmasters,
                            bot_type,
                            dev)
        ))

    except:
        for p in subs:
            p.terminate()
            p.wait()
        raise

    for p in subs:
        p.wait()


def get_beign_args(round_id, username, dev):
    a = get_popen_args({
        '--round-id': round_id,
        '--username': username,
        '--run-type': "benign"
    })
    if dev:
        a.append('--dev')
    return a


def get_bot_args(round_id, i, bot_type, botmaster, dev):
    a = get_popen_args({
        '--round-id': round_id,
        '--bot-id': str(i),
        '--bot-type': bot_type,
        '--run-type': "bot",
        '--username': botmaster,
    })
    if dev:
        a.append('--dev')
    return a


def get_master_args(round_id, username, bot_type, dev):
    a = get_popen_args({
        '--round-id': round_id,
        '--username': username,
        '--bot-type': bot_type,
        '--run-type': "master",
    })
    if dev:
        a.append('--dev')
    return a


def get_popen_args(options):
    base_args = [PY_PATH, "python", BOT_RUNNER]
    for k, v in options.items():
        base_args += [k, v]
    return base_args


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--round_id", help="set the round_id")
    parser.add_argument("-b", "--bot_type",
                        help="set the type of bot/master pair")
    parser.add_argument("--dev", action="store_true", default=False)
    args = parser.parse_args()
    main(args.round_id, args.bot_type, dev=args.dev)
