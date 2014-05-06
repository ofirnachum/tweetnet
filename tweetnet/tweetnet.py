import hashlib
import os

from enforce_roles import restrict_to_roles

class BaseTweetnet(object):
    """
    Different subclasses of this API class set different roles
    this is to enforce our internal rules about which agents
    are allowed to do what, yet still keep things in one class
    An alternative would be to use mixins to create the subclasses.
    
    Currently there exist:
    - bot: for the bot programs
    - benign: for benign people
    - admin: for set up
    """

    API_ROOT = os.environ.get('TWEETNET_API_SERVER', 'http://localhost:6857')

    def __init__(self, round_id, role, *args ,**kwargs):
        """
        round_id is the id of the round for this tweetnet.
        """
        self.round_id = round_id
        self.role = role

    @restrict_to_roles('bot')
    def submit_small_flag(self, flag_id, submitter_id):
        """
        Submits a small flag

        raises RuntimeError if unable to

        returns False if not a flag
        returns True if a flag
        """
        return self._submit_small_flag(flag_id, submitter_id)

    @restrict_to_roles('bot')
    def submit_large_flag(self, content, submitter_id):
        """
        submits a large flag

        raises RuntimeError if unable to
        """
        m = hashlib.md5()
        m.update(self.round_id + "||" + content)
        return self._submit_small_flag(m.hexdigest(), submitter_id)

    @restrict_to_roles('admin', 'master')
    def get_flags(self, since=None):
        """
        Gets flags. Since argument will
        filter to after timestamp given.
        """
        return self._get_flags(since)

    @restrict_to_roles('benign', 'admin', 'master')
    def get_realistic_tweet(self):
        """
        Somehow, gets and returns a realistic looking tweet,
        for use by benign people.

        This returns a _string_, not a Tweet
        """
        return self._get_realistic_tweet()

    @restrict_to_roles('admin')
    def create_user(self, username):
        """
        trys to create a handle with the given username.

        returns the new User

        raises RuntimeError if unable to
        """
        return self._create_user(username)

    @restrict_to_roles('admin')
    def add_follower(self, followed, follower):
        """
        given two usernames, tries to make the second follow the first.

        returns the modified User

        raises RuntimeError if unable to
        """
        return self._add_follower(followed, follower)

    @restrict_to_roles('admin', 'master', 'benign')
    def tweet(self, username, tweet):
        """
        broadcasts the given tweet as the specified user

        returns the new tweet object

        raises RuntimeError if unable to
        """
        return self._tweet(username, tweet)

    def get_all_users(self):
        """
        returns all the users
        """
        return self._get_all_users()

    def get_user(self, username):
        """
        returns User object with given username
         - followers
         - tweets

        raises RuntimeError if unable to
        """
        return self._get_user(username)

    def get_tweets(self):
        """
        returns all the Tweets related to this game
        """
        return self._get_tweets()

    def query_tweets(self, query):
        """
        returns tweets matching given query
        """
        return self._query_tweets(query)
