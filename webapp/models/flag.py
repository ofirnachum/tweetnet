import json

class Flag(object):

    @classmethod
    def from_json(cls, db, json_string):
        obj = json.loads(json_string)
        return cls(
            db,
            obj['flag_id'],
            obj['size'],
            obj['content'],
        )

    def __init__(self, db, flag_id, size, content):
        self.db = db
        self.flag_id = flag_id
        self.size = size
        self.content = content

    def url(self):
        return "/flags/%s" % self.flag_id

    def as_dict(self):
        return {
            'flag_id':self.flag_id,
            'size':self.size,
            'content':self.content,
        }

    def to_json(self):
        return json.dumps(self.as_dict())

    def __repr__(self):
        return repr(self.as_dict())