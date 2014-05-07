import time
import threading
import random

from common import Bot

import hash_common
import hash_secrets

# States enum
STATE_FLAG_WAITING = 'waiting on a flag start signal to arrive'
STATE_RECEIVING_FLAG = 'in the process of building up a flag'

class HashBot(Bot):

    def __init__(self, *args, **kwargs):
        super(HashBot, self).__init__(*args, **kwargs)
        self.bm1_seen_tweets = set()
        self.bm2_seen_tweets = set()

        self.bm1_state_machine = HashBotStateMachine(self.api, self.bot_id)
        self.bm2_state_machine = HashBotStateMachine(self.api, self.bot_id)


    def run(self):
        while True:
            bm1_tweets = [t['content'] for t in self.api.get_user(self.botmaster1)['tweets']]
            for tweet in bm1_tweets:
                if not tweet in self.bm1_seen_tweets:
                    self.bm1_state_machine.process_tweet(tweet)
                    self.bm1_seen_tweets.add(tweet)

            bm2_tweets = [t['content'] for t in self.api.get_user(self.botmaster2)['tweets']]
            for tweet in bm2_tweets:
                if not tweet in self.bm2_seen_tweets:
                    self.bm2_state_machine.process_tweet(tweet)
                    self.bm2_seen_tweets.add(tweet)
            time.sleep(2)


class HashBotStateMachine(object):

    def __init__(self, api, bot_id):
        self.api = api
        self.bot_id = bot_id
        self.transition_to_waiting()
        self.growing_signal = [];

    def transition_to_waiting(self):
        print "Transitioning to state waiting"
        self.state = STATE_FLAG_WAITING
        self.growing_flag = []
        self.growing_signal = [];
        self.prng = None
        self.pending_padding = None

    def transition_to_receiving(self, tweet):
        print "Transitioning to state receiving"
        self.state = STATE_RECEIVING_FLAG
        seed = hash_common.compute_seed(tweet)
        self.otp = hash_common.compute_otp(tweet);
        self.prng = random.Random(seed)
        self.pending_padding = self.prng.randint(hash_secrets.PADDING_RANGE_START, hash_secrets.PADDING_RANGE_END)

    def process_tweet(self, tweet):
        tweet_value = hash_common.compute_value(tweet);
        if self.state == STATE_RECEIVING_FLAG:
            if self.pending_padding == 0:
                # THEN THIS IS A FLAG TWEET YIPPPEE
                self.growing_flag.append(tweet_value)
                print "Got flag component!: ", self._flag_string()

                # check if we're at the end of the line
                if len(self.growing_flag) == 32:
                    self.submit_flag()
                    self.transition_to_waiting()
                else:
                    # Reset pending_padding for next chunk
                    self.pending_padding = self.prng.randint(hash_secrets.PADDING_RANGE_START, hash_secrets.PADDING_RANGE_END)
            else:
                # Then this is just a padding, ignore it.
                self.pending_padding -= 1

        elif self.state == STATE_FLAG_WAITING:
            # If it is a signal, transition!
            self.growing_signal.append(tweet_value);
            if (len(self.growing_signal) > len(hash_secrets.SIGNAL_VALUE)):
                self.growing_signal.pop(0);
            if self.growing_signal == hash_secrets.SIGNAL_VALUE:
                self.transition_to_receiving(tweet)
            else:
                # just ignore it
                pass
        else:
            raise RuntimeError("What kind of fucking state are you in???")

    def submit_flag(self):
        # TODO: start a thread that will submit the flag in some amount of time
        # for now, just submit it right away
        print "Submitting flag....."
        print "OTP: " + self.otp;
        flag = hash_common.compute_xor(self._flag_string(), self.otp);
        self.api.submit_small_flag(flag, self.bot_id)

    def _flag_string(self):
        return ''.join([hex(v)[-1] for v in self.growing_flag])