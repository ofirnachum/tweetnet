"""
Different Mixins for twitter functionality
"""
import requests

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

    def _get_all_users(self):
        raise NotImplementedError

    def _get_user(self, username):
        raise NotImplementedError

    def _get_tweets(self):
        raise NotImplementedError

    def _query_tweets(self, query):
        raise NotImplementedError


class MockTwitterMixin(BaseTwitterMixin):
    """
    calls out to the api
    """

    def _twitter_url(self):
        return self.API_ROOT + ("/round/%s/twitter" % self.round_id)

    def _create_user(self, username):
        url = self._twitter_url() + "/users"
        r = requests.post(url, {'username': username})
        r.raise_for_status()
        return r.json()

    def _add_follower(self, followed, follower):
        url = self._twitter_url() + ("/users/%s/followers" % followed)
        r = requests.post(url, {'username': follower})
        r.raise_for_status()
        return r.json()

    def _tweet(self, username, content):
        url = self._twitter_url() + "/tweets"
        r = requests.post(url, {'username':username, 'content':content})
        r.raise_for_status()
        return r.json()

    def _get_all_users(self):
        url = self._twitter_url() + "/users"
        r = requests.get(url)
        r.raise_for_status()
        return r.json()['usernames']

    def _get_user(self, username):
        url = self._twitter_url() + ("/users/%s" % username)
        r = requests.get(url)
        r.raise_for_status()
        return r.json()

    def _get_tweets(self):
        url = self._twitter_url() + "/tweets"
        r = requests.get(url)
        r.raise_for_status()
        return r.json()['tweets']

    def _query_tweets(self, query):
        return [tweet for tweet in self.get_tweets() if query in tweet['content']]


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
