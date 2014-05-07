"""
util for hash bot
"""
import random
import hashlib
import hash_secrets

def md5int(string):
    h = hashlib.md5(string.encode('utf-8'))
    return int(h.hexdigest(), 16)

def compute_value(tweet):
	return int(md5int(tweet) % 16);

def compute_seed(tweet):
    ti = md5int(tweet)
    v = ti ^ hash_secrets.SEED_KEY
    return md5int(str(v))

def compute_otp(tweet, length=32):
	seed = compute_seed(tweet + "#yolo");
	prng = random.Random(seed)
	otp = "";
	for i in xrange(length):
		otp += str(prng.randint(0x0, 0xf))[-1];
	return otp;

def compute_xor(str1, str2):
	if (len(str1) != len(str2)):
		return None;
	xor = "";
	for i in xrange(len(str1)):
		xor += str(hex(int(str1[i], 16) ^ int(str2[i], 16)))[-1];
	return xor
