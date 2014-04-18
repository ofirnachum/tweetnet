import uuid

def make_uuid():
    return uuid.uuid4().hex


from tweet import Tweet
from user import User
from twitter import Twitter

from flag import Flag
from round import Round

from database import Database