import flask
import json
from flask_socketio import SocketIO, join_room, emit
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from models.app_db import init, Model
from blueprint import apps
from flask_login import LoginManager, login_required, current_user
import os
import sys

app = flask.Flask(__name__)
app.secret_key = "sctkey"
app.config["static_url_path"] = "assets"
app.config["static_folder"] = 'assets'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'homepage'
socketio = SocketIO(app)

if len(sys.argv) and sys.argv[-1] == "debug":
    app.config["T_DEBUG"] = True
else:
    app.config["T_DEBUG"] = False


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


if app.config["T_DEBUG"]:

    @app.route("/")
    def root():
        return open("index.html", "r").read()

    @app.route("/lb")
    def leaderboard():
        return open("view.html", "r").read()

    @app.route("/home")
    def homepage():
        return render_template("homepage/home.html")

else:

    @app.route("/")
    def root():
        return render_template("homepage/home.html")


@app.route("/map")
@login_required
def map():
    mdf = Model.player_position.query.filter_by(id=current_user.id).first()
    if mdf is not None:
        rerr = mdf.preventRedone
    else:
        rerr = 0
    return render_template("map/map.html",
                           asset_file="/assets/video/newmap.mp4",
                           type_asset="video",
                           width="2020",
                           height="1520",
                           rerr=str(rerr))


for x in apps:
    app.register_blueprint(x)


@app.route("/<path:path>")
def asroot(path):
    return flask.send_from_directory("As_Root",
                                     path,
                                     conditional=False,
                                     as_attachment=False,
                                     download_name=None)


@app.route(app.static_url_path + '/' + '<path:path>' + ".ts")
def jsonl_mime_type(path):
    return flask.send_from_directory(directory=app.static_folder,
                                     path=path + ".ts",
                                     mimetype="text/javascript")


def hand(t, u):
    with app.app_context():
        usr = Model.Users.query.filter_by(id=u).first()
        name = usr.used_name
    socketio.emit('sdone', {"name": name, "time": t, "id": u}, to='manag')


@socketio.on('join')
def j(d):
    join_room("manag")
    print("[SocketIO] Teacher emitted event join")
    emit('joined', {})


@socketio.on('connect')
def onCon(conn):
    print("[SocketIO] Teacher joined")
    emit('ableToJoin', {})


Model.handler = hand

print("[Main] Runway Clear!")
if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
