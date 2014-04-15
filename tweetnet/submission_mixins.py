"""
Mixins for flag submission behavior
"""
import requests

class BaseSubmissionMixin(object):

    def _submit_small_flag(self, flag_id, submitter_id):
        raise NotImplementedError


class WebappSubmissionMixin(BaseSubmissionMixin):

    def _submit_small_flag(self, flag_id, submitter_id):
        url = self.API_ROOT + "/flags/" + flag_id
        # TODO catch error?
        r = requests.post(url, data={'submitter_id' : submitter_id})
        return r.status_code == 201
