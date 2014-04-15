import os
import json

import flask
app = flask.Flask(__name__)
app.debug = True

from models import Database

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
    return flask.render_template('round.html', round=round)

@app.route("/round/<round_id>/flags", methods=('GET', 'POST'))
def round_flags(round_id):
    d = db()
    round = d.get_round(round_id)

    if flask.request.method == 'GET':
        flags = round.flags
        return flask.jsonify({
            'count': len(flags),
            'flags': [flag.as_dict() for flag in flags],
        })
    else:
        round.add_flag(flask.request.form['size'], flask.request.form['contents'])
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
            return flask.jsonify({'ok':True}),  201


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 6857))
    app.run('0.0.0.0', port=port)