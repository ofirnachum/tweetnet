"""
Mixins for flag submission behavior
"""
import requests

class BaseFlagsMixin(object):

    def _submit_small_flag(self, flag_id, submitter_id):
        raise NotImplementedError

    def _get_flags(self, since):
        raise NotImplementedError

class WebappFlagsMixin(BaseFlagsMixin):

    def _submit_small_flag(self, flag_id, submitter_id):
        url = self.API_ROOT + "/flags/" + flag_id
        r = requests.post(url, data={'submitter_id' : submitter_id})
        r.raise_for_status()
        return r.status_code == 201

    def _get_flags(self, since):
        if since is None:
            data = {}
        else:
            data = {'since': since}
        url = self.API_ROOT + ("/round/%s/flags" % self.round_id)
        r = requests.get(url, params=data)
        r.raise_for_status()
        return r.json()['flags']
