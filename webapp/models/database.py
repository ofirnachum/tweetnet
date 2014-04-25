"""
source of models
"""
import redis
from . import Round
from . import Flag
from . import Tweet

class Database(object):

    def __init__(self, **kwargs):
        if 'url' in kwargs:
            self.r = redis.from_url(kwargs['url'])
        else:
            self.r = redis.Redis(**kwargs)

    def get_round(self, round_id):
        return Round(self, round_id)

    def get_flags_for_round(self, round_id):
        string_flags = self.r.lrange("round:%s:flags" % round_id, 0, -1)
        return [Flag.from_json(self, s) for s in string_flags]

    def add_flag_for_round(self, round_id, flag):
        flag_json = flag.to_json()
        self.r.rpush("round:%s:flags" % round_id, flag_json)
        self.r.set("flags:%s" % flag.flag_id, flag_json)

    def get_flag(self, flag_id):
        flag_json = self.r.get("flags:%s" % flag_id)
        if flag_json:
            return Flag.from_json(self, flag_json)
        else:
            return None

    def get_submissions_for_flag(self, flag_id):
        return self.r.smembers("flags:%s:submissions" % flag_id)

    def add_submission_for_flag(self, flag_id, submitter_id):
        self.r.sadd("flags:%s:submissions" % flag_id, submitter_id)


    def get_usernames_for_round(self, round_id):
        return self.r.smembers("round:%s:twitter:usernames" % round_id)

    def add_username_to_round(self, round_id, username):
        self.r.sadd("round:%s:twitter:usernames" % round_id, username)

    def is_username_in_round(self, round_id, username):
        return self.r.sismember("round:%s:twitter:usernames" % round_id, username)

    def get_tweets_for_round(self, round_id):
        tweet_strings = self.r.lrange("round:%s:twitter:tweets" % round_id, 0, -1)
        return [Tweet.from_json(self, s) for s in tweet_strings]

    def add_tweet_to_round(self, round_id, tweet):
        tweet_json = tweet.to_json()
        self.r.rpush("round:%s:twitter:tweets" % round_id, tweet_json)


    def add_follower_for_user_and_round(self, username, round_id, follower):
        return self.r.sadd("round:%s:twitter:users:%s:followers" % (round_id, username), follower)

    def get_followers_for_user_and_round(self, username, round_id):
        return self.r.smembers("round:%s:twitter:users:%s:followers" % (round_id, username))

    def add_tweet_for_user_and_round(self, username, round_id, tweet):
        tweet_json = tweet.to_json()
        self.r.rpush("round:%s:twitter:users:%s:tweets" % (round_id, username), tweet_json)

    def get_tweets_for_user_and_round(self, username, round_id):
        tweet_strings = self.r.lrange("round:%s:twitter:users:%s:tweets" % (round_id, username), 0, -1)
        return [Tweet.from_json(self, s) for s in tweet_strings]

    def get_sample_tweet(self):
        return self.r.lpop("sampletweets")

    def add_sample_tweet(self, text):
        return self.r.rpush("sampletweets", text)
