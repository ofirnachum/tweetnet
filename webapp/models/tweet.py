import json

class Tweet(object):

    @classmethod
    def from_json(cls, db, json_string):
        obj = json.loads(json_string)
        return cls(db, **obj)

    def __init__(self, db, username, content, timestamp):
        self.db = db
        self.username = username
        self.content = content
        self.timestamp = timestamp

    def as_dict(self):
        return {
            'username': self.username,
            'content': self.content,
            'timestamp': self.timestamp,
        }

    def to_json(self):
        return json.dumps(self.as_dict())
