"""
example of a stupid botmaster
"""
import sys
import time

from common import BotMaster

class StupidBotMaster(BotMaster):

    def run(self):
        while True:
            flags = self.get_new_flags()
            if flags:
                for flag in flags:
                    print "found one: %s" % flag['flag_id']
                    print "tweeting '#wow %s'" % flag['flag_id']
                    self.api.tweet(self.user, "#wow %s" % flag['flag_id'])

        time.sleep(3)
