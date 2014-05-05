"""
uses the twitter API to N realistic tweets
and put them in redis.

Reccommended number for a round is 10000
"""
import sys
import os

# Fuck it. Stick dir up from here into path.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

import tweepy

from models import Database

TWEETNET_DEV_DB = 7


def db():
    if os.environ.get('REDISTOGO_URL'):
        return Database(url=os.environ['REDISTOGO_URL'])
    else:
        # Assume local
        return Database(host='localhost', port=6379, db=TWEETNET_DEV_DB)


# Get text from a tweet from real twitter
api_key = 'bpzbu8YIoh7lZ4jUBTX1PsIdv'
# Horrible exposed secrets
api_secret = 'Mb407I4DPvvwejzMun8t3X9u19e52bFiDpdM7aUUbhWDpTj77N'

access_token = '2444646246-HejodGZWNtrB8kRFH36VDUWdEmvwQSewpEjqFeE'
access_token_secret = 'f0JKkRjEUoDdOpZB3g0rEs2SOlUy4A2uLLcRMcVYeXw1V'

n = int(sys.argv[1])
print n

chunk_size = 100
tweets = []

class TweetnetStreamListener(tweepy.streaming.StreamListener):

    def __init__(self):
        tweepy.streaming.StreamListener.__init__(self)
        self.count = 0

    def on_status(self, s):
        if self.count % 100 == 0:
            print self.count
        if self.count == n:
            return False
        if s.lang == 'en':
            tweets.append(s.text)
            self.count += 1

    def on_exception(self, e):
        sys.stderr.write(str(e) + "\n")

    def on_closed(self, r):
        print r

def authenticate(consumer_key, consumer_secret, access_key, access_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return auth

auth = authenticate(api_key, api_secret, access_token, access_token_secret)
s = tweepy.streaming.Stream(auth, TweetnetStreamListener())
s.sample()

# now, inject them into redis
print "Inserting them..."
d = db()
for tweet in tweets:
    d.add_sample_tweet(tweet)
