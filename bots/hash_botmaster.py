"""
example of a stupid botmaster
"""
import time

from common import BotMaster

class TweetQueue:
    # NOTE: Tweet frequency is relative
    # to how often you call 'pop'.
    def __init__(self, user, api, tweet_period=2):
        self.user = user;
        self.api = api;
        self.tweet_period = tweet_period;
        self.queue = [];

    def push(self, content):
        self.queue.append(content);

    def pop(self):
        # Successful pop happens
        # with probability 1/tweet_period
        if (self.queue):
            content = self.queue.pop(0);
            return content;
        return False;


class HashBotMaster(BotMaster):
	def __init__(self, *args, **kwargs):
		super(HashBotMaster, self).__init__(*args, **kwargs);
		self.queue1 = TweetQueue(self.botmaster1, self.api);
		self.queue2 = TweetQueue(self.botmaster2, self.api);

	def get_tweet(self, predicate = lambda x: True):
		while True:
			tweet = self.api.get_realistic_tweet();
    		if predicate(tweet):
    			return tweet;

	def tweet_flag(self, flag):
		for c in flag:
			tweet = self.get_tweet(
				lambda x: (hash(x) % 16 == int(c, 16));
			self.queue1.push(tweet);

    def run(self):
        while True:
            flags = self.get_new_flags()
            if flags:
                for flag in flags:
                    self.tweet_flag(flag);
            tweet = self.queue1.pop();
            self.api.tweet(self.user, tweet);
            time.sleep(3)



