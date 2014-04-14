"""
source of models
"""
import redis
from . import Round
from . import Flag

class Database(object):

    def __init__(self, **kwargs):
        self.r = redis.Redis(**kwargs)

    def get_round(self, round_id):
        return Round(self, round_id)

    def get_flags_for_round(self, round_id):
        string_flags = self.r.lrange("round:%s:flags" % round_id, 0, -1)
        return [Flag.from_json(self, s) for s in string_flags]

    def add_flag_for_round(self, round_id, flag):
        flag_json = flag.to_json()
        self.r.rpush("round:%s:flags" % round_id, flag_json)
        self.r.set("flags:%s" % flag.flag_id, flag_json)

    def get_flag(self, flag_id):
        flag_json = self.r.get("flags:%s" % flag_id)
        if flag_json:
            return Flag.from_json(self, flag_json)
        else:
            return None