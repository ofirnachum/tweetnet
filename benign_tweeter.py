"""
A benign user.
"""
import random
import time

from tweetnet import BenignTweetnet

class BenignTweeter(object):

    def __init__(self, round_id, username):
        """
        will need to set this up with some kind of
        probability distribution of tweets
        """
        self.username = username
        self.api = BenignTweetnet(round_id)

    def should_i_tweet(self):
        # TODO: some real kind of rando
        # for the distribution we want
        return random.random() > .5

    def run(self):
        try:
            while True:
                if self.should_i_tweet():
                    contents = self.api.get_realistic_tweet()
                    self.api.tweet(self.username, contents)
                time.sleep(1)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    import sys
    round_id = sys.argv[1]
    username = sys.argv[2]
    t = BenignTweeter(round_id, username)
    t.run()