import uuid

def make_uuid():
    return uuid.uuid1().hex

from flag import Flag
from round import Round

from database import Database