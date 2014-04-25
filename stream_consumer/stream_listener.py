import sys

import tweepy

class TweetnetStreamListener(tweepy.streaming.StreamListener):

    def __init__(self, handler):
        tweepy.streaming.StreamListener.__init__(self)
        self.handler = handler

    def on_status(self, s):
        self.handler(s)

    def on_exception(self, e):
        sys.stderr.write(str(e) + "\n")

    def on_closed(self, r):
        print r