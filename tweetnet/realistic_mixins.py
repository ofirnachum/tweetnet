"""
Mixins for getting realistic tweets
"""
import requests

class BaseRealisticMixin(object):

    def _get_realistic_tweet(self):
        raise NotImplementedError


class DeterministicRealisticMixin(BaseRealisticMixin):

    def __init__(self, *args, **kwargs):
        super(DeterministicRealisticMixin, self).__init__(*args, **kwargs)
        self._realistic_sequence_number = 0

    def _get_realistic_tweet(self):
        t = '#realistic tweet %d' % self._realistic_sequence_number
        self._realistic_sequence_number += 1
        return t


class WebappRealisticMixin(BaseRealisticMixin):
    def _get_realistic_tweet(self):
        url = self.API_ROOT + '/sample'
        r = requests.get(url)
        r.raise_for_status()
        return r.json()['text']

class ConstantRealisticMixin(BaseRealisticMixin):
    """
    returns a constant
    """

    def _get_realistic_tweet(self):
        return "#lol twitter is gr8 #shitpeoplesay"
