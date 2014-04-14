from main import TWEETNET_DEV_DB
from models import Database

d = Database(host='localhost', port=6379, db=TWEETNET_DEV_DB)
d.r.flushdb()