import math

window = 12;
half_window = window // 2;

def sweet_spot(time):
	"""
    returns True iff time is in a 'sweetspot'
    """
	return (time // half_window) % 2 == 0;

def significant(num_correct_tweets, num_users):
	"""
    returns True iff number of 'sweetspot' tweets
    	found is significant
    """
	return num_correct_tweets > 4 + math.log(num_users);


# Punctuation table used for communication
to_punctuation_map = {-1: u' ', 0: u'.', 1: u',', 2: u'!', 3: u'?'};
from_punctuation_map = dict((v,k) for k, v in to_punctuation_map.iteritems());

def to_punctuation(num):
	num = num % 4;
	return to_punctuation_map[num];

def from_punctuation(punc):
	return from_punctuation_map[punc];