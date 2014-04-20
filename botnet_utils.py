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
	return num_correct_tweets > math.log(5) + math.log(num_users);	