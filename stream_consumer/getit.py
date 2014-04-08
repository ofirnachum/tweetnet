"""
gets a streeem
"""
import os
import sys

import tweepy

consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']

access_key = os.environ['TWITTER_ACCESS_KEY']
access_secret = os.environ['TWITTER_ACCESS_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)

class MyStreamListener(tweepy.streaming.StreamListener):
    def on_status(self, s):
        print s

    def on_exception(self, e):
        sys.stderr.write(str(e) + "\n")

st = tweepy.streaming.Stream(auth, MyStreamListener())
st.firehose()
