import uuid

def make_uuid():
    return uuid.uuid4().hex

from flag import Flag
from round import Round

from database import Database