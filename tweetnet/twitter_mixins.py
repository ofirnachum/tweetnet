"""
Different Mixins for twitter functionality
"""
from tweetnet import BaseTweetnet

class BaseTwitterMixin(object):
    """
    abstract base class for different twitter backends
    """
    def _create_user(self, username):
        raise NotImplementedError

    def _add_follower(self, followed, follower):
        raise NotImplementedError

    def _tweet(self, username, tweet):
        raise NotImplementedError

    def _get_user(self, username):
        raise NotImplementedError

    def _get_tweets(self):
        raise NotImplementedError

    def _query_tweets(self, query):
        raise NotImplementedError


class JankyTwitterMixin(BaseTwitterMixin):
    """
    janks redis into use
    leaves:
     - create_user
     - add_follower
     - get_user
    unimplemented
    """

    def __init__(self, *args, **kwargs):
        BaseTweetnet.__init__(self, *args, **kwargs)

        import redis
        from webapp.main import TWEETNET_DEV_DB
        self._r = redis.Redis(host='localhost', port=6379, db=TWEETNET_DEV_DB)

    def _tweet(self, username, tweet):
        self._r.rpush('tweets', "%s:%s" % (username, tweet))
        print "%s tweets: %s" % (username, tweet)

    def _get_tweets(self):
        return [t.split(':') for t in self._r.lrange("tweets", 0, -1)]

    def _query_tweets(self, query):
        return [(user, tweet) for user, tweet in self.get_tweets() if query in tweet]
