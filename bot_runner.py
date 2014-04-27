import sys
import argparse

from tweetnet import get_api_type
from bots import get_bot_type

BENIGN = "benign"
BOT = "bot"
MASTER = "master"
DEV = "dev"
DEFAULT = "default"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--round-id")
    parser.add_argument("--bot-id")
    parser.add_argument("--bot-type")
    parser.add_argument("--username")
    parser.add_argument("--run-type",
                        choices=(BENIGN, BOT, MASTER))
    parser.add_argument("--dev", action="store_true", default=False)
    args = parser.parse_args()

    api_type = DEFAULT
    if args.dev:
        api_type = DEV

    bot = None

    api_obj = get_api_type(api_type)
    api = api_obj(args.round_id, role=args.run_type)

    is_master = args.run_type == MASTER
    bot_obj = get_bot_type(args.bot_type, args.run_type)

    if args.run_type == BENIGN:
        bot = bot_obj(args.username, api)
    elif args.run_type == BOT:
        bot = bot_obj(args.bot_id, api, args.username)
    elif args.run_type == MASTER:
        bot = bot_obj(args.username, api)

    if bot is None:
        raise Exception("Invalid type! %s" % args.run_type)

    if args.run_type == BENIGN and args.dev:
        # don't run benign!
        sys.exit(1)

    bot.run()
