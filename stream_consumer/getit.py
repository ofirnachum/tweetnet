"""
gets a streeem
"""
import os
import sys

import tweepy

from stream_listener import TweetnetStreamListener

def authenticate(consumer_key, consumer_secret, access_key, access_secret):


    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return auth

def getn(n, consumer_key, consumer_secret, access_key, access_secret):
    auth = authenticate(consumer_key, consumer_secret, access_key, access_secret)

    # I think I have do do this because python doesn't
    # lift like javascript..??????? maybe??????????
    st_h = {}
    out = []
    def handler(s):
        st_h['c'] += 1
        if s.lang == 'en':
            out.append(s)
            if len(out) == n:
                st_h['s'].disconnect()

    auth = authenticate(consumer_key, consumer_secret, access_key, access_secret)
    st_h['c'] = 0
    st_h['s'] = tweepy.streaming.Stream(auth, TweetnetStreamListener(handler))
    st_h['s'].sample()
    return out

if __name__ == "__main__":
    try:
        consumer_key = os.environ['TWITTER_CONSUMER_KEY']
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']

        access_key = os.environ['TWITTER_ACCESS_KEY']
        access_secret = os.environ['TWITTER_ACCESS_SECRET']
    except KeyError as e:
        print "You are missing an environment variable %r" % e.args[0]
        print "get it."
        sys.exit(1)

    for t in getn(100, consumer_key, consumer_secret, access_key, access_secret):
        print t.text
