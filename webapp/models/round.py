import time

from . import make_uuid

from . import Twitter
from . import Flag

import hashlib

def md5hash(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

NBOTS = 10

class Round(object):

    def __init__(self, db, round_id):
        self.db = db
        self.round_id = round_id

        self.bot_ids = [str(i) for i in range(0, NBOTS)]

    @property
    def flags(self):
        return self.db.get_flags_for_round(self.round_id)

    def add_flag(self, size, contents):
        if size == 'small':
            flag_id = make_uuid()
        else:
            flag_id = md5hash(self.round_id + "||" + contents)

        flag = Flag(self.db, flag_id, size, contents, int(time.time()))
        self.db.add_flag_for_round(self.round_id, flag)

    @property
    def twitter(self):
        return Twitter(self.db, self.round_id)

    def url(self):
        return "/round/%s" % self.round_id

    def flags_url(self):
        return self.url() + "/flags"