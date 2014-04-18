import json

class Flag(object):

    @classmethod
    def from_json(cls, db, json_string):
        obj = json.loads(json_string)
        return cls(db, **obj)

    def __init__(self, db, flag_id, size, contents, created_at):
        self.db = db
        self.flag_id = flag_id
        self.size = size
        self.contents = contents
        self.created_at = created_at

    @property
    def submissions(self):
        return self.db.get_submissions_for_flag(self.flag_id)

    def add_submission(self, submitter_id):
        self.db.add_submission_for_flag(self.flag_id, submitter_id)

    def url(self):
        return "/flags/%s" % self.flag_id

    def as_dict(self):
        return {
            'flag_id':self.flag_id,
            'size':self.size,
            'contents':self.contents,
            'created_at':self.created_at,
        }

    def to_json(self):
        return json.dumps(self.as_dict())

    def __repr__(self):
        return repr(self.as_dict())