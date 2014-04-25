import os
import os.path
import json
import tweepy
import flask
import random
app = flask.Flask(__name__)
app.debug = True

from models import Database

# Fuck it. Stick dir up from here into path.
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

import stream_consumer

TWEETNET_DEV_DB = 7


def db():
    if os.environ.get('REDISTOGO_URL'):
        return Database(url=os.environ['REDISTOGO_URL'])
    else:
        # Assume local
        return Database(host='localhost', port=6379, db=TWEETNET_DEV_DB)


@app.route("/")
def index():
    return "Hi"


@app.route("/round/<round_id>")
def round_index(round_id):
    d = db()
    round = d.get_round(round_id)
    return flask.render_template('round.html', round=round, twitter=round.twitter)


@app.route("/round/<round_id>/flags", methods=('GET', 'POST'))
def round_flags(round_id):
    d = db()
    round = d.get_round(round_id)

    if flask.request.method == 'GET':
        flags = round.flags
        since = flask.request.args.get('since')
        if since is not None:
            since = int(since)
            flags = [f for f in flags if f.created_at >= since]

        return flask.jsonify({
            'count': len(flags),
            'flags': [flag.as_dict() for flag in flags],
        })
    else:
        round.add_flag(
            flask.request.form['size'], flask.request.form['contents'])
        return flask.redirect(round.url())


@app.route("/flags/<flag_id>", methods=('GET', 'POST'))
def flag_detail(flag_id):
    """
    GET for detail, POST for a submission
    """
    d = db()

    if flask.request.method == "GET":
        flag = d.get_flag(flag_id)
        if flag:
            return repr(flag)
        else:
            flask.abort(404)
    else:
        # it is a post
        flag = d.get_flag(flag_id)
        if not flag:
            flask.abort(404)
        else:
            # they got it!
            # so add it.
            # TODO: worry about malformed? nahhh...
            submitter_id = int(flask.request.form['submitter_id'])
            flag.add_submission(submitter_id)
            return flask.jsonify({'ok': True}),  201

# Twitter endpoints


@app.route("/round/<round_id>/twitter/users", methods=('GET', 'POST'))
def user_list(round_id):
    # Returns all usernames, or creates a user (for post)
    d = db()
    twitter = d.get_round(round_id).twitter

    if flask.request.method == 'GET':
        usernames = list(twitter.usernames)
        return flask.jsonify({
            'count': len(usernames),
            'usernames': usernames,
        })
    else:  # POST
        user = twitter.create_user(flask.request.form['username'])
        if flask.request.args.get('redirect_to'):
            return flask.redirect(flask.request.args['redirect_to'])
        else:
            return flask.jsonify(user.as_dict())


@app.route("/round/<round_id>/twitter/users/<username>")
def user_detail(round_id, username):
    d = db()
    twitter = d.get_round(round_id).twitter

    u = twitter.get_user(username)
    if u is None:
        flask.abort(404)
    else:
        return flask.jsonify(u.as_dict())


@app.route("/round/<round_id>/twitter/users/<username>/followers", methods=('POST',))
def add_follower(round_id, username):
    d = db()
    twitter = d.get_round(round_id).twitter

    follower = flask.request.form['username']
    if follower == username:
        flask.abort(400, "Cannot follow oneself")

    u = twitter.get_user(username)
    if u is None:
        flask.abort(404, "user not found")
    f = twitter.get_user(follower)
    if f is None:
        flask.abort(404, "follower not found")

    u.add_follower(follower)

    if flask.request.args.get('redirect_to'):
        return flask.redirect(flask.request.args['redirect_to'])
    else:
        return flask.jsonify(u.as_dict())


@app.route("/round/<round_id>/twitter/tweets", methods=('GET', 'POST'))
def tweet_list(round_id):
    # API get tweets or create
    # can have a `matching` query parameter which is interpreted
    # as a regex.
    d = db()
    twitter = d.get_round(round_id).twitter

    if flask.request.method == 'GET':
        tweets = twitter.tweets
        return flask.jsonify({
            'count': len(tweets),
            'tweets': [t.as_dict() for t in tweets],
        })
    else:  # POST
        tweeter = flask.request.form['username']
        if twitter.get_user(tweeter) is None:
            flask.abort(404, "User %s not found" % tweeter)
        tweet = twitter.add_tweet(tweeter, flask.request.form['content'])
        if flask.request.args.get('redirect_to'):
            return flask.redirect(flask.request.args['redirect_to'])
        else:
            return flask.jsonify(tweet.as_dict())


@app.route("/sample")
def sample_tweet():
    d = db()

    # Get text from a tweet from real twitter
    api_key = 'bpzbu8YIoh7lZ4jUBTX1PsIdv'
    # Horrible exposed secrets
    api_secret = 'Mb407I4DPvvwejzMun8t3X9u19e52bFiDpdM7aUUbhWDpTj77N'

    access_token = '2444646246-HejodGZWNtrB8kRFH36VDUWdEmvwQSewpEjqFeE'
    access_token_secret = 'f0JKkRjEUoDdOpZB3g0rEs2SOlUy4A2uLLcRMcVYeXw1V'

    tweet = d.get_sample_tweet()
    while tweet is None:
        # Fill her up
        for t in stream_consumer.getn(150, api_key, api_secret, access_token, access_token_secret):
            d.add_sample_tweet(t.text)
        tweet = d.get_sample_tweet()

    return flask.jsonify({'text': tweet})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 6857))
    app.run('0.0.0.0', port=port)
