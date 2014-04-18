"""
Mixins for getting realistic tweets
"""

class BaseRealisticMixin(object):

    def _get_realistic_tweet(self):
        raise NotImplementedError


class ConstantRealisticMixin(BaseRealisticMixin):
    """
    returns a constant
    """

    def _get_realistic_tweet(self):
        return "#lol twitter is gr8 #shitpeoplesay"
