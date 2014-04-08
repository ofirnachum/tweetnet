import sys

import tweepy

class TweetnetStreamListener(tweepy.streaming.StreamListener):
    def on_status(self, s):
        # put it in queue...
        print s.user.name, "is not a botnet"

    def on_exception(self, e):
        sys.stderr.write(str(e) + "\n")