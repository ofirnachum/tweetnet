"""
1 character per tweet
"""
import sys
import time

from tweetnet import Tweetnet
from botmaster import SingleCharBotMaster, HashBotMaster

TYPES = {
    'SingleCharBotMaster': SingleCharBotMaster,
    'HashBotMaster': HashBotMaster,
}

if __name__ == "__main__":
    round_id = sys.argv[1]
    user = sys.argv[2]
    botmaster_type = sys.argv[3]
    api = Tweetnet(round_id, role='admin')

    master = TYPES[botmaster_type](user, api)

    master.run()
