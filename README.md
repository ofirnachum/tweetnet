tweetnet
========

 - stream\_consumer python module for consumption of twitter stream

 - webapp is a basic flask app for flag and game control

 - .tweetnet is a file that should contain required environment variables for storing auth
   we don't check them into git, for obvious reason. Get them from another team member.

 - requirements.txt has all the requirements, do a `virtualenv env && source env/bin/activate && pip install -r requirements.txt`



Infrastructure prototype
=========================

 1. Make sure you are in a virtualenv and have installed all requirements.
 2. Install redis on your system, make sure you have an instance running on your local host on the default port (6379)
    (if you do, running `redis-cli` should give you a redis prompt)
 3. WARNING this will clean out a local redis database, so don't do it if you care about stuff in your redis without
    changing the `TWEETNET_DEV_DB` variable in webapp/main.py. BUT then run: `python webapp/clear_db.py`.
 4. Start the webapp on port 6857: `python webapp/main.py`.
 5. In another terminal window, run `python round_runner.py 1 stupid_bot.py` to start 10 benign users and 10 infected
    computers in round 1.
 6. Go to `localhost:6857/rounds/1` and create a small flag (leave the text box empty). Grab its flag_id. for example,
    let's say it is `4699ae56b13e47e5af2d91958dace6bd`.
 7. In _another_ terminal window, run `python stupid_botmaster.py 1 botmaster 4699ae56b13e47e5af2d91958dace6bd`
    (substituting in your flag id).
 8. Shortly, the bots will see this tweet, and submit the flag. Yippee! (reload /round/1 and the bot ids will appear)

### EMBRACE THE JANK