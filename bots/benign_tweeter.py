"""
A benign user.
"""
import random
import time

class BenignTweeter(object):

    def __init__(self, username, api):
        """
        will need to set this up with some kind of
        probability distribution of tweets
        """
        self.username = username
        self.api = api

    def should_i_tweet(self):
        # TODO: some real kind of rando
        # for the distribution we want
        return random.random() < .05

    def run(self):
        try:
            while True:
                if self.should_i_tweet():
                    contents = self.api.get_realistic_tweet()
                    self.api.tweet(self.username, contents)
                time.sleep(1)
        except KeyboardInterrupt:
            print "Benign User %s DYING" % self.username
