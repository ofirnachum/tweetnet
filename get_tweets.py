import json
import sys
import os

if (len(sys.argv) < 2):
	sys.exit("Issue a command in the form:\n    python " + sys.argv[0] + " 'query' number");

# Search query
query = sys.argv[1];
# Number of desired query results
number = sys.argv[2];

# Path to tweepy
sys.path.append("/mit/ofir/6857/tweepy-2.2/");
import tweepy

# Keys given by Twitter
consumer_key = 
consumer_secret = 
access_token = 
access_token_secret = 

# Tweepy setup
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Attributes of tweet to extrac
# There is also an 'author' attribute which we do not 
# use for now.
attributes = [
	'contributors', 
	'coordinates', 
	'created_at', 
	'entities', 
	'favorite_count', 
	'favorited', 
	'geo', 
	'id', 
	'id_str', 
	'in_reply_to_screen_name', 
	'in_reply_to_status_id', 
	'in_reply_to_status_id_str', 
	'in_reply_to_user_id', 
	'in_reply_to_user_id_str', 
	'lang', 
	'metadata',  
	#'place', 
	'retweet_count', 
	'retweeted', 
	'source', 
	'source_url', 
	'text', 
	'truncated']

# Current count of query results
count = 0;
id = float('inf');
all_tweets = [];
while (count < number):
	public_tweets = api.search(query, max_id = id-1);
	if (len(public_tweets) == 0): break;
	for tweet in public_tweets:
		count += 1;
		if (tweet.id < id):
			id = tweet.id;
		# Only get attributes we care about
		new_tweet = {};
		for a in attributes:
			new_tweet[a] = getattr(tweet, a);
			if (a == "created_at"):
				new_tweet[a] = str(new_tweet[a]);
		all_tweets.append(new_tweet);

print json.dumps(all_tweets)


