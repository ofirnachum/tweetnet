import hashlib
import os

import requests

from enforce_roles import restrict_to_roles

# TEMPORARY
from webapp.main import TWEETNET_DEV_DB

class Tweetnet(object):

    # Different subclasses of this API class set different roles
    # this is to enforce our internal rules about which agents
    # are allowed to do what, yet still keep things in one class
    # An alternative would be to use mixins to create the subclasses.
    #
    # Currently there exist:
    # - bot: for the bot programs
    # - benign: for benign people
    # - admin: for set up

    ROLE = None
    API_ROOT = os.environ.get('TWEETNET_API_SERVER', 'http://localhost:6857')

    def __init__(self, round_id, *args ,**kwargs):
        """
        round_id is the id of the round for this tweetnet.
        """
        self.round_id = round_id

        # TEMPORARY!!
        import redis
        self._r = redis.Redis(host='localhost', port=6379, db=TWEETNET_DEV_DB)

    @restrict_to_roles('bot')
    def submit_small_flag(self, flag_id, submitter_id):
        """
        Submits a small flag

        raises RuntimeError if unable to

        returns False if not a flag
        returns True if a flag
        """
        url = self.API_ROOT + "/flags/" + flag_id
        # TODO catch error?
        r = requests.post(url, data={'submitter_id' : submitter_id})
        return r.status_code == 201

    @restrict_to_roles('bot')
    def submit_large_flag(self, content, submitter_id):
        """
        submits a large flag

        raises RuntimeError if unable to
        """
        m = hashlib.md5()
        m.update(self.round_id + "||" + content)
        return self.submit_small_flag(m.hexdigest(), submitter_id)

    @restrict_to_roles('benign', 'admin')
    def get_realistic_tweet(self):
        """
        Somehow, gets and returns a realistic looking tweet,
        for use by benign people.

        This returns a _string_, not a Tweet
        """
        return "#lol twitter is gr8 #shitpeoplesay"

    @restrict_to_roles('admin')
    def create_user(self, username):
        """
        trys to create a handle with the given username.

        returns the new User

        raises RuntimeError if unable to
        """
        pass

    @restrict_to_roles('admin')
    def add_follower(self, followed, follower):
        """
        given two usernames, tries to make the second follow the first.

        returns the modified User

        raises RuntimeError if unable to
        """
        pass

    def tweet(self, username, tweet):
        """
        broadcasts the given tweet as the specified user

        returns the new tweet object

        raises RuntimeError if unable to
        """
        # TEMPORARY
        self._r.rpush('tweets', "%s:%s" % (username, tweet))
        print "%s tweets: %s" % (username, tweet)

    def get_user(self, username):
        """
        returns User object with given username
         - followers
         - tweets
        
        raises RuntimeError if unable to
        """
        pass

    def get_tweets(self):
        """
        returns all the Tweets related to this game
        """
        # TEMPORARY
        return [t.split(':') for t in self._r.lrange("tweets", 0, -1)]

    def query_tweets(self, query):
        """
        returns tweets matching given query
        """
        # TEMPORARY
        return [(user, tweet) for user, tweet in self.get_tweets() if query in tweet]


# And now the subclasses
class AdminTweetnet(Tweetnet):
    ROLE = 'admin'

class BotTweetnet(Tweetnet):
    ROLE = 'bot'

class BenignTweetnet(Tweetnet):
    ROLE = 'benign'
