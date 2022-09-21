from flask import Blueprint
import flask

app = Blueprint('app_leader', __name__)


@app.route("/leaderboard")
def leader():
    return flask.render_template("leaderboard/leaderboard.html")
