"""
gets a streeem
"""
import os
import sys

import tweepy

from stream_listener import TweetnetStreamListener

def authenticate():
    try:
        consumer_key = os.environ['TWITTER_CONSUMER_KEY']
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']

        access_key = os.environ['TWITTER_ACCESS_KEY']
        access_secret = os.environ['TWITTER_ACCESS_SECRET']
    except KeyError as e:
        print "You are missing an environment variable %r" % e.args[0]
        print "get it."
        sys.exit(1)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return auth

auth = authenticate()
st = tweepy.streaming.Stream(auth, TweetnetStreamListener())
st.sample()
