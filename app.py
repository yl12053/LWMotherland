import flask
from blueprint import apps
from flask_sqlalchemy import SQLAlchemy
from models.app_db import init

app = flask.Flask(__name__)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQLAlchemy()
app.config[
    "SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://lwmotherland%40lwmland:LWm3therland@lwmland.mysql.database.azure.com"
init(db, app)


@app.route("/assets/<path:path>")
def assets(path):
    return flask.send_from_directory("assets", path)


@app.route("/google95a4c2e4ac08c0ae.html", methods=["GET", "POST"])
def google_verification_verify():
    return open("static_root/google95a4c2e4ac08c0ae.html").read()


@app.route("/")
def root():
    return open("index.html", "r").read()


@app.route("/lb")
def leaderboard():
    return open("view.html", "r").read()


@app.route("/login")
def login():
    return open("login.html", "r").read()


@app.route("/map")
def map():
    return open("map.html", "r").read()


for x in apps:
    app.register_blueprint(x)

if __name__ == "__main__":
    app.run("0.0.0.0", 80)
