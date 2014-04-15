"""
submits a flag

SHOULD NOT be used except for testing. so exits at the end.

"""
from tweetnet import Tweetnet

import sys

round_id = sys.argv[1]
api = Tweetnet(round_id, role='bot')

if sys.argv[2] == '-f':
    flag_source = sys.argv[3]
    submitter_id = sys.argv[4]
    with open(flag_source, 'r') as f:
        content = f.read()
    api.submit_large_flag(content, submitter_id)
else:
    flag_id = sys.argv[2]
    submitter_id = sys.argv[3]
    api.submit_small_flag(flag_id, submitter_id)


sys.exit(0)
