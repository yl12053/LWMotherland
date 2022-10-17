import flask
from flask import render_template
from blueprint import apps
from flask_sqlalchemy import SQLAlchemy
from models.app_db import init, Model
from flask_login import LoginManager, login_required
import os

app = flask.Flask(__name__)
app.secret_key = "sctkey"
app.config["static_url_path"] = "assets"
app.config["static_folder"] = 'assets'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'homepage'


@login_manager.user_loader
def user_loader(usr):
    user = Model.Users
    return user.query.get(int(usr))


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQLAlchemy()
app.config[
    "SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://lwmotherland:lwmotherland@db4free.net/lwmotherland"
init(db, app)


@app.route("/assets/<path:path>")
def assets(path):
    return flask.send_from_directory("assets",
                                     path,
                                     conditional=False,
                                     as_attachment=False,
                                     download_name=None)


@app.route("/google95a4c2e4ac08c0ae.html", methods=["GET", "POST"])
def google_verification_verify():
    return open("static_root/google95a4c2e4ac08c0ae.html").read()


@app.route("/")
def root():
    return open("index.html", "r").read()


@app.route("/lb")
def leaderboard():
    return open("view.html", "r").read()


@app.route("/home")
def homepage():
    return render_template("homepage/home.html")


#@app.route("/login")
#def login():
#    return open("login.html", "r").read()


@app.route("/map")
@login_required
def map():
    return render_template("map/map.html",
                           asset_file="/assets/video/newmap.mp4",
                           type_asset="video",
                           width="2020",
                           height="1520")


for x in apps:
    app.register_blueprint(x)


@app.route("/<path:path>")
def asroot(path):
    return flask.send_from_directory("As_Root",
                                     path,
                                     conditional=False,
                                     as_attachment=False,
                                     download_name=None)


if __name__ == "__main__":
    app.run("0.0.0.0", 80)
