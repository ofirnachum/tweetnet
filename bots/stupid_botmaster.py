"""
example of a stupid botmaster
"""
import time

from common import BotMaster


class StupidBotMaster(BotMaster):

    def run(self):
        while True:
            flags = self.get_new_flags()
            if flags:
                for flag in flags:
                    print "found one: %s" % flag
                    print "tweeting '#wow %s'" % flag
                    self.api.tweet(self.user, "#wow %s" % flag)

            time.sleep(3)
