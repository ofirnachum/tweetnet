
from . import make_uuid
from flag import Flag

import hashlib

def md5hash(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

class Round(object):

    def __init__(self, db, round_id):
        self.db = db
        self.round_id = round_id

    @property
    def flags(self):
        return self.db.get_flags_for_round(self.round_id)

    def add_flag(self, size, contents):
        if size == 'small':
            flag_id = make_uuid()
        else:
            flag_id = md5hash(self.round_id + "||" + contents)

        flag = Flag(self.db, flag_id, size, contents)
        self.db.add_flag_for_round(self.round_id, flag)

    def url(self):
        return "/round/%s" % self.round_id

    def flags_url(self):
        return self.url() + "/flags"