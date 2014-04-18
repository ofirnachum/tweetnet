

class User(object):

    def __init__(self, db, round_id, username):
        self.db = db
        self.round_id = round_id
        self.username = username

    @property
    def tweets(self):
        return self.db.get_tweets_for_user_and_round(self.username, self.round_id)

    def add_tweet(self, tweet):
        self.db.add_tweet_for_user_and_round(self.username, self.round_id, tweet)

    @property
    def followers(self):
        return self.db.get_followers_for_user_and_round(self.username, self.round_id)

    def add_follower(self, user):
        return self.db.add_follower_for_user_and_round(self.username, self.round_id, user)

    def as_dict(self):
        return {
            'username': self.username,
            'followers': list(self.followers),
            'tweets': [t.as_dict() for t in self.tweets]
        }
    