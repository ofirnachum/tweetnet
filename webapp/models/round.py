
from . import make_uuid
from . import Flag

class Round(object):

    def __init__(self, db, round_id):
        self.db = db
        self.round_id = round_id

    @property
    def flags(self):
        return self.db.get_flags_for_round(self.round_id)

    def add_flag(self, size, contents):
        flag_id = make_uuid()
        flag = Flag(self.db, flag_id, size, contents)
        self.db.add_flag_for_round(self.round_id, flag)

    def url(self):
        return "/round/%s" % self.round_id

    def flags_url(self):
        return self.url() + "/flags"