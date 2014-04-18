import time

from . import User
from . import Tweet

class Twitter(object):
    """
    Virtual Twitter Model
    """
    def __init__(self, db, round_id):
        self.db = db
        self.round_id = round_id

    @property
    def usernames(self):
        return self.db.get_usernames_for_round(self.round_id)

    def get_user(self, username):
        if self.db.is_username_in_round(self.round_id, username):
            return User(self.db, self.round_id, username)
        else:
            return None

    def create_user(self, username):
        self.db.add_username_to_round(self.round_id, username)
        return User(self.db, self.round_id, username)

    @property
    def tweets(self):
        return self.db.get_tweets_for_round(self.round_id)

    def add_tweet(self, username, content):
        now = int(time.time())
        tweet = Tweet(self.db, username, content, now)
        User(self.db, self.round_id, username).add_tweet(tweet)
        self.db.add_tweet_to_round(self.round_id, tweet)
        return tweet

    def url(self):
        return "/round/%s" % self.round_id

    def users_url(self):
        return self.url() + "/twitter/users"

    def tweets_url(self):
        return self.url() + "/twitter/tweets"
