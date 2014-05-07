"""
util for hash bot
"""
import hashlib

import hash_secrets

def md5int(string):
    h = hashlib.md5(string)
    return int(h.hexdigest(), 16)

def compute_seed(tweet):
    ti = md5int(tweet)
    v = ti ^ hash_secrets.SEED_KEY
    return md5int(str(v))
