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
        if (self.queue and (random.random() * self.tweet_period < 1)):
            content = self.queue.pop(0);
            self.api.tweet(self.user, content);
            return content;
        return False;


class HashBotMaster(BotMaster):
	def __init__(self, *args, **kwargs):
		super(HashBotMaster, self).__init__(*args, **kwargs);
		self.queue1 = TweetQueue(self.botmaster1, self.api);
		self.queue2 = TweetQueue(self.botmaster2, self.api);

	def tweet_flag(self, flag):


    def run(self):
        while True:
            flags = self.get_new_flags()
            if flags:
                for flag in flags:
                    self.tweet_flag(flag);
                    self.api.tweet(self.user, "#wow %s" % flag)
            
            time.sleep(3)



