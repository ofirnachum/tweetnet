"""
API that we can develop behind
"""

from tweetnet import BaseTweetnet
from twitter_mixins import *
from realistic_mixins import *
from flags_mixins import *


class Tweetnet(MockTwitterMixin, WebappRealisticMixin, WebappFlagsMixin, BaseTweetnet):
    pass


class DevTweetnet(MockTwitterMixin, DeterministicRealisticMixin, WebappFlagsMixin, BaseTweetnet):
    pass


TYPES = {
    'default': Tweetnet,
    'dev': DevTweetnet,
}

def get_api_type(flag):
    return TYPES[flag]
