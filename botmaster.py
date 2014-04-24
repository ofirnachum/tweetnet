from common import prng


class BotMaster(object):

    def __init__(self, user, api):
        self.user = user
        self.api = api
        self.prng = prng()  # TODO: make object

    def submit_flag(self, flag_id):
        raise NotImplementedError


class SingleCharBotMaster(BotMaster):

    def submit_flag(self, flag_id):
        sent_char = 0
        rand_num = self.prng.next()  # every how many tweets?
        while sent_char < len(flag_id):
            tweet = self.api.get_realistic_tweet()
            if rand_num == 0:
                rand_num = self.prng.next()
                tweet = self.insert_char(rand_num,
                                         flag_id[sent_char], tweet)
                sent_char += 1

            self.api.tweet(self.user, tweet)

    def insert_char(self, rand_num, char, tweet):
        content = list(tweet['content'])
        rand_num %= len(content)
        content[rand_num] = char  # replace w/char
        tweet['content'] = content
        return tweet
