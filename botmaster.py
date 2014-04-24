from common import BotMaster


class SingleCharBotMaster(BotMaster):

    def submit_flag(self, flag_id):
        sent_char = 0
        rand_num = self.prng.next()
        count = rand_num
        while sent_char < len(flag_id):
            tweet = self.api.get_realistic_tweet()
            if count != 0:
                count -= 1
            else:
                rand_num = self.prng.next()
                count = rand_num
                tweet = self.insert_char(rand_num,
                                         flag_id[sent_char], tweet)
                sent_char += 1

            self.api.tweet(self.user, tweet)

    def insert_char(self, rand_num, char, tweet):
        content = list(tweet['content'])
        index = rand_num % len(content)
        content[index] = char  # replace w/char
        tweet['content'] = content
        return tweet
