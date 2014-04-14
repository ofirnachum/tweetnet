"""
example of a stupid botmaster
"""
import sys

from tweetnet import AdminTweetnet

if __name__ == "__main__":
    round_id = sys.argv[1]
    user = sys.argv[2]

    api = AdminTweetnet(round_id)

    api.tweet(user, "#wow %s" % sys.argv[3])
